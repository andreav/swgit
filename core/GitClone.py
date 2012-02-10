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

import string
from optparse import OptionParser
import sys,os,stat

from ObjKey import *
from Utils_Submod import *

dbg = False

def log_clone( any ):
  indent = 0
  if os.environ.get('SWINDENT') != None:
    indent = int( os.environ.get('SWINDENT') )

  for r in any.splitlines():
    print "%s%s" % ( "\t"*indent, r )

def log_clone_dbg( any ):
  global dbg
  if dbg:
    log_clone( any )


def main():
  usagestr =  """\
Usage: swgit clone [-b <intbr>] [--integrator] [-recurse] <src-url> [<dst-path>]"""

  parser = OptionParser( usage = usagestr,
                         description='>>>>>>>>>>>>>> swgit - Cloning repository <<<<<<<<<<<<<<' )

  clone_group = OptionGroup( parser, "Clone options" )
  load_command_options( clone_group, gitclone_options )
  parser.add_option_group( clone_group )

  output_group = OptionGroup( parser, "Output options" )
  load_command_options( output_group, arr_output_options )
  parser.add_option_group( output_group )

  (options, args)  = parser.parse_args()

  global dbg
  help_mac( parser )

  if len( args ) == 0:
    print "ERROR: url argument is mandatory."
    sys.exit( 1 )
  if len( args ) > 2:
    print "ERROR: Too many arguments."
    sys.exit( 1 )

  #src
  src_url = args[0]
  src_obj_remote = create_remote_byurl( src_url )
  if not src_obj_remote.isValid():
    print src_obj_remote
    sys.exit( 1 )
  if src_obj_remote.getType() != "ssh" and src_obj_remote.getType() != "fs" :
    print "ERROR: at the moment, only ssh (ssh://user@addr/path/to/repo) or fs (/path/to/repo) urls supported"
    sys.exit( 1 )

  #dest
  if len( args ) == 1:
    dest = os.path.basename( src_obj_remote.getRoot() )
  else:
    dest = args[1]
  dest = os.path.abspath( dest )

  #branch
  branch = ""
  if options.branch != None:
    branch = options.branch

  dbg = options.debug

  log_clone( "Cloning repository " + src_obj_remote.getUrl() + " into " + dest + " ... " )
  log_clone_dbg( "src_user        : %s" % (src_obj_remote.getUser()) )
  log_clone_dbg( "src_addr        : %s" % (src_obj_remote.getAddress()) )
  log_clone_dbg( "src_path        : %s" % (src_obj_remote.getRoot()) )
  log_clone_dbg( "branch          : %s" % (branch) )
  log_clone_dbg( "dest            : %s" % (dest) )
  log_clone_dbg( "integrator_repo : %s" % (options.integrator_repo) )

  #
  # Dest exists
  #
  if os.path.exists( dest ) == True :
    if len(os.listdir(dest)) > 0 :
      log_clone( "  ERROR: \n    The directory " + dest + " already exists" )
      log_clone( "FAILED" )
      sys.exit( 1 )

  #
  # ssh key management
  #
  if src_obj_remote.getType() == "ssh":

    objKey = ObjKey( src_obj_remote.getUser(), src_obj_remote.getAddress() )

    out, errCode = objKey.is_reachable()
    if errCode != 0:
      log_clone( indentOutput( out, 1 ) )
      log_clone( "FAILED" )
      sys.exit( 1 )

    if objKey.create_and_copy() != 0:
      strerr  = "FAILED: cannot create/copy swgit pub key onto host \"%s\" with user \"%s\" via ssh.\n" % \
                         ( src_obj_remote.getAddress(), src_obj_remote.getUser() )
      strerr += "        Please use 'swgit key %s %s' command to investigate" % ( src_obj_remote.getUser(), src_obj_remote.getAddress() )
      log_clone( indentOutput( strerr, 1 ) )
      sys.exit( 1 )
    
