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

import sys,os,stat
from re import *

from Common import *
from Utils import *
from Utils_Submod import *
from ObjLog import *
from ObjLock import *
from ObjBranch import *
from ObjTag import *
from ObjStatus import *
from ObjMail import *

g_srcoptions_map = {}


########################
# GENERIC CHECKS
########################
def check(options):

  GLog.s( GLog.S, "Check " + dumpRepoName("your local") + " repository stabilize ..." )

  if options.showmailcfg == True:
    return 0


  if options.testmail:
    om = ObjMailPush()
    if om.isValid() == False:
      GLog.f( GLog.E, "FAILED - Mail not well configured." )
      GLog.f( GLog.E, om.dump() )
      return 1
    return 0

  if options.stb != None or options.cst != None:
    if options.src == None:
      GLog.f( GLog.E, "Option --src-reference mandatory with --stb or --cst" )
      return 1

  if options.liv != None and options.src != None:
      GLog.f( GLog.E, "Option --liv does not need --src" )
      return 1

  #only one option
  opts = 0
  for o in [ options.stb, options.liv, options.cst ]:
    if o != None:
      opts += 1
  if opts != 1:
    GLog.f( GLog.E, "Specify one among --stb or --liv or --cst" )
    return 1

  if options.sendmail == True:
    om = ObjMailStabilize()
    if not om.isValid():
      GLog.f( GLog.E, om.dump() )
      return 1

  # never on origin
  out, errCode = myCommand( "git remote show" )
  if len( out ) == 0:
    GLog.f( GLog.E, "Cannot execute this script on repository origin" )
    return 1 


  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()
  sb = Branch.getStableBr()


  # Stable branch must exist (stabilize not allowed on clone of clone)
  if options.cst == None:
    if not ib.isValid():
      GLog.f( GLog.E, "With --stb or --liv options, you must have an INT branch set, use 'swgit branch --set-integration' to set it." )
      return 1 
    if not sb.isValid():
      GLog.f( GLog.E, "Cannot execute this script on a repository without " + \
          "valid stable branch corresponding to develop branch: %s" % ib.getFullRef() )
      return 1 

  # on right branch
  if options.cst != None: #liv or stb
    if cb.getType() != SWCFG_BR_CST:
      GLog.f( GLog.E, "With --cst option, cannot execute this script on any branch but CST" )
      return 1 
  if options.stb != None:
    if cb.getShortRef() != ib.getShortRef():
      GLog.f( GLog.E, "With --stb option, cannot execute this script on any branch but develop" )
      return 1 
    sb = Branch.getStableBr()
    if not sb.isValid():
      GLog.f( GLog.E, "With --stb option, a stable branch must exists" )
      return 1 

    trackedInfo, tracked = sb.get_track_info()
    if not tracked:
      GLog.f( GLog.E, "With --stb option, a stable branch must be tarcked (track it with swgit branch --track <brname>" )
      return 1 

  if options.liv != None:
    if cb.getShortRef() != sb.getShortRef():
      GLog.f( GLog.E, "With --liv option, cannot execute this script on any branch but stable" )
      return 1 

  # right integration branch set
  if options.stb != None or options.liv != None:
    if ib.getType() != SWCFG_BR_INT:
      GLog.f( GLog.E, "With --stb or --liv options, you must have an INT branch set, use 'swgit branch --set-integration' to change it." )
      return 1
  if options.cst != None:
    if ib.getType() != SWCFG_BR_CST:
      GLog.f( GLog.E, "With --cst option, you must have a CST branch set as integration branch, use swgit branch --set-integration to change it." )
      return 1

  #
  # src management
  #
  if options.src != None:

    options.src = options.src.replace( '.:', './:' )

    if Env.is_aproj() == True:

      ret, options.src = src_reference_check( options.src )
      if ret != 0:
        GLog.f( GLog.E, options.src )
        return 1

    else: #inside repo

      if options.src.find( ',' ) != -1:
        GLog.f( GLog.E, "Outside root project directory, " + \
                         "you can stabilize only current repository, " + \
                         "do not specify multiple values inside options.src, " + \
                         "or move to root project (%s)" % Env.getLocalRoot() )
        return 1

    if options.src.find( ':' ) == -1: #only 1 val
      options.src = "./:%s" % options.src
    if options.src.find( './:' ) == -1: #not currdir listed
      options.src = "./:%s," % shaHEAD + options.src

    global g_srcoptions_map

    #substitute HEAD
    new_opt_str = ""
    for currentry in options.src.split( ',' ):
      dir, ref = currentry.split(':')
      if ref == "HEAD":
        err, shaHEAD = getSHAFromRef( "HEAD", dir )
        new_opt_str += "%s:%s," % ( dir, shaHEAD )
      else:
        new_opt_str += "%s:%s," % ( dir, ref )

    options.src = new_opt_str[:-1] #last ','


    for currentry in options.src.split( ',' ):
      dir, ref = currentry.split(':')
      if ref == "HEAD":
        GLog.f( GLog.E, "Please specify a valid source reference (HEAD it is not) inside repo: %s" % dir )
        return 1

      g_srcoptions_map[ dir ] = ref

      err, sha = getSHAFromRef( ref, dir )
      if err != 0:
        GLog.f( GLog.E, "Please specify a valid source reference inside repo: %s" % dir )
        return 1

      # stabilize anyref
      if get_repo_cfg_bool( SWCFG_STABILIZE_ANYREF, dir ) == False:
        if ref.find( "/NGT/" ) == -1:
          GLog.f( GLog.E, "iside repo %s, according to swgit.stabilize-anyref option, only NGT labels are allowed to be stabilized" % dir )
          return 1


  # reference must be on develop

  # KO:
  #     when anyone pushed on develop while creating NGT tag, 
  #       this NGT label is no more first parent of develop, and this check is bug
