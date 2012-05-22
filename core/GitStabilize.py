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
g_labelname = None
g_targetbr = None
g_rel_path = None
g_devs  = []
g_fixes = []
g_chgfname = None
g_fixfname = None
g_tktfname = None
_g_rargs   = []


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

def show_preview( options ):

  for (dir, tbs_ref) in g_srcoptions_map.items():

    if dir == '.': #root

      dir = os.getcwd()
      #bound = '='*len(dir)
      #strhead = "\n%s\n\n" % "\n".join( (bound,dir,bound) )

      prev_ref = g_targetbr

    else: #submods

      dir = dir2reponame( dir )
      bound = '='*len(dir)
      strhead = "\n%s\n\n" % "\n".join( (bound,dir,bound) )

      prev_ref, errCode = submod_getrepover_atref( Env.getLocalRoot(), dir, g_targetbr )
      if errCode != 0:
        GLog.f( GLog.E, strhead + prev_ref )
        return 1

    if Env.is_aproj( dir ) and dir != os.getcwd():

      str_opt_diff = ""
      if len( _g_rargs ) > 0:
        str_opt_diff = "-- %s" % " ".join( _g_rargs )

      cmd_diff = "cd %s && %s proj --diff %s %s %s" % ( dir, SWGIT, prev_ref, tbs_ref, str_opt_diff )
      #out, errCode = myCommand( cmd_diff )
      errCode = os.system( cmd_diff )

    else:

      row0 = "repo  %s" % dir
      row1 = "REF1: %s" % prev_ref
      row2 = "REF2: %s" % tbs_ref
      row_cmd   = "CMD:  git diff $REF1 $REF2 %s" % " ".join(_g_rargs)

      cmd_diff = "cd %s && git diff %s %s %s" % ( dir, prev_ref, tbs_ref, " ".join( _g_rargs ) )
      out, errCode = myCommand( cmd_diff )

      #only on python > 2.5
      #maxlen = len( max( row0, row1, row2, row_cmd, key=len ) )
      maxlen = max( len(x) for x in [ row0, row1, row2, row_cmd ] )
      bound = "="*maxlen
      strout = "\n%s\n\n" % "\n".join( (bound,row0, row1, row2, row_cmd, bound) )

      GLog.f( GLog.E, strout + out )

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

  chglog_fmt_file = SWCFG_STABILIZE_CHGLOG_FILE_FORMAT
  obj_chglog_fmt_file = ObjCfgStabilize_CHGLOG_fmt_file()
  if obj_chglog_fmt_file.isValid():
    chglog_fmt_file = obj_chglog_fmt_file.get_chglog_fmt_file()

  cmd_show_commitmsg = 'git for-each-ref --format="%s"' % chglog_fmt_file
  cmd_redirectfile = "tee %s" % ( g_changelog )

  out, errCode = myCommand( "%s %s | %s" % ( cmd_show_commitmsg, " ".join( [ "refs/tags/" + d for d in g_devs] ), cmd_redirectfile ) )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving changelog" )
    GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    GLog.logRet(errCode)
    return 1 
  return 0


def eval_fixlog_content():

  global g_fixlog
  g_fixlog = "%s/%s_%s.fix" % ( g_rel_path, SWCFG_TAG_LIV, g_labelname )

  if len( g_fixes ) == 0:
    touch_file( g_fixlog )
    return 0

  fixlog_fmt_file = SWCFG_STABILIZE_FIXLOG_FILE_FORMAT
  obj_fixlog_fmt_file = ObjCfgStabilize_FIXLOG_fmt_file()
  if obj_fixlog_fmt_file.isValid():
    fixlog_fmt_file = obj_fixlog_fmt_file.get_fixlog_fmt_file()

  cmd_show_commitmsg = "git for-each-ref --format='%s'" % fixlog_fmt_file
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


def eval_create_add_logs( upstream ):

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
  out, errCode = myCommand( cmd_add )
  if errCode != 0:
    GLog.f( GLog.E, "Error while adding Changelog, Fixlog and Ticketlog" )
    GLog.logRet(out)
    GLog.logRet(errCode)
    return 1 
  GLog.logRet( 0, indent="\t" )
  return 0


