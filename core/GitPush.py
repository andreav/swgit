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
from ObjStatus import *
from ObjBranch import *
from ObjTag import *
from ObjLog import *
from ObjEnv import *
from ObjLock import *
from ObjMail import *

import GitPull
import Utils_All

g_remote = "" 

def is_empty_branch( objBr ):

  errCode, startSHA = getSHAFromRef( objBr.getShortRef() )
  if errCode != 0:
    GLog.f( GLog.E, "\tError retrive SHA from branch %s" % objBr.getShortRef() )
    return 1

  errCode, startBrLblSHA = getSHAFromRef( objBr.getNewBrRef() )
  if errCode != 0: #on INT?
    if objBr.getType() == SWCFG_BR_INT:
      return 0
    else:
      GLog.f( GLog.E, "\tError retrieving tag %s, damaged branch." % objBr.getNewBrRef() )
      return 1

  if startSHA == startBrLblSHA:
    return 0

  return 2


def check( options ):

  if options.showmailcfg:
    return 0
  
  if options.testmail:
    om = ObjMailPush()
    if om.isValid() == False:
      GLog.f( GLog.E, "FAILED - Mail not well configured." )
      GLog.f( GLog.E, om.dump() )
      return 1
    return 0

  GLog.s( GLog.S, "Check " + dumpRepoName("your local") + " repository push ..." )
  output_opt = getOutputOpt(options)

  if options.quiet == True:
    options.noStat = True
  str_stat = ""
  if options.noStat == True:  
    str_stat = " --no-stat "

  startb = Branch.getCurrBr()

  #remote
  global g_remote
  remote_list = Remote.get_remote_list()
  if g_remote != "":
    if g_remote not in remote_list:
      GLog.f( GLog.E, "FAILED - Remote '%s' is not configured into this repository." % g_remote )
      return 1
  else:
    if len( remote_list ) == 0:
      strerr  = "FAILED - You are on 'origin' (no remote configured). Cannot push."
      GLog.f( GLog.E, strerr )
      return 1
    elif len( remote_list ) > 1:
      strerr  = "FAILED - Please specify one remote among these:\n"
      for r in remote_list:
        strerr += "           %s\n" % r
      GLog.f( GLog.E, strerr )
      return 1
    else:
      g_remote = remote_list[0]


  #wd
  err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
  if err != 0:
    GLog.f( GLog.E, errstr )
    return 1

  #detached head
  if not startb.isValid():
    GLog.f( GLog.E, "WARNING - in DETAHCED-HEAD only tags put-in-past will be pushed." )
    return 0

  #log intbr: 
  logib = Branch.getLogicalIntBr()
  if not logib.isValid():
    strerr  = "FAILED - Cannot push without an integration branch set.\n"
    strerr += "         Plase set it by 'swgit branch --set-integration-br'."
    GLog.f( GLog.E, strerr )
    return 1

  # Avoid remote but not tracked => pull will fail with:
  #		Fetching tags only, you probably meant:
  #   git fetch --tags
  rem_logib = Branch( "%s/%s" % (g_remote,logib.getShortRef()) )
  if rem_logib.isValid():
    trackedInfo, tracked = logib.get_track_info()
    if not tracked:
      strerr  = "FAILED - Your current integration branch remotely exists but is not tracked.\n"
      strerr += "         Please use swgit branch --track %s/%s" % (g_remote,logib.getShortRef())
      GLog.f( GLog.E, strerr )
      return 1


  #
  # side push checks
  #
  if startb.getShortRef() != logib.getShortRef():

    # option must be specified
    if not options.side_push:
      strerr  = "FAILED - Cannot directly push a develop branch.\n"
      strerr += "         Please chose one option:\n"
      strerr += "          1. merge it on your current int br (%s)\n" % logib.getShortRef()
      strerr += "          2. use   'swgit push -I'  option to automatically merge last DEV and push\n"
      strerr += "          3. if this is a just created branch, and you want to push it,\n"
      strerr += "                swgit branch --set-integration-br %s\n" % startb.getShortRef()
      strerr += "                swgit push"
      GLog.f( GLog.E, strerr )
      return 1

    # side push, at least some contribute
    ret = is_empty_branch( startb )
    if ret == 1:
      GLog.logRet( 1 )
      return 1
    if ret == 0:
      GLog.logRet( 0 )
      return 0

    errCode, dev, num = find_describe_label(startb.getShortRef()+"/DEV/*")
    
    if errCode != 0 :
      GLog.f( GLog.E, "FAILED - No DEV label found on branch %s" % startb.getShortRef() )
      return 1
  
    if num != "0":
      GLog.f( GLog.E, "FAILED - You must have at least a DEV label on "+startb.getShortRef() )
      return 1

  if not options.noMail:
    om = ObjMailPush()
    if not om.isValid():
      str_out_err = "WARNING cannot send mail due to wrong configuration.\n"
      str_log_err = str_out_err
      str_out_err += "Try issueing 'swgit push --show-mail-cfg' to investigate."
      str_log_err += om.dump()
      GLog.f( GLog.E, indentOutput( str_out_err, 1 ) )
      GLog.f( GLog.I, indentOutput( str_log_err, 1 ) )

  GLog.logRet( 0 )
  return 0