#  cmd_getfirst_parent = "git rev-list --first-parent %s --not %s~1 | tail -1" % ( ib.getShortRef(), sha )
#  foundSha, errCode = myCommand_fast( cmd_getfirst_parent )
#  if errCode != 0:
#    parser.error( "Internal error." )
#
#  if foundSha[:-1] != sha:
#    parser.error( "Please specify a valid source reference, must be any commit/reference on main develop branch" )


#  # only user owning origin can (hudson for us)
#  if Env.getCurrUser() != Env.getRemoteUser():
#    GLog.f( GLog.E, "Only user %s can execute this script" % Env.getRemoteUser() )
#    GLog.logRet(1)
#    return 1 

  # generic checks
  err, errstr = Status.checkLocalStatus_rec()
  if err != 0:
    GLog.f( GLog.E, errstr )
    return 1 

  if is_integrator_repo() == False:
    strerr  = "This repository has been created as a 'developer' one.\n"
    strerr += "  You can stabilize only inside 'integrator' repositories.\n"
    strerr += "  You can:\n"
    strerr += "   clone with --integrator\n"
    strerr += "  or\n"
    strerr += "   convert this repo with 'git config --bool swgit.integrator True'"
    GLog.f( GLog.E, strerr )
    return 1 

  ret = 0
  if options.stb != None:
    ret=check_stb(options)
  elif options.liv != None:
    ret=check_liv(options)
  elif options.cst != None:
    ret=check_cst(options)

  return ret



########################
# ONLY STB CHECKS
########################
def check_stb( options ):

  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()

  # this reference must be after last STB
  errCode, stb, num = find_describe_label("%s/%s/*" % ( ib.getShortRef(), SWCFG_TAG_STB), startpoint = ib.getShortRef(), nolog = True  )
  if errCode == 0:

    err, sha = getSHAFromRef( g_srcoptions_map[ "./" ] )
    if err != 0:
      GLog.f( GLog.E, "Please specify a valid source reference" )
      return 1

    errCode, f_ret = AisparentofB( sha, stb )
    if errCode != 0:
      GLog.f( GLog.E, "Internal error.")
      return 1
    
    if f_ret == True:
      GLog.f( GLog.E, "Cannot report on stable this input reference \"%s\". It is same or older of another STB label already present: \"%s\"" % (g_srcoptions_map[ "./" ], stb) )
      return 1

    #
    # Not STB over STB
    #
    errCode, dev, num = find_describe_label("%s/%s/*" % ( ib.getShortRef(), SWCFG_TAG_STB), startpoint = options.src )
    if errCode == 0 and str(num) == "0":
      GLog.f( GLog.E, "You already have a STB label on this commit: %s " % ( dev ) )
      return 1

  #
  # Only 1 STB per DROP 
  #
  err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), SWCFG_TAG_STB, options.stb )
  if len( labels ) != 0:
    GLog.f( GLog.E, "Already exists a STB label named %s (%s)" % (options.stb, "".join( labels )) )
    return 1 


  return 0


########################
# ONLY CST CHECKS
########################
def check_cst( options ):

  cb = Branch.getCurrBr()

  inputRef = g_srcoptions_map[ "./" ]
  err, sha = getSHAFromRef( inputRef )
  if err != 0:
    GLog.f( GLog.E, "Please specify a valid source reference" )
    return 1

  errCode, f_ret = AisparentofB( sha, cb.getShortRef() )
  if errCode != 0:
    GLog.f( GLog.E, "Internal error.")
    return 1
    
  if f_ret == True:
    GLog.f( GLog.E, "CST \"%s\" already contains this input reference \"%s\"." % ( cb.getShortRef(), inputRef ) )
    return 1

  #
  # Only 1 LIV per DROP
  #
  err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), SWCFG_TAG_LIV, options.cst )
  if len( labels ) != 0:
    GLog.f( GLog.E, "Already exists a LIV label named %s (%s)" % (options.cst, "".join( labels )) )
    return 1 

  return 0


