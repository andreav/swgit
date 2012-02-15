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

import sys,os,stat,string,pwd,re

from Common import *
from MyCmd import *
from ObjStatus import * 
from ObjBranch import *
from ObjTag import *
from ObjMail import *
from ObjSnapshotRepo import *
from ObjLog import *
from Utils_Submod import *
import GitSsh

g_newrepo = False

def options_to_username( options ):
  if options.user_name != None:
    currUser = options.user_name
  else:
    currUser = Env.getCurrUser()

  return currUser

def eval_dev_br( options ):
  devname = "develop"
  if options.intbr_name != None:
    devname = options.intbr_name + "_develop"

  devBr = options.rel + "/" + options.user_name + "/INT/" + devname
  return devBr

def eval_stb_br( options ):
  stbname = "stable"
  if options.intbr_name != None:
    stbname = options.intbr_name + "_stable"

  stableBr = options.rel + "/" + options.user_name + "/INT/" + stbname
  return stableBr

def eval_cst_br( options ):
  cstBrName = options.rel + "/" + options.user_name + "/CST/" + options.intbr_name
  return cstBrName


def create_develop_and_hop( options ):
  #
  # DEVELOP
  #
  devBr = eval_dev_br( options )
  GLog.s( GLog.S, "\tCreating branch %s ..." % devBr )

  cmd_devBr = "git branch " + devBr
  out, errCode = myCommand( cmd_devBr )
  GLog.logRet( errCode, indent = "\t" )

  brStartLbl = "%s/%s/%s" % ( devBr, SWCFG_TAG_NEW, SWCFG_TAG_NEW_NAME )
  GLog.s( GLog.S, "\tCreating label %s" % brStartLbl )

  cmd = "git tag %s -f %s -m \"Created branch\"" % ( brStartLbl, devBr )
  out,errCode = myCommand( cmd )
  if errCode != 0:
    GLog.f( GLog.E, indentOutput( out[:-1], 2 ) )
    GLog.logRet( errCode, indent = '\t' )
    return 1
  GLog.logRet( errCode, indent = '\t' )

  GLog.s( GLog.S, "\tCheckout to just created develop branch %s ..." % devBr )
  cmd_chk = ( "git checkout %s" % devBr )
  out, errCode = myCommand( cmd_chk )
  GLog.logRet( errCode, indent = "\t" )
  return errCode


def create_stable( options ):
  #
  # STABLE
  #
  stableBr = eval_stb_br( options )
  GLog.s( GLog.S, "\tCreating branch %s ..." % stableBr )

  cmd_stableBr = "git branch " + stableBr 
  out, errCode = myCommand( cmd_stableBr )
  GLog.logRet( errCode, indent = "\t" )

  brStartLbl = "%s/%s/%s" % ( stableBr, SWCFG_TAG_NEW, SWCFG_TAG_NEW_NAME )
  GLog.s( GLog.S, "\tCreating label %s" % brStartLbl )

  cmd = "git tag %s -f %s -m \"Created branch\"" % ( brStartLbl, stableBr )
  out,errCode = myCommand( cmd )
  if errCode != 0:
    GLog.f( GLog.E, indentOutput( out[:-1], 2 ) )
    GLog.logRet( errCode, indent = '\t' )
    return 1
  GLog.logRet( errCode, indent = '\t' )
  return 0


def create_cst_branch_check( options ):

  if options.src == None:
    return "ERROR - When creating CST branch, src option is mandatory.", 1

  errCode, sha = getSHAFromRef( options.src )
  if errCode != 0:
    return "Please specify a valid source reference", 1

  if options.intbr_name == None:
    return "ERROR - When creating CST branch, -c/--create option is mandatory to provide branch name.", 1

  cstBrName = eval_cst_br( options )
  cstBr = Branch( cstBrName )
  if cstBr.isValid() == True:
    return "ERROR - branch %s already exists " % cstBrName, 1

  if options.drop != None:
    cstBrName = eval_cst_br( options )
    liv = "%s/LIV/%s" % ( cstBrName, options.drop )

    newTag = Tag( liv )
    if newTag.isValid():
      return "ERROR - tag %s already exists" % liv, 1

  return "", 0