#    #check remote user,
#    # very important for push
#    # not allowed clone with users != repo owner.
#    chk_param = "\"\""
#    cmd_remote_checkes = "%s/scripts/checkRemote_skel.py %s %s %s %s | ssh %s@%s 'exec python' " % \
#        ( SWGIT_DIR , src_obj_remote.getRoot(), src_obj_remote.getUser(), branch, chk_param, src_obj_remote.getUser(), src_obj_remote.getAddress() )
#    out, errCode = myCommand_fast( cmd_remote_checkes )
#    if errCode != 0:
#      log_clone( out  )
#      log_clone( "FAILED" )
#      sys.exit( 1 )

  #
  # Clone
  #
  opt_branch = ""
  if branch != "":
    opt_branch = "-b " + branch


  cmd_clone="\tgit clone %s %s %s" % ( src_obj_remote.getUrl(), opt_branch, dest )
  log_clone( cmd_clone )

  out, retcode = myCommand_fast( cmd_clone )
  if retcode != 0:
    log_clone( out ) 
    log_clone( "FAILED" )
    sys.exit( 1 )
  log_clone_dbg( out )
  log_clone( "DONE" )

  #change cwd, now its a git repo
  os.chdir( dest )
  GLog.initGitLogs( options )


  #
  # ROOT repo:
  if branch != "":

    cmd_intBr = "%s branch --set-integration-br %s && %s branch -i" % \
        ( SWGIT, branch, SWGIT )
    out, errCode = myCommand( cmd_intBr )
    if errCode != 0:
      strerr  = "FAILED setting integration branch or jumping over it.\n"
      strerr += "       You can\n"
      strerr += "        look into repo %s for a valid branch and re-clone with right value\n" % dest
      strerr += "        (especially if this is a project or an 'integrator' repository)\n"
      strerr += "       or\n"
      strerr += "        use swgit branch --set-integration-br with a valid value"
      GLog.f( GLog.E, strerr )
      sys.exit( 1 )
    GLog.f( GLog.E, out[:-1] )


  #
  # SUB repos
  if options.recurse == True:

    if os.path.exists( "%s/%s" % (dest, SWFILE_PROJMAP) ) == True :

      GLog.s( GLog.S, "Managing contained repositories ... " )

      errCode = os.system( "SWINDENT=%s %s proj --init" % (1, SWGIT ) )
      if errCode != 0:
        GLog.logRet( 1 )
        sys.exit( 1 )
    GLog.logRet( 0 )

  #
  #SNAP repos
  if options.snapshot:

    GLog.s( GLog.S, "Managing snapshot repositories ... " )

    errCode = os.system( "SWINDENT=%s %s proj --update --snapshot" % ( 1, SWGIT ) )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )
    GLog.logRet( 0 )


  #
  #INTEGRATOR repo
  if options.integrator_repo == True:

    int_repos = submod_list_repos_byType( SWCFG_BR_INT, ".", excludeRoot = True )
    int_repos.insert( 0, "." )
    for r in int_repos:
      GLog.s( GLog.S, "Integrator repo, track also all INT branches inside %s ... " % r )

      #
      # Mark repo as integrator repo
      cmd_intBr = "cd %s && git config swgit.integrator TRUE" % ( r )
      log_clone_dbg( cmd_intBr )
      out,errCode = myCommand( cmd_intBr )
      if errCode != 0:
        GLog.logRet( 1, reason = "(Not critical): " + cmd_intBr )

      #
      # Look for all INT branches, track them
      #  at clone time, only 'origin' remote exists (can hardwire)
      cmd_brlist="cd %s && git for-each-ref --format='%%(refname:short)' refs/remotes/origin/*/*/*/*/*/INT/*" % r
      out,errCode = myCommand( cmd_brlist )
      log_clone_dbg( "INT branches: %s " % out )

      remotes = out.splitlines()
      develop = ""
      for rem in remotes:
        currbr = rem[ rem.find("/") + 1 : ]
        GLog.s( GLog.S, "  * [new branch]   %s  ->  %s" % ( rem, currbr) )

        out, errCode = myCommand("cd %s && git branch --set-upstream %s %s" % ( r, currbr, rem ))
        if errCode != 0:
          GLog.s( GLog.S, "FAILED tracking branch %s (continue anyway with othe branches)" % out )

      GLog.logRet( 0 )

  sys.exit( 0 )


gitclone_options = [
    [ 
      "-b",
      "--branch",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "branch",
        "metavar" : "<src_repo_branch_name>",
        "help"    : "Branch on origin. This brack will be tarcked and set as 'integration' repository.",
        }
      ],
    [ 
      "-i",
      "--integrator",
      {
        "action"  : "store_true",
        "dest"    : "integrator_repo",
        "default" : False,
        "help"    : "Create an 'integrator' repository. 'swgit stabilize' and LIV/STB tagging are allowed only inside these repositories."
        }
      ],
    [ 
      "-r",
      "--recurse",
      {
        "action"  : "store_true",
        "dest"    : "recurse",
        "default" : False,
        "help"    : 'Also initialize/clone all project contained repositories. Same as cloning and issueing swgit proj --init.'
        }
      ],
    [ 
      "-s",
      "--snapshot",
      {
        "action"  : "store_true",
        "dest"    : "snapshot",
        "default" : False,
        "help"    : "Also initialize snapshot repositoires after cloning."
        }
      ],
    ]
  
if __name__ == "__main__":
  main()


