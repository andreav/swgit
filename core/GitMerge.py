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
from ObjTag import *
from ObjLog import *
from ObjStatus import *

import GitPull
import Utils
import Utils_All

g_reference = ""
g_args = []

def merge( fullref_dev, options ):
  #err, errstr = Status.checkLocalStatus()
  #if err != 0:
  #  return err, errstr

  if not options.squash:
    cmd="git merge --no-ff %s" % fullref_dev
  else:
    cmd="git merge --squash %s" % fullref_dev
 
  out,errCode = myCommand( cmd )

  if not options.noStat:
    GLog.s( GLog.S, indentOutput( out[:-1], 1) )
  
  return errCode, out



def check_merge( ref, tb ):
  
  lb = Tag( ref )
  if lb.isValid():
    tagDsc = create_tag_dsc( lb.getType() )

  br = Branch( ref )

  if not lb.isValid() and not br.isValid():
    GLog.f( GLog.E, "Invalid ref : " + ref + " Please specify a valid label or branch to be merged in")
    return 1

  logib = Branch.getLogicalIntBr()

  onIntBr = False
  if tb.getShortRef() == logib.getShortRef():
    onIntBr = True

  if onIntBr and br.isValid():
    strerr  = "Cannot directly merge a branch into integration branch '%s'.\n" % tb.getShortRef()
    strerr += "Please specify a valid label to be merged in."
    GLog.f( GLog.E, strerr )
    return 1

  if tb.getType() == SWCFG_BR_CST and br.isValid():
    strerr  = "Cannot directly merge a branch into CST branch '%s'.\n" % tb.getShortRef()
    strerr += "Please specify a valid label to be merged in."
    GLog.f( GLog.E, strerr )
    return 1

  if tb.isDevelop() and lb.isValid() and not tagDsc.get_merge_on_develop():
    strerr  = "Cannot merge label %s into develop branch '%s'.\n" % (lb.getType(), tb.getShortRef())
    strerr += "Please specify valid label to be merged in."
    GLog.f( GLog.E, strerr )
    return 1

  if tb.isStable() and lb.isValid() and not tagDsc.get_merge_on_stable():
    strerr  = "Cannot merge label %s into stable branch '%s'.\n" % (lb.getType(), tb.getShortRef())
    strerr += "Please specify valid label to be merged in."
    GLog.f( GLog.E, strerr )
    return 1

  if tb.getType() == SWCFG_BR_CST and lb.isValid() and not tagDsc.get_merge_on_cst():
    strerr  = "Cannot merge label %s into CST branch '%s'.\n" % (lb.getType(), tb.getShortRef())
    strerr += "Please specify valid label to be merged in."
    GLog.f( GLog.E, strerr )
    return 1

#  TODO: how to force never merge back CST branches?
#  This is not ok because if you want to develop into CST repo, 
#    maybe you want to merge some CST upgrade onto your FTR branch ... 
#    But you could use a tag ... 
#  if ref.find( "/CST/" ) != -1:
#    GLog.f( GLog.E, "CST branches never can be used as sourece reference, use patches if you want a contribute from that branch" )
#    return 0

  if tb.getType() == SWCFG_BR_CST: #jump release checks
    return 0

  #TODO: make option to jump release checks during merge
  for objRef in ( br, lb ):
    if objRef.isValid() and tb.getRel() != objRef.getRel():
      strerr  = "Cannot merge references from different realses."
      strerr += " start-from release: %s" % objRef.getRel()
      strerr += " merge-into release: %s" % tb.getRel()
      GLog.f( GLog.E, strerr )
      return 1

  return 0