def execute_pre_liv_commit_hook():

  obj_prelivcommit_hook = ObjCfgStabilize_PreLivCommit_Hook()
  if not obj_prelivcommit_hook.isValid(): #no scripts configured
    return "", 0

  hook_script = obj_prelivcommit_hook.get_hook_precommit_script()
  cmd_hook_precommit = "%s %s %s" % ( hook_script, g_labelname, g_targetbr )

  hook_sshuser = obj_prelivcommit_hook.get_hook_precommit_sshuser()
  hook_sshaddr = obj_prelivcommit_hook.get_hook_precommit_sshaddr()

  ssherr = ""
  if hook_sshuser != "" and hook_sshaddr != "":

    ssherr = "%s@%s " % (hook_sshuser, hook_sshaddr)
    GLog.s( GLog.S, "\tExecuting pre-liv-commit hook %s%s ..." %  (ssherr, cmd_hook_precommit) )
    precommitout,precommiterr = mySSHCommand( cmd_hook_precommit, hook_sshuser, hook_sshaddr )

  elif hook_sshuser == "" and hook_sshaddr == "":

    GLog.s( GLog.S, "\tExecuting pre-liv-commit hook %s ..." %  (cmd_hook_precommit) )
    precommitout,precommiterr = myCommand( cmd_hook_precommit )

  else:
    strerr = "\tERROR - pre-liv-commit hook not well defined. Specify both or nothing among sshuser and sshaddr."
    return strerr, 1

  if precommitout[:-1] != "":
    GLog.f( GLog.E, indentOutput(precommitout[:-1], 2) )

  if precommiterr != 0:
    strerr = "\tFAILED - pre-liv-commit hook (%s%s) returned error. Abort stabilization." % (ssherr, cmd_hook_precommit)
    return strerr, 1

  GLog.s( GLog.S, "\tDONE" )
  return "", 0





def eval_body_mail():

  #tickets
  body_mail_tickets  = "List of Tickets fixed in %s/%s:\n\n" % ( SWCFG_TAG_LIV, g_labelname )
  body_mail_tickets += "\n".join( g_fixes )
  GLog.f( GLog.I, body_mail_tickets )

  chglog_fmt_mail = SWCFG_STABILIZE_CHGLOG_MAIL_FORMAT
  obj_chglog_fmt_mail = ObjCfgStabilize_CHGLOG_fmt_mail()
  if obj_chglog_fmt_mail.isValid():
    chglog_fmt_mail = obj_chglog_fmt_mail.get_chglog_fmt_mail()

  chglog_sort_mail = SWCFG_STABILIZE_CHGLOG_MAIL_SORT
  obj_chglog_sort_mail = ObjCfgStabilize_CHGLOG_sort_mail()
  if obj_chglog_sort_mail.isValid():
    chglog_sort_mail = obj_chglog_sort_mail.get_chglog_sort_mail()

  #Devs
  cmd_show_commitmsg = "git for-each-ref --format='%s' --sort='%s'" % (chglog_fmt_mail, chglog_sort_mail)
  out_devs, errCode = myCommand( "%s %s" % ( cmd_show_commitmsg, " ".join( [ "refs/tags/" + d for d in g_fixes] ) ) )
  if errCode != 0:
    GLog.f( GLog.E, "\tError executing command retrieving changelog" )

  body_mail_devs  = "\nList of DEV labels entered into %s/%s :\n\n" % ( SWCFG_TAG_LIV, g_labelname )
  body_mail_devs += "\n".join( out_devs )
  GLog.f( GLog.I, body_mail_devs )

  return body_mail_tickets + "\n" + body_mail_devs


def apply_src_map():
  #
  # Inside a project, move on src input references inside subrepos
  #
  srcoptions_map_noroot = g_srcoptions_map
  if "." in srcoptions_map_noroot.keys(): del srcoptions_map_noroot['.']
  for (dir, ref) in srcoptions_map_noroot.items():

    GLog.f( GLog.E, "\tAccording to --source param, moving %s onto %s" % (dir,ref) )
    cmd_selectref_subrepo = "cd %s && %s branch --switch %s" % ( dir, SWGIT, ref )
    out, errCode = myCommand( cmd_selectref_subrepo )
    if errCode != 0 :
      GLog.f( GLog.E, out )
      return 1

  return 0


