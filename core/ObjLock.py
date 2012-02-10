#!/usr/bin/env python

# Copyright (C) 2012 Andrea Valle
#
# This file is part of swgit.
#
# swgit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# swgit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with swgit.  If not, see <http://www.gnu.org/licenses/>.

import os

from Defines import *
from ObjEnv import *


def createLockStartegy_byname( rname ):
  objrem = create_remote_byname( rname )
  if not objrem.isValid():
    print objrem
    return NullLock()
  return createLockStartegy( objrem.getUrl() )


def createLockStartegy( url ):
  ret = NullLock()

  remote = create_remote_byurl( url )

  if remote.isValid():
    ret = RemoteLock( remote )
  else:
    print "For url: \"" + url + "\" not supported lock strategy, use NullLock"

  return ret


###########
#
# BaseLock
#
###########
class BaseLock( object ):
  def __init__( self, remoteObj ):
    self.remoteObj_ = remoteObj

###########
#
# NullLock
#
###########
class NullLock( BaseLock ):
  def __init__( self ):
    pass

  def acquire( self ):
    #print "NullLock - acquire"
    pass
  def release( self ):
    #print "NullLock - release"
    pass


#############
#
# RemoteLock
#
#############
class RemoteLock(  BaseLock ):
  RET_OK = "OK"
  RET_KO = "KO"
  NOT_EXIST_DIR = "NOT EXISTING LOCK DIRECROTY"

  def __init__( self, remoteObj ):
    super(RemoteLock, self).__init__( remoteObj )
    self.lock_fullPath_ = self.remoteObj_.getRoot() + "/" + SWDIR_LOCK

  def __str__( self ):
    retstr  = "remote:\n%s"        , self.remoteObj_
    retstr += "lockFullPath: [%s]", self.lock_fullPath_
    retstr += "user:         [%s]", Env.getCurrUser()
    return retstr

  def status( self ):
    retstr = ""

    #chech lock dir
    remotecmd = "test -e %s || echo %s" % ( self.lock_fullPath_, self.NOT_EXIST_DIR)
    outerr, errCode = self.remoteObj_.remote_command( remotecmd )
    if errCode != 0:
      errstr = "Cannot reach repository over ssh. Connection problems.\n"
      errstr += outerr[:-1]
      return  errCode, errstr

    if outerr[:-1] == self.NOT_EXIST_DIR:
      retstr += "Repository seems not to be a swgit repository, cannot lock it."
      return 1, retstr

    #chech write access
    locktest = self.lock_fullPath_ + "test" + "." + Env.getCurrUser()

    writeaccess = "touch %s && { rm -f %s && echo %s; } || echo %s" % ( locktest, locktest, self.RET_OK, self.RET_KO )
    outerr, errCode = self.remoteObj_.remote_command( writeaccess )
    if errCode != 0:
      errstr  = "Cannot reach repository over ssh. Connection problems.\n"
      errstr += outerr[:-1]
      return  errCode, errstr

    if outerr[:-1] == self.RET_OK:
      retstr += "Write access to repository ALLOWED (you can pull and push)\n"
    else:
      retstr += "Write access to repository DENIED (you can only pull from this repo)\n"

    #check lock
    remotecmd = "ls -1 %s" % ( self.lock_fullPath_ )
    outerr, errCode = self.remoteObj_.remote_command( remotecmd )
    if errCode != 0:
      errstr = "Cannot reach repository over ssh. Connection problems.\n"
      errstr += outerr[:-1]
      return  errCode, errstr

    retstr += outerr[:-1]
    return 0, retstr


  def acquire( self, type, forced = False  ):
    #
    # try to write
    #   [ ! -e /tmp/aaa ] && echo "vallea" > /tmp/aaa
    #

    lockName = self.lock_fullPath_ + type + "." + Env.getCurrUser()

    if type == "write":
      # write lock <=> no read/write lock at all or any my read/write lock
      remotecmd = "{ [ $( ls -1 \"%s\" 2>/dev/null | wc -l ) -eq 0  ] || [ $( ls -1 \"%s/*.%s\" 2>/dev/null | wc -l ) -ne 0  ]; } && { touch %s && echo %s; } || echo %s; " % \
          ( self.lock_fullPath_, self.lock_fullPath_, Env.getCurrUser(), lockName, self.RET_OK, self.RET_KO )
    elif type == "read":
      remotecmd = "{ [ $( ls -1 \"%s/write.*\" 2>/dev/null | wc -l ) -eq 0 ] || [ $( ls -1 \"%s/*.%s\" 2>/dev/null | wc -l ) -ne 0 ]; } && { touch %s && echo %s; } || exit echo %s;" % \
          ( self.lock_fullPath_, self.lock_fullPath_, Env.getCurrUser(), lockName, self.RET_OK, self.RET_KO )
  
    outerr, errCode = self.remoteObj_.remote_command( remotecmd )
    if errCode != 0:
      errstr  = "ACQUIRE KO (connectivity or permission problems)\n"
      errstr += "           try 'swgit lock -s %s' to investigate)" % self.remoteObj_.getUrl()
      return  errCode, errstr

    if outerr[:-1].find( self.RET_KO ) != -1:
      errstr  = "ACQUIRE KO (cannot lock)\n"
      errstr += "           try 'swgit lock -s %s' to investigate)" % self.remoteObj_.getUrl()
      return  1, errstr

    cmd = "ls -1 %s/*" % ( self.lock_fullPath_ )
    outerr, errCode = self.remoteObj_.remote_command( cmd )
    err = 0
    for f in outerr.splitlines():
      if type == "write":
        if f[f.rfind(".")+1:] !=  Env.getCurrUser() : 
          err = 1
          break
      if type == "read":
        if f[0:f.find(".")] != "read" and f[f.rfind(".")+1:] !=  Env.getCurrUser():
          err = 1
          break

    if err != 0:
      errstr  = "ACQUIRE KO (already locked file or connectivity problems)\n"
      errstr += "           try 'swgit lock -s %s' to investigate)" % self.remoteObj_.getUrl()
      self.release( type )
      return  1, errstr

    return 0, "ACQUIRE OK"
 
  def release( self, type, forced = False ):
    lockName = self.lock_fullPath_ + type + "." + Env.getCurrUser()
    cmd = " rm -f %s || echo %s" % (lockName, self.RET_KO)

    outerr, errCode = self.remoteObj_.remote_command( cmd )
    if errCode != 0:
      errstr  = "RELEASE KO (connectivity or permission problems)\n"
      errstr += "           try 'swgit lock -s %s' to investigate)" % self.remoteObj_.getUrl()
      return  errCode, errstr

    if outerr[:-1].find( self.RET_KO ) != -1:
      errstr  = "RELEASE KO (cannot release)\n"
      errstr += "           try 'swgit lock -s %s' to investigate)" % self.remoteObj_.getUrl()
      return  1, errstr

    errstr = "RELEASE OK - BOTH RELEASED OR NOT LOCKED BY ME"
    return 0, errstr



