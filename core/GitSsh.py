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
import Defines
import MyCmd
import ObjCfg
from Common import *
from ObjLog import *

DEFAULT_SSH_CFG = """\
#
# Please run
#   swgit ssh --show-local-cfg
# for more informations
#
#[ssh]
#bin            = (default: ssh)
#identity-1     = A private identity to be provided
#identity-2     =      "              "
# ... 
#use-nopassw-id = True/False: use default no-passw identity, if created

"""


def create_git_key():
  if os.path.exists( Defines.SWGIT_SSH_IDENTITY_NOPASS_PRIV ):
    print "ssh swgit nopassw identity (%s) already exists" % Defines.SWGIT_SSH_IDENTITY_NOPASS_PRIV
    return 1

  print "Creating swgit nopassw identity ... "
  cmd = "ssh-keygen -f %s -t dsa -N \"\"" % Defines.SWGIT_SSH_IDENTITY_NOPASS_PRIV
  out, errCode = MyCmd.myCommand_fast( cmd )
  if errCode != 0:
    print out
    print "FAILED"
    return 1
  print "DONE"
  return 0

def copy_identity( id, user, addr ): 
  objSsh = ObjCfg.ObjCfgSsh()

  print "Copying %s to %s@%s authorized_keys" % ( id, user, addr )
  cmd_cat_local = "cat %s | " % id
  cmd_ssh_bin_and_ids = objSsh.eval_git_ssh_envvar_str()
  cmd_coords  = "%s@%s" % (user,addr)
  cmd_cat_remote  = "umask 077; test -d .ssh || mkdir .ssh; cat >> .ssh/authorized_keys"

  cmd = "%s %s -T %s '%s'" % ( cmd_cat_local, cmd_ssh_bin_and_ids, cmd_coords, cmd_cat_remote )
  #print cmd

  out, errCode = myCommand_fast( cmd )
  if errCode != 0:
    print out
    print "FAILED"
    return 1
  print "DONE"
  return 0

def test_remote_access( user, addr ):
  cmd_echo = "echo REACHED"
  #ssh_options = "-oBatchMode=yes -oConnectTimeout=%s" % ( Defines.SWCFG_SSH_TESTACCESS_TIMEOUT )
  ssh_options = "-oConnectTimeout=%s" % ( Defines.SWCFG_SSH_TESTACCESS_TIMEOUT )
  out, errCode = MyCmd.mySSHCommand_fast( cmd_echo, user, addr, ssh_options )
  if errCode != 0:
    return 1
  return 0


def test_remote_reachability( user, addr ):
  #ssh_options  = "-oBatchMode=yes -oConnectTimeout=%s" % ( Defines.SWCFG_SSH_TESTACCESS_TIMEOUT )
  ssh_options  = "-oConnectTimeout=%s" % ( Defines.SWCFG_SSH_TESTACCESS_TIMEOUT )
  out, errCode = MyCmd.mySSHCommand_fast( "", user, addr, ssh_options )
  if errCode != 0:
    return 1
  return 0