def commit_proj( tagtype ):
  GLog.f( GLog.E, "\tCommitting actual project status" )

  srcoptions_map_noroot = g_srcoptions_map
  if "." in srcoptions_map_noroot.keys(): del srcoptions_map_noroot['.']

  #only on python > 2.5
  #maxlen = len( max( srcoptions_map_noroot.keys(), key = len ) )
  cmt_body = ""
  if len( srcoptions_map_noroot.keys() ) > 0:
    maxlen = max( len(x) for x in srcoptions_map_noroot.keys() )
    cmt_body = ""
    for (dir, ref) in srcoptions_map_noroot.items():
      cmt_body += ("%s" % dir).ljust( maxlen )
      cmt_body += " : %s\n" % ref

  cb = Branch.getCurrBr()
  comment = "'rel: %s - drop: %s_%s\n\n%s'" % \
      ( cb.getRel().replace( "/","." ), 
        tagtype, g_labelname, 
        cmt_body
      )
  cmd_commitmodules = "git commit -a --allow-empty -m %s" % comment
  out, errCode = myCommand( cmd_commitmodules )
  if errCode != 0 :
    GLog.f( GLog.E, out )
    return 1

  GLog.logRet( 0, indent="\t" )
  return 0




def show_chglogs_cfg():

  objs = []
  objs.append( ( "* PRE-COMMIT-HOOK"   ,        ObjCfgStabilize_PreLivCommit_Hook()) )
  objs.append( ( "* CHGLOG FILE FORMAT",        ObjCfgStabilize_CHGLOG_fmt_file()  ) )
  objs.append( ( "* FIXLOG FILE FORMAT",        ObjCfgStabilize_FIXLOG_fmt_file()  ) )
  objs.append( ( "* CHGLOG MAIL FORMAT",        ObjCfgStabilize_CHGLOG_fmt_mail()  ) )
  objs.append( ( "* CHGLOG MAIL SORT CRITERIA", ObjCfgStabilize_CHGLOG_sort_mail() ) )

  strout = ""

  for t, o in objs:
    strout += "\n%s\n%s\n%s\n" % ( "="*len(t), t, "="*len(t) )

    strval  = "%s\n" % ("-"*50)
    strval += o.dump( f_short = True )
    strval += "%s\n" % ("-"*50)
    strval += o.show_config_options()
    strval += "\n"

    strout += indentOutput( strval, 1)

  print strout
  return 0