def create_cst_branch_exec( options ):

  cstBrName = eval_cst_br( options )
  GLog.s( GLog.S, "\tCreating branch " + cstBrName + " in " + dumpRepoName("your local") + " repository init ..." )

  #already moved on right place
  #cmd_createBr = "git checkout -b %s %s" % ( cstBrName, options.src )
  cmd_createBr = "git checkout -b %s" % ( cstBrName )
  out, errCode = myCommand( cmd_createBr )
  if errCode != 0:
    GLog.f( GLog.E, "\tERROR: creating branch %s starting from reference %s" % ( cstBrName, options.src ) )
    GLog.logRet( errCode, indent = '\t' )
    return 1
  GLog.logRet( errCode, indent = '\t' )

  brStartLbl = "%s/%s/%s" % ( cstBrName, SWCFG_TAG_NEW, SWCFG_TAG_NEW_NAME )
  GLog.s( GLog.S, "\tCreating label %s" % brStartLbl )

  cmd = "git tag %s -f %s -m \"Created branch\"" % ( brStartLbl, cstBrName )
  out,errCode = myCommand( cmd )
  if errCode != 0:
    GLog.f( GLog.E, "\tERROR: creating starting tag %s" % ( brStartLbl ) )
    GLog.logRet( errCode, indent = '\t' )
    return 1
  GLog.logRet( errCode, indent = '\t' )

  #
  # if you ARE a project, set .gitattributes
  if os.path.exists( "./%s" % SWFILE_PROJMAP ) == True:

    dotgitattributes = "./.gitattributes"
    cmd_grep_swdefbr = "grep -e \"^%s\" %s" % ( SWFILE_DEFBR, dotgitattributes )
    out, errCode = myCommand_fast( cmd_grep_swdefbr )
    if errCode != 0:
      GLog.s( GLog.S, "\tEditing .gitattributes" )
      file = open( dotgitattributes, 'a' )
      file.write( "%s merge=merge_swdefbr\n" % SWFILE_DEFBR )
      file.close()

      cmd_add_commit = "git add %s" % dotgitattributes
      out, errCode = myCommand( cmd_add_commit )
      if errCode != 0:
        GLog.logRet( errCode, indent = '\t' )
        return 1
      GLog.logRet( errCode, indent = '\t' )


  #
  # if you are INSIDE a project, clean .swdefaultbr inherithed from src
  swdefbr_fileName = "./%s" % SWFILE_DEFBR
  if os.path.exists( swdefbr_fileName ) == True:

    GLog.s( GLog.S, "\tCreating empty default integration branch file into current project. " )

    cmd_add_commit = "echo \"\" > %s && git add %s" % ( swdefbr_fileName, swdefbr_fileName )
    out, errCode = myCommand( cmd_add_commit )
    if errCode != 0:
      GLog.f( GLog.E, out )
      GLog.logRet( errCode, indent = '\t' )
      return 1

    GLog.logRet( errCode, indent = '\t' )

  GLog.s( GLog.S, "\tAdding all and committing" )
  cmd_add_commit = "git add .; git commit -m \"Created CST branch %s\" --allow-empty" %  cstBrName
  out, errCode = myCommand( cmd_add_commit )
  GLog.s( GLog.S, "\tDONE" )

    #swdefbr_file = open( swdefbr_fileName, 'r' )
    #lines = swdefbr_file.read()
    #swdefbr_file.close()

    #swdefbr_file = open( swdefbr_fileName, 'w' )
    #newcontent = ""
    #for line in lines.splitlines():

    #  locdir, intbr = line.split( ':' )
    #  if locdir != repo_locdir:
    #    newcontent += line
    #    continue

    #  newcontent += "%s:%s\n" % ( locdir, cstBrName )

    #swdefbr_file.write( newcontent )
    #swdefbr_file.close()

  #  GLog.logRet(0)

  if options.drop != None:

    fullTagName = cstBrName + "/LIV/" + options.drop
    GLog.s( GLog.S, "\tCreating label %s ..." % fullTagName )
    cmd_create_tag = "git tag " + fullTagName + "  -m \" " + fullTagName + " \" " 
    out, errCode = myCommand( cmd_create_tag )
    GLog.logRet( errCode, indent = "\t" )


  return 0




