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

#TODO allow user make a --liv with ANY tag user defined tag (not only LIV)
#TODO option to merge back customizable as repo option

g_srcoptions_map = {}
g_labelname = None
g_targetbr = None
g_rel_path = None
g_devs  = []
g_fixes = []
g_chgfname = None
g_fixfname = None
g_tktfname = None

# 1. eval from cb
# 2. eval from intbr
def eval_mergeonto_br():

  global g_targetbr
  if g_targetbr != None:
    return 0

  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()

  if cb.isValid():

    if cb.isStable() or cb.getType() == SWCFG_BR_CST:
      g_targetbr = cb.getShortRef()
      return 0

  if ib.isValid() and ib.isStable():
    g_targetbr = ib.getShortRef()
    return 0

  if ib.isValid() and ib.isDevelop():
    literatl_stable = ib.getShortRef().replace( "develop", "stable" )
    g_targetbr = literatl_stable
    return 0

  strerr  = "Cannot deduce onto which branch to make stb/liv.\n"
  strerr += "You can choose among:\n"
  strerr += "    1. providing it on command line\n"
  strerr += "    2. moving on target branch with 'swgit branch --switch'\n"
  strerr += "    3. setting an 'INT/develop' integration branch by 'swgit branch --set-integration-br'\n"
  GLog.f( GLog.E, strerr )
  return 1 


def valorize_devs( upstream ):

  global g_devs
  cb = Branch.getCurrBr()

  errCode, out = info_eval_anylog( upstream, cb.getShortRef(), cb.getRel(), typeTag = SWCFG_TAG_DEV )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving all merged DEVs" )
    GLog.f( GLog.E, indentOutput( out,1 ) )
    GLog.logRet(errCode)
    return 1 

  g_devs = out.splitlines()

  GLog.f( GLog.I, "DEV Labels merged since last LIV are:\n\t" + "\n\t".join( g_devs ) )
  return 0

def valorize_fixes( upstream ):

  global g_fixes
  cb = Branch.getCurrBr()

  errCode, out = info_eval_anylog( upstream, cb.getShortRef(), cb.getRel(), typeTag = SWCFG_TAG_FIX )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving all merged FIXes" )
    GLog.f( GLog.E, indentOutput( out,1 ) )
    GLog.logRet(errCode)
    return 1 

  g_fixes = out.splitlines()

  GLog.f( GLog.I, "FIX Labels merged since last LIV are:\n\t" + "\n\t".join( g_fixes ) )
  return 0


def create_rel_path():

  cb = Branch.getCurrBr()

  global g_rel_path
  g_rel_path = "%s/%s/%s"  % ( Env.getLocalRoot(), SWDIR_CHANGELOG, cb.getRel() )
  if os.path.exists( g_rel_path ):
    return 0

  cmd_mkdir = "mkdir -p %s " % g_rel_path
  out, errCode = myCommand( cmd_mkdir )
  if errCode != 0:
    GLog.f( GLog.E, "\tError on creating dirs for changelog " )
    GLog.logRet(errCode)
    return 1 
  return 0


def touch_file( fname ):
  FILE = open( fname, "w" )
  FILE.close()
  #os.chmod( fname, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH )
  return 0


def eval_changelog_content():

  global g_changelog
  g_changelog = "%s/%s_%s.chg" % ( g_rel_path, SWCFG_TAG_LIV, g_labelname )

  if len( g_devs ) == 0:
    touch_file( g_changelog )
    return 0

  #TODO customize format
  cmd_show_commitmsg = "git for-each-ref --format='%s'" % SWCFG_STABILIZE_CHGLOG_FILE_FORMAT
  cmd_redirectfile = "tee %s" % ( g_changelog )

  out, errCode = myCommand( "%s %s | %s" % ( cmd_show_commitmsg, " ".join( [ "refs/tags/" + d for d in g_devs] ), cmd_redirectfile ) )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving changelog" )
    GLog.logRet(errCode)
    return 1 
  return 0


