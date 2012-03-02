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
from Common import *
from ObjBranch import *
from ObjTag import *
from ObjStatus import * 
from Utils_Submod import *
import Utils_All

g_args = []

########################
# CHECK
########################
def check( options ):
  global g_args

  Env.getLocalRoot() #exit if outisde
  
  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()
  sb = Branch.getStableBr() 

  #
  #check repolist params
  #
  proot = Env.getProjectRoot()
  if proot == "":
    if len( g_args ) > 0 or options.add_all_repos == True:
      GLog.f( GLog.E, "FAILED - Cannot commit repositories outside projects (please eliminate any command-line not-optional argument)." )
      return 1
  if len( g_args ) > 0 and options.add_all_repos == True:
    GLog.f( GLog.E, "FAILED - Cannot specify -A and any repositories together." )
    return 1


  #detached head
  if cb.isValid() == False:
    GLog.f( GLog.E, "FAILED - Cannot issue this command in DETACHED-HEAD." )
    return 1

  #int br
  if not ib.isValid():
    GLog.f( GLog.E, "FAILED - Cannot commmit without an integration branch set. Please use swgit branch --set-integration-br command" )
    return 1

  if options.msg == None:
    GLog.f( GLog.E, "FAILED - Please specify a commit message with -m option" )
    return 1

  localrepos = submod_list_repos( firstLev = True, excludeRoot = True, localpaths = True )


  #
  # repo-list checks
  #
  sanitized_args = []
  if len( g_args ) > 0 or options.add_all_repos == True:
    alls  = submod_list_all_default( proot )
    inits = submod_list_initialized( proot )
    snaps = submod_list_snapshot( proot )

    for rn in g_args:

      rn = dir2reponame( rn )
      if rn not in alls:
        GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( rn, Env.getProjectRoot() ) )
        return 1
      if rn in snaps:
        GLog.f( GLog.E,  "ERROR: Cannot commit snapshot repository '%s' without first initializing it.\nAttention, initializing a snapshot repository will pull repository entire history." % rn )
        return 1
      if rn not in inits:
        GLog.f( GLog.E,  "ERROR: Cannot commit repository '%s' without first initializing it" % rn )
        return 1
      sanitized_args.append( rn )

    #substitute user input repos
    g_args = sanitized_args

  #
  # check WD and index
  #
  fileConflict,fileChangedNotAdded,fileChangedAdded,fileUntrack,fileRemoved, \
  modConflict, modChangedNotAdded, modChangedAdded, modUntrack, modRemoved = \
    Status.getFile( ignoreSubmod = False )

  #add only submod modified
  fileModified = fileConflict + fileChangedNotAdded + fileChangedAdded + fileUntrack + fileRemoved
  smodModified   = modConflict + modChangedNotAdded + modChangedAdded + modUntrack + modRemoved
  if options.add_all_repos == True:
    g_args = smodModified

  #on intbr commit only in order to resolve conflict or commit repo upgrades
  f_conflict = False
  if len( fileConflict ) + len( modConflict ) > 0:
    f_conflict = True

  if cb.getShortRef() == ib.getShortRef():
    if not Status.pendingMerge() and \
       not len( fileModified ) == 0:
      strerr  = "FAILED - Cannot issue this command on integration branches except for\n"
      strerr += "           resolving conflicts or\n"
      strerr += "           committing pure subrepo upgrades\n"
      strerr += "         If you forgot creating a branch, you can:\n"
      strerr += "           swgit stash\n"
      strerr += "           swgit branch --create <your_topic>\n"
      strerr += "           swgit stash pop\n"
      strerr += "           swgit commit ... "
      GLog.f( GLog.E, strerr )
      return 1


  #
  # nothing to be committed
  #
  if len( fileModified ) == 0 and len( smodModified ) == 0:
    if not Status.pendingMerge(): #maybe nothing but pending merge (conflict only into submodules) plus git add submod
      GLog.f( GLog.E, "FAILED - Nothing to be committed" )
      return 1
  if len( fileModified ) == 0 and not Status.pendingMerge(): #but submod changes
    if options.add_all_modified:
      GLog.f( GLog.E, "FAILED - Nothing to be committed inside local repository. Please remove -a option." )
      return 1
    if len( g_args ) == 0:
      GLog.f( GLog.E, "FAILED - Nothing to be committed inside local repository. But if you want to commit any submodules upgrade, please specify it/them on input" )
      return 1
  if len( smodModified ) == 0: #but file changes
    if options.add_all_repos:
      GLog.f( GLog.E, "FAILED - Nothing to be committed inside submodules. Please remove -A option." )
      return 1

  #
  # removed files
  #
  if len(fileRemoved) > 0:
    GLog.f( GLog.E, "Found deleted file: \n\t" + "\n\t".join( fileRemoved ) +  "\nPlease use:\n  'git rm <file(s)>' to delete from git\n or\n  'swgit checkout HEAD <file(s)> ' to recover " )
    return 1
  if len(modRemoved) > 0:
    strmsg  = "Found deleted repository: \n\t" + "\n\t".join( modRemoved )
    strmsg += "\nIf you want to remove a repository from this project, please use\n\t'swgit proj --del-repo <reponame>...'"

    GLog.f( GLog.E, strmsg )
    return 1

  #
  # submod changes
  #
  if len( g_args ) > 0:
    for sm in g_args:
      if sm not in smodModified:
        GLog.f( GLog.E, "FAILED - Nothing to be committed for submodule %s, try eliminating this param." % sm )
        return 1

      #
      # Force inside - outside project commit
      #  i.e. if you are inside P and want to commit P1.
      #       P1 must be clean ( Ra and Rb must be committed inside P1).
      #       Otherwise when you return to this commit inside P, Ra and Rb shoul be anywhere
      #   P
      #   |
      #   P1
      #   |  \ 
      #   Ra  Rb
      #
      ret, out = Status.checkLocalStatus_rec( sm, ignoreSubmod = False )
      if ret != 0:
        GLog.f( GLog.E, indentOutput( out, 1 ) )
        GLog.f( GLog.E, "FAILED - You are committing an upgrade of submodule \"%s\", but it is in a \"dirty\" state." % sm )
        return 1

  for r in localrepos:
    if r not in g_args and r in modChangedAdded:
      GLog.f( GLog.E, "FAILED\n\tThere is a submodule added to the index (%s) but not specified as input.\n\tThis will not be committed.\n\tIf you just have added a submodule, pleae run 'swgit commit %s'" % (r,r) )
      return 1

  #
  # conflicts
  #
  if len(fileConflict) > 0:
    GLog.f( GLog.E, "Conflicts found on file(s): \nPlease resolve them\nGit add resolved files\nGit commit\n\t" + "\n\t".join( fileConflict ) )
    return 1
  if len(modConflict) > 0:
    GLog.f( GLog.E, "Conflicts found on repository(s): \nPlease resolve them\nGit add resolved files\nGit commit\n\t" + "\n\t".join( modConflict ) )
    GLog.f( GLog.E, "Try running 'swgit proj --diff' to investigate" )
    return 1

  
  #
  # -a option
  #
  if not options.add_all_modified and len( fileChangedAdded ) == 0:
    if len( g_args ) == 0:
      GLog.f( GLog.E, "FAILED - Nothing added to the index. Try using -a option." )
      return 1

  #
  # Forgotten files
  #
  if len( fileChangedNotAdded ) > 0 and not options.add_all_modified:
    GLog.f( GLog.E, "\nWARNING\n\tWithout -a option these files will not commit: \n\t" + "\n\t".join( fileChangedNotAdded ))

  #
  # untracked files
  #
  if len( fileUntrack ) > 0:
    GLog.f( GLog.E, "\nWARNING\n\tSome untracked files are present. Please check local status\n")

  #
  # --dev option
  #
  if options.dev == True:
    if cb.getType() == SWCFG_BR_INT:
      if Status.pendingMerge():
        strerr  = "No need to specify --dev option when you are on INT branch and you want to commit resolved conflicts.\n"
        strerr += "Please re-try eliminating that option"
        GLog.f( GLog.E, strerr )
        return 1
 
  return 0