###########
#
# Guard
#
###########
class Guard:
  def __init__( self, lock ):
    self.lock_ = lock
    self.type_ = ""

  def acquire( self, type ):
    self.type_ = type
    #print "acq guard "+self.type_
    return self.lock_.acquire( self.type_ )

  def __del__( self ):
    #print "del guard "+self.type_
    return self.lock_.release( self.type_ )



def main():
  if len( sys.argv ) != 2:
    print "Please pass remote name or url"
    sys.exit(1)

  objRem = create_remote( sys.argv[1] )
  if not objRem.isValid():
    print objRem
    sys.exit(1)

  print "\nTesting Lock class: \n"
  lock = createLockStartegy( objRem.getUrl() )
  #lock = createLockStartegy( "ssh://vallea@151.98.27.16/home/vallea/git-scripts" )
  print lock
  print "=================="
  print "acquire first time"
  ret, out = lock.acquire("read")
  print out
  print "\nstatus"
  ret,out=lock.status()
  print out
  print "\nacquire an already acquired lock"
  lock.acquire("read")
  print "\nstatus"
  ret,out=lock.status()
  print out
  print "\nrelease an acquired lock"
  lock.release("read")
  print "\nstatus"
  ret,out=lock.status()
  print out
  print "\nrelease a NOT already acquired lock"
  lock.release("read")
  print "\nstatus"
  ret,out=lock.status()
  print out


  # does not neeed to release, destrucotr releases it
  #lock.release()


if __name__ == "__main__":
    main()



