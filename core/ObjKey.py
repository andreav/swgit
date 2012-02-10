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

from optparse import *
import os
from string import *
import time
import sys
import getpass
import pwd

from Defines import *
from MyCmd import *
from Common import *
from ObjRemote import *
from ObjLog import *

class ObjKey:

  def __init__( self, user, addr ):
    self.user_         = user
    self.addr_         = addr

    # HOME DIRECOTRY => use ~
    #   because 
    #     $HOME depends only on UID
    #   but
    #     when UID != EUID => ~ looks on the right direcotry (that of EUID)
    euid_home = "~%s" % pwd.getpwuid( os.geteuid() )[0]
    euid_home = os.path.expanduser( euid_home )

    self.ssh_key_priv_ = "%s/.ssh/%s" % (euid_home, SWGIT_SSHKEY )
    self.ssh_key_pub_  = self.ssh_key_priv_ + ".pub"

  def get_user( self ):
    return self.user_
  def get_addr( self ):
    return self.addr_
  def get_ssh_key_pub( self ):
    return self.ssh_key_pub_
  def get_ssh_key_priv( self ):
    return self.ssh_key_priv_

  def is_reachable( self ):
    out,errCode = mySSHCommand_fast( "exit 0", self.get_user(), self.get_addr() )
    #print out, errCode
    if errCode !=0:
      strerr  = "Cannot reach host \"%s\" with user \"%s\" via ssh." % ( self.get_addr(), self.get_user() )
      return strerr, 1
    return "", 0
    

  def create_and_copy( self ):

    if not os.path.exists( self.ssh_key_pub_ ):
      #create and copy
      if self.create_git_key() != 0:
        return 1

      if self.copy_git_key() != 0:
        return 1

    else:

      #check already present key
      if self.check_remote_access() != 0:
        if self.copy_git_key() != 0:
          return 1

    return 0


  def create_git_key( self ):
    print "Creating Git key ... "
    cmd = "ssh-keygen -f " +self.ssh_key_priv_ + " -t dsa -N \"\""
    out, errCode = myCommand_fast( cmd )
    if errCode != 0:
      print out
      print "FAILED"
      return 1
    print "DONE"
    return 0


  def copy_git_key( self ):
    print "Copying %s to %s@%s authorized_keys" % (self.ssh_key_pub_, self.get_user(), self.get_addr())
    cmd = "cat " + self.ssh_key_pub_ + " | ssh " + self.get_user() + "@" + self.get_addr() + " 'umask 077; test -d .ssh || mkdir .ssh ; cat >> .ssh/authorized_keys' "
    print cmd
    out, errCode = myCommand_fast( cmd )
    if errCode != 0:
      print out
      print "FAILED"
      return 1
    print "DONE"
    return 0
  
  
  def check_remote_access( self ):
    
    # if id has already been copied, it will return ok
    cmd_echo = "echo REACHED"
    cmd_ssh  = "ssh -i %s -oNumberOfPasswordPrompts=0 %s@%s '%s'" % \
               ( self.ssh_key_priv_, self.get_user(), self.get_addr(), cmd_echo )
    out, errCode = myCommand_fast( cmd_ssh )
    if errCode != 0:
      return 1
    return 0

    


def main():
  usagestr =  """\
Usage: swgit key [-c] <user> <address>"""

  parser = OptionParser( usage = usagestr,
                         description='>>>>>>>>>>>>>> swgit - Key management <<<<<<<<<<<<<<' )

  gitkey_group = OptionGroup( parser, "Input options" )
  load_command_options( gitkey_group, gitkey_options )
  parser.add_option_group( gitkey_group )
  (options, args)  = parser.parse_args()

  help_mac( parser )

  if len( args ) != 2:
    parser.error( "Please specify user and address." )

  user = args[0]
  addr = args[1]
  objKey = ObjKey( user, addr )

  out, errCode = objKey.is_reachable()
  if errCode != 0:
    print out
    sys.exit(1)

  if options.create_and_copy == True:

    if objKey.create_and_copy() != 0:
      sys.exit(1)
    sys.exit(0)

  else:

    str_pub = "swgit public  key for user '%s' %s alredy created"
    if os.path.exists( objKey.get_ssh_key_pub() ):
      print str_pub % (user, "")
    else:
      print str_pub % (user, "NOT")

    str_priv = "swgit private key for user '%s' %s alredy craeted"
    if os.path.exists( objKey.get_ssh_key_priv() ):
      print str_priv % (user, "")
    else:
      print str_priv % (user, "NOT")

    if objKey.check_remote_access() != 0:
      print "swgit public  key NOT already copied onto remote machine '%s@%s'\n\n(you can issue this command with -c option to create/copy your swgit public key there)\n" % (objKey.get_user(), objKey.get_addr() )
    else:
      print "swgit public  key already copied onto remote machine '%s@%s'" % ( objKey.get_user(), objKey.get_addr() )

    sys.exit(0)



gitkey_options = [
    [ 
      "-c",
      "--create-copy",
      {
        "action"  : "store_true",
        "dest"    : "create_and_copy",
        "default" : False,
        "help"    : "Create swgit ssh key if necessary and copy onto remote."
        }
     ]
  ]



if __name__ == "__main__":
    main()