def get_tag_in_past_list():
  cmd_list_past_tags = "git for-each-ref --format='%%(refname:short)' 'refs/tags/%s/*/*/*/*/*/*/*/*/*'" % SWCFG_TAG_NAMESPACE_PAST
  out,errCode = myCommand( cmd_list_past_tags )
  return out[:-1].splitlines(), errCode


def execute_push_past_tag( options ):

  GLog.s( GLog.S, "Push " + dumpRepoName("local") + " past-tags on %s ..." % g_remote )

  past_tags,errCode = get_tag_in_past_list()

  if len( past_tags ) == 0:
    GLog.s( GLog.S, "DONE - No tags found." )
    return 0

  cmd_push = "git push %s refs/tags/%s/*:refs/tags/*" % (g_remote,SWCFG_TAG_NAMESPACE_PAST)
  out,errCode = myCommand( cmd_push )
  GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
  if errCode != 0:
    GLog.f( GLog.E, "FAILED - Pushing past tags" )
    return 1

  cmd_del_tags = "git tag -d %s" %  " ".join( past_tags )
  out,errCode = myCommand( cmd_del_tags )
  if errCode != 0:
    GLog.f( GLog.E, "FAILED - Deleting local refs/tags/%s/* references. (not critical)" % SWCFG_TAG_NAMESPACE_PAST )
    return 1

  GLog.logRet( 0 )
  return 0


def execute( options ):

  #
  # mail mgt
  #
  if options.showmailcfg:

    om = ObjMailPush()
    print om.dump()
    print om.show_config_options()
    print ""
    return 0

  if options.testmail:

    GLog.s( GLog.S, "Sending test mail" )

    om = ObjMailPush()
    out, err = om.sendmail( "PUSH TEST MAIL", debug = False )
    if out[:-1] != "":
      GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    GLog.logRet( err )
    return err

  output_opt = getOutputOpt(options)

  if options.quiet == True:
    options.noStat = True
  str_stat = ""
  if options.noStat == True:  
    str_stat = " --no-stat "

  startb = Branch.getCurrBr()
 
  #detached head
  if not startb.isValid():
    return execute_push_past_tag( options )

  #
  # START
  #
  GLog.s( GLog.S, "Push " + dumpRepoName("local") + " contributes on %s ..." % g_remote )
  