def eval_fixlog_content():

  global g_fixlog
  g_fixlog = "%s/%s_%s.fix" % ( g_rel_path, SWCFG_TAG_LIV, g_labelname )

  if len( g_fixes ) == 0:
    touch_file( g_fixlog )
    return 0

  #TODO customize format
  cmd_show_commitmsg = "git for-each-ref --format='%s'" % SWCFG_STABILIZE_FIXLOG_FILE_FORMAT
  cmd_redirectfile = "tee %s" % ( g_fixlog )
  
  out, errCode = myCommand( "%s %s | %s" % ( cmd_show_commitmsg, " ".join( [ "refs/tags/" + d for d in g_fixes] ), cmd_redirectfile ) )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving fixlog" )
    GLog.logRet(errCode)
    return 1 
  return 0

def eval_tktlog_content():

  global g_tktlog
  g_tktlog = "%s/%s_%s.tkt" % ( g_rel_path, SWCFG_TAG_LIV, g_labelname )
  tickets = [ tag_2_tagname( f ) for f in g_fixes ]
  GLog.f( GLog.I, "Tickets fixed in this drop are:\n\t" + "\n\t".join( tickets ) )

  FILE = open( g_tktlog, "w" )
  FILE.write( "\n".join(tickets) )
  FILE.close()
  os.chmod( g_tktlog, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH )
  return 0


def eval_create_commit_logs( upstream ):

  cb = Branch.getCurrBr()

  #
  # find dev labels from last LIV
  #
  GLog.s( GLog.S, "\tLooking for all contributes entered since last LIV" )

  ret = valorize_devs( upstream )
  if ret != 0:
    return 1

  ret = valorize_fixes( upstream )
  if ret != 0:
    return 1

  ret = create_rel_path()
  if ret != 0:
    return 1
  
  ret = eval_changelog_content()
  if ret != 0:
    return 1

  ret = eval_fixlog_content()
  if ret != 0:
    return 1

  ret = eval_tktlog_content()
  if ret != 0:
    return 1

  GLog.logRet( 0, indent="\t" )

  #
  # add and commit changelog, fixlog and ticketlog
  #
  stradd  = "\tAdding under configuration control these files:\n"
  stradd += "\t  %s\n" % g_changelog
  stradd += "\t  %s\n" % g_fixlog
  stradd += "\t  %s"   % g_tktlog

  GLog.s( GLog.S, stradd )

  cmd_add    = "git add %s %s %s " % ( g_changelog, g_fixlog, g_tktlog )
  cmd_commit = "git commit  --allow-empty  -m \"Added Changelog, Fixlog and Ticketlog for drop %s_%s, release %s )\"" % \
                            (SWCFG_TAG_LIV, g_labelname, cb.getRel().replace( "/","." ))
  
  out, errCode = myCommand( "%s && %s" % ( cmd_add, cmd_commit ) )
  if errCode != 0:
    GLog.f( GLog.E, "Error while adding and committing Changelog, Fixlog and Ticketlog" )
    GLog.logRet(out)
    GLog.logRet(errCode)
    return 1 
  GLog.logRet( 0, indent="\t" )
  return 0



def eval_body_mail():

  #tickets
  body_mail_tickets  = "List of Tickets fixed in %s/%s:\n\n" % ( SWCFG_TAG_LIV, g_labelname )
  body_mail_tickets += "\n".join( g_fixes )
  GLog.f( GLog.I, body_mail_tickets )

  #Devs
  cmd_show_commitmsg = "git for-each-ref --format='%s' --sort='%s'" % (SWCFG_STABILIZE_CHGLOG_MAIL_FORMAT,SWCFG_STABILIZE_CHGLOG_MAIL_SORT)
  out_devs, errCode = myCommand( "%s %s" % ( cmd_show_commitmsg, " ".join( [ "refs/tags/" + d for d in g_fixes] ) ) )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving changelog" )

  body_mail_devs  = "\nList of DEV labels entered into %s/%s :\n\n" % ( SWCFG_TAG_LIV, g_labelname )
  body_mail_devs += "\n".join( out_devs )
  GLog.f( GLog.I, body_mail_devs )

  return body_mail_tickets + "\n" + body_mail_devs


