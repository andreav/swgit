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

import os,sys,pwd,socket,re
from ObjRemote import * 

###########
#
# Env
#
###########
class Env:
  def __init__( self ):
    pass
    
  def __str__( self ):
    return Env.getCurrUser() + " " + \
      "["+ Env.getLocalRoot() +"] "

  @staticmethod
  def getCurrUser( ):
    genericUserName = re.compile( SWCFG_USER_REGEXP )

    str, errCode = get_repo_cfg( GITCFG_USERNAME )
    if errCode == 0:
      un = str[:-1]
      if len( genericUserName.findall( un ) ) > 0:
        return un

    str, errCode = get_repo_cfg( GITCFG_USERNAME, fglobal = True )
    if errCode == 0:
      un = str[:-1]
      if len( genericUserName.findall( un ) ) > 0:
        return un

    return pwd.getpwuid( os.getuid() )[0]


  @staticmethod
  def getCurrHost( ):
    return socket.gethostname()

  # return first repo (max depth 2) over me with a SWFILE_PROJMAP
  @staticmethod
  def getProjectRoot( dir = "." ):
    if os.path.exists( dir + "/./" + SWFILE_PROJMAP ) == True:
      return os.path.abspath( dir )

    root = Env.getLocalRoot( dir, fexit = False )
    if root == "":
      #print "not inside repo (%s)" % dir
      return ""

    reporoot = os.path.abspath( root )

    if os.path.exists( reporoot + "/./" + SWFILE_PROJMAP ) == True:
      return reporoot

    fdir = os.path.dirname( reporoot )
    froot = Env.getLocalRoot( fdir, fexit = False )
    if froot == "":
      #print "father not inside repo (%s)" % fdir
      return ""

    froot = os.path.abspath( froot )

    if os.path.exists( froot + "/" + SWFILE_PROJMAP ) == True:
      return froot

    return ""


  @staticmethod
  def getLocalRoot( dir = ".", fexit = True ):
    outerr, errCode = myCommand_fast( "cd %s && git rev-parse --show-toplevel" % dir )
    if errCode != 0:
      if fexit == True:
        print "%s Not inside a git repository" % dir
        sys.exit(1)
      else:
        return ""
    else:
      return os.path.abspath(outerr[:-1])

  @staticmethod
  def is_arepo( dir = "." ):
    root = Env.getLocalRoot( dir, fexit = False )
    if root == "":
      return False
    if os.path.exists( root + "/" + SWDOTGIT ) == True:
      return True
    return False

  @staticmethod
  def is_aproj( dir = "." ):
    root = Env.getLocalRoot( dir, fexit = False )
    if root == "":
      return False
    if os.path.exists( root + "/" + SWFILE_PROJMAP ) == True:
      return True
    return False

  @staticmethod
  def is_inside_aproj( dir = "." ):
    if Env.getProjectRoot( dir ) != "":
      return True
    return False

  @staticmethod
  def isRemoteValid( remote ):
    cmd = "git config --get remote."+remote+".url"
    outerr, errCode = myCommand_fast( cmd )
    if errCode != 0:
      #print "Error while issueing git config --get remote.%s.url, repository not found" % (remote)
      return False
    return  True
  

def main():
 
  print "Local Root".ljust(20)         + Env.getLocalRoot()
  print "Curr User".ljust(20)          + Env.getCurrUser()
  print "getCurrHost".ljust(20)        + Env.getCurrHost()
  print "getProjectRoot".ljust(20)     + Env.getProjectRoot()
  print "getLocalRoot".ljust(20)       + Env.getLocalRoot()
  print "is_arepo".ljust(20)           , Env.is_arepo()
  print "is_aproj".ljust(20)           , Env.is_aproj()
  print "is_inside_aproj".ljust(20)    , Env.is_inside_aproj()
  remotes = Remote.get_remote_list()
  print "isRemoteValid".ljust(20)      , Env.isRemoteValid( remotes[0] )


if __name__ == "__main__":
    main()