########################
# ONLY LIV CHECKS
########################
def check_liv( options ):
  #
  # Not LIV over LIV
  #
  cb = Branch.getCurrBr()
  sb = Branch.getStableBr()
  startref = sb.getShortRef()

  errCode, dev, num = find_describe_label("%s/%s/*" % ( sb.getShortRef(), SWCFG_TAG_LIV), startpoint = startref )
  if errCode == 0 and str(num) == "0":
    GLog.f( GLog.E, "You already have a LIV label on this commit: %s " % ( dev ) )
    return 1 

  #
  # once: There must be a STB before a LIV with same name (without .1 .2 ...)
  # now:  Find last stable and prompt user (usefull in repackage scenario: 
  #        first round:  --stb AI_34
  #                      --liv AI_34
  #        second round: --liv AI_35 (without intermediate STB) (hudson increment automatically build number)
  #
  err, labels = Tag.list( sb.getRel(), sb.getUser(), sb.getType(), sb.getName(), SWCFG_TAG_STB )
  if len( labels ) == 0:
    strerr  = "There is no stable label named %s\n" % options.liv
    strerr += "You must run 'swgit stabilize --stb %s' to stabilize some contribute before creating a LIV"
    GLog.f( GLog.E, indentOutput( strerr, 1 ) )
    return 1  

  #
  # Only 1 LIV per DROP
  #
  err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), SWCFG_TAG_LIV, options.liv )
  if len( labels ) != 0:
    GLog.f( GLog.E, "Already exists a LIV label named %s (%s)" % (options.liv, "".join( labels )) )
    return 1 

  return 0


########################
# STABILIZE
########################
def stabilize( lblType, lblName, src_str, mergeOntoBr = None ):

  cb = Branch.getCurrBr()
  startref = g_srcoptions_map[ "./" ]

  GLog.s( GLog.S, "On %s repo: creating %s tag for drop %s on release %s starting from %s" % ( dumpRepoName("local"), lblType, lblName, cb.getRel().replace( "/","." ), startref ) )


# you can assign a different regexp and don't know how to increment =>
#  force specifying new label
#  #
#  # increment if necessary
#  #
#  num = 0
#  GLog.f( GLog.I, "Looking for an existing label %s on branch %s" % ( lblName, cb.getShortRef() ) )
#  err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, lblName )
#  while len( labels ) != 0:
#    num += 1
#    GLog.f( GLog.I, "Looking for an existing label %s.%s on branch %s" % ( lblName, num, cb.getShortRef() ) )
#    err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, "%s.%s" % (lblName,num) )
#  if num != 0:
#    lblName = "%s.%s" % ( lblName, num )

  
  #
  # Create STB Tag on develop
  #
  if lblType == SWCFG_TAG_STB:
    fullTagName_dev = "%s/%s/%s/%s/%s/%s" % ( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, lblName )
    cmd_create_tag_dev = "%s branch --quiet -s %s && SWINDENT=%d %s tag -m \"%s\" %s %s && %s branch -S --quiet" %  ( SWGIT, startref, GLog.tab+1, SWGIT, fullTagName_dev, lblType, lblName, SWGIT )

    #GLog.s( GLog.S, "\tCreating tag %s on ref %s" % ( fullTagName_dev, startref ) )

    #out, errCode = myCommand( cmd_create_tag_dev )
    errCode = os.system( cmd_create_tag_dev )
    if errCode != 0:
      GLog.f( GLog.E, "\tError while creating label %s on branch %s" % ( lblName, cb.getShortRef() ) )
      GLog.logRet(errCode)
      return 1 

    #GLog.logRet( 0, indent="\t" )


  if mergeOntoBr != None:
    #
    # Switch on stable branch
    #
    cmd_goto_stb = "git checkout %s" % mergeOntoBr.getShortRef()
    out, errCode = myCommand( cmd_goto_stb )
    if errCode != 0:
      GLog.f( GLog.E, "Error while switching onto %s branch" % mergeOntoBr.getShortRef() )
      GLog.logRet(errCode)
      return 1 

    cb = Branch.getCurrBr()


  #
  # Inside a project, clean local status before merging
  #
  if os.path.exists( "./%s" % (SWFILE_PROJMAP) ) == True:
    cmd_resethead = "SWINDENT=%d %s proj --reset HEAD" % ( GLog.tab+1, SWGIT )
    errCode = os.system( cmd_resethead )
    if errCode != 0 :
      return 1


  #
  # Merge ref label
  #
  cmd_merge_stblbl = "git merge --no-ff %s" % startref

  GLog.s( GLog.S, "\tMerging reference %s on branch %s" % ( startref, cb.getShortRef() ) )

  out, errCode = myCommand( cmd_merge_stblbl )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while merging %s on branch %s" % ( startref, cb.getShortRef() ) )
    GLog.logRet(errCode)
    return 1 

  GLog.logRet( 0, indent="\t" )


  #
  # If you are a proj, move on src input references inside subrepos
  #   and comit proj to freeze repos alignment
  #
  if os.path.exists( "./%s" % (SWFILE_PROJMAP) ) == True: #inside project

    for currentry in src_str.split( ',' ):
      dir, ref = currentry.split(':')
      if dir == "./":
        continue

      cmd_selectref_subrepo = "cd %s && git checkout %s" % ( dir, ref )
      out, errCode = myCommand( cmd_selectref_subrepo )
      if errCode != 0 :
        GLog.f( GLog.E, out )
        return 1

    # now commit repositories changes
    cmd_commitmodules = "git commit -a -m \"Submodules commit\" --allow-empty"
    out, errCode = myCommand( cmd_commitmodules )
    if errCode != 0 :
      GLog.f( GLog.E, out )
      return 1

  #
  # Create Tag on mergeOntoBr
  #
  fullTagName_stb = "%s/%s/%s/%s/%s/%s" % ( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, lblName )
  cmd_create_tag_stb = "SWINDENT=%d %s tag -m \"%s\" %s %s" %  ( GLog.tab+1, SWGIT, fullTagName_stb, lblType, lblName )

  #GLog.s( GLog.S, "\tCreating tag %s on branch %s" % ( fullTagName_stb, cb.getShortRef() ) )

  #out, errCode = myCommand( cmd_create_tag_stb )
  errCode = os.system( cmd_create_tag_stb )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while creating label %s on branch %s" % ( lblName, cb.getShortRef() ) )
    GLog.logRet(errCode)
    return 1 

  #GLog.logRet( 0, indent="\t" )

  GLog.logRet( 0 )
  return 0