########################
# GENERIC CHECKS
########################
def check(options):

  GLog.s( GLog.S, "Check " + dumpRepoName("your local") + " repository stabilize ..." )

  # mail checks #####
  if options.showmailcfg == True:
    return 0

  if options.testmail:
    om = ObjMailPush()
    if om.isValid() == False:
      GLog.f( GLog.E, "FAILED - Mail not well configured." )
      GLog.f( GLog.E, om.dump() )
      return 1
    return 0

  if options.sendmail:
    om = ObjMailStabilize()
    if not om.isValid():
      GLog.f( GLog.E, om.dump() )
      return 1
  # mail checks END #####

  if options.stb and options.src == None:
    GLog.f( GLog.E, "Option --src-reference mandatory with --stb/--stb-label" )
    return 1

  tagDsc = None
  if options.stb:
    tagDsc = create_tag_dsc( SWCFG_TAG_STB )
  if options.liv:
    tagDsc = create_tag_dsc( SWCFG_TAG_LIV )

  if not tagDsc.check_valid_value( g_labelname ):
    strerr  = "Please specify a valid name for label %s" % tagDsc.get_type()
    strerr += "  (i.e. satisfying at least 1 regexp inside: %s)" % tagDsc.get_regexp()
    GLog.f( GLog.E, strerr )
    return 1

  # never on origin
  out, errCode = myCommand( "git remote show" )
  if len( out ) == 0:
    GLog.f( GLog.E, "Cannot execute this script on repository origin" )
    return 1 

  cb = Branch.getCurrBr()
  ib = Branch.getIntBr()
  sb = Branch.getStableBr()

  #valorize g_targetbr
  ret = eval_mergeonto_br()
  if ret != 0:
    return 1

  tb = Branch( g_targetbr )

  if not tb.isValid():
    GLog.f( GLog.E, "Please specify a valid branch onto which to make stb/liv.")
    GLog.f( GLog.E, tb.getNotValidReason() )
    return 1 

  if not tb.isStable() and tb.getType() != SWCFG_BR_CST:
    strerr  = "Can create stb/liv only onto <INT/stable> or <CST/customer> branches.\n"
    strerr += "You are trying to make it on %s, not allowed.\n" % tb.getShortRef()
    strerr += "You can choose among:\n"
    strerr += "    1. providing an <INT/stable> or <CST/customer> target branch on command line\n"
    strerr += "    2. moving on target branch with 'swgit branch --switch'\n"
    strerr += "    3. setting an 'INT/develop' integration branch by 'swgit branch --set-integration-br'\n"
    GLog.f( GLog.E, strerr )
    return 1 

  trackedInfo, tracked = tb.get_track_info()
  if not tracked:
    strerr  = "When stabilizing, target branch (here, %s) must be tracked\n" % tb.getFullRef()
    strerr += "You can track it with swgit branch --track <brname>"
    GLog.f( GLog.E, strerr )
    return 1 

  if options.no_merge_back and not options.liv:
    GLog.f( GLog.E, "option --no-merge-back must be provided only whith --liv one.")
    return 1 

  if options.no_merge_back and not tb.isStable(): #liv for CST branch
    GLog.f( GLog.E, "option --no-merge-back must be provided only when stabilizing INT/develop branches.")
    return 1 

  if not options.no_merge_back:
    literal_develop = tb.getShortRef().replace( "stable", "develop" )
    devBr = Branch( literal_develop )
    trackedInfo, tracked = devBr.get_track_info()
    if not tracked:
      strerr  = "When needing to merge LIV back on INT/develop, target branch (here, %s) must be tracked." % devBr.getFullRef()
      strerr += "You can track it with swgit branch --track <brname>"
      GLog.f( GLog.E, strerr )
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

  # stabilizing only new commits except if --force is provided
  if options.stb:

    err, srcsha = getSHAFromRef( g_srcoptions_map[ "./" ] )
    if err != 0:
      GLog.f( GLog.E, "Please specify a valid --src-reference." )
      return 1

    errCode, f_ret = AisparentofB( srcsha, tb.getShortRef() )
    if errCode != 0:
      GLog.f( GLog.E, "Internal error. (%s/%s)" % (srcsha, tb.getShortRef()) )
      return 1
    
    if f_ret == True:
      if not options.force:
        strerr  = "Reference '%s' has already been reported on '%s'\n" % (g_srcoptions_map[ "./" ], tb.getShortRef())
        strerr += "If you really want to continue (for instance to create new labels)\n"
        strerr += "   please provide --force option."
        GLog.f( GLog.E, strerr )
        return 1
      else:
        GLog.s( GLog.I, "Stabilizing reference %s, already merged into %s" % (srcsha,tb.getShortRef()) )


  # Only 1 STB per DROP 
  if options.stb:
    to_be_created_tag = "%s/%s/%s" % ( tb.getShortRef(), SWCFG_TAG_STB, g_labelname)
  if options.liv:
    to_be_created_tag = "%s/%s/%s" % ( tb.getShortRef(), SWCFG_TAG_LIV, g_labelname)

  tbcTag = Tag( to_be_created_tag )
  if tbcTag.isValid():
    GLog.f( GLog.E, "Already exists a tag named '%s'" % to_be_created_tag )
    return 1 

  ret = 0
  if options.stb:
    ret=check_stb(options)
    if ret != 0:
      return 1

  if options.liv:
    ret=check_liv(options)
    if ret != 0:
      return 1

  return ret



