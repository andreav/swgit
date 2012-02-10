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

from MyCmd import * 

#################
# factory methods
#################
def create_remote( something, dir = "." ):
  objrem_byname = create_remote_byurl( something )
  objrem_byurl  = create_remote_byname( something, dir )

  if not objrem_byurl.isValid() and not objrem_byname.isValid():
    return NullRemote( "%s and %s" % ( objrem_byname , objrem_byurl ) )

  if objrem_byurl.isValid():
    return objrem_byurl
  return objrem_byname


def create_remote_byname( rname, dir = "." ):

# here: always specify a remote name
#
#  if rname == "":
#    remotes = Remote.get_remote_list()
#    if len( remotes ) == 0:
#      return NullRemote( "There is no remote configured for repository at '%s'" % dir )
#    elif len( remotes ) > 0:
#      return NullRemote( "More that one remote configured for repository at '%s'" % dir )
#    else:
#      rname = remotes[0]

  # avoid including Env
  cmd = "cd %s && git rev-parse --show-toplevel" % dir
  rroot, errCode = myCommand_fast( cmd )
  if errCode != 0:
    return NullRemote( "Dir '%s' is not inside git repository" % dir )
  rroot = rroot[:-1]

  if rname == "local":
    return FsRemote( rroot )

  # avoid including Env
  cmd = "cd %s && git config --get remote.%s.url" % ( rroot, rname )
  remote_url, errCode = myCommand_fast( cmd )
  if errCode != 0:
    return NullRemote( "Remote '%s' does not exists" % (rname) )

  return create_remote_byurl( remote_url[:-1] )


def create_remote_byurl( url ):

  if url.find("ssh://") == 0:
    return SshRemote( url )
  elif url.find( "/" ) == 0:
    return FsRemote( url )
  else:
    return NullRemote( "Not supported url '%s'" % (url) )



###########
#
# Remote
#
###########
class Remote( object ):
  def __init__( self, url ):
    self.url_     = url
    self.err_str_ = ""
    self.Type_    = ""
    self.Address_ = ""
    self.User_    = ""
    self.Root_    = ""
    self.isValid_ = False 

  def __str__( self ):
    if not self.isValid_:
      return self.err_str_

    return "url:\t\t[%s]\ntype:\t\t[%s]\naddress:\t[%s]\nuser:\t\t[%s]\nroot:\t\t[%s]" % \
        ( self.url_, self.Type_, self.Address_, self.User_, self.Root_ )
  
  def isValid( self ):
    return self.isValid_
  def getUrl ( self ):
    return self.url_
  def getRoot( self ):
    return self.Root_
  def getType( self ):
    return self.Type_
  def getAddress( self ):
    return self.Address_
  def getUser( self ):
    return self.User_

  def remote_command( self, cmd ):
    return "NOT IMPLEMENTED remote_command for repo '%s'" % self.getType(), 1

  @staticmethod
  def get_remote_list( dir = "." ):
    cmd_remotes = "cd %s && git remote show" % dir
    out, errCode = myCommand_fast( cmd_remotes )
    if errCode != 0:
      return []
    return out.splitlines()

  @staticmethod
  def is_origin_repo( dir = "." ):
    remotes = Remote.get_remote_list( dir )
    if len( remotes ) == 0:
      return True
    return False



#############
#
# NullRemote
#
#############
class NullRemote( Remote ):
  def __init__( self, err_str ):
    self.url_     = ""
    self.err_str_ = err_str
    self.Type_    = ""
    self.Address_ = ""
    self.User_    = ""
    self.Root_    = ""
    self.isValid_ = False 


###########
#
# SshRemote
#
###########
class SshRemote( Remote ):
  def __init__( self, url ):
    self.isValid_ = False
    self.url_     = url
    self.err_str_ = ""
    self.Type_    = "ssh"

    shell_pos = url.find('@')
    if shell_pos == -1:
      self.err_str_ = "Not well formatted ssh url (no @): %s" % url
      return

    self.User_    = url[6:url.find("@")] # 6 = len("ssh://")

    path_pos = url.find( "/",shell_pos )
    if path_pos == -1:
      self.err_str_ = "Not well formatted ssh url (no repo path): %s" % url
      return

    self.Address_ = url[shell_pos+1:path_pos]
    self.Root_    = url[url.find("/",6):] 
    if self.Root_ == "":
      self.err_str_ = "Not well formatted ssh url (empty repo path): %s" % url
      return

    self.isValid_ = True


  def remote_command( self, cmd ):
    git_ssh = "$HOME/.ssh/swgit_sshKey"
    cmd = "ssh -i %s %s@%s '%s'" % ( git_ssh, self.getUser(), self.getAddress(), cmd )
    out, errCode = myCommand_fast( cmd )
    return (out, errCode)
  




##########
#
# FsRemote
#
##########
class FsRemote( Remote ):
  def __init__( self, url ):
    self.isValid_ = False
    self.url_     = url
    self.err_str_ = ""
    self.Type_    = "fs"

    if os.path.exists( "%s/.git" % url ) == False:
      self.err_str_ = "Not valid filesystem remote (not a git repo): %s" % url
      return

    self.User_    = pwd.getpwuid( os.getuid() )[0] #not git user
    self.Address_ = "localhost"
    self.Root_    = url
    self.isValid_ = True

  def remote_command( self, cmd ):
    out, errCode = myCommand_fast( cmd )
    return (out, errCode)
  




def main():
 
  if len( sys.argv ) == 2:

    print "\ntest create_remote_byname( %s )" % sys.argv[1]
    objrem = create_remote_byname( sys.argv[1] )
    print objrem

    print "\ntest create_remote_byurl( %s )" % sys.argv[1]
    objrem = create_remote_byurl( sys.argv[1] )
    print objrem

  else:

    remotes = Remote.get_remote_list()
    print "\nremotes: [%s]" % "] [".join( remotes )

    print "\ntest 'local' remote"
    objrem = create_remote_byname( "local" )
    print objrem

    print "\ntest 'origin' remote"
    objrem = create_remote_byname( remotes[0] )
    print objrem

    print "\ntest 'fs' remote"
    objrem = create_remote_byurl( os.getcwd() )
    print objrem


if __name__ == "__main__":
    main()