########################
# GENERIC CHECKS
########################
def check(options):

  GLog.s( GLog.S, "Check " + dumpRepoName("your local") + " repository stabilize ..." )

  # mail checks #####
  if options.showmailcfg or options.showcfg:
    return 0

  if options.testmail:
    om = ObjMailPush()
    if om.isValid() == False:
      GLog.f( GLog.E, "\tMail not well configured." )
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
    options.src =  ".:HEAD"
    GLog.f( GLog.E, "\t(No option -S/--source specified, using HEAD)" )
    #GLog.f( GLog.E, "Option -S/--source mandatory with --stb/--stb-label" )
    #return 1

  if options.preview and not options.stb:
    GLog.f( GLog.E, "\t-p/--preview option can only be provided with --stb" )
    return 1

  if len( _g_rargs) > 0 and not options.preview:
    GLog.f( GLog.E, "\tCan specify additional arguments (after -- ) only with -p/--preview" )
    return 1

  tagDsc = None
  if options.stb:
    tagDsc = create_tag_dsc( SWCFG_TAG_STB )
  if options.liv:
    tagDsc = create_tag_dsc( SWCFG_TAG_LIV )

  if not tagDsc.check_valid_value( g_labelname ):
    strerr  = "Please specify a valid name for label %s" % tagDsc.get_type()
    strerr += "  (i.e. satisfying at least 1 regexp inside: %s)" % tagDsc.get_regexp()
    GLog.f( GLog.E, indentOutput(strerr,1) )
    return 1

  # never on origin
  out, errCode = myCommand( "git remote show" )
  if len( out ) == 0:
    GLog.f( GLog.E, "\tCannot execute this script on repository origin" )
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
    GLog.f( GLog.E, "\tPlease specify a valid branch onto which to make stb/liv.")
    GLog.f( GLog.E, indentOutput(tb.getNotValidReason(),1) )
    return 1 

  if not tb.isStable() and tb.getType() != SWCFG_BR_CST:
    strerr  = "Can create stb/liv only onto <INT/stable> or <CST/customer> branches.\n"
    strerr += "You are trying to make it on %s, not allowed.\n" % tb.getShortRef()
    strerr += "You can choose among:\n"
    strerr += "    1. providing an <INT/stable> or <CST/customer> target branch on command line\n"
    strerr += "    2. moving on target branch with 'swgit branch --switch'\n"
    strerr += "    3. setting an 'INT/develop' integration branch by 'swgit branch --set-integration-br'\n"
    GLog.f( GLog.E, indentOutput( strerr, 1 ) )
    return 1 

  trackedInfo, tracked = tb.get_track_info()
  if not tracked:
    strerr  = "When stabilizing, target branch (here, %s) must be tracked\n" % tb.getFullRef()
    strerr += "You can track it with swgit branch --track <brname>"
    GLog.f( GLog.E, strerr )
    return 1 

  if options.merge_back and not options.liv:
    GLog.f( GLog.E, "\toption --merge-back must be provided only with --liv one.")
    return 1 

  if options.merge_back and not tb.isStable(): #liv for CST branch
    GLog.f( GLog.E, "\toption --merge-back must be provided only when stabilizing onto INT/stable branches.")
    return 1 

  if options.merge_back:
    literal_develop = tb.getShortRef().replace( "stable", "develop" )
    devBr = Branch( literal_develop )
    trackedInfo, tracked = devBr.get_track_info()
    if not tracked:
      strerr  = "When needing to merge LIV back on INT/develop, target branch (here, %s) must be tracked." % devBr.getFullRef()
      strerr += "You can track it with swgit branch --track <brname>"
      GLog.f( GLog.E, indentOutput( strerr, 1 ) )
      return 1 

  #
  # src management
  #
  if options.src != None:

    ret, options.src = src_reference_check( options.src, options.batch )
    if ret != 0:
      GLog.f( GLog.E, options.src )
      return 1

    options.src = options.src.replace( './:', '.:' )

    if options.src.find( ':' ) == -1: #only 1 val
      options.src = ".:%s" % options.src
    if options.src.find( '.:' ) == -1: #not currdir listed
      options.src = ".:HEAD," + options.src
      GLog.f( GLog.E, "\t(Option -S/--source not conatining '.' entry, using HEAD)" )
      #strerr = "Option -S/--source not containing '.' entry. Mandatory."
      #GLog.f( GLog.E, strerr )
      #return 1

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

    inits_notsnaps = submod_list_initialized_notsnapshot()

    for currentry in options.src.split( ',' ):
      dir, ref = currentry.split(':')
      rn = dir2reponame( dir )

      #substututed before
      #if ref == "HEAD":
      #  GLog.f( GLog.E, "Please specify a valid source reference (HEAD it is not) inside repo: %s" % rn )
      #  return 1

      if rn != "." and rn not in inits_notsnaps:
        strerr  = "Repository '%s' is not directly contained into current project.\n" % rn
        strerr += "It is not possible to stabilize repositories deeper than 1 level.\n"
        strerr += "You must stabilize '%s' inside its container project,\n" % rn
        strerr += "then provied here that stabilized sha/label."
        GLog.f( GLog.E, indentOutput( strerr, 1 ) )
        return 1

      g_srcoptions_map[ rn ] = ref

      err, sha = getSHAFromRef( ref, rn )
      if err != 0:
        GLog.f( GLog.E, "\tPlease specify a valid source reference inside repo: %s" % rn )
        return 1

      # stabilize anyref (only root project is actually stabilizing, no need to check other src values
      if get_repo_cfg_bool( SWCFG_STABILIZE_ANYREF, rn ) == False:
        if rn == ".":
          if ref.find( "/NGT/" ) == -1:
            strerr  = "Inside repository %s, only NGT labels are allowed to be stabilized.\n" % rn
            strerr += "You can change this behaviour by issueing:\n"
            strerr += "    git config --bool swgit.stabilize-anyref True"
            GLog.f( GLog.E, indentOutput( strerr,1 ) )
            return 1


  # generic checks
  err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
  if err != 0:
    GLog.f( GLog.E, indentOutput( errstr, 1 ) )
    return 1 

  if not is_integrator_repo():
    strerr  = "This repository has been created as a 'developer' one.\n"
    strerr += "  You can stabilize only inside 'integrator' repositories.\n"
    strerr += "  You can:\n"
    strerr += "   clone with --integrator\n"
    strerr += "  or\n"
    strerr += "   convert this repo with 'git config --bool swgit.integrator True'"
    GLog.f( GLog.E, indentOutput( strerr, 1 ) )
    return 1 

  # stabilizing only new commits except if --force is provided
  if options.stb:

    err, srcsha = getSHAFromRef( g_srcoptions_map[ "." ] )
    if err != 0:
      GLog.f( GLog.E, "\tPlease specify a valid -S/--source for top repository." )
      return 1

    errCode, f_ret = AisparentofB( srcsha, tb.getShortRef() )
    if errCode != 0:
      GLog.f( GLog.E, "\tInternal error. (%s/%s)" % (srcsha, tb.getShortRef()) )
      return 1
    
    if f_ret == True:
      if not options.force:
        strerr  = "Reference '%s' has already been reported on '%s'\n" % (g_srcoptions_map[ "." ], tb.getShortRef())
        strerr += "If you really want to continue (for instance to create new labels)\n"
        strerr += "   please provide --force option."
        GLog.f( GLog.E, indentOutput( strerr, 1 ) )
        return 1
      else:
        GLog.s( GLog.I, "\tStabilizing reference %s, already merged into %s" % (srcsha,tb.getShortRef()) )


  # Only 1 STB per DROP 
  if options.stb:
    to_be_created_tag = "%s/%s/%s" % ( tb.getShortRef(), SWCFG_TAG_STB, g_labelname)
  if options.liv:
    to_be_created_tag = "%s/%s/%s" % ( tb.getShortRef(), SWCFG_TAG_LIV, g_labelname)

  tbcTag = Tag( to_be_created_tag )
  if tbcTag.isValid():
    GLog.f( GLog.E, "\tAlready exists a tag named '%s'" % to_be_created_tag )
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
# GENERIC EXECUTE
########################
def execute( options ):

  # mail exec #####
  if options.showmailcfg:

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

  #output cfg ####
  if options.showcfg:
    return show_chglogs_cfg()
  #output cfg END

  if options.preview:
    return show_preview( options )

  if options.stb:
    ret = execute_stb( options )
    if ret != 0:
      return 1

  if options.liv:
    ret = execute_liv( options )
    if ret != 0:
      return 1

  return ret
 