########################
# GENERIC EXECUTE
########################
def execute( options ):

  if options.showmailcfg == True:

    om = ObjMailStabilize()
    print om.dump()
    print om.show_config_options()
    print ""
    return 0

  elif options.testmail:

    GLog.s( GLog.S, "Sending test mail" )

    om = ObjMailStabilize()
    out, err = om.sendmail( "TAG DROP TEST MAIL", debug = False )
    if out[:-1] != "":
      GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    GLog.logRet( err )
    return err

  if options.stb != None:
    ret = tag_drop_stb( options )

  if options.cst != None:
    ret = tag_drop_cst( options )

  if options.liv != None:
    ret = tag_drop_liv( options )

  return ret
 

########################
# STB EXECUTE
########################
def tag_drop_stb( options ):

  err, sha = getSHAFromRef( options.src )

  return stabilize( SWCFG_TAG_STB, options.stb, sha, Branch.getStableBr() )
  

########################
# CST EXECUTE
########################
def tag_drop_cst( options ):

  # stabilize
  errCode = stabilize( SWCFG_TAG_LIV, options.cst, options.src )
  if errCode != 0:
    return errCode

  # push on origin
  cb = Branch.getCurrBr()
  GLog.s( GLog.S, "Pushing %s on origin ... " % ( cb.getShortRef() ))

  mail_opt = "--no-mail"
  if options.sendmail:
    mail_opt = ""

  cmd_push_cst = "SWINDENT=%d %s push %s %s" % ( GLog.tab + 1, SWGIT, getOutputOpt(options), mail_opt )
  errCode = os.system( cmd_push_cst )
  if errCode != 0 :
    GLog.logRet( errCode )
    return 1
  
  GLog.logRet( 0 )
  return 0



########################
# LIV EXECUTE
########################
def tag_drop_liv( options ):

  lblType = SWCFG_TAG_LIV
  lblName = options.liv

  base = sys.argv[0][0:sys.argv[0].rfind("/")+1]
  output_opt = getOutputOpt(options)

  notdottedLblName = lblName

  cb = Branch.getCurrBr()
  sb = Branch.getStableBr()
  ib = Branch.getIntBr()

  GLog.s( GLog.S, "On %s repo: creating %s tag for drop %s on release %s" % ( dumpRepoName("local"), lblType, lblName, cb.getRel().replace("/",".") ) )