########################
# EXECUTE
########################
def execute( options ):

  GLog.s( GLog.S, "Committing your contributes ..." )

  # ADD to index
  if options.add_all_modified == True:
    cmd_add = "cd %s && git add -u" % Env.getLocalRoot()
    out,errCode = myCommand( cmd_add )
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet(1)
      return 1

  for sm in g_args:
    cmd_add = "cd %s && git add %s" % (Env.getLocalRoot(), sm)
    out,errCode = myCommand( cmd_add )
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet(1)
      return 1

  # REMOVE SUBMODULES
  cmd_rm_modules = ""
  localrepos = submod_list_repos( firstLev = True, excludeRoot = True, localpaths = True )
  #print "subrepos %s" % localrepos
  for r in localrepos:
    #print "curr subrepo %s" % r
    if r in g_args:
      continue

    if cmd_rm_modules == "":
      cmd_rm_modules = "git reset -q HEAD -- "

    cmd_rm_modules += " %s " % r

  if cmd_rm_modules != "":
    out,errCode = myCommand( cmd_rm_modules  )
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet(1)
      return 1


  # Stampo i file prima della commit
  cmd="git status -s"
  myCommand( cmd )


  # COMMIT
  cmd_commit = "git commit -m \"%s\"" % options.msg
  out,errCode = myCommand( cmd_commit  )
  if errCode != 0:
    GLog.f( GLog.E, out )

  # Stampo i file dopo la commit
  cmd="git status -s"
  myCommand( cmd )

  GLog.logRet( errCode )
  if errCode != 0:
    return 1

  if options.dev == True:
    cmd_tag = ( "SWINDENT=%s %s tag DEV -m \"%s\" %s" % ( GLog.tab, SWGIT, options.msg, getOutputOpt(options) ) )
    errCode = os.system(  cmd_tag )
    if errCode != 0:
      return 1

  if options.fix != None:
    cmd_tag = ( "SWINDENT=%s %s tag FIX %s -m \"%s\" %s" % ( GLog.tab, SWGIT, options.fix, options.msg, getOutputOpt(options) ) )
    errCode = os.system(  cmd_tag )
    if errCode != 0:
      return 1

  return 0