def main():
  usagestr =  """\
Usage: swgit init -r <x.y.z.t> [-u <user>] [-l <label>] [-c <int-br-name>] 
   or: swgit init -r <x.y.z.t> [-u <user>] [-l <label>] --src <startpoint> [-c <int-br-name>]
   or: swgit init -r <x.y.z.t> [-u <user>] [-l <label>] --cst -c <int-br-name> --src <startpoint>"""

  parser       = OptionParser( usage = usagestr,
                               description='>>>>>>>>>>>>>> swgit - Init repository <<<<<<<<<<<<<<' )
  mgt_group    = OptionGroup( parser, "Management options" )
  output_group = OptionGroup( parser, "Output options" )
  load_command_options( mgt_group, init_mgt_options )
  load_command_options( output_group, arr_output_options )
  parser.add_option_group( mgt_group )
  parser.add_option_group( output_group )
    
  (options, args)  = parser.parse_args()
  help_mac( parser )

  if len(args) != 0:
    parser.error("Too many arguments")

  root         = os.getcwd()
  dotgit       = "%s/%s" % (root  , SWDOTGIT)
  global g_newrepo
  if not os.path.exists( dotgit ):
    g_newrepo  = True

  #release
  if options.rel == None :
    print "ERROR - Please specify a release parameter"
    sys.exit( 1 )