# you can assign a different regexp and don't know how to increment =>
#  force specifying new label
#  #
#  # increment if necessary
#  #
#  num = 0
#  GLog.f( GLog.D, "Looking for an existing label %s on branch %s" % ( lblName, sb.getShortRef() ) )
#  err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, lblName )
#  while len( labels ) != 0:
#    num += 1
#    GLog.f( GLog.D, "Looking for an existing label %s.%s on branch %s" % ( lblName,num, cb.getShortRef() ) )
#    err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, "%s.%s" % (lblName,num) )
#  if num != 0:
#    lblName = "%s.%s" % ( lblName, num )

  
  #
  # once: There must be a STB before a LIV with same name (without .1 .2 ...)
  # now:  Find last stable and prompt user (usefull in repackage scenario: 
  #        first round:  --stb AI_34
  #                      --liv AI_34
  #        second round: --liv AI_35 (without intermediate STB) (hudson increment automatically build number)
  #
  err, labels = Tag.list( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), SWCFG_TAG_STB )
  if len( labels ) == 0:
    GLog.f( GLog.E, "There is no stable label named %s, please run \"swgit stabilize --stb <%s>\" to freeze develop contributes" % (lblName, lblName) )
    GLog.logRet(1)
    return 1 

  last = len( labels ) - 1

  GLog.s( GLog.S, "Last stable label is: %s" % ( labels[last] ) )
  GLog.s( GLog.S, "You are going to create a %s tag named \"%s\" on release %s" % ( lblType, lblName, cb.getRel().replace( "/","." ) ) )

  if options.noint == False:
    ans = raw_input( "Continue? [Y/n]" )
    if ans=="no" or ans=="n" or ans=="N" or ans == "NO" or ans == "No" or ans == "nO":
      GLog.s( GLog.S, "\tLabel creation aborted by user" )
      GLog.logRet(0)
      sys.exit(0)
  

  #LIV on stable
  errCode, lastbutone_liv, dist = find_describe_label( '\'%s/%s/%s/%s/%s/*\'' % ( cb.getRel(), cb.getUser(), cb.getType(), sb.getName(), SWCFG_TAG_LIV ) )
  if errCode != 0:
    firstCommit_cmd = "git log --format='%H %ad'  | tail -n 1"
    out, errCode = myCommand( firstCommit_cmd )
    firstCommit = out[ : out.find(" ")-1 ]

    GLog.s( GLog.S, "\tThis is your first LIV label " )
    lastbutone_liv = firstCommit
    lastbutone_stb = ""

  else: 
    GLog.s( GLog.S, "\tLast LIV Label is %s" % lastbutone_liv )

    lastbutone_lblName = lastbutone_liv[ lastbutone_liv.rfind("/") +1 :]
    #
    # from repackaging on, STB evaluated in this way may not exist!!! 
    #    (more LIV and just 2 STB) => do not use it, just LIV
    #
    lastbutone_stb = "%s/%s/%s/%s/%s/%s" % ( cb.getRel(), cb.getUser(), cb.getType(), ib.getName(), SWCFG_TAG_STB, lastbutone_lblName )
  
    #GLog.s( GLog.S, "\tLast STB Label is %s" % lastbutone_stb )


  #
  # find dev labels from last LIV
  #
  GLog.s( GLog.S, "\tLooking for all contributes entered since last LIV" )

  #upstream = "%s %s" % ( lastbutone_liv, lastbutone_stb )
  upstream = "%s" % ( lastbutone_liv )
  errCode, out = info_eval_anylog( upstream, "HEAD", cb.getRel(), typeTag = SWCFG_TAG_DEV )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving all merged DEVs" )
    GLog.logRet(errCode)

    return 1 
  devs = out.splitlines()

  GLog.f( GLog.D, "DEV Labels merged since last LIV are:\n\t" + "\n\t".join( devs ) )
  
  pathChangeLog = "%s/%s/%s"  % ( Env.getLocalRoot(), SWDIR_CHANGELOG, cb.getRel() )
  if os.path.exists( pathChangeLog ) != True :
    cmd_mkdir = "mkdir -p %s " % pathChangeLog
    out, errCode = myCommand( cmd_mkdir )
    if errCode != 0:
      GLog.f( GLog.E, "\tError on creating dirs for changelog " )
      GLog.logRet(errCode)
      return 1 

  changelog = "%s/%s_%s.chg" % ( pathChangeLog, lblType, lblName )
  cmd_redirectfile = " tee %s" % ( changelog )
  cmd_show_commitmsg = " git for-each-ref \
  --format='From:    %(*authorname) %(*authoremail)\nDate:    %(*authordate)\nRef:     %(refname)\n\n    %(subject)\n\n'"
  errCode = 0
  if len(devs) == 0:
    out, errCode = myCommand( "echo \"No DEV\" | %s" % ( cmd_redirectfile ) )
  else: 
    out, errCode = myCommand( "%s %s | %s" % ( cmd_show_commitmsg, "refs/tags/"+" refs/tags/".join(devs), cmd_redirectfile ) )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving changelog" )
    GLog.logRet(errCode)
    return 1 


  #
  # find fix labels from last LIV
  #
  errCode, out = info_eval_anylog( upstream, "HEAD", cb.getRel(), typeTag = SWCFG_TAG_FIX )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving all merged FIXes" )
    GLog.logRet(errCode)
    return 1 

  lblfixes = out.splitlines()

  GLog.f( GLog.D, "FIX Labels merged since last LIV are:\n\t" + "\n\t".join( lblfixes ) )

  fixlog = "%s/%s/%s/%s_%s.fix" % ( Env.getLocalRoot(), SWDIR_CHANGELOG, cb.getRel(), lblType, lblName )
  cmd_redirectfile = " tee %s" % ( fixlog )
  cmd_show_commitmsg = " git for-each-ref \
  --format='From:    %(*authorname) %(*authoremail)\nDate:    %(*authordate)\nRef:     %(refname)\n\n    %(subject)\n\n'"
  
  if len(lblfixes) == 0:
    out, errCode = myCommand( "echo \"No FIX\" | %s" % ( cmd_redirectfile ) )
  else: 
    out, errCode = myCommand( "%s %s | %s" % ( cmd_show_commitmsg, "refs/tags/"+" refs/tags/".join(lblfixes), cmd_redirectfile ) )
  
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving fixlog" )
    GLog.logRet(errCode)
    return 1 


  #
  # ticket numbers fixed in this drop
  #
  ticketlog = "%s/%s/%s/%s_%s.tkt" % ( Env.getLocalRoot(), SWDIR_CHANGELOG, cb.getRel(), lblType, lblName )
  tickets = []
  for f in lblfixes:
    #example of lblfixes: tags/4.0/vallea/FTR/fixos/FIX/Issue11112
    tickets.append( f[ f.rfind("/")+1 : ] )

  GLog.f( GLog.D, "Tickets fixed in this drop are:\n\t" + "\n\t".join( tickets ) )

  FILE = open( ticketlog, "w" )
  FILE.write( "%s\n" % "\n".join(tickets) )
  FILE.close()
  os.chmod( ticketlog, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH )

  GLog.logRet( 0, indent="\t" )

  #
  # add and commit changelog, fixlog and ticketlog
  #
  stradd  = "\tAdding under configuration control these files:\n"
  stradd += "\t  %s\n" % changelog
  stradd += "\t  %s\n" % fixlog
  stradd += "\t  %s" % ticketlog

  GLog.s( GLog.S, stradd )

  cmd_add_and_commit = "git add %s %s %s && git commit  --allow-empty  -m \"Added Changelog, Fixlog and Ticketlog for drop %s_%s , release %s )\"" % \
        ( changelog, fixlog, ticketlog, lblType, lblType, cb.getRel().replace( "/","." ) )
  out, errCode = myCommand( cmd_add_and_commit )
  if errCode != 0:
    GLog.f( GLog.E, "Error while adding and committting Changelog and Fixlog" )
    GLog.logRet(errCode)
    return 1 
  GLog.logRet( 0, indent="\t" )

  #
  # Create Tag
  #
  fullTagName = "%s/%s/%s/%s/%s/%s" % ( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), lblType, lblName )
  cmd_create_tag = "SWINDENT=%d %s tag -m \"%s\" %s %s" %  ( GLog.tab+1, SWGIT, fullTagName, lblType, lblName )

  #GLog.s( GLog.S, "\tCreating tag %s" % ( fullTagName ) )

  #out, errCode = myCommand( cmd_create_tag )
  errCode = os.system( cmd_create_tag )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while tagging Changelog and Fixlog" )
    GLog.logRet(errCode)
    return 1 
  #GLog.logRet( 0, indent="\t" )

  #
  # push on origin stable
  #
  GLog.s( GLog.S, "\tPushing %s on origin ... " % ( sb.getShortRef() ))

  mail_opt = "--no-mail"
  if options.sendmail:
    mail_opt = ""

  cmd_push_stable = "SWINDENT=%d %s push %s %s" % ( GLog.tab+2, SWGIT, output_opt, mail_opt )
  errCode = os.system( cmd_push_stable )
  if errCode != 0 :
    GLog.logRet( errCode )
    sys.exit( 1 )  
  GLog.logRet( 0, indent="\t" )


  #
  # prepare and send mail
  #
  if options.sendmail == True:
    GLog.s( GLog.S, "\tSending mail" )

    try:
      cmd_order_devs = "git for-each-ref --sort='*authorname' --format='%%(refname:short) %%(subject)' %s" % ( "refs/tags/"+" refs/tags/".join( devs ) )
      out, errCode = myCommand( cmd_order_devs )
      if errCode != 0:
        raise "\tError while grouping devs to send mail"

      #
      # Tickets list
      #
      body_mail_tickets = "List of Tickets fixed in %s/%s:\n\n" % ( lblType, lblName )
      linestring = open( ticketlog, 'r').read()[:-1]
      if len(linestring) == 0:
        body_mail_tickets = body_mail_tickets + "  * No Tickets fixed in this DROP \n"
      else:
        body_mail_tickets = body_mail_tickets + "  * " + "\n  * ".join( linestring.split('\n') ) + "\n"

      GLog.f( GLog.D, body_mail_tickets )

      #
      # Dev list by user
      #
      body_mail_devs = "\nList of DEV labels entered %s/%s for each user:\n" % ( lblType, lblName )
      prevname = ""
      currname = ""
      for dev in out.splitlines():
        currname = dev
        currname = currname[ currname.find("/")+1 : ] #cut off rel
        currname = currname[ findnth( currname, "/", 4 ) + 1 :  ] #cut off rel (4 "/")
        currname = currname[ 0 : currname.find('/')]
        if currname != prevname:
          body_mail_devs += "\n%s\n * User %s:\n%s\n" % ( "="*58, currname, "="*58 )
          prevname = currname

        body_mail_devs += "     %s\n          %s\n%s\n" % ( dev[ 0 : dev.find(' ') ], dev[ dev.find(' ') : ], '-'*58 )

      GLog.f( GLog.D, body_mail_devs )

      #
      # Prepare and send mail
      #
      om = ObjMailStabilize()
      if om.isValid() == False:
        raise Exception( "\tCannot send mail, bad configured\n" % om.dump() )

      out, err = om.sendmail( "%s\n%s" % (body_mail_tickets, body_mail_devs), debug = False )

      GLog.f( GLog.I, out )
      if err != 0:
        raise Exception( "\tError while sending mail\n%s" % indentOutput( out[:-1], 2 ) )

    except Exception, e:
      GLog.f( GLog.E, e.__str__ )
      GLog.logRet( 1, indent = "\t" )
    GLog.logRet( 0, indent = "\t" )



  #
  # Merge on develop
  #
  
  # 1. checkout develop
  ib = Branch.getIntBr()
  GLog.s( GLog.S, "\tMerging LIV %s in %s ... " % ( fullTagName, ib.getShortRef() ))
  if os.path.exists( "./%s" % (SWFILE_PROJMAP) ) == True: #inside project
    cmd_goto_dev = "SWINDENT=%d %s branch -s %s && SWINDENT=%d %s proj --reset HEAD" % ( GLog.tab+2, SWGIT, ib.getShortRef(), GLog.tab+2, SWGIT )
  else:
    cmd_goto_dev = "SWINDENT=%d %s branch -s %s" % ( GLog.tab+2, SWGIT, ib.getShortRef() )
  out, errCode = myCommand( cmd_goto_dev )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while switching to %s branch" % ib.getShortRef() )
    GLog.logRet(errCode)
    return 1 


  cb = Branch.getCurrBr()

  # 2. merge LIV
  cmd_merge_liv = "SWINDENT=%d %s merge %s %s" % ( GLog.tab+2, SWGIT, fullTagName, output_opt )
  errCode = os.system( cmd_merge_liv )
  if errCode != 0 :
    GLog.logRet( errCode )
    sys.exit( 1 )  
  GLog.logRet( 0, indent="\t" )

  #
  # Proj: after merge, update subrepos according to new map 
  #       also on develop
  if os.path.exists( "./%s" % (SWFILE_PROJMAP) ) == True: #inside project
    cmd_refresh = "cd %s && SWINDENT=%s %s proj --reset HEAD" % ( Env.getProjectRoot(), GLog.tab, SWGIT )
    errCode = os.system( cmd_refresh )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )


  # 3. push on origin develop
  GLog.s( GLog.S, "\tPushing %s on origin ... " % ( ib.getShortRef() ))

  cmd_push_dev = "SWINDENT=%d %s push %s %s" % ( GLog.tab+2, SWGIT, output_opt, mail_opt )
  errCode = os.system( cmd_push_dev )
  if errCode != 0 :
    GLog.logRet( errCode )
    sys.exit( 1 )  
  GLog.logRet( 0, indent="\t" )