def main():
  usagestr =  """\
Usage: swgit commit -m <message> [-a] [--dev] [--fix] [<repository>...] """

  parser = OptionParser( usage = usagestr, 
                         description='>>>>>>>>>>>>>> swgit - Commit <<<<<<<<<<<<<<' )

  mgt_group    = OptionGroup( parser, "Management options" )
  output_group = OptionGroup( parser, "Output options" )

  load_command_options( mgt_group, gitcommit_options )
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( mgt_group )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()
  args = parser.largs

  global g_args
  g_args = args

  help_mac( parser )
  
  GLog.initGitLogs( options )
  GLog.s( GLog.I, " ".join( sys.argv ) )

#  if options.all == True:
#    ret = Utils_All.All( options )
#    sys.exit( ret )

  if os.environ.get('SWCHECK') != "NO":
    if check(options) != 0:
      sys.exit(1)

  if os.environ.get('SWCHECK') == "ONLY":
    sys.exit(0)

  ret = execute(options)
  if ret != 0:
    sys.exit( 1 )
  sys.exit( 0 )


def check_fix(option, opt_str, value, parser):
  check_input( option, opt_str, value, parser )

  tagDsc = create_tag_dsc( SWCFG_TAG_FIX )
  if tagDsc.check_valid_value( value ) == False:
    parser.error( "Please specify a valid value for option \"FIX\", satisfying rexgexp: %s" % 
                  ( " or ".join( tagDsc.get_regexp() ) ) )

  if type == "":
    parser.error( "Please specify a valid ticket number (i.e. Issue12345 or 1234567)" )
  
  setattr(parser.values, option.dest, value)

gitcommit_options = [
    [ 
      "-m",
      "--message",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "msg",
        "metavar" : "<message>",
        "help"    : "Specify commit Message"
        }
      ],
    [ 
      "-a",
      "--all-modified",
      {
        "action"  : "store_true",
        "dest"    : "add_all_modified",
        "default" : False,
        "help"    : "Automatically add all modified files to commit"
        }
      ],
    [ 
      "--dev",
      "--dev-label",
      {
        "action"  : "store_true",
        "dest"    : "dev",
        "default" : False,
        "help"    : "Create a DEV label associated to this commit"
        }
      ],
    [ 
      "--fix",
      "--fix-label",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_fix,
        "dest"    : "fix",
        "metavar" : "<fix_tag_argument>",
        "help"    : "Create a tag specifying ticket number it will fix, configurable. (default example: Issue12345)"
        }
      ],
    [ 
      "-A",
      "--all-repos",
      {
        "action"  : "store_true",
        "dest"    : "add_all_repos",
        "default" : False,
        "help"    : "Commit also all repositories (as passing all initialized repositories on command line)"
        }
      ],
#    [ 
#      "--all",
#      {
#        "action"  : "store_true",
#        "dest"    : "all",
#        "default" : False,
#        "help"    : "Execute pull over all repositories of current project"
#        }
#      ]
    ]


if __name__ == "__main__":
	main()
	
