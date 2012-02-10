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

import ConfigParser

from Common import *
from ObjKey import * 
from ObjStatus import * 
#from ObjLog import help_mac
from ObjBranch import *
from ObjLog import *
from ObjMap import *
from ObjOperation import *
from Utils_Submod import *
from ObjSnapshotRepo import *

import sys

scriptPath=os.path.abspath( os.path.dirname( __file__ ) + "/../" )

def check_BRexists_and_WDclean( dir ):
  # 1. on swProjMap directory only
  if os.getcwd() != dir:
    return 1, "Please issue this commad inside project directory (maybe: %s)" % dir

  # 2. on a branch FTR
  cb = Branch.getCurrBr()
  if cb.isValid() == False or cb.getType() != SWCFG_BR_FTR:
    err = "ERROR: This opration will modify swProjMap and/or other repo files. \n" + \
        "Please issue this command on a FTR branch in order to later commit and push on origin your work."
    return 1, err

  # 3. clean WD
  err, errstr = Status.checkLocalStatus_rec()
  if err != 0:
    return 1, errstr

  return 0, ""


def checkRepo( url, branch, chk=None ):
  src_obj_remote = create_remote_byurl( url )
  if not src_obj_remote.isValid():
    GLog.f( GLog.E, str(src_obj_remote) )
    return 1
  if src_obj_remote.getType() != "ssh" and src_obj_remote.getType() != "fs" :
    GLog.f( GLog.E, "ERROR: at the moment, only ssh (ssh://user@addr/path/to/repo) or fs (/path/to/repo) urls supported " )
    return 1

  errCode = 0

  #
  # ssh key management
  #
  if src_obj_remote.getType() == "ssh":

    GLog.s( GLog.S, "Remote login password maybe asked during this operation ... " )

    objKey = ObjKey( src_obj_remote.getUser(), src_obj_remote.getAddress() )

    out, errCode = objKey.is_reachable()
    if errCode != 0:
      GLog.f( GLog.E, indentOutput( out, 1 ) )
      return 1

    if objKey.create_and_copy() != 0:
      strerr  = "FAILED: cannot create/copy swgit pub key onto host \"%s\" with user \"%s\" via ssh." % \
                         ( src_obj_remote.getAddress(), src_obj_remote.getUser() )
      strerr += "        Please use 'swgit key %s %s' command to investigate" % ( src_obj_remote.getUser(), src_obj_remote.getAddress() )
      GLog.f( GLog.E, indentOutput( strerr, 1 ) )
      return 1

  return errCode


def write_swdefbr_addindex_config( proot, reponame, branch ):

  filename = "%s/%s" % ( proot, SWFILE_DEFBR )

  if os.path.exists( filename ) == False:
    fin = open( filename, "w+" )
  else:
    fin = open( filename, "r" )

  data_list = fin.readlines()
  fin.close()

  found = False
  new_content = ""

  for line in data_list:
    if line.find( "%s:" % reponame ) == 0:
      found = True
      if branch == "":
        continue #eliminate this row
      else:
        new_content += "%s:%s\n" % ( reponame, branch )
    else:
      new_content += line

  if not found and branch != "":
    new_content += "%s:%s\n" % ( reponame, branch )

  fout = open( "%s/%s" % ( proot, SWFILE_DEFBR ), "w")
  fout.writelines(new_content)
  fout.close()

  #add to index
  cmd_submod_defaultbr = "cd %s && git add %s" % ( proot, SWFILE_DEFBR )
  GLog.f( GLog.I, "%s" % cmd_submod_defaultbr )
  ret = os.system( cmd_submod_defaultbr )
  if ret != 0:
    return "FAILED", 1

  #set config 
  if branch != "":
    out, errCode = set_repo_cfg( SWCFG_INTBR, branch, "%s/%s" % (proot, reponame) )
  else:
    repodir = "%s/%s" % (proot, reponame)
    if os.path.exists( repodir ):
      out, errCode = set_repo_cfg( SWCFG_INTBR, SWCFG_UNSET, repodir )
    else:
      #this happens when deleting already removed repository
      errCode = 0

  if errCode != 0:
    return "FAILED setting Integration branch inside repo: " + "%s/%s" % (proot, reponame), 1

  return "DONE", 0


def write_snapshotfile_addindex( proot, reponame, url, branch ):

  config   = ConfigParser.RawConfigParser()
  filename = "%s/%s" % ( proot, SWFILE_SNAPCFG )
  try:
    config.read( filename )
  except Exception, e:
    return "ERROR - malformed file content %s" % ( filename ), 1

  if config.has_section( reponame ):
    return "ERROR - %s already is configured as snapshot repo inside project %s" % ( proot, reponame ), 1

  #create section
  #config.add_section( reponame )
  #config.set( reponame, SWFILE_SNAPCFG_URL   ,    url     )
  #config.set( reponame, SWFILE_SNAPCFG_BRANCH,    branch  )
  #config.set( reponame, SWFILE_SNAPCFG_ALWAYSUPD, "False" )
  new_cont = "[%s]\n%s = %s\n%s = %s\n" % ( reponame, SWFILE_SNAPCFG_URL, url, SWFILE_SNAPCFG_BRANCH, branch )
  cmd_echo = "echo '%s' >> %s" % (new_cont, filename)
  ret = os.system( cmd_echo )
  if ret != 0:
    return "ERROR editing file %s" % filename, 1

  #add to index
  cmd_add_snapfile = "cd %s && git add %s" % ( proot, filename )
  GLog.f( GLog.I, "%s" % cmd_add_snapfile )
  ret = os.system( cmd_add_snapfile )
  if ret != 0:
    return "FAILED", 1

  return "DONE", 0



def refresh_repo_intbr( abs_projdir, abs_repodir ):

  intbr = submod_get_defbr( abs_projdir, abs_repodir )
  locdir = os.path.basename( abs_repodir )

  if intbr != "":

    cmd_intBr = "cd %s && SWINDENT=%s %s branch --set-integration-br %s" % \
        ( abs_repodir, GLog.tab + 1, SWGIT, intbr )
    errCode = os.system( cmd_intBr )
    return errCode

  else: #clean intbr info (maybe go onto CST branch)

    ib = Branch.getIntBr( abs_repodir )
    if ib.isValid() != True:
      #already unset
      return 0

    GLog.s( GLog.S, "\tUnsetting INTEGRATION branch into repo %s ... " % (locdir) )
    out, errCode = set_repo_cfg( SWCFG_INTBR, SWCFG_UNSET, abs_repodir )
    if errCode != 0:
      GLog.f( GLog.E, "\tFAILED unsetting Integration branch inside repo: " + locdir )
      return 1

    GLog.logRet( 0, indent = "\t" )

  return 0