#
#  Locking should be good because you will NEVER have a 
#    ! [reject] "non-fast-forward"
#
#  However is somewhat compicated for when creating --share repositories
#    (because we try to write under .swgit/lock and maybe we have no permission)
#    Lock file should be created with right mask.
#    but
#    we always do a pull before pushing => "non-fast-forward" risk is less frequent.
#    Only when two concurrent pushes happen, this can occour.
#    In these cases, second user will re-push and everithing should work
#
#
#  remote_name = "origin"
#  lock = createLockStartegy_byname( remote_name )
#  guard = Guard( lock ) # When out of scope it automatically releases lock
#  errCode, errstr = guard.acquire("write")
#  if errCode != 0:
#    strerr  = "Cannot lock '%s'. Please retry later\n" % (remote_name)
#    strerr += errstr + "\n"
#    strerr += "If you want you can always update your local repository by swgit pull"
#    GLog.f( GLog.E, indentOutput( strerr, 1 ) )
#    GLog.logRet(errCode, reason="Lock ")
#    return 1
#

  logib = Branch.getLogicalIntBr()
  rem_logib = Branch( "%s/%s" % (g_remote,logib.getShortRef()) )

  f_sidepush = True
  if startb.getShortRef() == logib.getShortRef():
    f_sidepush = False

  if not f_sidepush:

    #in case you previously set this as int br but never pushed it on origin,
    # avoid pulling it (or will get error:
    #  
    #   Fetching origin
    #		Fetching tags only, you probably meant:
    #		  git fetch --tags
    #
    if rem_logib.isValid():

      GLog.s( GLog.S, "\tFirst update %s repository. Pulling branch %s ... " % ( dumpRepoName("local"), logib.getShortRef() ) )

      errCode = GitPull.pull( options.noStat, GLog.tab+2 )
      GLog.logRet( errCode, indent="\t" )
      if errCode != 0:
        GLog.logRet( errCode )
        return 1

  else: #side push

    #empty => return ok
    ret = is_empty_branch( startb )
    if ret == 0:
      GLog.s( GLog.S, "\tBranch %s is empty, no-op" % ( startb.getShortRef() ) )
      GLog.logRet( 0 )
      return execute_push_past_tag( options )

    #goto int
    cmd_swto_int = "SWINDENT=%d %s branch -s %s %s" % ( GLog.tab+1, SWGIT, logib.getShortRef(), output_opt)
    errCode = os.system( cmd_swto_int )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1     

    #already checked, must return ok
    errCode, dev, num = find_describe_label( startb.getShortRef()+"/DEV/*" ,startpoint=startb.getShortRef())

    #merge also pulls
    errCode = os.system("SWINDENT=%d %s merge %s %s %s" % ( GLog.tab+1, SWGIT, dev, output_opt, str_stat ) )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1  


  #
  #   PUSH
  #

  cb = Branch.getCurrBr()

  # Output stat
  if rem_logib.isValid():
    cmd = "git diff %s/%s %s --stat " % ( g_remote, logib.getShortRef(), logib.getShortRef() ) 
  else:
    cmd = "git diff --stat %s %s" % ( logib.getNewBrRef(), logib.getShortRef() ) 
  out, errCode=myCommand(cmd)
  fileUp = ""
  if not options.noStat and not options.quiet and len(out) > 0:
    fileUp = indentOutput( "\nFiles updated:\n"+out[:-1], 1  )


  GLog.s( GLog.S, "\tPushing contributes, branches and labels ... " )

  ref_discard_list = [] 
  ref_push_list = []

  # get pushable tag list
  push_on_origin_labels = []
  for tt in TagDsc.get_all_tagtypes():
    td = create_tag_dsc( tt )
    if td.get_push_on_origin() == True:
      push_on_origin_labels.append( tt )

  # set limit to git log
  # exclude my origin
  notBr = ""
  if rem_logib.isValid():
    notBr = " %s/%s " % ( g_remote, cb.getShortRef() )

  # exclude all REMOTE INT branches
  remotes_INT = getAllIntBranches_remotes()
  notBr += " " + " ".join( remotes_INT )

  if cb.getType() == SWCFG_BR_CST:
    # exclude all LOCAL INT branches
    local_INT = getAllIntBranches_local()
    notBr += " "
    notBr += " ".join( local_INT )

  cmd_local_references = "git log --format='%%d' %s --not %s | sed -e 's/tag://g' -e 's/ //g' -e 's/(//g' -e 's/)//g' -e '/^$/d'" % ( cb.getShortRef(),  notBr )
  out, errCode=myCommand( cmd_local_references )
 
  #
  # process git log result
  #
  for line in out.splitlines():

    currcommit_references = line.split(",")
    for r in currcommit_references:

      #branch reference
      if r.count("/") == 6: #is a branch
        bt = getFromSlash( r, 5, 6 ) #branchtype
        nb = "%s/%s/%s" % (r,SWCFG_TAG_NEW,SWCFG_TAG_NEW_NAME)
        if bt in [ SWCFG_BR_INT ]: #INT br can stay on NEW at creation, but must be pushed anyway
          ref_push_list.append( r )
          ref_push_list.append( nb )
          continue
        if nb not in currcommit_references: #branch has moved from NEW/BRANCH =>push also NEW/BRANCH
          ref_push_list.append( r )
          ref_push_list.append( nb )
        else:
          ref_discard_list.append( r )
          ref_discard_list.append( nb )

      #tag reference
      if r.count("/") == 8:
        tt = getFromSlash( r, 7, 8 ) #tagtype
        if tt in push_on_origin_labels:
          ref_push_list.append(r)
        else:
          ref_discard_list.append(r)

  #fix for shared feature branch when commit never done (no contribs)
  if not rem_logib.isValid():
    r = logib.getShortRef()
    if r not in ref_push_list:
      nb = "%s/%s/%s" % (r,SWCFG_TAG_NEW,SWCFG_TAG_NEW_NAME)
      ref_push_list.append( r )
      ref_push_list.append( nb )

  GLog.f( GLog.I, "\t\tBranches and labels to push: \n\t\t\t" + "\n\t\t\t".join( ref_push_list ) )
  GLog.f( GLog.I, "\t\tBranches and labels discarded: \n\t\t\t" + "\n\t\t\t".join( ref_discard_list ) )


  # every past tag must be pushed and shifted on origin
  opt_past_tags = "refs/tags/%s/*:refs/tags/*" % SWCFG_TAG_NAMESPACE_PAST

  ########
  # push #
  ########
  cmd_push = "git push %s %s %s" % ( g_remote, " ".join( ref_push_list ), opt_past_tags )
  pushOut,errCode = myCommand( cmd_push )
  if options.noStat == False :
    GLog.f( GLog.E, indentOutput( pushOut[:-1], 2 ) )
  if errCode != 0:
    GLog.f( GLog.E, "\t\tPush contributes, branches and labels \n\t\t\t" + "\n\t\t\t".join( ref_push_list ) + "\n\t\tFAILED (not critical)" )

  
  # dump file list
  if fileUp != "" and errCode == 0:
    GLog.s( GLog.S, indentOutput( fileUp, 1 ) )
  
  # DONE or FAILED of PUSH
  GLog.logRet( errCode, "\t" )
  if errCode != 0:
    GLog.logRet( 1 )
    sys.exit(1)

  #if you have pushed now on origin intbr => track it
  if not rem_logib.isValid():
    cmd_tarck_local_int_br = ""
    errCode = os.system("SWINDENT=%d %s branch --track %s/%s %s" % ( GLog.tab+1, SWGIT, g_remote, logib.getShortRef(), output_opt ) )

  #delete past tags
  past_tags,errCode = get_tag_in_past_list()
  if len( past_tags ) > 0:
    cmd_del_tags = "git tag -d %s" %  " ".join( past_tags )
    out,errCode = myCommand( cmd_del_tags )
    if errCode != 0:
      GLog.f( GLog.E, "\tFAILED - Deleting local refs/tags/%s/* references. (not critical)" % SWCFG_TAG_NAMESPACE_PAST )

  # Come back onto starting br
  #TODO make option for this behaviour
  if f_sidepush:
    errCode = os.system("SWINDENT=%d %s branch -s %s %s" % ( GLog.tab+1, SWGIT, startb.getShortRef(), output_opt ) )
    if errCode != 0 :
      GLog.logRet( errCode )
      return 1

  if not options.noMail:

    om = ObjMailPush()
    if om.isValid():

      if fileUp != "":

        GLog.s( GLog.S, "\tSending mail" )

        log, errCode = myCommand( "git log -1 %s " % logib.getShortRef() )
        LIV, errCode = myCommand( "%s info -t LIV -r %s | head -2 " % ( SWGIT, logib.getShortRef() ) )

        body_mail = log + "\n" + LIV + "\n" +  pushOut + "\n\nFiles changed:\n" + fileUp

        out, err = om.sendmail( "%s" % (body_mail), debug = False )
        if err != 0:
          GLog.f( GLog.E, indentOutput( out[:-1], 2 ) )
          GLog.logRet( 1, reason = "NOT CRITICAL", indent = "\t" )
        else:
          GLog.f( GLog.I, out )
          GLog.logRet( 0, indent = "\t" )


  GLog.logRet( 0 )
  return 0


