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
import sys,os
from MyCmd import *
from Common import *
from ObjStatus import *
from ObjBranch import *
from ObjLog import *
from ObjMap import *
import Utils
import Utils_All


def pull( noStat=False, tab="" ):
  cmd="git pull --all --tags " #--recurse-submodules compatible from 1.7.4.3
  out,errCode = myCommand( cmd )

  if tab == "":
    tab = GLog.tab + 1
  
  if noStat == False :
    print indentOutput( out[:-1], tab  )

  GLog.f( GLog.I, out[:-1] )

  if errCode != 0:
    fileConflicts = Status.getFileConflict()
    if len( fileConflicts ) > 0:
      GLog.f( GLog.E, "Conflicts found on file(s).\nIn ordet to complete pull operation, please resolve them\nGit add resolved files\nGit commit\n\t" + "\n\t".join( fileConflicts ) )

  return errCode

def check(options):
  GLog.s( GLog.S, "Check " + dumpRepoName("your local") + " repository pull ..." )

  #wd
  err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
  if err != 0:
    GLog.f( GLog.E, errstr )
    GLog.logRet( 1 )
    return 1 

  startb = Branch.getCurrBr()

  #detached head
  if not startb.isValid():
    GLog.f( GLog.E, "FAILED - Cannot pull in DETAHCED-HEAD." )
    return 1

  #int br
  logib = Branch.getLogicalIntBr()
  if not logib.isValid():
    strerr  = "FAILED - Cannot pull without an integration branch set.\n"
    strerr += "         Plase set it by 'swgit branch --set-integration-br'."
    GLog.f( GLog.E, strerr )
    return 1

  if startb.getShortRef() != logib.getShortRef():
    if not options.side_pull:
      strerr  = "FAILED - Cannot directly pull a develop branch.\n"
      strerr += "         Please move onto your current int br (%s)\n" % logib.getShortRef()
      strerr += "         or\n"
      strerr += "         use 'swgit pull -I' option to merge automatically after pulling integration branch"
      GLog.f( GLog.E, strerr )
      return 1

  #intbr only local
  rem_ib = logib.branch_to_remote_obj()
  if not rem_ib.isValid():
    strerr  = "FAILED - Your current integration branch is only a local branch (%s).\n" % startb.getShortRef()
    strerr += "         If you want to pull it, before push it on origin\n"
    strerr += indentOutput( rem_ib.getNotValidReason(), 1 )
    GLog.f( GLog.E, strerr )
    return 1

  #intbr not tracked
  trackedInfo, tracked = logib.get_track_info()
  if not tracked:
    GLog.f( GLog.E, "FAILED - Your current integration branch is not tracked. Please use swgit branch --track %s" % startb.getShortRef() )
    return 1

  GLog.logRet( 0 )
  return 0

def execute(options):
  output_opt = getOutputOpt(options)

  if options.quiet == True:
    options.noStat = True
  str_stat = ""
  if options.noStat ==True:  
    str_stat = " --no-stat "

  GLog.s( GLog.S, "Pull contributes from origin into " + dumpRepoName("your local") + " repository ..." )
  
  startb = Branch.getCurrBr()
  logib = Branch.getLogicalIntBr()

  #
  # pull on intbr
  #
  if startb.getShortRef() == logib.getShortRef():

    errCode = pull( options.noStat )
    GLog.logRet( errCode )
    return errCode

  else: #side pull

    # Go onto int br
    cmd_swto_int = "SWINDENT=%d %s branch -s %s %s" % ( GLog.tab+1, SWGIT, logib.getShortRef(), output_opt)
    errCode = os.system( cmd_swto_int )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1     

    GLog.s( GLog.S, "\tPulling contributes for branch %s ... " % ( logib.getShortRef() ) )

    # pull
    errCode = pull( options.noStat )
    GLog.logRet( errCode, indent="\t" )
    if errCode != 0 :
      GLog.logRet( 1 )
      return 1
    
    # Come back onto starting br
    errCode = os.system("SWINDENT=%d %s branch -s %s %s" % ( GLog.tab+1, SWGIT, startb.getShortRef(), output_opt ) )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1 

    cmd = "SWINDENT=%d %s merge %s %s %s " % ( GLog.tab+1, SWGIT, logib.getShortRef(), output_opt, str_stat )
    GLog.f( GLog.I, cmd )
    errCode = os.system( cmd )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1 
   
  return 0



def main():
  usagestr =  """\
Usage: swgit pull [-I][--no-stat][--no-side-merge] """

  parser = OptionParser( usage = usagestr, 
                         description='>>>>>>>>>>>>>> swgit - Pull <<<<<<<<<<<<<<' )

  management_group = OptionGroup( parser, "Management options" )
  load_command_options( management_group, arr_management_options )
  parser.add_option_group( management_group )

  output_group = OptionGroup( parser, "Output options" )
  load_command_options( output_group, arr_output_options )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()
  args = parser.largs

  help_mac( parser )

  GLog.initGitLogs( options )
   
  if len( args ) > 0:
    parser.error( "Too many arguments: unknow \"%s\"" % args[0] )    

  GLog.s( GLog.I, " ".join( sys.argv ) )

#  if options.all == True:
#    #
#    # PULL ALL
#    #
#    ret = Utils_All.All( options, noCHK=False, lockType="read" )
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


arr_management_options = [
    [ 
      "-I",
      "--merge-from-int",
      {
        "action"  : "store_true",
        "dest"    : "side_pull",
        "default" : False,
        "help"    : "If not on int br, automatically merge on int br and push"
        }
    ],
    [ 
      "--no-stat",
      {
        "action"  : "store_true",
        "dest"    : "noStat",
        "default" : False,
        "help"    : "Disable printing changed files"
        }
      ],
    [ 
      "--no-side-merge",
      {
        "action"  : "store_true",
        "dest"    : "noSideMerge",
        "default" : False,
        "help"    : "Disable automatic merge from %s branch into current %s branch." % (SWCFG_BR_INT, SWCFG_BR_FTR)
        }
      ],
  ]



if __name__ == "__main__":
  main()