def refresh_intbr( root ):

  #use al contained projects
  #plus first level repos

  f_err = 0

  #
  # first level repos
  #
  for r in submod_list_repos( root, firstLev = True, excludeRoot = True ):

    ret = refresh_repo_intbr( root, r )
    if ret != 0:
      f_err = 1

  #
  # all levels projects
  #
  #  root already processed previously
  #
  for p in submod_list_projs( root, excludeRoot = True ):

    for r in submod_list_repos( p, firstLev = True, excludeRoot = True ):

      ret = refresh_repo_intbr( p, r )
      if ret != 0:
        f_err = 1


  return f_err


#
# proj --reset XYZ
#
def proj_reset_all( root, ref, nolog = False ):

  err, errstr = Status.checkLocalStatus_rec( root, ignoreSubmod=True )
  if err != 0:
    GLog.f( GLog.E, errstr )
    return 1

  errCode, sha = getSHAFromRef( ref, root )
  if errCode != 0:
    GLog.f( GLog.E, "Reference %s not existing into project %s." % ( ref, root ) )
    return 1

  proj_repo_info = "project %s" % root

  commit_info = ""
  if ref == "HEAD":
    commit_info = "HEAD (%s)" % ( getSHAFromRef( ref )[1][0:8] )
  else:
    commit_info = "reference %s" % ref

  if not nolog:
    GLog.s( GLog.S, "Setting %s onto %s ... " % ( proj_repo_info, commit_info ) )

  #Split it in 2 parts in order to show only interestig output 
  cmd_submod_upd_1 = "cd %s && git checkout %s" % ( root, ref )
  out, errCode = myCommand( cmd_submod_upd_1 )
  if errCode != 0:
    GLog.f( GLog.E, out )
    return 1

  cmd_submod_upd_2 = "cd %s && git submodule update --recursive" % ( root )
  out, errCode = myCommand( cmd_submod_upd_2 )
  if out != "":
    GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
  if errCode != 0:
    return 1

  ret = refresh_intbr( root )
  if ret != 0:
    if not nolog:
      GLog.logRet( 1 )
    return 1

  if not nolog:
    GLog.logRet( 0 )
  return 0


#
# proj --reset XYZ <repo>
#
def proj_reset_repo( proot, pref, rname ):

  errCode, sha = getSHAFromRef( pref, proot )
  if errCode != 0:
    GLog.f( GLog.E, "Reference %s not existing into project %s." % ( pref, proot ) )
    return 1

  if os.path.exists( "%s/%s" % ( proot, rname)  ) == False:
    GLog.f( GLog.E, "Repository %s not existing into project %s." % ( rname, proot ) )
    return 1

  #
  # snapshot repo
  #
  if dir2reponame( rname ) in submod_list_snapshot():
    objSnapRepo = ObjSnapshotRepo( rname )
    out, errCode = objSnapRepo.pull_reference( proot, pref, rname )
    if errCode != 0:
      GLog.f( GLog.E, out )
      return 1
    return 0


  # check only that subtree, i can have proj wd dirty (specially usefull when adding repo)
  err, errstr = Status.checkLocalStatus_rec( "%s/%s" % (proot,rname), ignoreSubmod=True )
  if err != 0:
    GLog.f( GLog.E, errstr )
    return 1

  repover, errCode = submod_getrepover_atref( proot, rname, pref )
  if errCode != 0:
    GLog.f( GLog.E, repover )
    return 1

  abs_repo_path = os.path.abspath( "%s/%s" % ( proot, rname ) )

  GLog.s( GLog.S, "Setting repository %s to its version %s ... " % ( rname, repover ) )

  errCode = proj_reset_all( abs_repo_path, repover, nolog = True )
  #cmd_reset = "cd %s && SWINDENT=%s %s proj --reset %s" % ( abs_repo_path, GLog.tab+1, SWGIT, repover )
  #errCode = os.system( cmd_reset )
  if errCode != 0:
    GLog.logRet( 1 )
    return 1
  GLog.logRet( 0 )
  return 0


def proj_update_old( map ):

    #otherwise, pull will fail 
    cb = Branch.getCurrBr()
    if cb.isValid() == False:
      GLog.f( GLog.E, "FAILED - Cannot issue \"proj --update\" command in DETACHED-HEAD." )
      return 1


    #
    # In case you have developped only inside submodules, 
    #   reset HEAD so that no pull go on (no dirty WD)
    #
    cmd_reset = "cd %s && SWINDENT=%s %s proj --reset HEAD" % ( map.getDir(), GLog.tab, SWGIT )
    errCode = os.system( cmd_reset )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )

    #
    # Update local map and local repo
    #
    cmd_reset = "cd %s && SWINDENT=%s %s pull" % ( map.getDir(), GLog.tab, SWGIT )
    errCode = os.system( cmd_reset )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )

    #
    # Update submodules according to new map
    #
    cmd_reset = "cd %s && SWINDENT=%s %s proj --reset HEAD" % ( map.getDir(), GLog.tab, SWGIT )
    errCode = os.system( cmd_reset )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit( 1 )

    #
    # If you are on a CST branch, all your subrepos will do the same, 
    #  swgit proj --reset HEAD already downloaded their history and placed them on the right place. 
    #  Nothin else to do.
    #
    cb = Branch.getCurrBr()
    if cb.getType() == SWCFG_BR_CST:
      sys.exit( 0 )


    #
    # If you have INT sbrepos, pull them too
    #
    intrepos = submod_list_repos_byType( SWCFG_BR_INT, map.getDir(), firstLev = True, excludeRoot = True  )

    if len( intrepos ) > 0:
      GLog.s( GLog.S, "Updating ALL INT repositories inside %s ... " %  os.path.basename( map.getDir() ) )

    strerr = ""
    for intrepo in intrepos:

      GLog.s( GLog.S, "\tUpdating INT repository %s ... " % intrepo )
      
      errCode = 0
      if os.path.exists( "%s/%s" % ( intrepo, SWFILE_PROJMAP)  ) == True :  #inside project
        cmd_update = "cd %s && SWINDENT=%s %s branch -i && SWINDENT=%s %s proj --update" % ( intrepo, GLog.tab + 2 , SWGIT, GLog.tab + 2 , SWGIT )
        errCode = os.system( cmd_update )
      else: #inside repo
        cmd_update_intrepo = "cd %s && SWINDENT=%s %s branch -i && SWINDENT=%s %s pull" % ( intrepo, GLog.tab + 2, SWGIT, GLog.tab + 2,  SWGIT )
        errCode = os.system( cmd_update_intrepo )
      
      if errCode != 0:
        if strerr == "":
          strerr += " %s " % intrepo
        else:
          strerr += " - %s " % intrepo
        GLog.logRet( 1, indent = "\t")
      else:
        GLog.logRet( 0, indent = "\t")

    if strerr != "":
      GLog.logRet( 1, reason = strerr )
      sys.exit( 1 )
    else:
      if len( intrepos ) != 0:
        GLog.logRet( 0 )





