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

  if options.squash == False :
    cmd="git merge --no-ff " + fullref_dev
  else:
    cmd="git merge --squash " + fullref_dev
 
  out,errCode = myCommand( cmd )

  if options.noStat == False :
    GLog.s( GLog.S, indentOutput( out[:-1], 1) )
  
  if errCode != 0:
    return errCode, out

  return errCode, out



def check_merge( ref, cb, ib, sb ):
  
  lb = Tag( ref )
  if lb.isValid():
    tagDsc = create_tag_dsc( lb.getType() )

  br = Branch( ref )

  if not lb.isValid() and not br.isValid():
    GLog.f( GLog.E, "Invalid ref : " + ref + " Please specify a valid label or branch to be merged in")
    return 1

  if cb.getShortRef() != ib.getShortRef():
    onDevelop = False
  else:
    onDevelop = True
  if sb.isValid() and cb.getShortRef() == sb.getShortRef() :
    onStable = True
  else:
    onStable = False
  if onDevelop == True and br.isValid() == True:
    GLog.f( GLog.E, "Cannot merge a branch into develop. Please specify a valid reference to be merged in")
    return 1
  if onStable == True and br.isValid() == True:
    GLog.f( GLog.E, "Cannot merge a branch into stable. Please specify a valid reference to be merged in")
    return 1
  if onDevelop == True and lb.isValid() == True and tagDsc.get_merge_on_develop() == False:
    GLog.f( GLog.E, "Cannot merge label %s into develop. Please specify valid label to be merged in" % lb.getType() )
    return 1
  if onStable == True and lb.isValid() == True and not tagDsc.get_merge_on_stable():
    GLog.f( GLog.E, "Cannot merge label %s into stable. Please specify valid label to be merged in" % lb.getType() )
    return 1
  if cb.getType() == SWCFG_BR_CST and br.isValid() == True:
    GLog.f( GLog.E, "Cannot merge a branch into CST branches. Please specify a valid reference to be merged in")
    return 1
  if cb.getType() == SWCFG_BR_CST and lb.isValid() == True and not tagDsc.get_merge_on_cst():
    GLog.f( GLog.E, "Cannot merge label %s into CST branch. Please specify valid label to be merged in" % lb.getType() )
    return 1
#  TODO
#  how to force never merge back CST branches?
#  This is not ok because if you want to develop into CST repo, maybe you want to erge some CST upgrade onto your FTR branch ... 
#  if ref.find( "/CST/" ) != -1:
#    GLog.f( GLog.E, "CST branches never can be used as sourece reference, use patches if you want a contribute from that branch" )
#    return 0
  if cb.getType() == SWCFG_BR_CST: #jump release checks
    return 0
  if br.isValid() == True and cb.getRel() != br.getRel():
    GLog.f( GLog.E, "Cannot merge branch references from different realses (%s) vs (%s)" % ( cb.getShortRef(), br.getShortRef() ) )
    return 1
  if lb.isValid() == True and cb.getRel() != lb.getRel():
    GLog.f( GLog.E, "Cannot merge label references from different realses (%s) vs (%s)" % ( cb.getShortRef(), lb.getTagShortRef() ) )
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

  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()
  sb = Branch.getStableBr()

  if len(g_args) == 0 and options.merge_on_int == False:
      GLog.f( GLog.E, "FAILED - Without merge arguments, -I option is mandatory." )
      return 1

  if options.merge_on_int == True:
    if cb.getShortRef() == ib.getShortRef():
      GLog.f( GLog.E, "FAILED - You already are on your current integration branch, please remote -I option" )
      return 1


  if not cb.isValid():
    if options.merge_on_int == False:
      strerr  = "FAILED - Cannot merge anything into detached-head.\n"
      strerr += "         You can specify -I to find any previous DEV and merge it on you current integration branch"
      GLog.f( GLog.E, strerr )
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
    return check_merge( g_reference, ib, ib, sb )
  else:
    return check_merge( g_reference, cb, ib, sb )


def execute( options ):
  
  if options.quiet == True:
    options.noStat = True
  str_stat = ""
  if options.noStat ==True:  
    str_stat = " --no-stat "

  if options.merge_on_int == True:
    output_opt = getOutputOpt(options)
    cmd_swto_int = "SWINDENT=%d %s branch -i %s" % ( GLog.tab, SWGIT, output_opt)
    errCode = os.system( cmd_swto_int )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1     

  refer = ""
  lb = Tag( g_reference )
  if lb.isValid() == True:
    refer = lb.getFullRef()

  br = Branch( g_reference )
  if br.isValid() == True:
    refer = br.getFullRef()

  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()
  sb = Branch.getStableBr()

  if cb.getShortRef() == ib.getShortRef():

    rem_ib = ib.branch_to_remote_obj()
    if not rem_ib.isValid():
      GLog.f( GLog.E, rem_ib.getNotValidReason() )
    else:
      # Pull only if intbr is already pushed on origin.
      # But it can also happen you work locally with intbr, and only when you push, 
      #  you will push also this intbr => no pull available now
      GLog.s( GLog.S, "First update your local repository ..." )
      errCode = GitPull.pull( ib.getShortRef(), options.noStat, GLog.tab+1 )
      GLog.logRet( errCode )
      if errCode != 0:
        return 1

  #
  #  merge on develop 
  #
  GLog.s( GLog.S, "Merging " + refer + " into " + cb.getFullRef() + " ..." )
  errCode, out = merge( refer, options  )
  GLog.logRet( errCode )
  if errCode != 0:
    return 1

  return 0 



def main():
  usagestr =  """\
Usage: swgit merge <startpoint> [-I] [--squash] [--no-stat] """

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

  global g_args
  g_args = args

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