#  #
#  # 4. push on origin old develop/STB ( created using --src )
#  #
#  errCode, out = info_eval_anylog( lastbutone_liv, "HEAD", cb.getRel(), typeTag=SWCFG_TAG_STB )
#  if errCode != 0 :
#    GLog.f(GLog.F, "\tNOT CRITICAL ERROR on retriving list of develop/STB label from %s. Check develop/STB label pushed" % lastbutone_liv )
#    GLog.logRet( errCode )
#    sys.exit( 1 )  
#
#  stbLblToPush = out.replace("\n"," ")
#  
#  cmd_stbToPush = "git push origin %s " % stbLblToPush
#  out, errCode = myCommand( cmd_stbToPush  )
#  if errCode != 0:
#    GLog.f( GLog.E, "\tNOT CRITICAL ERROR on pushing list of STB label from %s. Check develop/STB label pushed" % lastbutone_liv )
#    GLog.logRet(errCode)
#    sys.exit(1)

  GLog.logRet( 0 )
  return 0




#def perform_recurse( options ):
#  
#  ret, src_str = src_reference_check( options.src )
#  if ret != 0:
#    return 1, src_str
#
#  # deepest repo, execust true stabilize
#  if options.src.find( ',' ) == -1:
#    options.src = options.src[ options.src.find( ':' ) + 1 : ]
#    return 0, ""
#
#  err_str ""
#  children = submod_list_repos( firstLev = True )
#  for r in children:
#    src_subtree = ""
#    subtree_begin = "./%s" % r
#
#    for currentry in src_str.split( ',' ):
#      dir = currentry.split(':')[0]
#      ref = currentry.split(':')[1]
#      if dir .find( subtree_begin ) == 0:
#        src_subtree += "%s:%s," % ( dir.replace( src_subtree, "./" ), ref )
#
#    if len( src_subtree ) > 0:
#      src_subtree = src_subtree[ : -1] #eliminate last comma
#
#    input_without_src = input_eliminate_option( [ "--src", "--src-reference" ], optionWithParam = True )
#
#    cmd_stabilize_subtree = "cd %s && SWCHECK=ONLY %s --src %s" % ( dir, input_without_src, src_subtree )
#    errCode = os.system( cmd_stabilize_subtree )
#    if errCode != 0:
#      err_str += dir + " "
#
#  # after children, process containing project
#  options.src.find( '.'
#  cmd_stabilize_subtree = "SWCHECK=ONLY %s --src %s" % ( dir, input_without_src, src_subtree )
#  errCode = os.system( cmd_stabilize_subtree )
#  if errCode != 0:
#    err_str += dir + " "
#
#
#  if err_str != ""
#    return 1, err_str

    