########################
# ONLY STB CHECKS
########################
def check_stb( options ):
  return 0


########################
# ONLY LIV CHECKS
########################
def check_liv( options ):
  return 0


########################
# STABILIZE
########################
def stabilize( lblType, lblName, src_str, mergeOntoBr = None ):

  cb = Branch.getCurrBr()
  startref     = g_srcoptions_map[ "./" ]

  str_begin = ""
  err, beginning_sha = getSHAFromRef( "HEAD" )
  if cb.isValid():
    str_begin = "%s (%s)" % (cb.getShortRef(), beginning_sha[0:8])
  else:
    str_begin = "%s" % beginning_sha


  #strout = "Stabilizing reference '%s', onto branch '%s', into '%s' repo ... " % ( startref, mergeOntoBr, dumpRepoName("local") )
  strout  = "Stabilizing contributes:\n"
  strout += "\tlabel              : %s\n" % g_labelname
  strout += "\tinto repository    : %s\n" % (dumpRepoName("local"))
  strout += "\treporting reference: %s\n" % (startref)
  strout += "\ton target branch   : %s\n" % (mergeOntoBr)
  strout += "\tstarting from      : %s\n" % (str_begin)
  GLog.s( GLog.S, strout )


  #
  # Switch on target branch
  #
  cmd_goto_stb = "%s branch --switch %s" % (SWGIT,mergeOntoBr)
  out, errCode = myCommand( cmd_goto_stb )
  if errCode != 0:
    GLog.f( GLog.E, indentOutput(out[:-1],1) )
    GLog.logRet(errCode)
    return 1 

  cb = Branch.getCurrBr()


  #
  # Inside a project, clean local status before merging
  #
  if Env.is_aproj():
    cmd_resethead = "SWINDENT=%d %s proj --reset HEAD" % ( GLog.tab+1, SWGIT )
    errCode = os.system( cmd_resethead )
    if errCode != 0 :
      return 1


  #
  # Merge ref label
  #
  cmd_merge_stblbl = "git merge --no-ff %s" % startref

  GLog.s( GLog.S, "\tMerging reference %s into branch %s" % ( startref, cb.getShortRef() ) )

  out, errCode = myCommand( cmd_merge_stblbl )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while merging %s into branch %s" % ( startref, cb.getShortRef() ) )
    GLog.f( GLog.E, indentOutput( out[:-1], 2 ) )
    GLog.logRet(errCode)
    return 1 

  GLog.logRet( 0, indent="\t" )



  #
  # If you are a proj, move on src input references inside subrepos
  #   and comit proj to freeze repos alignment
  #
  if Env.is_aproj():

    for currentry in src_str.split( ',' ):
      dir, ref = currentry.split(':')
      if dir == "./":
        continue

      cmd_selectref_subrepo = "cd %s && %s branch --switch %s" % ( dir, SWGIT, ref )
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
  # Create STB Tag on develop
  #
  if lblType == SWCFG_TAG_STB and cb.isStable(): #this tag only when stabilizing develop
    devShortRef = cb.getShortRef().replace( "stable", "develop" )

    fullTagName_dev = "%s/%s/%s" % ( devShortRef, lblType, lblName )

    cmd_chk_startref   = "%s branch --quiet -s %s" % (SWGIT, devShortRef)
    cmd_tag_create     = "SWINDENT=%d %s tag -m \"%s\" %s %s" % (GLog.tab+1, SWGIT, fullTagName_dev, lblType, lblName)
    cmd_create_tag_dev = "%s && %s" % ( cmd_chk_startref, cmd_tag_create )
    errCode = os.system( cmd_create_tag_dev )
    if errCode != 0:
      GLog.f( GLog.E, "\tError while creating label %s on branch %s" % ( lblName, cb.getShortRef() ) )
      GLog.logRet(errCode)
      return 1 

  #
  # Create Tag on mergeOntoBr
  #
  fullTagName_target = "%s/%s/%s" % ( cb.getShortRef(), lblType, lblName )

  cmd_chk_back       = "%s branch --quiet -s %s" % (SWGIT, cb.getShortRef())
  cmd_tag_create     = "SWINDENT=%d %s tag -m \"%s\" %s %s" % (GLog.tab+1, SWGIT, fullTagName_target, lblType, lblName)
  cmd_create_tag_target = "%s && %s" % ( cmd_chk_back, cmd_tag_create )
  errCode = os.system( cmd_create_tag_target )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while creating label %s on branch %s" % ( lblName, cb.getShortRef() ) )
    GLog.logRet(errCode)
    return 1 

  GLog.logRet( 0 )
  return 0