########################
# STB EXECUTE
########################
def execute_stb( options ):

  cb       = Branch.getCurrBr()
  startref = g_srcoptions_map[ "." ]

  str_begin = ""
  err, beginning_sha = getSHAFromRef( "HEAD" )
  if cb.isValid():
    str_begin = "%s (%s)" % (cb.getShortRef(), beginning_sha[0:8])
  else:
    str_begin = "%s" % beginning_sha


  strout  = "Stabilizing contributes:\n"
  strout += "\tlabel              : %s\n" % g_labelname
  strout += "\tinto repository    : %s\n" % (dumpRepoName("local"))
  strout += "\treporting reference: %s\n" % (startref)
  strout += "\ton target branch   : %s\n" % (g_targetbr)
  strout += "\tstarting from      : %s\n" % (str_begin)
  GLog.s( GLog.S, strout )


  #
  # Switch on target branch
  #
  cmd_goto_stb = "%s branch --switch %s" % (SWGIT,g_targetbr)
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
  GLog.s( GLog.S, "\tMerging reference %s into branch %s" % ( startref, cb.getShortRef() ) )

  #Jump swgit merge checks.
  # Here swgit merge should deny because no label is provided (sha instead).
  # We cannot tag before issuing merge, in order to the let user resolving conflicts.
  # We will create INT/develop/STB label only once, after successful merge
  cmd_merge_stblbl = "SWINDENT=%d SWCHECK=NO %s merge %s" % ( GLog.tab+2, SWGIT, startref )
  errCode = os.system( cmd_merge_stblbl )
  if errCode != 0:
    GLog.logRet(errCode)
    return 1 
  GLog.logRet( 0, indent="\t" )

  #
  # Inside a project, after merge update subrepos according to new .gitmodules
  #
  if Env.is_aproj():
    cmd_resethead = "SWINDENT=%d %s proj --reset HEAD" % ( GLog.tab+1, SWGIT )
    errCode = os.system( cmd_resethead )
    if errCode != 0 :
      return 1

  #
  # Inside a project, move on src input references inside subrepos
  #   and comit proj to freeze repos alignment
  #
  if Env.is_aproj():

    apply_src_map()
    if errCode != 0 :
      return 1

    srcoptions_map_noroot = g_srcoptions_map
    if "." in srcoptions_map_noroot.keys(): del srcoptions_map_noroot['.']
    # commit repositories changes only if any
    if len( srcoptions_map_noroot ) > 0:
      commit_proj( SWCFG_TAG_STB )
      if errCode != 0 :
        return 1


  #
  # Create Tag on g_targetbr
  #
  fullTagName_target = "%s/%s/%s" % ( cb.getShortRef(), SWCFG_TAG_STB, g_labelname )
  cmd_tag_create     = "SWINDENT=%d %s tag -m \"%s\" %s %s" % (GLog.tab+1, SWGIT, fullTagName_target, SWCFG_TAG_STB, g_labelname)
  errCode = os.system( cmd_tag_create )
  if errCode != 0:
    GLog.f( GLog.E, "\tError while creating label %s on branch %s" % ( g_labelname, cb.getShortRef() ) )
    GLog.logRet(errCode)
    return 1 

  #
  # Create STB Tag on develop
  # Note: if you stabilize any ref outside develop, any FTR/topic/STB/Drop.X 
  #       can be created
  #
  if cb.isStable(): #this tag only when stabilizing develop

    if options.start_point_label:

      devShortRef = cb.getShortRef().replace( "stable", "develop" )
      fullTagName_dev    = "%s/%s/%s" % ( devShortRef,      SWCFG_TAG_STB, g_labelname )

      cmd_chk_startref   = "%s branch --quiet -s %s" % (SWGIT, startref)
      cmd_tag_create     = "SWINDENT=%d %s tag -m \"%s\" %s %s" % (GLog.tab+1, SWGIT, fullTagName_dev, SWCFG_TAG_STB, g_labelname)
      cmd_create_tag_dev = "%s && %s" % ( cmd_chk_startref, cmd_tag_create )
      errCode = os.system( cmd_create_tag_dev )
      if errCode != 0:
        GLog.f( GLog.E, "\tError creating label %s on branch %s, not critical." % ( g_labelname, cb.getShortRef() ) )

      cmd_chk_back       = "%s branch --quiet -s %s" % (SWGIT, cb.getShortRef())
      errCode = os.system( cmd_chk_back )
      if errCode != 0:
        GLog.f( GLog.E, "\tError while coming back on %s" % ( cb.getShortRef() ) )
        GLog.logRet(errCode)
        return 1 

  GLog.logRet( 0 )
  return 0
  