def main():
  usagestr =  """\
Usage: swgit stabilize --stb <label> [--src <startpoint>]
   or: swgit stabilize --liv <label>
   or: swgit stabilize --cst <label> """

  parser       = OptionParser( usage = usagestr,
                               description='>>>>>>>>>>>>>> swgit - Stabilize Management <<<<<<<<<<<<<<' )
  mgt_group    = OptionGroup( parser, "Management options" )
  mail_group    = OptionGroup( parser, "Mail options" )
  output_group = OptionGroup( parser, "Output options" )

  load_command_options( mgt_group, gitstabilize_mgt_options )
  load_command_options( mail_group, gitstabilize_mail_options )
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( mgt_group )
  parser.add_option_group( mail_group )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()

  help_mac( parser )

  if len( args ) != 0:
    parser.error("Too many arguments")

  GLog.initGitLogs( options )
  GLog.s( GLog.I, " ".join( sys.argv ) )


  if os.environ.get('SWCHECK') != "NO":
    if check(options) != 0:
      GLog.logRet(1)
      sys.exit(1)
    GLog.logRet(0)
  
  if os.environ.get('SWCHECK') == "ONLY":
    sys.exit(0)

  ret = execute(options)
  if ret != 0:
    sys.exit( 1 )
  sys.exit( 0 )
 