########################
# GENERIC EXECUTE
########################
def execute( options ):

  # mail exec #####
  if options.showmailcfg == True:

    om = ObjMailStabilize()
    print om.dump()
    print om.show_config_options()
    print ""
    return 0

  elif options.testmail:

    GLog.s( GLog.S, "Sending test mail" )

    om = ObjMailStabilize()
    out, err = om.sendmail( "SWGIT STABILIZE TEST MAIL", debug = False )
    if out[:-1] != "":
      GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    GLog.logRet( err )
    return err
  # mail exec END #####

  if options.stb:
    ret = tag_drop_stb( options )
    if ret != 0:
      return 1

  if options.liv:
    ret = tag_drop_liv( options )
    if ret != 0:
      return 1

  return ret
 

########################
# STB EXECUTE
########################
def tag_drop_stb( options ):

  return stabilize( SWCFG_TAG_STB, g_labelname, options.src, g_targetbr )
  

########################
# LIV EXECUTE
########################
def tag_drop_liv( options ):

  output_opt = getOutputOpt(options)

  cb = Branch.getCurrBr()
  sb = Branch.getStableBr()
  ib = Branch.getIntBr()
  tb = Branch( g_targetbr )

  str_begin = ""
  err, beginning_sha = getSHAFromRef( "HEAD" )
  if cb.isValid():
    str_begin = "%s (%s)" % (cb.getShortRef(), beginning_sha[0:8])
  else:
    str_begin = "%s" % beginning_sha

  strout  = "Creating LIV                 : %s\n" % (g_labelname)
  strout += "         into repository     : %s\n" % (dumpRepoName("local"))
  strout += "         on target branch    : %s\n" % (tb.getShortRef())
  strout += "         starting from       : %s\n" % (str_begin)

  #look for last stable
  err, labels = Tag.list( tb.getRel(), tb.getUser(), tb.getType(), tb.getName(), SWCFG_TAG_STB )
  if len( labels ) > 0:
    strout += "         last stable label   : %s\n" % ( labels[-1] )
  else:
    strout += "         last stable label   : Not existing any STB, using %s\n" % tb.getNewBrRef()

  GLog.s( GLog.S, strout )

  if not options.batch:
    ans = raw_input( "Continue? [Y/n]" )
    if ans=="no" or ans=="n" or ans=="N" or ans == "NO" or ans == "No" or ans == "nO":
      GLog.s( GLog.S, "\tLabel creation aborted by user." )
      GLog.logRet(0)
      sys.exit(0)

  #go onto target br
  cmd_chk_targetbr = "%s branch --quiet -s %s" % (SWGIT, tb.getShortRef())
  errCode = os.system( cmd_chk_targetbr )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while checking out target branch" )
    GLog.logRet(errCode)
    return 1 

  cb = Branch.getCurrBr()

  #LIV on stable
  generic_liv_dsc = '\'%s/%s/%s/%s/%s/*\'' % ( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), SWCFG_TAG_LIV )
  errCode, lastbutone_liv, dist = find_describe_label( generic_liv_dsc )
  if errCode != 0:
    firstCommit_cmd = "git log --format='%H'  | tail -n 1"
    out, errCode = myCommand( firstCommit_cmd )
    firstCommit = out[ : out.find(" ")-1 ]

    GLog.s( GLog.S, "\tThis is your first LIV label " )
    lastbutone_liv = firstCommit

  else: 
    GLog.s( GLog.S, "\tLast LIV Label is %s" % lastbutone_liv )


  #
  # Eval logs
  #
  ret = eval_create_commit_logs( lastbutone_liv )
  if ret != 0:
    GLog.logRet(1)
    return 1


  #
  # Create Tag
  #
  fullTagName = "%s/%s/%s/%s/%s/%s" % ( cb.getRel(), cb.getUser(), cb.getType(), cb.getName(), SWCFG_TAG_LIV, g_labelname )

  cmd_create_tag_liv = "SWINDENT=%d %s tag -m \"%s\" %s %s" %  ( GLog.tab+1, SWGIT, fullTagName, SWCFG_TAG_LIV, g_labelname )
  errCode = os.system( cmd_create_tag_liv )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while creating label %s" % ( fullTagName ) )
    GLog.logRet(errCode)
    return 1 


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

    #
    # Prepare and send mail
    #
    om = ObjMailStabilize()
    if om.isValid() == False:
      raise Exception( "\tCannot send mail, bad configured\n" % om.dump() )

    out, err = om.sendmail( eval_body_mail(), debug = False )

    GLog.f( GLog.I, out )
    if err != 0:
      raise Exception( "\tError while sending mail\n%s" % indentOutput( out[:-1], 2 ) )

    GLog.logRet( 0, indent = "\t" )

  #
  # Custom branch liv has finished here
  # no-merge-back, has finished here
  #
  if options.no_merge_back or cb.getType() == SWCFG_BR_CST:
    GLog.logRet( 0 )
    return 0

  #
  # Merge on develop
  #
  # 1. checkout develop
  literal_develop = cb.getShortRef().replace( "stable", "develop" )
  devBr = Branch( literal_develop )

  GLog.s( GLog.S, "\tMerging LIV %s into %s ... " % ( fullTagName, devBr.getShortRef() ))
  if Env.is_aproj():
    cmd_goto_dev = "SWINDENT=%d %s branch -s %s && SWINDENT=%d %s proj --reset HEAD" % ( GLog.tab+2, SWGIT, devBr.getShortRef(), GLog.tab+2, SWGIT )
  else:
    cmd_goto_dev = "SWINDENT=%d %s branch -s %s" % ( GLog.tab+2, SWGIT, devBr.getShortRef() )
  out, errCode = myCommand( cmd_goto_dev )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while switching to %s branch" % devBr.getShortRef() )
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
  if Env.is_aproj():
    cmd_refresh = "cd %s && SWINDENT=%s %s proj --reset HEAD" % ( Env.getProjectRoot(), GLog.tab, SWGIT )
    errCode = os.system( cmd_refresh )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )

  # 3. push on origin develop
  GLog.s( GLog.S, "\tPushing %s on origin ... " % ( devBr.getShortRef() ))

  cmd_push_dev = "SWINDENT=%d %s push %s %s" % ( GLog.tab+2, SWGIT, output_opt, mail_opt )
  errCode = os.system( cmd_push_dev )
  if errCode != 0 :
    GLog.logRet( errCode )
    sys.exit( 1 )  
  GLog.logRet( 0, indent="\t" )

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
Usage: swgit stabilize [--force] --stb [--src <startpoint>] <label> [<dst-br>]
       swgit stabilize [--force] --liv <label> [<dst-br>]
       swgit stabilize [--force] --stb --liv <label> [<dst-br>]
       swgit stabilize --show-mail-cfg|--test-mail-cfg"""

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

  global g_labelname
  global g_targetbr

  if options.showmailcfg or options.testmail:
    if len( args ) != 0:
      parser.error("Testing mail do not requires arguments.")
  else:

    if not options.liv and not options.stb:
      parser.error("Please specify at least --liv or --stb" )

    if len( args ) == 0:
      parser.error("Please specify at least label name" )
    elif len( args ) == 1:
      g_labelname = args[0]
    elif len( args ) == 2:
      g_labelname = args[0]
      g_targetbr = args[1]
    else:
      parser.error("Too many parameters")

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
 


gitstabilize_mgt_options = [
    [
      "--stb",
      "--stb-label",
      {
        "action"  : "store_true",
        "dest"    : "stb",
        "default" : False,
        "help"    : 'Reports --src argument on \"/INT/stable\" or \"/CST/customer\" branches according to starting branch. Labelize merge boundaries with STB label.'
        }
      ],
    [
      "--src",
      "--src-reference",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "src",
        "metavar" : "<reference>",
        "help"    : "With --stb option. Provides staring point to be stabilized. Its argument can be a reference, a comma-separed list of <dir>:<reference> pairs, a file (these last two modes are useful inside projects)"
        }
      ],
    [
      "--liv",
      "--liv-label",
      {
        "action"  : "store_true",
        "dest"    : "liv",
        "default" : False,
        "help"    : 'Create LIV label on \"/INT/stable\" or \"/CST/customer\" branches according to starting branch. Evaluates changelog, fixlog from last LIV.'
        }
      ],
    [
      "-f",
      "--force",
      {
        "action"  : "store_true",
        "dest"    : "force",
        "default" : False,
        "help"    : 'Force stabilizing also when src reference has already been stabilized. For instance, to create new tags.'
        }
      ],
    [
      "--no-merge-back",
      {
        "action"  : "store_true",
        "dest"    : "no_merge_back",
        "default" : False,
        "help"    : 'Do not report INT/stable on INT/develop after liv creation.'
        }
      ],
    [
      "--batch",
      {
        "action"  : "store_true",
        "dest"    : "batch",
        "default" : False,
        "help"    : 'No answers, useful with scripts'
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
  