########################
# LIV EXECUTE
########################
def execute_liv( options ):

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

  tb_repo, tb_repo_errcode = tb.branch_to_remote()
  if tb_repo_errcode != 0:
    strerr  = "\tError while retrieving remote for pushing everthing:\n"
    strerr += indentOutput( tb_repo, 2 )
    GLog.f( GLog.E, strerr )
    GLog.logRet(errCode)
    return 1 
  strout += "         pushing to remote   : %s\n" % (tb_repo)

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
  if not options.no_chglogs:

    ret = eval_create_add_logs( lastbutone_liv )
    if ret != 0:
      GLog.logRet(1)
      return 1

  #
  # Inside a project, move on src input references inside subrepos
  #   and commit proj to freeze repos alignment
  #
  if Env.is_aproj():

    apply_src_map()
    if errCode != 0 :
      return 1

  #
  # hook pre commit
  #
  obj_prelivcommit_hook = ObjCfgStabilize_PreLivCommit_Hook()
  if obj_prelivcommit_hook.isValid():

    out, errCode = execute_pre_liv_commit_hook()
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet(1)
      return 1

  #
  # liv commit, create it only if necessary
  #
  srcoptions_map_noroot = g_srcoptions_map
  if "." in srcoptions_map_noroot.keys(): del srcoptions_map_noroot['.']
  if (len( srcoptions_map_noroot ) > 0) or (not options.no_chglogs) or obj_prelivcommit_hook.isValid():

    GLog.s( GLog.S, "\tCreating LIV commit" )

    commit_proj( SWCFG_TAG_LIV )
    if errCode != 0 :
      GLog.f( GLog.E, "Error while creating LIV commit" )
      GLog.logRet(errCode)
      return 1 
    GLog.logRet( 0, indent="\t" )


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
  GLog.s( GLog.S, "\tPushing %s on '%s' ... " % ( sb.getShortRef(), tb_repo ))

  mail_opt = "--no-mail"
  if options.sendmail:
    mail_opt = ""

  cmd_push_stable = "SWINDENT=%d %s push %s %s %s" % ( GLog.tab+2, SWGIT, output_opt, mail_opt, tb_repo )
  errCode = os.system( cmd_push_stable )
  if errCode != 0 :
    GLog.logRet( errCode )
    sys.exit( 1 )  
  GLog.logRet( 0, indent="\t" )


  #
  # prepare and send mail
  #
  if options.sendmail:

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
  if ( not options.merge_back ) or cb.getType() == SWCFG_BR_CST:
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
    cmd_refresh = "cd %s && SWINDENT=%s %s proj --reset HEAD" % ( Env.getProjectRoot(), GLog.tab + 1, SWGIT )
    errCode = os.system( cmd_refresh )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )

  # 3. push on origin develop
  GLog.s( GLog.S, "\tPushing %s on '%s' ... " % ( devBr.getShortRef(), tb_repo ))

  cmd_push_dev = "SWINDENT=%d %s push %s %s %s" % ( GLog.tab+2, SWGIT, output_opt, mail_opt, tb_repo )
  errCode = os.system( cmd_push_dev )
  if errCode != 0 :
    GLog.logRet( errCode )
    sys.exit( 1 )  
  GLog.logRet( 0, indent="\t" )

  GLog.logRet( 0 )
  return 0