def main():
  usagestr =  """\
Usage: swgit push [-I][--no-mail] [<remote>]"""

  parser = OptionParser( description='>>>>>>>>>>>>>> swgit - Push on origin <<<<<<<<<<<<<<' )

  management_group = OptionGroup( parser, "Management options" )
  mail_group = OptionGroup( parser, "Mail options" )
  load_command_options( management_group, arr_management_options )
  load_command_options( mail_group, arr_mail_options )
  parser.add_option_group( management_group )
  parser.add_option_group( mail_group )
 
  output_group = OptionGroup( parser, "Output options" )
  load_command_options( output_group, arr_output_options )
  parser.add_option_group( output_group )

  (options, args)  = parser.parse_args()

  help_mac( parser )

  GLog.initGitLogs( options )

  if len( args ) > 1:
    parser.error( "Too many arguments: unknow \"%s\"" % args[0] ) 
  if len( args ) == 1:
    global g_remote
    g_remote = args[0]

  GLog.s( GLog.I, " ".join( sys.argv ) )
  
  
#  if options.all == True:
#    ret = Utils_All.All( options, lockType="write", noCHK=False, bottomup = True )
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
      "--merge-on-int",
      {
        "action"  : "store_true",
        "dest"    : "side_push",
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
        "help"    : "Disable print changed files"
        }
    ],
   ]

arr_mail_options = [
    [ 
      "--no-mail",
      {
        "action"  : "store_true",
        "dest"    : "noMail",
        "default" : False,
        "help"    : "Disable automatic mail delivery"
        }
    ],
    [
      "--show-mail-cfg",
      {
        "action"  : "store_true",
        "dest"    : "showmailcfg",
        "default" : False,
        "help"    : 'Show mail configuration.'
        }
      ],
    [
      "--test-mail-cfg",
      {
        "action"  : "store_true",
        "dest"    : "testmail",
        "default" : False,
        "help"    : 'This command will send a test mail, accordingly to --show-mail-cfg.'
        }
      ],
    ]



   
if __name__ == "__main__":
  main()
  