def main():
  usagestr =  """\
Usage: swgit ssh --create-nopassw-id
       swgit ssh --show-local-cfg
       swgit ssh --test-remote-access [<user>] <address>
       swgit ssh --copy-identity [--identity <identity>] [<user>] <address> """

  parser = OptionParser( usage = usagestr,
                         description='>>>>>>>>>>>>>> swgit - ssh management <<<<<<<<<<<<<<' )

  gitkey_group = OptionGroup( parser, "Input options" )
  load_command_options( gitkey_group, gitkey_options )
  parser.add_option_group( gitkey_group )
  (options, args)  = parser.parse_args()

  help_mac( parser )

  if options.create:
    if create_git_key() != 0:
      sys.exit(1)

  if options.show_local_cfg:
    objSsh = ObjCfg.ObjCfgSsh()

    strret  = "\n* ssh local repository configuration:\n"
    strret += indentOutput( objSsh.dump(), 1 )

    strret += "\n* Configuration:\n"
    strret += indentOutput( objSsh.show_config_options(), 1 )

    strret += "\n\n* No-password identity:\n"
    for iden in ( Defines.SWGIT_SSH_IDENTITY_NOPASS_PRIV, Defines.SWGIT_SSH_IDENTITY_NOPASS_PUB ):
      strret += ("\t%s" % iden).ljust( len(Defines.SWGIT_SSH_IDENTITY_NOPASS_PUB) + 4 ) 
      val = "Created\n"
      if not  os.path.exists( iden ):
        val = "NOT " + val
      strret += val

    strret += "\n* GIT_SSH:\n"
    strret += indentOutput( "%s\n" % objSsh.eval_git_ssh_envvar_str(), 1 )

    print strret

  if options.test_remote_access:
    if len( args ) < 1 or len( args ) > 2:
      parser.error( "Please specify <user> and <address> with --test-remote-access option" )
      sys.exit(1)

    if len( args ) == 1:
      user = Defines.EUID_NAME
      addr = args[0]
    else:
      user = args[0]
      addr = args[1]

    strret  = "\nTesting reachability for current user '%s' toward '%s@%s'" % ( Defines.EUID_NAME, user, addr )
    #strret += " ... (%s sec timeout) ..." % Defines.SWCFG_SSH_TESTACCESS_TIMEOUT
    print strret
    ret = test_remote_reachability( user, addr )
    if ret != 0:
      strret = "NOT REACHABLE.\n"
      print strret
      sys.exit(1)
    strret = "REACHABLE!\n"
    print strret

    strret  = "Testing shell access for current user '%s' toward '%s@%s'" % ( Defines.EUID_NAME, user, addr )
    #strret += " ... (%s sec timeout) ..." % Defines.SWCFG_SSH_TESTACCESS_TIMEOUT
    print strret
    ret = test_remote_access( user, addr )
    if ret != 0:
      strret = "NO SHELL ACCESS.\n"
      print strret
      return 1
    strret = "SHELL ACCESS!\n"
    print strret


  if options.copy_identity:
    if len( args ) < 1 or len( args ) > 2:
      parser.error( "Please specify <user> and <address> with --copy-identity option" )
      sys.exit(1)
    if len( args ) == 1:
      user = Defines.EUID_NAME
      addr = args[0]
    else:
      user = args[0]
      addr = args[1]

    id = Defines.SWGIT_SSH_IDENTITY_NOPASS_PUB
    if options.identity == None:
      id = Defines.SWGIT_SSH_IDENTITY_NOPASS_PUB

      if not os.path.exists( id ):
        if create_git_key() != 0:
          sys.exit(1)

    else:
      id = options.identity
      if not os.path.exists( id ):
        print "ssh identity %s NOT exists" % id
        sys.exit(1)

    if copy_identity( id, user, addr ) != 0:
      sys.exit(1)
    sys.exit(0)

  sys.exit(0)



gitkey_options = [
    [ 
      "--create-nopassw-id",
      {
        "action"  : "store_true",
        "dest"    : "create",
        "default" : False,
        "help"    : "Create swgit ssh identity without password."
        }
     ],
    [ 
      "--show-local-cfg",
      {
        "action"  : "store_true",
        "dest"    : "show_local_cfg",
        "default" : False,
        "help"    : "Shows swgit ssh configuration for current user/repo."
        }
     ],
    [ 
      "--test-remote-access",
      {
        "action"  : "store_true",
        "dest"    : "test_remote_access",
        "default" : False,
        "help"    : "Tries ssh communication for current user/repo towards provided user/address."
        }
     ],
    [ 
      "--copy-identity",
      {
        "action"  : "store_true",
        "dest"    : "copy_identity",
        "default" : False,
        "help"    : "Tries copying swgit no-pass identity (or user provided public identity with --identity) onto remote <addr> into ~<user>/.ssh/authorized_keys"
        }
     ],
    [ 
      "--identity",
      {
        "action"  : "store",
        "dest"    : "identity",
        "default" : None,
        "metavar" : "<identity>",
        "help"    : "When specifying --copy-identity, use this option to provide a different identity."
        }
     ]
  ]



if __name__ == "__main__":
    main()