def check_dropname( option, opt_str, value, parser ):
  check_input( option, opt_str, value, parser )
  
  if parser.values.stb != None and parser.values.liv != None:
    parser.error( "Cannot specify --stb and --liv togheter" )

  #TODO allow user make a --liv with ANY tag user defined tag (not only LIV)
  tagDsc = None
  if parser.values.stb != None:
    tagDsc = create_tag_dsc( SWCFG_TAG_STB )
  elif parser.values.liv != None:
    tagDsc = create_tag_dsc( SWCFG_TAG_LIV )
  elif parser.values.cst != None:
    tagDsc = create_tag_dsc( SWCFG_TAG_LIV )

  if not tagDsc.check_valid_value( value ):
    parser.error( "Please specify a valid name for label %s (i.e. satisfying at least 1 regexp inside: %s)" % 
        ( tagDsc.get_type(), tagDsc.get_regexp() ) )

  setattr(parser.values, option.dest, value)


def check_src( option, opt_str, value, parser ):
  check_input( option, opt_str, value, parser )


gitstabilize_mgt_options = [
    [
      "--stb",
      "--stb-label",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_dropname,
        "dest"    : "stb",
        "metavar" : "<label_name>",
        "help"    : "Reports --src argument on \"/INT/stable\" branch, labelize merge boundaries with STB label. Must match default regexp '%s' or customized version (see 'swgit tag --custom-tag-show-cfg STB' )"  % SWCFG_TAG_LIVREGEXP
        }
      ],
    [
      "--src",
      "--src-reference",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_src,
        "dest"    : "src",
        "metavar" : "<reference>",
        "help"    : "With --stb option. Provides staring point to be stabilized on \"/INT/stable\" branch. Its argument can be a reference, a comma-separed list of <dir>:<reference> pairs, a file (these last two modes are useful inside projects)"
        }
      ],
    [
      "--liv",
      "--liv-label",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_dropname,
        "dest"    : "liv",
        "metavar" : "<label_name>",
        "help"    : "Create LIV label on \"/INT/stable\" branch with last stabilized contributes. Evaluates changelog, fixlog from last LIV. Report everithing on \"/INT/develop\"."
        }
      ],
    [
      "--cst",
      "--cst-label",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_dropname,
        "dest"    : "cst",
        "metavar" : "<label_name>",
        "help"    : "Report --src argument on \"/CST/a_customer\" branch, labelize merge boundaries with LIV label. Must match default regexp '%s' or customized version (see 'swgit tag --custom-tag-show-cfg LIV' )"  % SWCFG_TAG_LIVREGEXP
        }
      ],
    [
      "--no-interactive",
      {
        "action"  : "store_true",
        "dest"    : "noint",
        "default" : False,
        "help"    : 'Avoid requesting integrator "yes" (used with scripts)'
        }
      ]
   ]

gitstabilize_mail_options = [
    [
      "--sm",
      "--send-mail",
      {
        "action"  : "store_true",
        "dest"    : "sendmail",
        "default" : False,
        "help"    : 'Send mail. Please configure mail parameters.'
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
  