#########
#  MAIN #
#########
def main():
  usagestr =  """\
Usage: swgit stabilize --stb [-f] [-S <ref>] <label> [<dst-br>]
       swgit stabilize --stb [-f] [-S <ref>] <label> [<dst-br>] --preview [-- <diff options>...]
       swgit stabilize --liv [-f] <label> [<dst-br>]
       swgit stabilize --stb --liv [-f] [-S <ref>] <label> [<dst-br>]
       swgit stabilize --show-mail-cfg|--test-mail-cfg|--show-cfg"""

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
  args = parser.largs

  help_mac( parser )

  global g_labelname
  global g_targetbr
  global _g_rargs
  _g_rargs = parser.rargs

  if options.showmailcfg or options.testmail or options.showcfg:
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
        "help"    : 'Reports --source argument on \"/INT/stable\" or \"/CST/customer\" branches according to starting branch. Labelize merge boundaries with STB label.'
        }
      ],
    [
      "-S",
      "--source",
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
      "-p",
      "--preview",
      {
        "action"  : "store_true",
        "dest"    : "preview",
        "default" : False,
        "help"    : 'With --stb. Only makes checks and shows differences between current target branch and current stabilizing sources.'
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
      "--merge-back",
      {
        "action"  : "store_true",
        "dest"    : "merge_back",
        "default" : False,
        "help"    : 'Force reporting INT/stable onto INT/develop after LIV creation.'
        }
      ],
    [
      "--no-chglogs",
      {
        "action"  : "store_true",
        "dest"    : "no_chglogs",
        "default" : False,
        "help"    : 'Jump changelog, fixlog, ticketlog evaluation.'
        }
      ],
    [
      "--start-point-label",
      {
        "action"  : "store_true",
        "dest"    : "start_point_label",
        "default" : False,
        "help"    : 'Also create start point label when stabilizing onto /INT/stable (usually tag will be created on /INT/develop).'
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
      ],
    [
      "--show-cfg",
      {
        "action"  : "store_true",
        "dest"    : "showcfg",
        "default" : False,
        "help"    : 'Show how chglog and fixlog outputr will be formatted both for file and mail.'
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
  