#  if g_newrepo and options.cst:
#    strerr  = "ERROR: Cannot create CST branch without first creating a swgit repository."
#    strerr += "       Please split this action in two phases: init and then create cst branch"
#    print strerr
#    sys.exit( 1 )
#


  rel, ret = check_release( options.rel )
  if ret != 0:
    print rel
    sys.exit( ret )
  options.rel = rel

  #username
  if options.user_name != None:
    strerr, err = check_username( options.user_name )
    if err != 0:
      strerr  = "ERROR - Please specify a valid user name (matching this regexp '%s')\n" % SWCFG_USER_REGEXP
      strerr += "        Otherwise suppress this option and user.name config value will be used."
      print strerr
      sys.exit( 1 )
  options.user_name = options_to_username( options )

  #liv
  if options.drop != None : 
    livDsc = create_tag_dsc( SWCFG_TAG_LIV )
    if not livDsc.check_valid_value( options.drop ):
      strerr  = "ERROR - In order to create a starting LIV label,\n"
      strerr += "        please enter -l argument respecting '%s' regular expression\n" % livDsc.get_regexp()
      strerr += "        If you don't like this regexp, you can overwrite it.\n"
      strerr += "        Try 'swgit tag --custom-tag-show-cfg LIV' to investigate."
      print strerr
      sys.exit( 1 )

  if options.intbr_name != None:
    strerr, err = check_brname( options.intbr_name )
    if err != 0:
      print "ERROR - " + strerr
      sys.exit( 1 )

  # convert git native repos
  # 
  #if not g_newrepo and options.src == None:
  #   print "\tERROR: \n\tThe directory " + root + " already is a GIT repository.\n\tFound .git dir"
  #   sys.exit( 1 )


  if not g_newrepo:

    # dirty WD 
    err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
    if err != 0:
      print errstr
      sys.exit( 1 )

    # valid src
    if options.src != None:
      errCode, sha = getSHAFromRef( options.src )
      if errCode != 0:
        print "Please specify a valid source reference"
        sys.exit( 1 )


    # valid branch name
    intname = ""
    if options.intbr_name != None:
      strerr, err = check_brname( options.intbr_name )
      if err != 0:
        print strerr
        sys.exit( 1 )
      intname = options.intbr_name + "_"

    if not options.cst:

      #validate INT
      baseInt = "%s/%s/%s/%s" % ( options.rel, options.user_name, SWCFG_BR_INT, intname )
      intBr = ["develop","stable"]
      for br in intBr:
        newBrName = baseInt + br
        newBr = Branch( newBrName )

        if newBr.isValid() == True:
          print "ERROR - branch %s already exists" % newBrName
          sys.exit( 1 )

      # valid label name
      if options.drop != None:
        liv = "%sstable/LIV/%s" % ( baseInt, options.drop )

        newTag = Tag( liv )
        if newTag.isValid():
          print "ERROR - tag %s already exists" % liv
          sys.exit( 1 )


  #validate cst
  if options.cst:
    strerr, err = create_cst_branch_check( options )
    if err != 0:
      print strerr
      sys.exit( 1 )

 
  #
  # create git repo
  #################

  if g_newrepo:

    print "Initializing new git repository ..."

    opt_shared = ""
    if options.shared != None:
      opt_shared = "--shared=%s" % options.shared

    cmd_init = "git init %s " % ( opt_shared)
    out, errCode = myCommand_fast( cmd_init )
    if errCode != 0:
      print out
      print "FAILED"
      sys.exit( 1 )

    print "DONE"

  set_repo_cfg( GITCFG_USERNAME, options.user_name )

  #
  # crete swgit repo (or migrate to it if some parts already exists)
  ##################


  dotgitignore   = "%s/%s"   % (root, SWFILE_DOTGITIGNORE)
  swgitdir       = "%s/%s"   % (root, SWREPODIR)
  cfgdir         = "%s/%s"   % (root, SWDIR_CFG)
  logdir         = "%s/%s"   % (root, SWDIR_LOG)
  logplaceholder = "%s/%s"   % (root, SWFILE_LOGPLACEHOLDER )
  changelogdir   = "%s/%s%s" % (root, SWDIR_CHANGELOG, options.rel )
  chglogplaceholder   = "%s/%s" % (changelogdir, SWFILE_PLACEHOLDER )
  add_and_commit = False

  # create minimum direcotries to allow initializing logs
  if os.path.exists( swgitdir ) == False:
    cmd_create_dir = "mkdir %s" % swgitdir
    out, errCode = myCommand_fast( cmd_create_dir )
  if os.path.exists( logdir ) == False:
    cmd_create_dir = "mkdir %s" % logdir
    out, errCode = myCommand_fast( cmd_create_dir )

  #now can initialize logs!
  GLog.initGitLogs( options )
  GLog.s( GLog.I, " ".join( sys.argv ) )

  #
  # Manage src
  #  before making any modif
  #
  if options.src != None:
    GLog.s( GLog.S, "Checkout to starting reference %s ..." % options.src )
    cmd_chk = ( "git checkout %s" % ( sha ) )
    out, errCode = myCommand( cmd_chk  )
    if errCode != 0:
      GLog.logRet(1)
    GLog.logRet(0)


  GLog.s( GLog.S, "Initializing swgit repository ..." )

  # log directory
  if os.path.exists( logplaceholder ) == False:

    GLog.s( GLog.S, "\tCreating dir  %s" % logdir )
    cmd_log = "touch %s && git add %s" % ( logplaceholder, logplaceholder )
    out, errCode = myCommand( cmd_log )
    add_and_commit = True

  # changelog
  if os.path.exists( changelogdir ) == False:

    GLog.s( GLog.S, "\tCreating dir  %s" % changelogdir )
    cmd_chglog = "mkdir -p %s && touch %s && git add %s" % ( changelogdir, chglogplaceholder, chglogplaceholder )
    out, errCode = myCommand( cmd_chglog )
    add_and_commit = True


  # cfg directory
  if not os.path.exists( cfgdir ):
    GLog.s( GLog.S, "\tCreating dir  %s" % cfgdir )
    os.mkdir( cfgdir )
    add_and_commit = True

  # generic cfg
  genericcfg_file = "%s/%s" % (root, SWFILE_GENERICCFG)
  if os.path.exists( genericcfg_file ) == False:
    GLog.s( GLog.S, "\tCreating file %s" % genericcfg_file )
    file = open( genericcfg_file, 'w+' )
    file.write( GitSsh.DEFAULT_SSH_CFG )
    file.close()
    add_and_commit = True

  # custom tags
  custom_tags_file = "%s/%s" % (root, SWFILE_TAGDESC)
  if os.path.exists( custom_tags_file ) == False:
    GLog.s( GLog.S, "\tCreating file %s" % custom_tags_file )
    file = open( custom_tags_file, 'w+' )
    file.write( TagDsc.DEFAULT_CUSTOMTAG_CFG )
    file.close()
    add_and_commit = True

  # mail cfg
  mail_file = "%s/%s" % (root, SWFILE_MAILCFG)
  if os.path.exists( mail_file ) == False:
    GLog.s( GLog.S, "\tCreating file %s" % mail_file )
    file = open( mail_file, 'w+' )
    file.write( ObjMailBase.DEFAULT_MAIL_CFG )
    file.close()
    add_and_commit = True

  # snapshot cfg
  snapcfg_file = "%s/%s" % (root, SWFILE_SNAPCFG)
  if os.path.exists( snapcfg_file ) == False:
    GLog.s( GLog.S, "\tCreating file %s" % snapcfg_file )
    file = open( snapcfg_file, 'w+' )
    file.write( ObjSnapshotRepo.DEFAULT_SNAPSHOT_CFG )
    file.close()
    add_and_commit = True

  # .gitignore
  if os.path.exists( dotgitignore ) == False:
    GLog.s( GLog.S, "\tCreating file %s" % dotgitignore )
    file = open( dotgitignore, 'w' )
    file.write('')
    file.close()
    add_and_commit = True

  ignore_file = open( dotgitignore, 'r' )
  gitignore_cont = ignore_file.read()
  ignore_files = [ "%s*" % SWDIR_LOG, "!%s.placeholder" % SWDIR_LOG,
    "*~", "*.swp", "*.pyc", "!.gitattributes" ]

  for ign in ignore_files:
    if gitignore_cont.find( "%s\n" % ign ) == -1:
      GLog.s( GLog.S, "\tIgnoring %s" % ign )
      cmd_ignore = "echo \'%s\' >> .gitignore" % ign
      out, errCode = myCommand( cmd_ignore )
      add_and_commit = True
  ignore_file.close()

  ## locks directory
  #lock_dir         = "%s"  % SWDIR_LOCK
  #lock_placeholder = "%s.placeholder" % (lock_dir)
  #if not os.path.exists( lock_dir ):
  #  GLog.s( GLog.S, "\tCreating %s directory" % lock_dir )
  #  cmd_log = "mkdir -p %s && touch %s && git add -f %s" % ( lock_dir, lock_placeholder, lock_placeholder )
  #  out, errCode = myCommand_fast( cmd_log )

  ## .gitattributegitattributes
  #GLog.s( GLog.S, "\tEditing .gitattributes" )
  #file = open( dotgitattributes, 'w+' )
  ##file.write( "%s merge=ours" % SWFILE_DEFBR )
  #file.write( ".gitattributes merge=ours\n" )
  #file.close()



  #
  # Manage cst
  ############
  if options.cst == True:
    GLog.logRet(0)

    GLog.s( GLog.S, "Initializing %s branch ..." % SWCFG_BR_CST )

    ret = create_cst_branch_exec( options )
    if ret != 0:
      GLog.logRet(1)
      sys.exit( 1 )

    GLog.logRet(0)
    strerr= "\nPLEASE VERIFY EVERYTHING IS OK, THEN:\n"
    strerr += "       If you are on your origin repository, that's all.\n"
    strerr += "       If you are on a clone, push it on origin with 'swgit push'"
    GLog.s( GLog.S, strerr )
    sys.exit( 0 )


  #
  # Commit
  #
  GLog.s( GLog.S, "\tAdding all and committing" )
  cmd_add_commit = "git add .; git commit -m \"created INT branch %s\" --allow-empty" % eval_dev_br( options )
  out, errCode = myCommand( cmd_add_commit )
  GLog.s( GLog.S, "\tDONE" )
  GLog.logRet(0)


  #
  # Manage rel
  ############
  GLog.s( GLog.S, "Initializing %s branches ..." % SWCFG_BR_INT )

  create_develop_and_hop( options )

  if g_newrepo:
    GLog.s( GLog.S, "\tDeleting branch master" )
    cmd_del_master = "git branch -d master"
    out, errCode = myCommand( cmd_del_master )
    GLog.s( GLog.S, "\tDONE" )

  create_stable( options )

  if options.drop != None:

    fullTagName = eval_dev_br( options ) + "/STB/" + options.drop
    GLog.s( GLog.S, "\tCreating label %s ..." % fullTagName )
    cmd_create_tag = "git tag " + fullTagName + "  -m \" " + fullTagName + " \" " 
    out, errCode = myCommand( cmd_create_tag )
    GLog.logRet( errCode, indent = "\t" )

    fullStbTagName = eval_stb_br( options ) + "/STB/" + options.drop
    GLog.s( GLog.S, "\tCreating label %s ..." % fullStbTagName )
    cmd_create_tag = "git tag " + fullStbTagName + "  -m \" " + fullStbTagName + " \" " 
    out, errCode = myCommand( cmd_create_tag )
    GLog.logRet( errCode, indent = "\t" )

    fullLivTagName = eval_stb_br( options ) + "/LIV/" + options.drop
    GLog.s( GLog.S, "\tCreating label %s ..." % fullLivTagName )
    cmd_create_tag = "git tag " + fullLivTagName + "  -m \" " + fullLivTagName + " \" " 
    out, errCode = myCommand( cmd_create_tag )
    GLog.logRet( errCode, indent = "\t" )

    GLog.s( GLog.S, "\tCheckout to just created label %s ... " % fullLivTagName )
    cmd_chk = ( "%s branch -s %s" % (SWGIT, fullLivTagName) )
    out, errCode = myCommand( cmd_chk )
    GLog.logRet( errCode, indent = "\t" )


  GLog.logRet(0)

  strerr= "\nPLEASE VERIFY EVERYTHING IS OK, THEN:\n"
  strerr += "       If you are on your origin repository, that's all.\n"
  strerr += "       If you are on a clone, push it on origin with:\n"
  strerr += "         swgit branch -s %s\n" % eval_dev_br( options )
  strerr += "         or\n"
  strerr += "         swgit branch -s %s\n" % eval_stb_br( options )
  strerr += "         and\n"
  strerr += "         swgit push"
  GLog.s( GLog.S, strerr )

  sys.exit( 0 )