def main():
  usagestr =  """\
Usage: swgit proj --add-repo [-b branch] [--snapshot] <url> [<localname>]
   or: swgit proj --del-repo <reponame>...
   or: swgit proj --edit-repo --set-int-br|--unset-int-br <new-int-br> <reponame>...
   or: swgit proj --init [--snapshot] <reponame>...
   or: swgit proj --un-init <reponame>...
   or: swgit proj --update [-I|-N] [--snapshot] [<snapshotrepo>...]
   or: swgit proj --reset <proj-reference> [<reponame>...]
   or: swgit proj --list|--list-all
   or: swgit proj --get-configspec [--pretty]
   or: swgit proj --diff [<ref1>] [<ref2>] [<reponame>...]
"""

  parser       = OptionParser( usage = usagestr,
                               description='>>>>>>>>>>>>>> swgit - ProjMap Management <<<<<<<<<<<<<<' )

  mod_group    = OptionGroup( parser, "Mod proj options" )
  init_group   = OptionGroup( parser, "Init options" )
  move_group   = OptionGroup( parser, "Update options" )
  list_group   = OptionGroup( parser, "List options" )
  common_group = OptionGroup( parser, "Common options" )
  output_group = OptionGroup( parser, "Output options" )

  load_command_options( common_group, common_options )
  load_command_options( mod_group, mod_options )
  load_command_options( init_group, init_options )
  load_command_options( move_group, move_options )
  load_command_options( list_group, list_options ) 
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( common_group )
  parser.add_option_group( mod_group )
  parser.add_option_group( init_group )
  parser.add_option_group( move_group )
  parser.add_option_group( list_group )
  parser.add_option_group( output_group )
  
  (options, args)  = parser.parse_args()

  help_mac( parser )
 
  # All other cases
  GLog.initGitLogs( options )
  GLog.s( GLog.I, " ".join( sys.argv ) )
  output_opt = getOutputOpt(options)

  #######
  # ADD #
  #######
  if options.add_repo == True:

    out, err = check_allowed_options_p( "--add-repo", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if options.proj_branch == "" and options.snap_repo == True:
      GLog.f( GLog.E, "ERROR: When adding new snapshot repo --branch option is mandatory " )
      sys.exit( 1 )

    repo_name = None
    proj_url  = None
    if len( args ) == 0:
      GLog.f( GLog.E, "ERROR: url argument is mandatory." )
      sys.exit( 1 )
    elif len( args ) == 1:
      proj_url  = args[0]
      repo_name = os.path.basename( proj_url )
    elif len( args ) == 2:
      proj_url  = args[0]
      repo_name = args[1]
    else:
      GLog.f( GLog.E, "ERROR: Too many arguments." )
      sys.exit( 1 )

    if repo_name in submod_list_all_default( Env.getLocalRoot() ):
      GLog.f( GLog.E, "ERROR: Already existing repository '%s' inside project %s" % ( repo_name, Env.getLocalRoot() ) )
      sys.exit( 1 )

    ret, errstr = check_BRexists_and_WDclean( Env.getLocalRoot() )
    if ret != 0:
      GLog.f( GLog.E, errstr )
      sys.exit( 1 )

    ret = checkRepo( proj_url, options.proj_branch )
    if ret != 0:
      sys.exit( 1 )

    GLog.s( GLog.S, "Adding section %s to project %s" % ( repo_name , Env.getLocalRoot() ) )

    #
    # git bug, adding a repo with -b, when HEAD in on -b tip, does not work at first (make it twice)
    #  if error occours => must de-initialize it (from git config) otherwise consequent init will fail
    #
    opt_br = ""
    if options.proj_branch != "":
      opt_br = "-b %s" % options.proj_branch
    cmd_submod_add = "cd %s && ( git submodule add %s %s %s || git submodule add %s %s %s && cd %s && git checkout -- && cd - )" % ( Env.getLocalRoot(), opt_br, proj_url, repo_name, opt_br, proj_url, repo_name, repo_name )
    out,ret = myCommand( cmd_submod_add )
    if ret != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    #when frst submod fail, second dsubmodule also initialize repo, must not => undo it here
    set_repo_cfg( "submodule.%s.url" % repo_name, SWCFG_UNSET )

    #
    # Def br
    # moved before init, otherwise init will not find file for defbr
    #
    out, errCode = write_swdefbr_addindex_config( Env.getLocalRoot(), repo_name, options.proj_branch )
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet( 1 )
      sys.exit(1)

    #
    # Init repo
    #
    cmd_init_added_repo = "cd %s && SWINDENT=%s %s proj --init %s" % \
                           ( Env.getLocalRoot(), GLog.tab + 1, SWGIT, repo_name )
    errCode = os.system( cmd_init_added_repo )
    if errCode != 0:
      GLog.logRet( 1 )
      sys.exit(1)

    #
    # Manage snapshot repo
    #
    if options.snap_repo == True:
      out, errCode = write_snapshotfile_addindex( Env.getLocalRoot(), repo_name, proj_url, options.proj_branch )
      if errCode != 0:
        GLog.f( GLog.E, out )
        GLog.logRet( 1 )
        sys.exit(1)


    GLog.logRet( 0 )

    # work is finished, notify user about commit and push
    GLog.s( GLog.S, "\nPLEASE VERIFY EVERITHING IS OK, THEN COMMIT with \"swgit commit --dev %s\", MERGE ON DEVELOP AND PUSH PROJECT DIRECTORY (%s)\n" % ( repo_name, Env.getLocalRoot() ) )

    sys.exit( 0 )


  map = create_swmap( debug = options.debug )
  if not map.isValid():
    if options.proj_list or options.proj_list_all:
      repo = create_swrepo( debug = options.debug )
      dumpproj_op = SwOp_DumpProj()
      repo.accept( dumpproj_op )
      sys.exit( 0 )
    else:
      GLog.f( GLog.E, "ERROR: NOT inside a project, cannot issue this command" )
      sys.exit( 1 )

  alls  = submod_list_all_default( map.getDir() )
  inits = submod_list_initialized( map.getDir() )
  snaps = submod_list_snapshot( map.getDir() )

  ##########
  # DELETE #
  ##########
  if options.del_repo == True:

    out, err = check_allowed_options_p( "--del-repo", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if len( args ) == 0:
      GLog.f( GLog.E, "ERROR: please specify at least 1 repository to be deleted" )
      sys.exit( 1 )

    for rn in args:
      rn = dir2reponame( rn )
      if rn not in alls:
        GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( rn, map.getDir() ) )
        sys.exit( 1 )
    # delete also if not initialized
    #  if rn not in submod_list_initialized( map.getDir() ):
    #    GLog.f( GLog.E, "ERROR: Not initialized repository '%s' inside project %s" % ( rn, map.getDir() ) )
    #    sys.exit( 1 )

    proot = map.getDir()
    ret, errstr = check_BRexists_and_WDclean( proot )
    if ret != 0:
      GLog.f( GLog.E, errstr )
      sys.exit( 1 )

    for rn in args:
      rn = dir2reponame( rn )

      GLog.s( GLog.S, "Deleting section %s from project %s" % (rn, proot) )

      # Delete the relevant line from the .gitmodules file.
      fin = open( "%s/%s" % ( proot, SWFILE_PROJMAP ), "r" )
      data_list = fin.readlines()
      fin.close()

      new_content = ""
      jumpnextNlines = -1
      #print data_list

      for line in data_list:
        #print "line: %s" % line[:-1]
        if jumpnextNlines >= 0:
          jumpnextNlines -= 1

        if line[:-1] == "[submodule \"%s\"]" % rn:
          #print "found"
          jumpnextNlines = 2
          continue

        if jumpnextNlines >= 0:
          #print "cont"
          continue

        #print "add"
        new_content += line

      #print new_content

      fout = open( "%s/%s" % ( proot, SWFILE_PROJMAP ), "w")
      fout.writelines(new_content)
      fout.close()

      # Delete the relevant section from .git/config.
      out, errCode = set_repo_cfg( "submodule.%s.url" % rn, SWCFG_UNSET, proot )
      if errCode != 0:
        GLog.f( GLog.E, out )
        GLog.logRet(1)
        sys.exit( 1 )

      # Delete the relevant section from .swDIR/swdefbr
      out, errCode = write_swdefbr_addindex_config( Env.getLocalRoot(), rn, "" )
      if errCode != 0:
        GLog.f( GLog.E, out )
        GLog.logRet(1)
        sys.exit(1)

      # Run git rm --cached path_to_submodule (no trailing slash).
      cmd_remote_checkes = "cd %s && git rm --cached %s" % ( proot, rn )
      out, errCode = myCommand( cmd_remote_checkes )
      if errCode != 0:
        GLog.f( GLog.E, out )
        GLog.logRet(1)
        sys.exit( 1 )

      # work is finished, notify user about commit and push
      GLog.s( GLog.S, "\nPLEASE VERIFY EVERITHING IS OK, THEN COMMIT with \"swgit commit --dev %s\" option set, MERGE ON DEVELOP AND PUSH PROJECT DIRECTORY (%s)\n" % ( rn, proot ) )

      GLog.logRet( 0 )

    sys.exit( 0 )

  ########
  # EDIT #
  ########

  elif options.edit_repo == True:

    out, err = check_allowed_options_p( "--edit-repo", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if len( args ) != 1:
      GLog.f( GLog.E, "Please specify 1 repository to be edited." )
      sys.exit( 1 )

    repo_name = dir2reponame( args[0] )
    if repo_name not in submod_list_all_default( map.getDir() ):
      GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( repo_name, map.getDir() ) )
      sys.exit( 1 )

    if options.set_int_br == None and options.unset_int_br == False:
      GLog.f( GLog.E, "Please specify --set-int-br or --unset-int-br option" )
      sys.exit( 1 )

    if options.set_int_br != None:

      objBr = Branch( options.set_int_br, repo_name )
      if not objBr.isValid():
        GLog.f( GLog.E, "Please specify a valid branch for option --set-int-br" )
        sys.exit( 1 )

      if not is_local_branch( options.set_int_br, repo_name ):
        GLog.f( GLog.E, "Please specify a local branch for option --set-int-br" )
        sys.exit( 1 )


    GLog.s( GLog.S, "Editing section %s into project %s" % ( repo_name, map.getDir() ) )

    # Edit the relevant section from .swdir/cfg/default_branches.cfg
    if options.set_int_br != None:
      br = options.set_int_br
    else:
      br = ""

    out, errCode = write_swdefbr_addindex_config( map.getDir(), repo_name, br )
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet( 1 )
      sys.exit(1)

    GLog.logRet( 0 )
    sys.exit( 0 )



  ########
  # INIT #
  ########
  #
  # No repo   => initialize all
  #
  elif options.init_repo == True:

    out, err = check_allowed_options_p( "--init", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if len( args ) != 0:
      if options.snap_repo:
          GLog.f( GLog.E, "ERROR: Cannot specify '--snapshot' option and single repository/ies together" )
          sys.exit( 1 )

      for rn in args:
        rn = dir2reponame( rn )
        if rn not in alls:
          GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( rn, map.getDir() ) )
          sys.exit( 1 )
        if rn in inits:
          GLog.f( GLog.E, "ERROR: Already initialized repository '%s' inside project %s" % ( rn, map.getDir() ) )
          sys.exit( 1 )

    first_level_invoke = True
    if os.getenv( "SWRECURSE" ) == "YES":
      first_level_invoke = False

    if os.path.exists( "%s/%s" % (os.getcwd(), SWFILE_PROJMAP) ) == False:
      if not first_level_invoke:
        sys.exit(0)
      else:
        GLog.f( GLog.E, "Cannot issue this command outside project root direcotry (%s)" % (map.getDir()) )
        sys.exit(1)

    dir = map.getDir()

    repo_names = []
    if len( args ) != 0:
      repo_names = args
    else:
      if options.snap_repo:
        repo_names = submod_list_not_initialized( dir )
      else:
        repo_names = submod_list_notinitialized_notsnapshot( dir )

    remotes = Remote.get_remote_list()
    on_ori = True
    if len( remotes ) > 0:
      on_ori = False
      remote_name = eval_default_remote_name()
      projRemote = create_remote_byname( remote_name )

    #
    # 1. init
    # 2. clone
    #
    RESPONSE_LOCALIZED = "LOCALIZED"
    RESPONSE_REMOTIZED = "REMOTIZED"
    for rn in repo_names:
      rn = dir2reponame( rn )
      if submod_is_initialized( dir, rn ):
        continue

      str  = "Initializing repository %s " % rn
      if not on_ori:
        str += "according to '%s' remote" % remote_name
      GLog.s( GLog.S, str )

      if rn in submod_list_snapshot():
        GLog.s( GLog.S, "\tRepo %s is a \"snapshot\" repo, emtpying it before converting to \"standard\" repo" % rn )
        shutil.rmtree( rn, True ) #ignore errors
        os.mkdir( rn )
        GLog.s( GLog.S, "\tDONE" )


      if not on_ori:
        cmd_remote_repo_is_localized = "test -e \"%s/%s/.git\" && echo %s || echo %s" % \
                                        ( projRemote.getRoot(), rn, RESPONSE_LOCALIZED, RESPONSE_REMOTIZED )
        GLog.f( GLog.D, "onto\n%s\ncmd:\n %s" % ( projRemote, cmd_remote_repo_is_localized ) )
        out, retcode = projRemote.remote_command( cmd_remote_repo_is_localized )
        GLog.f( GLog.D, "response: %s" % out[:-1] )
        if retcode != 0:
          GLog.f( GLog.E, "FAILED - Cannot contact \"origin\" at %s (user: %s)" % (projRemote.getAddress(), projRemote.getUser()) )
          sys.exit(1)
      else:
        #on origin, use .gitmodules
        out = RESPONSE_REMOTIZED


      if RESPONSE_LOCALIZED in out[:-1]: #there is a space more, cannot use ==

        #init by hand, no output
        cmd_submod_init = "cd %s && git config submodule.%s.url %s/%s" % ( dir, rn, projRemote.getUrl(), rn )
        cmd_submod_upd  = "cd %s && git submodule update -- %s" % ( dir, rn )

      else:

        cmd_submod_init = "cd %s && git submodule init -- %s" % ( dir, rn )
        cmd_submod_upd  = "cd %s && git submodule update -- %s" % ( dir, rn )


      out, errCode = myCommand( cmd_submod_init )
      if errCode != 0:
        GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
        GLog.f( GLog.E, "FAILED" )
        sys.exit(1)

      out, errCode = myCommand( cmd_submod_upd )
      if out[:-1] != "":
        GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
      if errCode != 0:
        GLog.f( GLog.E, "FAILED" )
        sys.exit(1)

      #
      # 3. config
      #
      cmd_merge = "cd %s/%s && git config merge.merge_swdefbr.name \"always keep mine during merge\" \
          && git config merge.merge_swdefbr.driver \"%s/scripts/merge_swdefbr.sh %%O %%A %%B\"" % ( dir, rn, SWGIT_DIR )
      GLog.f( GLog.I, cmd_merge )
      out,errCode = myCommand( cmd_merge )
      if errCode != 0:
        GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
        GLog.f( GLog.E, "FAILED" )
        sys.exit(1)

      #
      # 4. reset HEAD (set int br)
      #
      #if first_level_invoke:
      #  errCode = refresh_repo_intbr( dir, dir + rn )
      #else:
      #  cmd_submod_reset_head  = "cd %s && SWINDENT=%s %s proj --reset HEAD %s" % ( dir, GLog.tab + 1, SWGIT, rn )
      #  out, errCode = myCommand( cmd_submod_reset_head )
      errCode = refresh_repo_intbr( dir, dir + "/" + rn )
      if errCode != 0:
        GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
        GLog.f( GLog.E, "FAILED" )
        sys.exit(1)

      #
      # 5. goto INT if develop repo
      #
      abspaths = submod_list_repos_byType( SWCFG_BR_INT, dir, excludeRoot = True, firstLev = True )
      for absp in abspaths:
        cmd_branch_i = "cd %s && SWINDENT=%s %s branch -i --quiet" % ( absp, GLog.tab + 1, SWGIT )
        errCode = os.system( cmd_branch_i )


      #
      # 6. recurse
      #
      cmd_init_recurse = "cd %s/%s && SWRECURSE=YES SWINDENT=%s %s proj --init" % ( dir, rn, GLog.tab + 1, SWGIT )
      errCode = os.system( cmd_init_recurse )
      if errCode != 0:
        GLog.logRet( 1 )
        sys.exit(1)

      GLog.logRet( 0 )

    sys.exit(0)


  ###########
  # UN-INIT #
  ###########
  #
  # No repo   => un-init all
  #
  elif options.uninit_repo == True:

    out, err = check_allowed_options_p( "--un-init", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if len( args ) != 0:
      for rn in args:
        rn = dir2reponame( rn )
        if rn not in inits:
          GLog.f( GLog.E, "ERROR: Cannot un-init %s, it is not initialized" % ( rn ) )
          sys.exit( 1 )

    repo_names = []
    if len( args ) != 0:
      repo_names = args
    else:
      repo_names = inits


    for rn in repo_names:

      rn = dir2reponame( rn )

      GLog.s( GLog.S, "Deleting local clone repository %s" % rn )

      #remove directory
      cmd_submod_remove = "cd %s && rm -rf ./%s/* && rm -rf ./%s/.??*" % ( map.getDir(), rn, rn )
      out, errCode = myCommand( cmd_submod_remove )
      if errCode != 0:
        GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
        GLog.f( GLog.E, "FAILED" )
        sys.exit(1)

      #uninit directory
      out, errCode = set_repo_cfg( "submodule.%s.url" % rn, SWCFG_UNSET, map.getDir() )
      if errCode != 0:
        GLog.f( GLog.E, "\tFAILED un-initializing repository %s" % rn  )
        GLog.f( GLog.E, "FAILED" )
        sys.exit(1)

      GLog.f( GLog.E, "DONE" )

    sys.exit(0)


  ##########
  # UPDATE #
  ##########
  elif options.update_repo == True:

    def manage_strerr( errCode, strerr ):
      if errCode != 0:
        if strerr == "":
          strerr += "%s" % repo
        else:
          strerr += " - %s" % repo
      GLog.logRet( errCode )
      return strerr

    out, err = check_allowed_options_p( "--update", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if Remote.is_origin_repo():
      GLog.f( GLog.E, "FAILED - Cannot issue \"proj --update\" on origin." )
      sys.exit( 1 )

    if len( args ) != 0 and options.snap_repo:
        GLog.f( GLog.E, "ERROR: Cannot specify '--snapshot' option and single repository/ies together" )
        sys.exit( 1 )

    if options.update_repo_yesmerge and options.update_repo_nomerge:
        GLog.f( GLog.E, "ERROR: Cannot specify both '--merge-from-int' and '--no-merge' options together" )
        sys.exit( 1 )

    #### START snapshot update (only with parameter passed
    if len( args ) != 0 or options.snap_repo:
      repo_names = []
      if len( args ) != 0:
        repo_names = args
      else:
        repo_names = submod_list_snapshot()

      for rn in repo_names:
        rn = dir2reponame( rn )
        if rn not in alls:
          GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( rn, map.getDir() ) )
          sys.exit( 1 )
        if rn in snaps:
          continue
        GLog.f( GLog.E, "ERROR: proj --update <repo> can be issued only on \"snapshot repositories\". \"%s\" is not." % ( rn ) )
        sys.exit( 1 )

      for rn in repo_names:
        rn = dir2reponame( rn )
        objSnapRepo = ObjSnapshotRepo( rn )
        out, errCode = objSnapRepo.pull_reference( map.getDir(), "HEAD", rn )
        if errCode != 0:
          GLog.f( GLog.E, out )
          sys.exit( 1 )

      sys.exit( 0 )
    #### END snapshot update

    #### START NO MERGE -> git submodule update
    # Note this mode behaves exatly like git submodule update => if any new history is not necessary, it is not downloaded
    if options.update_repo_nomerge:

      GLog.s( GLog.S, "Updating ALL repositories in one shot, no pull no side merges ... " )

      cmd_update_all  = "cd %s && git submodule update --recursive" % map.getDir()
      out, errCode = myCommand( cmd_update_all )

      GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
      GLog.logRet( errCode )
      if errCode != 0:
        sys.exit( 1 )
      sys.exit( 0 )
    #### END NO MERGE

    #### START: UPDATE DEFAULT or UPDATE WITH MERGE

    #some checks
    cb = Branch.getCurrBr()
    ib = Branch.getIntBr()
    if not cb.isValid() and not ib.isValid():
      GLog.f( GLog.E, "FAILED - Cannot issue \"proj --update\" command in DETACHED-HEAD and without and INTEGRATION branch set." )
      return 1

    if not cb.isValid() and options.update_repo_yesmerge:
      GLog.f( GLog.E, "FAILED - Cannot issue \"proj --update\" command in DETACHED-HEAD and without and INTEGRATION branch set." )
      return 1

    #
    # Update local map and local repo
    #   side merge    => pull -I
    #   no-side-merge => branch -i
    #                    pull
    #
    GLog.s( GLog.S, "Updating project root repository ... " )

    if options.update_repo_yesmerge:

      cmd_reset = "SWINDENT=%s %s pull --merge-from-int" % ( GLog.tab + 1, SWGIT )
      errCode = os.system( cmd_reset )

    else:

      #cmd_reset = "SWINDENT=%s %s branch -i && SWINDENT=%s %s proj --reset HEAD && SWINDENT=%s %s pull" % \
      #    ( GLog.tab + 1, SWGIT, GLog.tab + 1, SWGIT, GLog.tab + 1, SWGIT )
      cmd_reset = "SWINDENT=%s %s branch -i && SWINDENT=%s %s pull" % \
          ( GLog.tab + 1, SWGIT, GLog.tab + 1, SWGIT )
      errCode = os.system( cmd_reset )

    GLog.logRet( errCode )
    if errCode != 0:
      sys.exit( 1 )


    #
    # Process subrepos:
    #  CST always submodule update
    #  INT pull develop and/or side merge
    #
    repos = submod_list_repos( map.getDir(), firstLev = True, excludeRoot = True, localpaths = True )
    if len( repos ) == 0:
      sys.exit( 0 )

    strerr = ""
    for repo in repos:
      errCode = 0

      repocb = Branch.getCurrBr( repo )
      repoib = Branch.getIntBr( repo )
      repotype = getRepoType( repo )
      isproj   = Env.is_aproj( repo )

      #print "name   ", repo
      #print "isproj ", isproj
      #print "type   ", repotype
      #print "cb:    ", repocb
      #print "ib:    ", repoib

      str_repo = "repository"
      if isproj:
        str_repo = "project"
      GLog.s( GLog.S, "Updating %s %s %s ... " % (repotype,str_repo,repo) )


      if repotype == SWCFG_BR_CST: #CST

        cmd_update_cst  = "cd %s && git submodule update --recursive -- %s" % ( map.getDir(), repo )
        out, errCode = myCommand( cmd_update_cst )
        if out[:-1] != "":
          GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )

        strerr = manage_strerr( errCode, strerr )
        continue


      if not repoib.isValid(): #INT, no intbr

        GLog.s( GLog.S, "No integration branch set, just download new commits without merging ... " % (repo) )

        cmd_update_cst  = "cd %s && git submodule update --recursive -- %s" % ( map.getDir(), repo )
        out, errCode = myCommand( cmd_update_cst )
        if out[:-1] != "":
          GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )

        strerr = manage_strerr( errCode, strerr )
        continue


      #detached head or update without options => pull intbr
      if not repocb.isValid() or \
         (not options.update_repo_yesmerge and not options.update_repo_nomerge):

        cmd_gotoint = "cd %s && SWINDENT=%s %s branch -i" % ( repo, GLog.tab + 1,  SWGIT )
        errCode = os.system( cmd_gotoint )

        if errCode != 0:
          continue


      str_opt_merge = ""
      if options.update_repo_yesmerge:
        str_opt_merge = "--merge-from-int"

      if isproj:

        cmd_update_proj = "cd %s && SWINDENT=%s %s proj --update %s" % ( repo, GLog.tab + 1 , SWGIT, str_opt_merge )
        errCode = os.system( cmd_update_proj )

        strerr = manage_strerr( errCode, strerr )
        continue

      else:

        cmd_update_intrepo = "cd %s && SWINDENT=%s %s pull %s" % ( repo, GLog.tab + 1,  SWGIT, str_opt_merge )
        errCode = os.system( cmd_update_intrepo )

        strerr = manage_strerr( errCode, strerr )
        continue


    if strerr != "":
      GLog.logRet( 1, reason = strerr )
      sys.exit( 1 )
    sys.exit( 0 )



  ##########
  # FREEZE #
  ##########
  #elif options.proj_freeze == True:

  #  out, err = check_allowed_options( "--freeze" )
  #  if err != 0:
  #    print out
  #    sys.exit( 1 )

  #  err, errstr = Status.checkLocalStatus_rec( map.getDir(), ignoreSubmod = True )
  #  if err != 0:
  #    print errstr
  #    sys.exit( 1 )

  #  GLog.s( GLog.S, "Freezing project %s ... " % ( map.getDir() ) )

  #  msg = "Freezing project"
  #  if options.message != None:
  #    msg = options.message

  #  bottom_up_list = submod_list_projs( map.getDir() )
  #  bottom_up_list.reverse()

  #  for p in bottom_up_list:
  #    #cmd_submod_freeze = "cd %s && SWINDENT=%s %s commit -a -m \"Freezing project\"" % ( p, GLog.tab + 1, SWGIT ) 
  #    err, errstr = Status.checkLocalStatus( p, ignoreSubmod = False )
  #    if err != 0:
  #      #some module moved on
  #      cmd_submod_freeze = "cd %s && git commit -a -m \"%s\"" % ( p, msg ) 
  #      #print cmd_submod_freeze
  #      out, errCode = myCommand( cmd_submod_freeze )
  #      if errCode != 0:
  #        GLog.f( GLog.E, out )
  #        sys.exit( 1 )

  #  GLog.logRet( 0 )


  #########
  # RESET #
  #########
  elif options.reset_ref != None:

    out, err = check_allowed_options_p( "--reset", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    if len( args ) != 0:
      for rn in args:
        rn = dir2reponame( rn )
        if rn not in alls:
          GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( rn, map.getDir() ) )
          sys.exit( 1 )
        if rn in snaps: #snap alway allow
          continue
        if rn not in inits:
          GLog.f( GLog.E, "ERROR: Cannot reset %s, it is not initialized" % ( rn ) )
          sys.exit( 1 )

    retall = 0
    if len( args ) != 0:
      for rn in args:
        rn = dir2reponame( rn )
        ret = proj_reset_repo( map.getDir(), options.reset_ref, rn )
        if ret != 0:
          retall = 1
    else:
      retall = proj_reset_all( map.getDir(), options.reset_ref )

    if retall != 0:
      sys.exit( 1 )
    sys.exit( 0 )

  ########
  # LIST #
  ########
  elif options.proj_list == True:

    if len(args) != 0:
      parser.error("Too many arguments")

    out, err = check_allowed_options_p( "--list", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    proj = create_swproj( debug = options.debug )
    dumpproj_op = SwOp_DumpProj()
    proj.accept( dumpproj_op )

  elif options.proj_list_all == True:

    if len(args) != 0:
      parser.error("Too many arguments")

    out, err = check_allowed_options_p( "--list-all", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    proj = create_swproj( debug = options.debug )
    dumpproj_op = SwOp_DumpProj( listall = True )
    proj.accept( dumpproj_op )

  ##########
  # GET-CS #
  ##########
  elif options.get_cs == True:

    ref = "HEAD"
    if len(args) == 1:
      ref = args[0]
    if len(args) > 1:
      parser.error("Too many arguments")

    out, err = check_allowed_options_p( "--get-configspec", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    errCode, sha = getSHAFromRef( ref )
    if errCode != 0:
      GLog.f( GLog.E, "Reference %s not existing into project %s." % ( ref, map.getDir() ) )
      sys.exit( 1 )

    if options.pretty == False:
      retstr = "./:%s" % sha
    else:
      retstr = "%s\n\t%s" % ( os.getcwd(), sha )
      desc = cs_desribe_ref( map.getDir(), sha )
      retstr += indentOutput( desc, 2 )


    localrepos = submod_list_all_default( map.getDir() )
    for rn in localrepos:
      rn = dir2reponame( rn )
      #print rn
      repover, errCode = submod_getrepover_atref( map.getDir(), rn, ref )
      if errCode != 0:
        GLog.f( GLog.E, repover )
        sys.exit( 1 )

      if options.pretty == False:

        retstr += "\n%s:%s" % ( rn, repover ) 

      else:

        retstr += "\n%s\n\t%s" % ( rn, repover )

        desc = cs_desribe_ref( "%s/%s" % (map.getDir(), rn), repover )
        retstr += indentOutput( desc, 2 )

    print retstr[:-1]

  ########
  # DIFF #
  ########
  elif options.diff == True:

    out, err = check_allowed_options_p( "--diff", proj_allowmap, parser )
    if err != 0:
      GLog.f( GLog.E, out )
      sys.exit( 1 )

    args_submod = args #args without ref1 and ref2
    ref1 = "HEAD"
    ref2 = ""
    if len( args ) == 0:
      pass
    if len( args ) == 1:
      errCode, sha = getSHAFromRef( args[0] )
      if errCode == 0:
        args_submod = args[1:]
        ref1 = args[0]
    if len( args ) >= 2:
      errCode, sha = getSHAFromRef( args[0] )
      if errCode == 0:
        args_submod = args[1:]
        ref1 = args[0]
        errCode, sha = getSHAFromRef( args[1] )
        if errCode == 0:
          args_submod = args[2:]
          ref2 = args[1]

    if ref1 != "":
      errCode, sha = getSHAFromRef( ref1 )
      if errCode != 0:
        GLog.f( GLog.E, "Reference '%s' not existing into project %s." % ( ref1, map.getDir() ) )
        sys.exit( 1 )
    if ref2 != "":
      errCode, sha = getSHAFromRef( ref2 )
      if errCode != 0:
        GLog.f( GLog.E, "Reference '%s' not existing into project %s." % ( ref2, map.getDir() ) )
        sys.exit( 1 )

    if Status.pendingMerge( map.getDir() ):
      if ref1 != "HEAD" or ref2 != "":
        GLog.f( GLog.E, "Conflict is present, ignoring <ref1> and/or <ref2> arguments and showing merge differences." )
      ref1 = "HEAD"
      ref2 = "MERGE_HEAD"

    for rn in args_submod:
      rn = dir2reponame( rn )
      if rn not in alls:
        GLog.f( GLog.E, "ERROR: Not existing repository '%s' inside project %s" % ( rn, map.getDir() ) )
        sys.exit( 1 )
      if rn in snaps:
        GLog.f( GLog.E, "ERROR: repository '%s' is a snapshot repo, cannot present conflicts." % ( rn ) )
        sys.exit( 1 )
      if rn not in inits:
        GLog.f( GLog.E, "ERROR: repository '%s' it is not initialized." % ( rn ) )
        sys.exit( 1 )

    if len( args_submod ) == 0:
      args_submod = submod_list_initialized( map.getDir() )

    #print "ref1: ", ref1
    #print "ref2: ", ref2
    #print "args: ", args_submod

    for rn in args_submod:
      rn = dir2reponame( rn )
      smodref_1, errCode = submod_getrepover_atref( map.getDir(), rn, ref1 )
      if errCode != 0:
        GLog.f( GLog.E, smodref_1 )
        return 1
      if ref2 != "":
        smodref_2, errCode = submod_getrepover_atref( map.getDir(), rn, ref2 )
        if errCode != 0:
          GLog.f( GLog.E, smodref_2 )
          return 1
      else: #i.e. swgit proj -D HEAD
        smodref_2 = ""

      #if smodref_1 == smodref_2:
      #  continue

      for aref in (smodref_1, smodref_2):
        if aref != "":
          errCode, sha = getSHAFromRef( aref, "%s/%s" % (map.getDir(),rn) )
          if errCode != 0:
            strerr  = "Reference %s not existing into project %s.\n" % ( aref, map.getDir() )
            strerr += "In order to download any new commit, you could issue:\n"
            strerr += "  swgit submodule update -- %s" % rn
            GLog.f( GLog.E, strerr )
            return 1

      strbody = "repository  %s" % rn
      if ref2 == "MERGE_HEAD":
        str_tit1 = "HEAD:       "
        str_tit2 = "MERGE_HEAD: "
      else:
        str_tit1 = "REF1:       "
        str_tit2 = "REF2:       "
      str_smodref_2 = smodref_2
      if smodref_2 == "":
        str_smodref_2 = "working dir"

      print "%s\n%s\n%s%s\n%s%s\n%s" % ( "="*len(strbody), strbody, str_tit1, smodref_1, str_tit2, str_smodref_2, "="*len(strbody) )

      #cmd_submod_diff = "git --git-dir=%s/%s/.git diff %s %s" % ( map.getDir(), rn, smodref_1, smodref_2 )
      cmd_submod_diff = "cd %s/%s && git diff %s %s" % ( map.getDir(), rn, smodref_1, smodref_2 )
      out, errCode = myCommand( cmd_submod_diff )
      print out


  sys.exit( 0 )


def cs_desribe_ref( dir, ref ):
  #print "ref: %s" % ref
  retstr = ""
  for t in [ SWCFG_TAG_LIV, SWCFG_TAG_STB, "CST", SWCFG_TAG_DEV ]:
    cmd_describe_commit = "cd %s && git describe --tags --long %s --match \"*/*/*/*/*/*/*/%s/*\"" % ( dir, ref, t )
    #print "cmd: %s" % cmd_describe_commit
    lbl, errCode = myCommand_fast( cmd_describe_commit )
    if errCode == 0:
      retstr += "\n%s" % ( lbl[:-1] )

  return retstr



common_options = [
    [ 
      "--branch",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "proj_branch",
        "default" : "",
        "metavar" : "<src_repo_branch_name>",
        "help"    : "Project branch to be tracked"
        }
      ],
    [ 
      "--set-int-br",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "set_int_br",
        "default" : None,
        "metavar" : "<branch_name>",
        "help"    : "Set default integration branch. Repo will become a 'work-on-HEAD' repo in respect to this branch."
        }
      ],
    [ 
      "--unset-int-br",
      {
        "action"  : "store_true",
        "dest"    : "unset_int_br",
        "default" : False,
        "help"    : "Unset default integration branch. Repo will be no more a \"develop repository\", disable work-on-HEAD behaviour."
        }
      ],
    [ 
      "--snapshot",
      {
        "action"  : "store_true",
        "dest"    : "snap_repo",
        "default" : False,
        "help"    : "With --add-repo: add repository as \"snapshot repository\" to current-directory project. With --init/--update will init/update also all snapshot repositories."
        }
      ],
    ]



mod_options = [
    [ 
      "-a",
      "--add-repo",
      {
        "action"  : "store_true",
        "dest"    : "add_repo",
        "default" : False,
        "help"    : "Add repository to current-directory project"
        }
      ],
    [
      "-d",
      "--del-repo",
      {
        "action"  : "store_true",
        "dest"    : "del_repo",
        "default" : False,
        "help"    : "Delete repository from current-directory project"
        }
      ],
    [ 
      "-e",
      "--edit-repo",
      {
        "action"  : "store_true",
        "dest"    : "edit_repo",
        "default" : False,
        "help"    : "Edit default integration branch (--set-int-br, --unset-int-br)."
        }
      ]
    ]


init_options = [
    [ 
      "--init",
      {
        "action"  : "store_true",
        "dest"    : "init_repo",
        "default" : False,
        "help"    : "Initialize repository and clone it locally."
        }
      ],
    [ 
      "--un-init",
      {
        "action"  : "store_true",
        "dest"    : "uninit_repo",
        "default" : False,
        "help"    : "Remove local repository."
        }
      ],
    ]


move_options = [
    [ 
      "-u",
      "--update",
      {
        "action"  : "store_true",
        "dest"    : "update_repo",
        "default" : False,
        "help"    : "Pull all INT repositories, update all CST repositories"
        }
      ],
    [ 
      "-I",
      "--merge-from-int",
      {
        "action"  : "store_true",
        "dest"    : "update_repo_yesmerge",
        "default" : False,
        "help"    : "Pull all INT repositories and merge on side branch if necessary, update all CST repositories"
        }
      ],
    [ 
      "-N",
      "--no-merges",
      {
        "action"  : "store_true",
        "dest"    : "update_repo_nomerge",
        "default" : False,
        "help"    : "Treat INT repositories as CST ones. Just update content, no pull at all. (like plain git submodule)"
        }
      ],
    [ 
      "-r",
      "--reset",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "reset_ref",
        "default" : None,
        "metavar" : "<reference>",
        "help"    : "Checkout every repositories history according to project provided reference"
        }
      ],
#    [ 
#      "--freeze",
#      {
#        "action"  : "store_true",
#        "dest"    : "proj_freeze",
#        "default" : False,
#        "help"    : "Freeze project commits in all repositories in order to come back here"
#        }
#      ],
#    [ 
#      "-m",
#      "--message",
#      {
#        "nargs"   : 1,
#        "type"    : "string",
#        "action"  : "callback",
#        "callback": check_input,
#        "dest"    : "message",
#        "default" : None,
#        "metavar" : "<message>",
#        "help"    : "Add a message when freezeing project" 
#        }
#      ]
    ]


