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

from test_proj_util import *


class Test_Stabilize( Test_ProjBase ):
  STABILIZE_CLONE_DIR = SANDBOX + "TEST_STABILIZE_CLONE"
  STABILIZE_REPO_DIR  = SANDBOX + "TEST_STABILIZE_REPO"
  BRANCH_NAME        = "test_stabilize"
  FULL_BRANCH_NAME    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, ORIG_REPO_GITUSER, BRANCH_NAME )
  BRANCH_NAME_SS     = "side_of_side"
  FULL_BRANCH_NAME_SS = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, BRANCH_NAME_SS )

  BUILTIN_DEV_0  = "%s/DEV/000" % ( FULL_BRANCH_NAME )
  BUILTIN_DEV_1  = "%s/DEV/001" % ( FULL_BRANCH_NAME )
  BUILTIN_FIX_0  = "%s/FIX/000" % ( FULL_BRANCH_NAME )

  DDTS          = "Issue12345"
  CREATED_FIX   = "%s/FIX/%s"  % ( FULL_BRANCH_NAME, DDTS )
  CREATED_DEV_0 = "%s/DEV/000" % ( FULL_BRANCH_NAME )
  CREATED_DEV_1 = "%s/DEV/001" % ( FULL_BRANCH_NAME )

  CFG = "swgit.stabilize-anyref"

  LBL = "Drop.B"
  CREATED_STBDEV = "%s/STB/%s" % ( ORIG_REPO_DEVEL_BRANCH,  LBL )
  CREATED_STBSTB = "%s/STB/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL )
  CREATED_LIV    = "%s/LIV/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL )

  MYCST_REL      = "1/1"
  MYCST_BR       = "mycst"
  MYCST_FULL_BR  = "%s/%s/%s/CST/%s" % ( MYCST_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST_BR )
  MYCST_LIV      = "%s/LIV/%s" % ( MYCST_FULL_BR, TEST_REPO_LIV )


  def setUp( self ):
    super( Test_Stabilize, self ).setUp()

    shutil.rmtree( self.STABILIZE_REPO_DIR, True )
    shutil.rmtree( self.STABILIZE_CLONE_DIR, True )

    self.sw_ori_h = swgit__utils( self.STABILIZE_REPO_DIR )
    self.sw_clo_h = swgit__utils( self.STABILIZE_CLONE_DIR )

  def tearDown( self ):
    super( Test_Stabilize, self ).tearDown()


  def util_create_stabilizetest_repo( self, label ):

    out, errCode = create_dir_some_file( self.STABILIZE_REPO_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "create dir and files %s" % self.STABILIZE_REPO_DIR ) 

    out, errCode = swgit__utils.init_dir( self.STABILIZE_REPO_DIR, l = label )
    self.util_check_SUCC_scenario( out, errCode, "", "init new repo WITHOUT LIV %s" % self.STABILIZE_REPO_DIR ) 


    #create also an empty commit on develop
    out, errCode = self.sw_ori_h.int_branch_set( ORIG_REPO_DEVEL_BRANCH )
    out, errCode = self.sw_ori_h.branch_switch_to_int()
    out, errCode = self.sw_ori_h.branch_create( self.BRANCH_NAME )

    out, errCode = self.sw_ori_h.modify_file( TEST_REPO_FILE_A, msg = "some content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" ) 
    out, errCode = self.sw_ori_h.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" ) 

    out, errCode = self.sw_ori_h.modify_file( TEST_REPO_FILE_A, msg = "some other content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file 2" ) 
    out, errCode = self.sw_ori_h.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "commit" ) 

    out, errCode = self.sw_ori_h.modify_file( TEST_REPO_FILE_A, msg = "some third content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file 3" ) 
    out, errCode = self.sw_ori_h.commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev" ) 

    out, errCode = self.sw_ori_h.merge_on_int( "" )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_ori_h.init_dir( self.STABILIZE_REPO_DIR,
                                           "1/1", 
                                           u   = TEST_USER, 
                                           c   = self.MYCST_BR,
                                           cst = True, 
                                           src = ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % self.MYCST_FULL_BR )


  def util_clone_repo_stabilize( self, dst, label ):
    orig      = self.STABILIZE_REPO_DIR
    orig_bkp  = orig                     + ".%s.BKP" % label
    clone     = orig                     + "_aclone"
    clone_bkp = clone                    + ".%s.BKP" % label

    shutil.rmtree( orig, True ) #ignore errors
    shutil.rmtree( clone, True ) #ignore errors
    shutil.rmtree( dst, True ) #ignore errors

    if os.path.exists( orig_bkp ) == False:
      #orig first time
      self.util_create_stabilizetest_repo( label )
      shutil.copytree( orig, orig_bkp )
    else:
      shutil.copytree( orig_bkp, orig )

    if os.path.exists( clone_bkp ) == False:
      # clone first time
      out, errCode = swgit__utils.clone_repo_integrator( orig, clone )
      self.util_check_SUCC_scenario( out, errCode, "", "clone into %s" % clone ) 

      shutil.copytree( clone, clone_bkp )
      shutil.copytree( clone_bkp, dst )
    else:
      shutil.copytree( clone_bkp, dst )


  def test_Satbilize_00_00_DevelopRepo( self ):
    self.util_create_stabilizetest_repo( "Drop.A" )

    out, errCode = swgit__utils.clone_repo( self.STABILIZE_REPO_DIR, self.STABILIZE_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "clone into %s" %  self.STABILIZE_CLONE_DIR ) 

    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "a stable branch must be tarcked",
                                   "stabilize without stable branch tracked" ) 

    out, errCode = self.sw_clo_h.branch_track( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "tracking stable int" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "This repository has been created as a 'developer' one.",
                                   "stabilize inside develop repo" ) 

    out, errCode = self.sw_clo_h.set_cfg( "swgit.integrator", "True" )

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.B", "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize inside develop repo" ) 



  def test_Satbilize_01_00_NoLbl_STB( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    #
    # STABILIZE
    #
    #
    # origin
    #
    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize anyref" ) 

    out, errCode = self.sw_ori_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "FAILSREGEXP", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label STB", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "--src-reference mandatory",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize from another branch" ) 

    #
    # clone
    #
    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 


    out, errCode = self.sw_clo_h.stabilize_stb( "FAILSREGEXP", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label STB", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "--src-reference mandatory",
                                   "stabilize without src" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but develop",
                                   "stabilize from another branch" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 


    out, errCode = self.sw_clo_h.set_cfg( "swgit.integrator", "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "changing repo into integrator" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize without stable branch tracked" ) 




  def test_Satbilize_01_02_YesLbl_STB( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "Drop.A" )

    #
    # STABILIZE
    #
    #
    # origin
    #
    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize anyref" ) 

    out, errCode = self.sw_ori_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "FAILSREGEXP", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label STB", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "--src-reference mandatory",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize from another branch" ) 

    #
    # clone
    #
    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 


    out, errCode = self.sw_clo_h.stabilize_stb( "FAILSREGEXP", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label STB", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "--src-reference mandatory",
                                   "stabilize without src" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but develop",
                                   "stabilize from another branch" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 


    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize without stable branch tracked" ) 


    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Already exists a STB label named",
                                   "stabilize without stable branch tracked" ) 

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.B", "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize without stable branch tracked" ) 

  def test_Satbilize_01_03_NoLbl_LIV( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    #
    # STABILIZE
    #
    #
    # origin
    #
    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize anyref" ) 

    out, errCode = self.sw_ori_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 

    out, errCode = self.sw_clo_h.stabilize_liv( "FAILSREGEXP" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label LIV", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize from another branch" ) 

    #
    # clone
    #
    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 


    out, errCode = self.sw_clo_h.stabilize_liv( "FAILSREGEXP" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label LIV", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but stable",
                                   "stabilize without src" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but stable",
                                   "stabilize from another branch" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 


    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but stable",
                                   "stabilize without stable branch tracked" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_br( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to stable" ) 


    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You must run 'swgit stabilize --stb",
                                   "stabilize without stable branch tracked" ) 


  def test_Satbilize_01_04_YesLbl_LIV( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "Drop.A" )

    #
    # STABILIZE
    #
    #
    # origin
    #
    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize anyref" ) 

    out, errCode = self.sw_ori_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 

    out, errCode = self.sw_clo_h.stabilize_liv( "FAILSREGEXP" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label LIV", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_ori_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot execute this script on repository origin",
                                   "stabilize from another branch" ) 

    #
    # clone
    #
    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" ) 


    out, errCode = self.sw_clo_h.stabilize_liv( "FAILSREGEXP" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid name for label LIV", 
                                   "stabilize with wrong regexp" ) 

    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but stable",
                                   "stabilize without src" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but stable",
                                   "stabilize from another branch" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 


    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "cannot execute this script on any branch but stable",
                                   "stabilize without stable branch tracked" ) 

    out, errCode = self.sw_clo_h.branch_switch_to_br( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to stable" ) 


    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You already have a LIV label on this commit:",
                                   "stabilize without stable branch tracked" ) 


  def test_Satbilize_02_00_NoLbl_STB_LIV( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    #on ori move away from head (for push)
    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" ) 

    #on clone track stable
    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )
    #out, errCode = self.sw_clo_h.branch_track( ORIG_REPO_STABLE_BRANCH )
    #self.util_check_SUCC_scenario( out, errCode, "", "tracking stable int" ) 

    sha_before, errCode = self.sw_clo_h.get_currsha()
    self.util_check_SUCC_scenario( out, errCode, "", "get sha before" ) 

    sha_stb_before, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" ) 

    sha_dev_before, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" ) 

    self.assertEqual   ( sha_before, sha_dev_before, "NOT on develop before starting stb" )
    self.assertNotEqual( sha_dev_before, sha_stb_before, "develop and stable must differ" )

    #make stb
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize --stb" ) 

    sha_dev_after_stb, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" ) 
    sha_stb_after_stb, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" ) 
    sha_STBDEV, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBDEV )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on develop" ) 
    sha_STBSTB, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBSTB )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on stable" ) 
    sha_LIV, errCode = self.sw_clo_h.get_currsha( self.CREATED_LIV )
    self.util_check_DENY_scenario( out, errCode, "", "get sha LIV" ) 


    self.assertEqual   ( sha_dev_before, sha_dev_after_stb, "" )
    self.assertEqual   ( sha_STBDEV,     sha_dev_after_stb, "" )
    self.assertEqual   ( sha_STBSTB,     sha_stb_after_stb, "" )
    self.assertNotEqual( sha_stb_before, sha_stb_after_stb, "" )

    #make liv
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize --liv" ) 


    sha_dev_after_liv, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" ) 
    sha_stb_afetr_liv, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" ) 
    sha_STBDEV, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBDEV )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on develop" ) 
    sha_STBSTB, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBSTB )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on stable" ) 
    sha_LIV, errCode = self.sw_clo_h.get_currsha( self.CREATED_LIV )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha LIV" ) 

    sha_LIV_minus1, errCode = self.sw_clo_h.get_currsha( "%s~1" % self.CREATED_LIV )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha LIV~1" ) 
    sha_dev_minus1, errCode = self.sw_clo_h.get_currsha( "%s^1" % ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha dev^1" ) 
    sha_dev_minus2, errCode = self.sw_clo_h.get_currsha( "%s^2" % ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha dev^2" ) 

    self.assertNotEqual( sha_dev_after_stb, sha_dev_after_liv, "" )
    self.assertNotEqual( sha_STBDEV       , sha_dev_after_liv, "" )
    self.assertNotEqual( sha_STBDEV       , sha_STBSTB       , "" )
    self.assertNotEqual( sha_STBSTB       , sha_LIV          , "" )
    self.assertNotEqual( sha_LIV          , sha_dev_after_liv, "" )
    self.assertEqual( sha_LIV_minus1   , sha_STBSTB       , "" )
    self.assertEqual( sha_dev_minus1   , sha_STBDEV       , "" )
    self.assertEqual( sha_dev_minus2   , sha_LIV          , "" )

    changelog_dir = "%s/%s/changelog/%s/%s" % ( self.sw_clo_h.getDir(), SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL )
    chg_file = "%s/LIV_%s.chg" % ( changelog_dir, self.LBL )
    fix_file = "%s/LIV_%s.fix" % ( changelog_dir, self.LBL )
    tkt_file = "%s/LIV_%s.tkt" % ( changelog_dir, self.LBL )
    self.assertTrue( os.path.exists( chg_file ), "chg file not found" )
    self.assertTrue( os.path.exists( chg_file ), "fix file not found" )
    self.assertTrue( os.path.exists( chg_file ), "tkt file not found" )

    #TODO
    # content of files


  def test_Satbilize_03_00_YesLbl_CST( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    #on ori move away from head (for push)
    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to %s" % self.BRANCH_NAME ) 

    #switch to CST
    #set CST as INT BR
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to cst" ) 
    out, errCode = self.sw_clo_h.int_branch_set( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "set int branch to cst" ) 
    #on clone track stable
    out, errCode = self.sw_clo_h.set_cfg( self.CFG, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize anyref" ) 


    #make stb already contained
    out, errCode = self.sw_clo_h.stabilize_cst( self.LBL, ORIG_REPO_STABLE_BRANCH )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already contains this input reference",
                                   "stabilize --cst" ) 

    #make stb
    out, errCode = self.sw_clo_h.stabilize_cst( self.LBL, self.BUILTIN_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize --cst" )

    #make same label
    out, errCode = self.sw_clo_h.stabilize_cst( self.LBL, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Already exists a LIV label named", 
                                   "stabilize --cst same label" ) 




if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()






