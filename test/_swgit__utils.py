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

import shutil
from pprint import pprint
from string import Template

from _utils import *


#########################################################
#
# xzGIT tools
#
#########################################################
class swgit__utils:
  ALL_BRSELECTORS_STAR = "--all-releases --local-remote"
  ALL_BRSELECTORS_STAR_BUTUSER = "--all-releases"


  def __init__( self, repodir ):
    self.repodir_ = repodir
    self.projmap_ = os.path.abspath( repodir + "/" + PROJMAP )

  def getDir( self ):
    return self.repodir_

  def get_currsha( self, ref="HEAD" ):
    cmd = "cd %s && git rev-parse --quiet --verify %s^{}" % ( self.repodir_, ref )
    return myCommand( cmd )

  def is_file_under_cc( self, filename ):
    cmd = "cd %s && git cat-file -t HEAD:%s" % ( self.repodir_, filename )
    return myCommand( cmd )

  def get_cfg( self, key, fglobal = False ):
    return get_cfg( key, self.repodir_, fglobal )
  def set_cfg( self, key, value ):
    return set_cfg( key, value, self.repodir_ )

  def ref2sha( self, ref ):
    cmd = "cd %s; git rev-list -1 %s" % (self.repodir_, ref )
    return myCommand( cmd )


  #plain command as test wants
  def system_swgit( self, subcommad ):
    cmd = "cd %s && %s %s" % ( self.repodir_, SWGIT, subcommad )
    return myCommand( cmd )

  def system_unix( self, cmd ):
    cmd = "cd %s && %s" % ( self.repodir_, cmd )
    return myCommand( cmd )

  #
  # Init
  #
  @staticmethod
  def init_dir( dir, r = TEST_REPO_R, s = TEST_REPO_S, l = TEST_REPO_LIV, u = ORIG_REPO_GITUSER, c = "", cst = False, src = "" ):
    str_liv_opt = ""
    if l != "":
      str_liv_opt = " -l %s " % l

    str_c_opt = ""
    if c != "":
      str_c_opt = " -c %s " % c

    str_cst_opt = ""
    if cst == True:
      str_cst_opt = " --cst "

    str_src_opt = ""
    if src != "":
      str_src_opt = " --src %s " % src

    cmd = "cd %s && %s init -r %s/%s %s --git-user %s %s %s %s" % ( dir, SWGIT, r, s, str_liv_opt, u, str_c_opt, str_cst_opt, str_src_opt )
    return myCommand( cmd )

  @staticmethod
  def create_repo( dir ):
    out, retcode = create_dir_some_file( dir )
    if retcode != 0:
      return out, errCode

    out, errCode = swgit__utils.init_dir( dir )
    if retcode != 0:
      return out, errCode

    return "Repo created!", 0

  def modify_file( self, filename = "", msg = "some content" ):
    return echo_on_file( self.repodir_ + "/" +filename, msg )

  def modify_repo( self, filename = "", msg = "", gotoint = True ):

    if gotoint == True:
      #1. go on develop
      out, retcode = self.branch_switch_to_int()
      if retcode != 0:
        return out, retcode

    #2. edit
    if filename != "":
      out, retcode = echo_on_file( self.repodir_ + "/" + filename, msg )
      if retcode != 0:
        return out, retcode

    #3. commit
    comment = "modified repo file <%s>" % filename
    if msg != "":
      comment = msg
    cmd_commit = "cd %s && git commit -a -m \"%s\" --allow-empty" % ( self.repodir_, msg )
    out, retcode = myCommand( cmd_commit )
    if retcode != 0:
      return out, retcode

    return "OK",0


  #
  # Clone
  #
  @staticmethod
  def clone_scripts_repo( dst ):
    #print "rm %s" % dst
    orig_bkp  = TEST_ORIG_REPO + ".BKP"
    clone     = TEST_ORIG_REPO + "_CLONE"
    clone_bkp = clone          + ".BKP"
    aremote     = TEST_ORIG_REPO + AREMOTE_PATH + ".PARK"
    aremote_bkp = aremote        + ".BKP"
    aremote_dst = TEST_ORIG_REPO + AREMOTE_PATH

    shutil.rmtree( TEST_ORIG_REPO, True ) #ignore errors
    shutil.rmtree( clone, True ) #ignore errors
    shutil.rmtree( dst, True ) #ignore errors
    shutil.rmtree( aremote_dst, True ) #ignore errors

    #
    # PROTOREPO
    #
    if os.path.exists( orig_bkp ) == False:
      #orig first time
      create_protorepo()
      shutil.copytree( TEST_ORIG_REPO, orig_bkp )
    else:
      shutil.copytree( orig_bkp, TEST_ORIG_REPO )

    #
    # PROTOREPO_AREMOTE
    #
    if os.path.exists( aremote_bkp ) == False:
      # clone first time
      cmd = "%s clone -r %s %s -b %s " % ( SWGIT, ORIG_REPO_URL, aremote, ORIG_REPO_DEVEL_BRANCH )
      out, retcode = myCommand( cmd )
      if retcode != 0:
        return out, retcode

      #lcoalize taht branch (so when adding this repo as remote, i will have a remote branch more)
      cmd = "cd %s && %s branch -s %s" % ( aremote, SWGIT, ORIG_REPO_aBRANCH )
      out, retcode = myCommand( cmd )
      if retcode != 0:
        return out, retcode

      shutil.copytree( aremote, aremote_bkp )
      shutil.copytree( aremote_bkp, aremote_dst )
    else:
      shutil.copytree( aremote_bkp, aremote_dst )

    #
    # PROTOREPO_CLONE
    #
    if os.path.exists( clone_bkp ) == False:
      # clone first time
      cmd = "%s clone %s %s -b %s " % ( SWGIT, ORIG_REPO_URL, clone, ORIG_REPO_DEVEL_BRANCH )
      out, retcode = myCommand( cmd )
      if retcode != 0:
        return out, retcode

      if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
        print "\n%s\nMOREREMOTES\n%s\n" % ( "="*20, "="*20 )
        helper = swgit__utils( clone )
        out, errCode = helper.remote_add( ORIG_REPO_AREMOTE_NAME, ORIG_REPO_AREMOTE_URL )
        out, errCode = helper.pull()

      shutil.copytree( clone, clone_bkp )
      shutil.copytree( clone_bkp, dst )
    else:
      shutil.copytree( clone_bkp, dst )



    return "OK", 0

  

  @staticmethod
  def clone_scripts_repo_integrator( dst, append="" ):
    #cmd = "%s clone -r %s %s --integrator -b %s %s" % ( SWGIT, ORIG_REPO_URL, dst, ORIG_REPO_DEVEL_BRANCH, append )
    cmd = "%s clone -r %s %s --integrator %s" % ( SWGIT, ORIG_REPO_URL, dst, append )
    return myCommand( cmd )

  @staticmethod
  def clone_repo( src, dst, br="", user="", addr="" ):
    if user=="":
      user = TEST_USER_SSH
    if addr=="":
      addr = TEST_ADDR
    if br=="":
      br=TEST_REPO_BR_DEV

    if os.environ.get( SWENV_TESTMODE ) == SWENV_LOCALREPOS:
      cmd = "%s clone -r %s %s -b %s" % ( SWGIT, src, dst, br )
    else:
      cmd = "%s clone -r ssh://%s@%s%s %s -b %s" % ( SWGIT, user, addr, src, dst, br )

    out, retcode = myCommand( cmd )
    return out, retcode

  @staticmethod
  def clone_repo_integrator( src, dst, br="", user="", addr="" ):
    if user=="":
      user = TEST_USER_SSH
    if addr=="":
      addr = TEST_ADDR
    if br=="":
      br=TEST_REPO_BR_DEV

    if os.environ.get( SWENV_TESTMODE ) == SWENV_LOCALREPOS:
      cmd = "%s clone --integrator -r %s %s -b %s" % ( SWGIT, src, dst, br )
    else:
      cmd = "%s clone --integrator -r ssh://%s@%s%s %s -b %s" % ( SWGIT, user, addr, src, dst, br )

    out, retcode = myCommand( cmd )
    return out, retcode


  @staticmethod
  def clone_repo_url( url, dst, br, opt = "" ):
    cmd = "%s clone -r %s %s -b %s %s" % ( SWGIT, url, dst, br, opt )
    out, retcode = myCommand( cmd )
    return out, retcode
  @staticmethod
  def clone_repo_url_norec( url, dst, br, opt = "" ):
    cmd = "%s clone %s %s -b %s %s" % ( SWGIT, url, dst, br, opt )
    out, retcode = myCommand( cmd )
    return out, retcode

  @staticmethod
  def clone_repo_url_integrator( url, dst, br ):
    return swgit__utils.clone_repo_url( url, dst, br, opt = " --integrator " )


  @staticmethod
  def clone_repo_integrator( src, dst, user="", addr="" ):
    if user=="":
      user = TEST_USER_SSH
    if addr=="":
      addr = TEST_ADDR

    if os.environ.get( SWENV_TESTMODE ) == SWENV_LOCALREPOS:
      cmd = "%s clone -r %s  %s --integrator -b %s" % ( SWGIT, src, dst, TEST_REPO_BR_DEV )
    else:
      cmd = "%s clone -r ssh://%s@%s%s  %s --integrator -b %s" % ( SWGIT, user, addr,src, dst, TEST_REPO_BR_DEV )
    return myCommand( cmd )


  #
  # Branches
  #
  @staticmethod
  def int_branch_get_dst( dst, all = "" ):
    cmd = "cd %s && %s branch --get-integration-br %s" % ( dst, SWGIT, all )
    out, retcode = myCommand( cmd )
    if retcode != 0:
      return out, retcode
    # out like this: refs/heads/2/2/2/2/vallea/INT/develop
    out = out[ out.find('/') +1 : ]
    out = out[ out.find('/') +1 : ]
    return out, 0

  def int_branch_get( self, all = "" ):
    return swgit__utils.int_branch_get_dst( self.repodir_, all )

  @staticmethod
  def int_branch_set_dst( dst, ib, all = "" ):
    cmd = "cd %s && %s branch --set-integration-br %s %s" % ( dst, SWGIT, ib, all )
    return myCommand( cmd )

  def int_branch_set( self, ib, all = "" ):
    return swgit__utils.int_branch_set_dst( self.repodir_, ib, all )

  @staticmethod
  def current_branch_dst( dst, all=""):
    cmd = "cd %s && SWNOINTERACTIVE=TRUE %s branch --current-branch %s " % ( dst, SWGIT, all)
    return myCommand( cmd )

  def current_branch( self , all=""):
    return swgit__utils.current_branch_dst( self.repodir_, all )

  def all_branches( self , all="" ):
    cmd = "cd %s && %s branch %s %s " % ( self.repodir_, SWGIT, self.ALL_BRSELECTORS_STAR, all ) 
    return myCommand( cmd )

  def local_branches( self , all="" ):
    cmd = "cd %s && %s branch --all-releases %s " % ( self.repodir_, SWGIT, all )
    return myCommand( cmd )

  def remote_branches( self, all="" ):
    cmd = "cd %s && %s branch --all-releases --remote %s" % ( self.repodir_, SWGIT, all )
    return myCommand( cmd )

  def local_branches_byuser( self, user, all="" ):
    cmd = "cd %s && %s branch %s -U %s %s" % ( self.repodir_, SWGIT, self.ALL_BRSELECTORS_STAR_BUTUSER, user, all )
    return myCommand( cmd )

  def branch_create( self, name, all="" ):
    cmd = "cd %s && %s branch -c %s %s" % ( self.repodir_, SWGIT, name, all )
    return myCommand( cmd )

  def branch_create_src( self, name, src, all = ""  ):
    cmd = "cd %s && %s branch -c %s --src %s %s" % ( self.repodir_, SWGIT, name, src, all )
    return myCommand( cmd )

  def branch_switch_to_int( self, all="" ):
    cmd = "cd %s && %s branch -i %s" % ( self.repodir_, SWGIT, all )
    return myCommand( cmd )

  def branch_switch_to_br( self, tobr, all="" ):
    cmd = "cd %s && %s branch -s %s %s" % ( self.repodir_, SWGIT, tobr, all )
    return myCommand( cmd )

  def branch_switch_back( self, all="" ):
    cmd = "cd %s && %s branch -S %s" % ( self.repodir_, SWGIT, all )
    return myCommand( cmd )

  def branch_delete_d( self, tbdbr, all="" ):
    cmd = "cd %s && %s branch -d %s %s" % ( self.repodir_, SWGIT, tbdbr, all )
    return myCommand( cmd )

  def branch_delete_D( self, tbdbr, all="" ):
    cmd = "cd %s && %s branch -D %s %s" % ( self.repodir_, SWGIT, tbdbr, all )
    return myCommand( cmd )

  def branch_delete_e( self, tbdbr, all="" ):
    cmd = "cd %s && %s branch -e %s %s" % ( self.repodir_, SWGIT, tbdbr, all )
    return myCommand( cmd )

  def branch_delete_E( self, tbdbr, all="" ):
    cmd = "cd %s && %s branch -E %s %s" % ( self.repodir_, SWGIT, tbdbr, all )
    return myCommand( cmd )

  def branch_move_m( self, newbr ):
    cmd = "cd %s && %s branch -m %s " % ( self.repodir_, SWGIT, newbr )
    return myCommand( cmd )

  def branch_move_M( self, newbr ):
    cmd = "cd %s && %s branch -M %s " % ( self.repodir_, SWGIT, newbr )
    return myCommand( cmd )


  def branch_track( self, br, all="" ):
    cmd = "cd %s && %s branch --track %s %s" % ( self.repodir_, SWGIT, br, all )
    return myCommand( cmd )

  def branch_list_track( self, track = False ):
    cmd = "cd %s && %s branch --list-tracked" % ( self.repodir_, SWGIT )
    return myCommand( cmd )


  #
  # Commit
  #
  def commit( self, msg="default commit message", all="" ):
    cmd = "cd %s && %s commit -m \"%s\" %s" % ( self.repodir_, SWGIT, msg, all )
    return myCommand( cmd )

  def commit_repolist( self, repolist, msg="default commit message" ):
    cmd = "cd %s && %s commit -m \"%s\" %s" % ( self.repodir_, SWGIT, msg, repolist )
    return myCommand( cmd )

  def commit_dev_repolist( self, repolist, msg="default commit message", all = "" ): 
    cmd = "cd %s && %s commit -m \"%s\" %s --dev %s" % ( self.repodir_, SWGIT, msg, repolist, all )
    return myCommand( cmd )

  def commit_minusA( self, msg="default commit message", all="" ):
    cmd = "cd %s && %s commit -a -m \"%s\" %s " % ( self.repodir_, SWGIT, msg, all )
    return myCommand( cmd )

  def commit_minusA_repolist( self, msg="default commit message", all="", repolist = "" ):
    cmd = "cd %s && %s commit -a -m \"%s\" %s %s" % ( self.repodir_, SWGIT, msg, all, repolist )
    return myCommand( cmd )

  def commit_minusA_dev_repolist( self, msg="default commit message", all="", repolist = "" ):
    cmd = "cd %s && %s commit -a --dev -m \"%s\" %s %s" % ( self.repodir_, SWGIT, msg, all, repolist )
    return myCommand( cmd )

  @staticmethod
  def commit_dst_minusA_dev( dir, msg="default commit message", all="" ):
    cmd = "cd %s && %s commit -a -m \"%s\" --dev %s " % ( dir, SWGIT, msg, all )
    return myCommand( cmd )

  def commit_minusA_dev( self, msg="default commit message", all="" ):
    return swgit__utils.commit_dst_minusA_dev( self.repodir_, msg, all )

  def commit_minusA_fix( self, ddts, msg="default commit message", all="" ):
    cmd = "cd %s && %s commit -a -m \"%s\" --fix %s %s" % ( self.repodir_, SWGIT, msg, ddts, all )
    return myCommand( cmd )

  def commit_minusA_dev_fix( self, ddts, msg="default commit message", all="" ):
    cmd = "cd %s && %s commit -a -m \"%s\" --dev --fix %s %s" % ( self.repodir_, SWGIT, msg, ddts, all )
    return myCommand( cmd )

  def add( self, file, path="" ):
    if path=="":
      path = self.repodir_
    cmd = "cd %s && %s add %s" % ( path, SWGIT, file )
    return myCommand( cmd )


  #
  # Tag
  #
  customtag_template = Template("""
[$tagtype]
regexp                  = $regexp
push-on-origin          = $push_on_origin
one-x-commit            = $one_x_commit
only-on-integrator-repo = $only_on_integrator_repo
allowed-brtypes         = $allowed_brtypes
denied-brtypes          = $denied_brtypes
tag-in-past             = $tag_in_past
hook-pretag-script      = $hook_pretag_script
hook-pretag-sshuser     = $hook_pretag_sshuser
hook-pretag-sshaddr     = $hook_pretag_sshaddr
hook-posttag-script     = $hook_posttag_script
hook-posttag-sshuser    = $hook_posttag_sshuser

""" )

  def tag_define_custom_tag( self, tagDsc ):
    tag_file = self.repodir_ + SWTAG_FILE

    customtag = self.customtag_template.substitute( tagDsc )

    tagf = open( tag_file, "a" )
    tagf.write( customtag )
    tagf.close()



  def tag_define_all_100_custom( self ):
    tag_file = self.repodir_ + SWTAG_FILE
    tags_def = """
[G2C]
regexp                  = ^[-._0-9a-zA-Z]{1,30}$
push-on-origin          = true
one-x-commit            = True
only-on-integrator-repo = false
allowed-brtypes         = INT
denied-brtypes          = 

[DAT]
regexp                  = ^[-._0-9a-zA-Z]{1,30}$
push-on-origin          = true
one-x-commit            = True
only-on-integrator-repo = false
allowed-brtypes         = FTR
denied-brtypes          = 

[PLT]
regexp                  = ^[-._0-9a-zA-Z]{1,30}$
push-on-origin          = true
one-x-commit            = True
only-on-integrator-repo = false
allowed-brtypes         = FTR
denied-brtypes          = 

[ZIC]
regexp                  = ^[-._0-9a-zA-Z]{1,30}$
push-on-origin          = true
one-x-commit            = True
only-on-integrator-repo = false
allowed-brtypes         = FTR
denied-brtypes          = 

[SLC]
regexp                  = ^[-._0-9a-zA-Z]{1,30}$
push-on-origin          = true
one-x-commit            = True
only-on-integrator-repo = false
allowed-brtypes         = FTR
denied-brtypes          = 
"""
    file = open( tag_file, 'w+' )
    file.write( tags_def )
    file.close()




  def tag_create( self, type, arg = "", msg = "", reuse = False ):
    opt_reuse = ""
    if reuse == True:
      opt_reuse = "-M"

    opt_msg = ""
    if msg != "":
      opt_msg = " -m \"%s\" " % msg

    cmd = "cd %s && %s tag %s %s %s %s" % ( self.repodir_, SWGIT, opt_reuse, opt_msg, type, arg )
    return myCommand( cmd )

  def tag_delete( self, tag ):
    cmd = "cd %s && %s tag -d %s" % ( self.repodir_, SWGIT, tag )
    return myCommand( cmd )

  def tag_delete_e( self, tag ):
    cmd = "cd %s && %s tag -e %s" % ( self.repodir_, SWGIT, tag )
    return myCommand( cmd )

  def tag_dev( self, msg="default commit message", all="" ):
    cmd = "cd %s && %s tag -m \"%s\" dev %s" % ( self.repodir_, SWGIT, msg, all )
    return myCommand( cmd )

  def tag_fix( self, ddts, msg="default commit message", all="" ):
    cmd = "cd %s && %s tag -m \"%s\" fix %s %s" % ( self.repodir_, SWGIT, msg, ddts, all )
    return myCommand( cmd )

  def tag_dev_fix( self, ddts, msg="default commit message", all="" ):
    cmd = "cd %s && %s tag -m \"%s\" dev && %s tag -m \"%s\" fix %s %s" % ( self.repodir_, SWGIT, msg, SWGIT, msg, ddts, all )
    return myCommand( cmd )

  def tag_dev_replace( self, msg="default commit message", all="" ):
    cmd = "cd %s && %s tag -m \"%s\" --replace dev %s" % ( self.repodir_, SWGIT, msg, all )
    return myCommand( cmd )

  def tag_fix_replace( self, ddts, msg="default commit message", all="" ):
    cmd = "cd %s && %s tag -m \"%s\" --replace fix %s %s" % ( self.repodir_, SWGIT, msg, ddts, all )
    return myCommand( cmd )

  def tag_ngt( self, build, msg="default commit message", all="" ):
    cmd = "cd %s && %s tag -m \"%s\" NGT %s %s" % ( self.repodir_, SWGIT, msg, build, all )
    return myCommand( cmd )

  #
  # Merge
  #
  def merge( self, ref, all="" ):
    cmd = "cd %s && %s merge %s %s" % ( self.repodir_, SWGIT, ref, all )
    return myCommand( cmd )

  def merge_on_int( self, ref = "", all="" ):
    cmd = "cd %s && %s merge -I %s %s" % ( self.repodir_, SWGIT, ref, all )
    return myCommand( cmd )

  #
  # Pull
  #
  def pull( self, all="" ):
    cmd = "cd %s && %s pull %s" % ( self.repodir_, SWGIT, all )
    return myCommand( cmd )

  def pull_with_merge( self, all="" ):
    cmd = "cd %s && %s pull -I %s" % ( self.repodir_, SWGIT, all )
    return myCommand( cmd )

  #
  # Push
  #
  @staticmethod
  def push_dst( dir, minusI, remote = "", all="" ):
    opt_merge = ""
    if minusI:
      opt_merge = " --merge-on-int " 
    cmd = "cd %s && %s push %s %s %s --no-mail" % ( dir, SWGIT, opt_merge, remote, all )
    return myCommand( cmd )

  def push( self, remote = "", all="" ):
    return swgit__utils.push_dst( self.repodir_, False, remote, all )

  def push_with_merge( self, remote = "", all="" ):
    return swgit__utils.push_dst( self.repodir_, True, remote, all )

  #
  # swProj
  #

  # first check if REPO_BKP repos are created,
  #  if yes, copy them instead of re-creating them every time 
  #  if no, creating them
  #  repoinfolist must be like this:
  #    REPOS_INFOS = (
  #         # name  | rel | subrel | liv |  file 
  #         (REPO_A, "1/0", "0/0", "A", "a.txt"),
  #         (REPO_B, "2/0", "0/0", "B", "b.txt"),
  #        )
  @staticmethod
  def create_default_repos():
    for r in REPOS_INFOS:
      out, errCode = swgit__utils.create_repo_withbkp( r )
      if errCode != 0:
        return out, errCode
    return "OK", 0

  @staticmethod
  def create_default_proj_repos():
    for r in REPOS_PROJ__INFOS:
      out, errCode = swgit__utils.create_repo_withbkp( r )
      if errCode != 0:
        return out, errCode
    return "OK", 0


  @staticmethod
  def create_repo_withbkp( repoinfo ):

    orig     = repoinfo[0]
    orig_bkp = orig + "_BKP"
    orig_tbd = orig + "_TBD"

    aremote_tbd = orig        + AREMOTE_PATH + ".TBD"
    aremote_dst = orig        + AREMOTE_PATH
    aremote_bkp = aremote_dst + ".BKP"

    shutil.rmtree( orig, True ) #ignore errors
    shutil.rmtree( aremote_dst, True ) #ignore errors

    #
    # AREPO CREATE (with bkp)
    #
    if os.path.exists( orig_bkp ):
      shutil.copytree( orig_bkp, orig )
    else:
      # create dir
      out, errCode = create_dir_some_file( orig, repoinfo[4] )
      if errCode != 0:
        print "create_dir FAILED for dir %s - \n%s\n" % ( orig, out)
        sys.exit( 1 )

      # init dir
      out, errCode = swgit__utils.init_dir( orig, repoinfo[1], repoinfo[2], repoinfo[3], repoinfo[5])
      if errCode != 0:
        print "init_dir FAILED for dir %s - \n%s\n" % ( orig, out )
        sys.exit( 1 )

      # craete CST branch
      if repoinfo[6] != None:

        shutil.rmtree( orig_tbd, True ) #ignore errors

        #clone just created repo 
        out, errCode = swgit__utils.clone_repo_url( repoinfo[8], orig_tbd, repoinfo[9] )
        if errCode != 0:
          print "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % ( repoinfo[8], orig_tbd, repoinfo[9], out)
          sys.exit( 1 )

        cst_full = repoinfo[6]
        cst_name = cst_full[ findnth( cst_full, "/", 6 ) + 1 :  ]
        cst_rel = cst_full = cst_full[ 0 : findnth( cst_full, "/", 4 ) ]

        out, errCode = swgit__utils.init_cst_dst( orig_tbd, repoinfo[7], cst_name, cst_rel )
        if errCode != 0:
          print "init_cst FAILED for dir %s - \n%s\n" % ( orig_tbd, out )
          sys.exit( 1 )

        out, errCode = swgit__utils.push_dst( orig_tbd, True )
        if errCode != 0:
          print "init_cst FAILED for dir %s - \n%s\n" % ( orig_tbd, out )
          sys.exit( 1 )

        shutil.rmtree( orig_tbd, True ) #ignore errors

      # first time create _BKP (next will be faster
      shutil.copytree( orig, orig_bkp )

    #
    # AREPO_AREMOTE CREATE (with bkp)
    #
    if os.path.exists( aremote_bkp ) == False:
      # clone first time
      cmd = "%s clone %s %s -b %s " % ( SWGIT, repoinfo[8], aremote_tbd, repoinfo[9] )
      out, retcode = myCommand( cmd )
      if retcode != 0:
        return out, retcode

      #lcoalize taht branch (so when adding this repo as remote, i will have a remote branch more)
      cmd = "cd %s && %s branch -s %s" % ( aremote_tbd, SWGIT, repoinfo[9] )
      out, retcode = myCommand( cmd )
      if retcode != 0:
        return out, retcode

      shutil.copytree( aremote_tbd, aremote_bkp )
      shutil.copytree( aremote_bkp, aremote_dst )
      shutil.rmtree( aremote_tbd, True ) #ignore errors
    else:
      shutil.copytree( aremote_bkp, aremote_dst )