list_options = [
    [ 
      "-l",
      "--list",
      {
        "action"  : "store_true",
        "dest"    : "proj_list",
        "default" : False,
        "help"    : "Recusively print tree of repositories inside this project"
        }
      ],
    [ 
      "--list-all",
      {
        "action"  : "store_true",
        "dest"    : "proj_list_all",
        "default" : False,
        "help"    : "Recusively print tree of repositories inside this project, including un-initialized"
        }
      ],
    [
      "-C",
      "--get-configspec",
      {
        "action"  : "store_true",
        "dest"    : "get_cs",
        "default" : False,
        "help"    : "Given a proj commit (default HEAD), shows commit selected in any repository"
        }
      ],
    [
      "-D",
      "--diff",
      {
        "action"  : "store_true",
        "dest"    : "diff",
        "default" : False,
        "help"    : "Show repository diff between two commits."
        }
      ],
    [ 
      "--pretty",
      {
        "action"  : "store_true",
        "dest"    : "pretty",
        "default" : False,
        "help"    : "Only woth --get-configspec option, show more infos. Howeve its output is not suitable for using with swgit stabilize --src."
        }
      ],

    ]


debug_options = [
    [ 
      "--debug",
      {
        "action"  : "store_true",
        "dest"    : "debug",
        "default" : False,
        "help"    : 'print executed commands to stdout'
        }
      ]
    ]

proj_opt_allowed = [ "--quiet", "--verbose", "--debug" ]
proj_allowmap = {
      "--add-repo"        : proj_opt_allowed + [ "--branch", "--snapshot" ],
      "--del"             : proj_opt_allowed,
      "--edit"            : proj_opt_allowed + [ "--set-int-br", "--unset-int-br" ],
      "--reset"           : proj_opt_allowed,
      "--init"            : proj_opt_allowed + [ "--snapshot" ],
      "--un-init"         : proj_opt_allowed,
      "--update"          : proj_opt_allowed + [ "--snapshot", "--merge-from-int", "--no-merges" ],
      #"--freeze"          : proj_opt_allowed,
      "--list"            : proj_opt_allowed,
      "--list-all"        : proj_opt_allowed,
      "--diff"            : proj_opt_allowed,
      "--get-config-spec" : proj_opt_allowed + [  "--pretty" ],
      }




if __name__ == "__main__":
  main()