init_mgt_options = [
    [
      "-r",
      "--release",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "rel",
        "metavar" : "<release_val>",
        "help"    : 'Specify release for develop/stable/cst branch. Format: \"X.Y.Z.T\"'
        }
      ],
    [ 
      "-u",
      "--git-user",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "user_name",
        "default" : None,
        "metavar" : "<user_val>",
        "help"    : "Specifying this option will create INT or CST branches with provided user. Remeber: this user is different from ssh user specified in swgit clone (always $USER)"
        }
      ],
    [ 
      "-c",
      "--create",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "intbr_name",
        "metavar" : "<INT_branch_name>",
        "help"    : "Create INT develop/stable branches specifying their name (default is INT/develop and INT/stable)",
        }
      ],
    [ 
      "-l",
      "--liv-label",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "drop",
        "metavar" : "<label_name>",
        "help"    : "Create initial LIV tags after creating develop/stable. Must match default regexp '%s' or customized version (see 'swgit tag --custom-tag-show-cfg LIV' )" % SWCFG_TAG_LIVREGEXP
        }
      ],
    [ 
        "--src",
        "--source-reference",
        {
          "nargs"   : 1,
          "type"    : "string",
          "action"  : "callback",
          "callback": check_input,
          "dest"    : "src",
          "metavar" : "<reference>",
          "help"    : "Create develop/stable or cst starting from an existing reference."
          }
        ],
    [ 
        "--cst",
        "--cst-branch",
        {
          "action"  : "store_true",
          "dest"    : "cst",
          "default" : False,
          "help"    : "Instead of creating INT branches, create CST branches."
          }
        ],
    [ 
        "--shared",
        {
          "nargs"   : 1,
          "type"    : "string",
          "action"  : "callback",
          "callback": check_input,
          "dest"    : "shared",
          "metavar" : "<shared_mode>",
          "help"    : "Specify that the git repository is to be shared among several users, see git init --help"
          }
        ],
    ]




if __name__ == "__main__":
  main()