#    #
#    # test mode MOREREPOS => add remote to orig
#    #
#    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
#      print "\n%s\nMOREREMOTES for repo %s\n%s\n" % ( "="*20, orig, "="*20 )
#      helper = swgit__utils( orig )
#      AREPO_AREMOTE_URL = "ssh://%s@%s%s" % ( TEST_USER, TEST_ADDR, aremote_dst )
#      out, errCode = helper.remote_add( ORIG_REPO_AREMOTE_NAME, AREPO_AREMOTE_URL )
#      out, errCode = helper.system_swgit( "fetch --all" )


    return "OK", 0


  def proj_create( self ):
    return swgit__utils.proj_create_dst( self.repodir_ )

  @staticmethod
  def proj_create_dst( dst ):
    #just create dir and initialize it
    shutil.rmtree( dst, True )
    os.mkdir( dst )
    return swgit__utils.init_dir( dst )


  #  mapinfolist must be like this:
  #    list of (
  #     name,
  #     url,
  #     localpath,
  #     branch,
  #     checkout, (or None)
  #    )
  @staticmethod
  def proj_add_dst( dst, mapinfolist, opt = "" ):
    #print "mapinfolist: %s" % mapinfolist
    for currmapinfo in mapinfolist:
      opt_snap = ""
      if currmapinfo[3] == True:
        opt_snap = " --snapshot "
      opt_branch = ""
      if currmapinfo[2] != "":
        opt_branch = "--branch %s" % currmapinfo[2]

      cmd = "cd %s && %s proj --add-repo %s %s %s %s %s" % \
          ( dst, SWGIT, currmapinfo[1], currmapinfo[0], opt_branch, opt, opt_snap )
      out, retcode = myCommand( cmd )
      if retcode != 0:
        return out, retcode

    return "OK",0

  def proj_add( self, mapinfolist ):
    return swgit__utils.proj_add_dst( self.repodir_, mapinfolist )

  def proj_add_snapshot( self, mapinfolist ):
    return swgit__utils.proj_add_dst( self.repodir_, mapinfolist, opt = "--snapshot" )

  def proj_del( self, sectname ):
    cmd = "cd %s && %s proj --del-repo %s" % ( self.repodir_, SWGIT, sectname )
    return myCommand( cmd )

  @staticmethod
  def proj_edit_dst( dst, repo, def_int_br ):
    opt_edit = "--unset-int-br"
    if def_int_br != "":
      opt_edit = "--set-int-br %s" % def_int_br

    cmd = "cd %s && %s proj --edit-repo %s %s" % ( dst, SWGIT, repo, opt_edit )
    out, retcode = myCommand( cmd )
    if retcode != 0:
      return out, retcode
    return "OK",0

  def proj_edit( self, repo, def_int_br ):
    return swgit__utils.proj_edit_dst( self.repodir_, repo, def_int_br )



  def proj_reset( self, ref = "HEAD", repo = "" ):
    opt_repo = ""
    if repo != "":
      opt_repo = " %s " % repo

    cmd = "cd %s && %s proj --reset %s %s" % ( self.repodir_, SWGIT, ref, opt_repo )
    return myCommand( cmd )


  def proj_update( self, repo = "" ):
    opt_repo = ""
    if repo != "":
      opt_repo = " %s " % repo
    cmd = "cd %s && %s proj --update %s" % ( self.repodir_, SWGIT, opt_repo )
    return myCommand( cmd )

  def proj_update_yesmerge( self, repo = "" ):
    opt_repo = ""
    if repo != "":
      opt_repo = " %s " % repo
    cmd = "cd %s && %s proj --update %s -I" % ( self.repodir_, SWGIT, opt_repo )
    return myCommand( cmd )

  def proj_update_nomerge( self, repo = "" ):
    opt_repo = ""
    if repo != "":
      opt_repo = " %s " % repo
    cmd = "cd %s && %s proj --update %s -N" % ( self.repodir_, SWGIT, opt_repo )
    return myCommand( cmd )

  def proj_init( self, repo = "", opt = "" ):
    opt_repo = ""
    if repo != "":
      opt_repo = " %s " % repo

    cmd = "cd %s && %s proj --init %s %s" % ( self.repodir_, SWGIT, opt_repo, opt )
    return myCommand( cmd )

  def proj_UNinit( self, repo = "" ):
    opt_repo = ""
    if repo != "":
      opt_repo = " %s " % repo

    cmd = "cd %s && %s proj --un-init %s" % ( self.repodir_, SWGIT, opt_repo )
    return myCommand( cmd )


  def proj_edit_commit_and_checkout( self, sectname, newchk ):
    #1. go on develop
    out, retcode = self.branch_switch_to_int()
    if retcode != 0:
      return out, retcode

    #2. enter repo and move on new commit
    cmd = "cd %s/%s && %s branch -s %s" % ( self.repodir_, sectname, SWGIT, newchk )
    out, retcode =  myCommand( cmd )
    if retcode != 0:
      return out, retcode

    #3. commit project
    cmd_commit = "cd %s && %s commit -a -m \"edited map\" --dev" % ( self.repodir_, SWGIT )
    out, retcode = myCommand( cmd_commit )
    if retcode != 0:
      return out, retcode

    # ?? proj --reset HEAD ??

    ##4. checkout last commit to select new modif
    #out, retcode =  self.get_currsha()
    #if retcode != 0:
    #  return out, retcode
    #out, retcode =  self.branch_switch_to_br( out )
    #if retcode != 0:
    #  return out, retcode

    return "OK",0


  def proj_check_dir_is_proj( self, checkmappresence = True ):

    if os.path.exists( self.repodir_ ) == False:
      return "Project %s not existing directory" % ( self.repodir_ ), 1

    if os.path.exists( self.repodir_ + "/.gitignore" ) == False:
      return "Not exising .gitignore under project %s" % ( self.repodir_), 1

    if os.path.exists( self.repodir_ + "/.git" ) == False:
      return "Project %s, has NO .git directory." % ( self.repodir_), 1

    if checkmappresence == True: #check it is also a repo (.git, .gitignore ... )
      if os.path.exists( self.projmap_ ) == False:
        return "map %s not existing" % ( self.projmap_), 1

    return "OK", 0


  @staticmethod
  def proj_getrepo_chk_dst( dst, reponame ):
    cmd_get_submod_chk = "cd %s && git submodule status | grep \" %s \" | cut -c2- | cut -d ' ' -f 1" % ( dst, reponame )
    return myCommand( cmd_get_submod_chk )

  def proj_getrepo_chk( self, reponame ):
    return swgit__utils.proj_getrepo_chk_dst( self.repodir_, reponame )

  @staticmethod
  def proj_getrepo_info( dst, reponame ):
    cmd_get_submod_url = "cd %s && git config -l | grep \"submodule.%s.url=\" | cut -d '=' -f 2" % ( dst, reponame )
    url,errCode = myCommand( cmd_get_submod_url )
    if errCode != 0:
      return url, errCode

    chk,errCode = swgit__utils.proj_getrepo_chk_dst( dst, reponame )
    if errCode != 0:
      return chk, errCode

    ib,errCode = swgit__utils.int_branch_get_dst( "%s/%s" % ( dst, reponame ) )
    if errCode != 0:
      #it happens inside REPOS under CST projects
      #return ib, errCode
      ib = ""

    return [ reponame, url, reponame, ib, chk ], 0


  # mapentry must be vector like this:
  #   ( #name, #url, #localpath, #branch, #checkout )
  @staticmethod
  def proj_check_map_unix_dst( dst, mapentry ):
    swmap = os.path.abspath( dst + "/" + PROJMAP )
    gitignore = os.path.abspath( dst + "/.gitignore" )

    repoinfo, retcode = swgit__utils.proj_getrepo_info( dst, mapentry[0] )
    if retcode != 0:
      return repoinfo, retcode

    for i in range( 0, 2 ):
      if mapentry[i] != repoinfo[i]:
        return "error on field %s, repoinfo: %s, mapentry: %s" % ( i, repoinfo, mapentry ), 1

    cmd_grep_gitmodules = "cd %s && egrep '^\[submodule \"%s\"\]$' %s" % ( dst, mapentry[0], swmap )
    out, retcode = myCommand( cmd_grep_gitmodules )
    if retcode != 0:
      return out, retcode

    cmd_grep_gitmodules = "cd %s && grep -e \"	path = .*%s$\" %s" % ( dst, mapentry[0], swmap )
    out, retcode = myCommand( cmd_grep_gitmodules )
    if retcode != 0:
      return out, retcode

    cmd_grep_gitmodules = "cd %s && grep -e \"	url = .*%s$\" %s" % ( dst, mapentry[1], swmap )
    out, retcode = myCommand( cmd_grep_gitmodules )
    if retcode != 0:
      return out, retcode

    return "OK",0


  def proj_check_map_unix( self, mapentry ):
    return swgit__utils.proj_check_map_unix_dst( self.repodir_, mapentry )


  #This create 3 repos described in MAP_INFOS, (A, B, C)
  #  creates a project referencing them
  # does a copy if anything as already been created
  @staticmethod
  def proj_create_default_repos_and_default_proj( dst ):

    #1. create brick repos
    out, errCode = swgit__utils.create_default_repos()
    if errCode != 0:
      return out, errCode

    #2. create proj repo
    shutil.rmtree( dst, True )

    if os.path.exists( dst + "_BKP" ):
        shutil.copytree( dst + "_BKP", dst )
    else:
      #2.1 create empty proj
      out, errCode = swgit__utils.proj_create_dst( dst )
      if errCode != 0:
        return out, errCode

      #2.2 Add 3 repos to project
      out, errCode = swgit__utils.proj_add_dst( dst, MAP_INFOS )
      if errCode != 0:
        return out, errCode

      #2.3 initialize project repo
      out, errCode = swgit__utils.init_dir( dst )
      if errCode != 0:
        return out, errCode

      #2.4 first time create _BKP (next will be faster
      shutil.copytree( dst, dst + "_BKP" )

    return "OK", 0



  def getProjects( self, filename="", noCHK=False ):
    if filename != "":
      filename = "--filename " + filename
    CHK = ""
    if noCHK == True:
      CHK = "--no-chk"
    cmd = "cd %s && %s proj %s --get-projects %s" % ( self.repodir_, SWGIT, filename, CHK )
    #print cmd
    return myCommand( cmd )


  #
  # stabilize
  #
  def stabilize_stb( self, stb, src ):
    opt_src = ""
    if src != "":
      opt_src = "--src %s" % src
    cmd = "cd %s && %s stabilize --stb %s %s" % ( self.repodir_, SWGIT, stb, opt_src )
    return myCommand( cmd )

  def stabilize_liv( self, liv ):
    cmd = "cd %s && %s stabilize --liv %s --no-interactive" % ( self.repodir_, SWGIT, liv )
    return myCommand( cmd )
  
  def stabilize_cst( self, cst, src ):
    opt_src = ""
    if src != "":
      opt_src = "--src %s" % src
    cmd = "cd %s && %s stabilize --cst %s %s" % ( self.repodir_, SWGIT, cst, opt_src )
    return myCommand( cmd )




  #
  # init
  #
  def init_src( self, src, r = TEST_REPO_R, s = TEST_REPO_S, l = "", u = "", c = "", cst = False ):

    str_src_opt = ""
    if src != "":
      str_src_opt = " --src %s " % src

    str_liv_opt = ""
    if l != "":
      str_liv_opt = " -l %s " % l

    str_c_opt = ""
    if c != "":
      str_c_opt = " -c %s " % c

    str_u_opt = ""
    if u != "":
      str_u_opt = " -u %s " % u

    str_cst_opt = ""
    if cst == True:
      str_cst_opt = " --cst "

    cmd = "cd %s && %s init -r %s/%s %s %s %s %s %s" % ( self.repodir_, SWGIT, r, s, str_liv_opt, str_u_opt, str_c_opt, str_cst_opt, str_src_opt )
    return myCommand( cmd )


  @staticmethod
  def init_cst_dst( dir, src, cstname, rel ):
    cmd = "cd %s && %s init --create %s --cst --src %s -r %s --git-user %s" % ( dir, SWGIT, cstname, src, rel.replace( '/','.' ), ORIG_REPO_GITUSER )
    return myCommand( cmd )

  def init_cst( self, src, cstname, rel ):
    return swgit__utils.init_cst_dst( self.repodir_, src, cstname, rel )

  #
  # Remotes
  #
  def remote_add( self, name, url ):
    cmd = "cd %s && git remote add %s %s" % (self.repodir_, name, url)
    return myCommand( cmd )