def check( options ):

  global g_reference

  if len(g_args) > 1:
    GLog.f( GLog.E, "Please specify only a reference to be merged" )
    return 1

  err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
  if err != 0:
    GLog.f( GLog.E, errstr )
    return 1

  if len(g_args) == 0 and not options.merge_on_int:
      GLog.f( GLog.E, "FAILED - Without merge arguments, -I option is mandatory." )
      return 1

  cb = Branch.getCurrBr()
  if not cb.isValid():
    if options.merge_on_int == False:
      strerr  = "FAILED - Cannot merge anything into detached-head.\n"
      strerr += "         You can specify -I to find any previous DEV and merge it on you current integration branch"
      GLog.f( GLog.E, strerr )
      return 1

  logib = Branch.getLogicalIntBr()

  if options.merge_on_int:

    if not logib.isValid():
      strerr  = "FAILED - Cannot merge without an integration branch set.\n"
      strerr += "         Plase set it by 'swgit branch --set-integration-br'."
      GLog.f( GLog.E, strerr )
      return 1

    if cb.getShortRef() == logib.getShortRef():
      GLog.f( GLog.E, "FAILED - You already are on your current integration branch, please remove -I option" )
      return 1



    cb_sr, cb_strerr = Utils.eval_curr_branch_shortref( "HEAD" )
    if cb_sr == "":
      GLog.f( GLog.E, cb_strerr )
      return 1

  # no param => search for last DEV
  if len(g_args) == 0:

    if not cb.isValid():
      cb_sr, cb_strerr = Utils.eval_curr_branch_shortref( "HEAD" )
      if cb_sr == "":
        GLog.f( GLog.E, cb_strerr )
        return 1

      cb = Branch( cb_sr )
      if not cb.isValid():
        GLog.f( GLog.E, "FAILED - Cannot find a valid branch starting from this reference: %s" % cb_sr )
        return 1

    #
    # get last DEV label starting from HEAD, named like current branch
    #
    errCode, dev, num = Utils.find_describe_label( "%s/DEV/*" % cb.getShortRef(), startpoint = "HEAD" )
    if errCode != 0:
      GLog.f( GLog.E, "FAILED - No DEV label found previous to HEAD. Please specify on command line which label you want to merge." )
      return 1

    g_reference = dev

  else: 

    g_reference = g_args[0]


  if options.merge_on_int == True:
    return check_merge( g_reference, logib )
  else:
    return check_merge( g_reference, cb )


def execute( options ):
  
  logib = Branch.getLogicalIntBr()

  if options.merge_on_int:

    cmd_swto_int = "SWINDENT=%d %s branch -s %s %s" % ( GLog.tab, SWGIT, logib.getShortRef(), getOutputOpt(options))
    errCode = os.system( cmd_swto_int )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1     

  #after switching
  cb = Branch.getCurrBr()

  # stabilize invoke without checks and with a sha reference
  refer = g_reference

  lb = Tag( g_reference )
  if lb.isValid():
    refer = lb.getFullRef()

  br = Branch( g_reference )
  if br.isValid():
    refer = br.getFullRef()

  if cb.getShortRef() == logib.getShortRef():

    # Pull 
    #  only if intbr is already pushed on origin.
    #  But it can also happen you work locally with intbr,
    #   and first time you will push, you will push also this intbr 
    #   => jump pull if intbr not on remote
    rem_logib = logib.branch_to_remote_obj()
    if not rem_logib.isValid():
      GLog.f( GLog.E, rem_logib.getNotValidReason() )
    else:
      GLog.s( GLog.S, "First update %s repository. Pulling branch %s ... " % ( dumpRepoName("local"), logib.getShortRef() ) )
      errCode = GitPull.pull( options.noStat, GLog.tab+1 )
      GLog.logRet( errCode )
      if errCode != 0:
        return 1

  #
  # merge
  #
  GLog.s( GLog.S, "Merging %s into %s ..." % (refer, cb.getShortRef()) )
  errCode, out = merge( refer, options  )
  GLog.logRet( errCode )
  if errCode != 0:
    return 1

  return 0 



def main():
  usagestr =  """\
Usage: swgit merge [--squash] [--no-stat] <reference> 
       swgit merge [--squash] [--no-stat] -I [<reference>]"""

  parser = OptionParser( usage = usagestr, 
                         description='>>>>>>>>>>>>>> swgit - Merge <<<<<<<<<<<<<<' )

  gitmerge_group = OptionGroup( parser, "Output options" )
  output_group = OptionGroup( parser, "Output options" )

  load_command_options( gitmerge_group, gitmerge_options )
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( gitmerge_group )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()

  help_mac( parser )

  GLog.initGitLogs( options )
  GLog.s( GLog.I, " ".join( sys.argv ) )

  global g_args, g_reference
  g_args = args
  if len( g_args ) > 0:
    g_reference = g_args[0]

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



  


gitmerge_options = [
    [ 
      "-I",
      "--merge-on-int",
      {
        "action"  : "store_true",
        "dest"    : "merge_on_int",
        "default" : False,
        "help"    : "Execute a 'swgit branch -i' before the merge"
        }
     ],
    [ 
      "--squash",
      {
        "action"  : "store_true",
        "dest"    : "squash",
        "default" : False,
        "help"    : "Does not draw merge arrow"
        }
     ],
     [ 
      "--no-stat",
      {
        "action"  : "store_true",
        "dest"    : "noStat",
        "default" : False,
        "help"    : "Disable print changed files"
        }
     ],
#    [ 
#      "--all",
#      {
#        "action"  : "store_true",
#        "dest"    : "all",
#        "default" : False,
#        "help"    : "Execute merge over all repositories of current project"
#        }
#     ]
  ]


if __name__ == "__main__":
  main()
