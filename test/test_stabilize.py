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

#TODO projects
#TODO more repos, ambiguous stable (or devevlopon mergeback)?


class Test_Stabilize( Test_ProjBase ):
  STABILIZE_CLONE_DIR = SANDBOX + "TEST_STABILIZE_CLONE"
  STABILIZE_REPO_DIR  = SANDBOX + "TEST_STABILIZE_REPO"
  BRANCH_NAME        = "test_stabilize"
  FULL_BRANCH_NAME    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, ORIG_REPO_GITUSER, BRANCH_NAME )
  BRANCH_NAME_SS     = "side_of_side"
  FULL_BRANCH_NAME_SS = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, BRANCH_NAME_SS )

  DDTS          = "Issue12345"
  BUILTIN_DEV_0  = "%s/DEV/000" % ( FULL_BRANCH_NAME )
  BUILTIN_DEV_1  = "%s/DEV/001" % ( FULL_BRANCH_NAME )
  BUILTIN_FIX_0  = "%s/FIX/%s" % ( FULL_BRANCH_NAME, DDTS )

  CFG_ANYREF = "swgit.stabilize-anyref"

  LBL_B = "Drop.B"
  CREATED_STBDEV_B = "%s/STB/%s" % ( ORIG_REPO_DEVEL_BRANCH,  LBL_B )
  CREATED_STBSTB_B = "%s/STB/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL_B )
  CREATED_LIV_B    = "%s/LIV/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL_B )
  CHGLOG_B = "%s/%s/changelog/%s/%s/LIV_%s.chg" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_B )
  FIXLOG_B = "%s/%s/changelog/%s/%s/LIV_%s.fix" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_B )
  TKTLOG_B = "%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_B )

  LBL_C = "Drop.C"
  CREATED_STBDEV_C = "%s/STB/%s" % ( ORIG_REPO_DEVEL_BRANCH,  LBL_C )
  CREATED_STBSTB_C = "%s/STB/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL_C )
  CREATED_LIV_C    = "%s/LIV/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL_C )
  CHGLOG_C = "%s/%s/changelog/%s/%s/LIV_%s.chg" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_C )
  FIXLOG_C = "%s/%s/changelog/%s/%s/LIV_%s.fix" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_C )
  TKTLOG_C = "%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_C )

  LBL_D = "Drop.D"
  CREATED_STBDEV_D = "%s/STB/%s" % ( ORIG_REPO_DEVEL_BRANCH,  LBL_D )
  CREATED_STBSTB_D = "%s/STB/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL_D )
  CREATED_LIV_D    = "%s/LIV/%s" % ( ORIG_REPO_STABLE_BRANCH, LBL_D )
  CHGLOG_D = "%s/%s/changelog/%s/%s/LIV_%s.chg" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_D )
  FIXLOG_D = "%s/%s/changelog/%s/%s/LIV_%s.fix" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_D )
  TKTLOG_D = "%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( STABILIZE_CLONE_DIR, SWREPO_DIR, ORIG_REPO_REL, ORIG_REPO_SUBREL, LBL_D )


  MYCST_REL      = "1/1"
  MYCST_BR       = "cst111"
  MYCST_FULL_BR  = "%s/%s/%s/CST/%s" % ( MYCST_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST_BR )
  MYCST_LIV      = "%s/LIV/%s" % ( MYCST_FULL_BR, TEST_REPO_LIV )
  CREATED_STBCST_B = "%s/STB/%s" % ( MYCST_FULL_BR, LBL_B )
  CREATED_STBCST_C = "%s/STB/%s" % ( MYCST_FULL_BR, LBL_C )
  CREATED_LIVCST_B = "%s/LIV/%s" % ( MYCST_FULL_BR, LBL_B )
  CREATED_LIVCST_C = "%s/LIV/%s" % ( MYCST_FULL_BR, LBL_C )

  MYCST2_REL      = "2/2"
  MYCST2_BR       = "cst222"
  MYCST2_FULL_BR  = "%s/%s/%s/CST/%s" % ( MYCST2_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST2_BR )
  MYCST2_LIV      = "%s/LIV/%s" % ( MYCST2_FULL_BR, TEST_REPO_LIV )
  CREATED_STBCST2_B = "%s/STB/%s" % ( MYCST2_FULL_BR, LBL_B )
  CREATED_STBCST2_C = "%s/STB/%s" % ( MYCST2_FULL_BR, LBL_C )
  CREATED_LIVCST2_B = "%s/LIV/%s" % ( MYCST2_FULL_BR, LBL_B )
  CREATED_LIVCST2_C = "%s/LIV/%s" % ( MYCST2_FULL_BR, LBL_C )

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
                                           self.MYCST_REL,
                                           u   = TEST_USER,
                                           c   = self.MYCST_BR,
                                           cst = True,
                                           src = ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % self.MYCST_FULL_BR )

    out, errCode = self.sw_ori_h.init_dir( self.STABILIZE_REPO_DIR,
                                           self.MYCST2_REL,
                                           u   = TEST_USER,
                                           c   = self.MYCST2_BR,
                                           cst = True,
                                           src = ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % self.MYCST2_FULL_BR )


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


  def test_Stabilize_00_00_DevelopRepo( self ):
    self.util_create_stabilizetest_repo( "Drop.A" )

    out, errCode = swgit__utils.clone_repo( self.STABILIZE_REPO_DIR, self.STABILIZE_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "clone into %s" %  self.STABILIZE_CLONE_DIR )

    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "must be tracked",
                                   "stabilize without stable branch tracked" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD", dstbr = TEST_REPO_BR_STB )
    self.util_check_DENY_scenario( out, errCode,
                                   "must be tracked",
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



  def test_Stabilize_01_00_STB_NoLbl_fromdevelop( self ):

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

    out, errCode = self.sw_ori_h.set_cfg( self.CFG_ANYREF, "True" )
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
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" )


    out, errCode = self.sw_clo_h.stabilize_stb( "FAILSREGEXP", "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Please specify a valid name for label STB",
                                   "stabilize with wrong regexp" )

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "" )
    self.util_check_DENY_scenario( out, errCode,
                                   "--src-reference mandatory",
                                   "stabilize without src" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    #############
    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )
    #############

    out, errCode = self.sw_clo_h.set_cfg( "swgit.integrator", "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "changing repo into integrator" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize without stable branch tracked" )

    stbdev_sha, stbdev_err = self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )
    stbstb_sha, stbstb_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )
    stbstb_minus1_sha, stbstbminus1__err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B + "~1" )

    self.util_check_EQUAL( stbdev_err, 0, "must be craeted STB tag" )
    self.util_check_EQUAL( stbstb_err, 0, "must be craeted STB tag" )

    self.util_check_EQUAL( devbr_before_sha, stbdev_sha,  "STB tag on wrong commit" )
    self.util_check_EQUAL( stbbr_before_sha, stbstb_minus1_sha,  "STB tag on wrong commit" )

    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_minus1_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    self.util_check_NOTEQ( stbbr_before_sha, stbbr_after_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_minus1_after_sha, "stable not moved" )


  #
  # Test:
  #   stabilize can be done from any branch
  #   Here we test what happens when current branch is FTR 
  #      and a develop intbr is or is not set
  def test_Stabilize_01_01_STB_NoLbl_fromFTR( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME ) #localize
    out, errCode = self.sw_clo_h.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "settinf FTR intbr")

    #stabilize with FTR intbr
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot deduce onto which branch to make stb/liv.", 
                                   "stabilize from branch, with FTR intbr" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch detached head" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Cannot deduce onto which branch to make stb/liv.", 
                                   "stabilize from detached, with FTR intbr" )

    #############
    out, errCode = self.sw_clo_h.int_branch_set( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "setting develop intbr")
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch" )
    #############

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize from another branch" )

    stbdev_sha, stbdev_err = self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )
    stbstb_sha, stbstb_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )
    stbstb_minus1_sha, stbstb_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B + "~1" )

    self.util_check_EQUAL( stbdev_err, 0, "must be craeted STB tag" )
    self.util_check_EQUAL( stbstb_err, 0, "must be craeted STB tag" )

    self.util_check_EQUAL( devbr_before_sha, stbdev_sha,  "STB tag on wrong commit" )
    self.util_check_EQUAL( stbbr_before_sha, stbstb_minus1_sha,  "STB tag on wrong commit" )

    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_minus1_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    self.util_check_NOTEQ( stbbr_before_sha, stbbr_after_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_minus1_after_sha, "stable not moved" )


  def test_Stabilize_01_02_STB_IntBrFTRr_fromDetached( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME ) #localize
    ##################
    out, errCode = self.sw_clo_h.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "settinf FTR intbr")
    ##################

    #stabilize with FTR intbr
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot deduce onto which branch to make stb/liv.", 
                                   "stabilize from branch, with FTR intbr" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch detached head" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Cannot deduce onto which branch to make stb/liv.", 
                                   "stabilize from detached, with FTR intbr" )

    ##################
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, TEST_REPO_BR_DEV, TEST_REPO_BR_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize from detached head, without intbr set, specifying target" )
    ##################

    stbdev_sha, stbdev_err = self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )
    stbstb_sha, stbstb_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )
    stbstb_minus1_sha, stbstb_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B + "~1" )

    self.util_check_EQUAL( stbdev_err, 0, "must be craeted STB tag" )
    self.util_check_EQUAL( stbstb_err, 0, "must be craeted STB tag" )

    self.util_check_EQUAL( devbr_before_sha, stbdev_sha,  "STB tag on wrong commit" )
    self.util_check_EQUAL( stbbr_before_sha, stbstb_minus1_sha,  "STB tag on wrong commit" )

    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_minus1_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    self.util_check_NOTEQ( stbbr_before_sha, stbbr_after_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_minus1_after_sha, "stable not moved" )


  def test_Stabilize_01_03_STB_IntBrDev_fromDetached( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME ) #localize
    ##################
    out, errCode = self.sw_clo_h.int_branch_set( TEST_REPO_BR_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "settinf FTR intbr")

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch detached head" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, TEST_REPO_BR_DEV, TEST_REPO_BR_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize from detached head, without intbr set, specifying target" )
    ##################

    stbdev_sha, stbdev_err = self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )
    stbstb_sha, stbstb_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )
    stbstb_minus1_sha, stbstb_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B + "~1" )

    self.util_check_EQUAL( stbdev_err, 0, "must be craeted STB tag" )
    self.util_check_EQUAL( stbstb_err, 0, "must be craeted STB tag" )

    self.util_check_EQUAL( devbr_before_sha, stbdev_sha,  "STB tag on wrong commit" )
    self.util_check_EQUAL( stbbr_before_sha, stbstb_minus1_sha,  "STB tag on wrong commit" )

    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_minus1_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    self.util_check_NOTEQ( stbbr_before_sha, stbbr_after_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_minus1_after_sha, "stable not moved" )



  def test_Stabilize_01_04_STB_YesLbl( self ):

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

    out, errCode = self.sw_ori_h.set_cfg( self.CFG_ANYREF, "True" )
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
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )
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
    self.util_check_SUCC_scenario( out, errCode, "", "switch to br" )

    out, errCode = self.sw_ori_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Cannot execute this script on repository origin",
                                   "stabilize without stable branch tracked" )

    out, errCode = self.sw_clo_h.stabilize_stb( "Drop.A", "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Already exists a tag named",
                                   "stabilize without stable branch tracked" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize without stable branch tracked" )


  #
  # Test 1:
  #   stabilize gets a conflict in the middle
  #   resolve it
  #   re-issue with --force to complete
  #
  # Test 2:
  #   Now issue another stabilize,
  #   In order to complete we need:
  #     1. --force
  #     2. change LBL name
  #
  def test_Stabilize_01_05_STB_Conflict( self ):

    #clone repo
    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" )

    #genearte conflict
    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )
    out, errCode = self.sw_clo_h.modify_repo( filename = TEST_REPO_FILE_A, msg = "modif from develop" )
    self.util_check_SUCC_scenario( out, errCode, "", "modif from develop" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( TEST_REPO_BR_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to stable" )
    out, errCode = self.sw_clo_h.modify_repo( filename = TEST_REPO_FILE_A, msg = "modif from stable", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modif from stable" )

    out, errCode = self.sw_clo_h.branch_switch_to_int()
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode, "Merge conflict", "stabilize will conflict" )

    #no tag created
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[1], 1, "must not be craeted STB tag" )

    #resolve conflict, re-issue
    out, errCode = self.sw_clo_h.system_swgit( "add %s" % TEST_REPO_FILE_A )
    self.util_check_SUCC_scenario( out, errCode, "", "simulate resolving conflict" )
    out, errCode = self.sw_clo_h.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "committing resolved conflict" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "please provide --force option.",
                                   "stabilize from stable after resolve conflict" )

    #no tag created
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[1], 1, "must not be craeted STB tag" )

    # re-issue, without force
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode, "please provide --force option",
                                   "re-issue same stabilize after resolving conflict, but directly from stable" )

    #no tag created
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[1], 1, "must not be craeted STB tag" )

    #re-issue, forced
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH, force = True )
    self.util_check_SUCC_scenario( out, errCode, "",
                                   "re-issue same stabilize after resolving conflict" )

    #tag created
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[1], 0, "must be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[1], 0, "must be craeted STB tag" )


    ##########
    # TEST 2


    #re-issue same same
    out, errCode = self.sw_clo_h.branch_switch_to_int()
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode, "please provide --force option",
                                   "re-issue same stabilize after resolving conflict" )

    #re-issue, forced
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH, force = True )
    self.util_check_DENY_scenario( out, errCode,
                                   "Already exists a tag named",
                                   "re-issue same stabilize after just done stabilize" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_C, ORIG_REPO_DEVEL_BRANCH, force = True )
    self.util_check_SUCC_scenario( out, errCode, "",
                                   "re-issue same stabilize after just done stabilize" )

    #tag created
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_C )[1], 0, "must be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_C )[1], 0, "must be craeted STB tag" )

    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[0], 
                           self.sw_clo_h.ref2sha( self.CREATED_STBDEV_C )[0], "must be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[0], 
                           self.sw_clo_h.ref2sha( self.CREATED_STBSTB_C )[0], "must be craeted STB tag" )


  def test_Stabilize_02_00_LIV_NoLbl( self ):

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

    out, errCode = self.sw_ori_h.set_cfg( self.CFG_ANYREF, "True" )
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
    out, errCode = self.sw_clo_h.stabilize_liv( "FAILSREGEXP" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Please specify a valid name for label LIV",
                                   "stabilize with wrong regexp" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize outside stable" )

    devbr_afterB_sha, devbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterB_minus1_sha, stbbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivB_sha, stblivB_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterB_sha,  stblivB_sha, "livB label not created" )

    self.util_check_EQUAL( os.path.getsize( self.CHGLOG_B ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.FIXLOG_B ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.TKTLOG_B ), 0, "empty, chglog" )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_DENY_scenario( out, errCode,
                                   "Already exists a tag named",
                                   "re-issue same LIV" )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_C )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "issue Another LIV without no contributes" )

    devbr_afterC_sha, devbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterC_minus1_sha, devbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterC_sha, stbbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterC_minus1_sha, stbbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivC_sha, stblivC_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_C )

    self.util_check_EQUAL( devbr_afterC_minus1_sha, devbr_afterB_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterC_minus1_sha, stbbr_afterB_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_afterC_sha,  stblivC_sha, "liv label not created" )

    self.util_check_EQUAL( os.path.getsize( self.CHGLOG_C ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.FIXLOG_C ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.TKTLOG_C ), 0, "empty, chglog" )

    # no-merge-back
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_D, nomergeback = True )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "issue Another LIV without no contributes" )

    devbr_afterD_sha, devbr_afterD_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterD_minus1_sha, devbr_afterD_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterD_sha, stbbr_afterD_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterD_minus1_sha, stbbr_afterD_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivD_sha, stblivD_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_D )

    self.util_check_EQUAL( devbr_afterD_sha, devbr_afterC_sha, "develop MUST NOT move" )
    self.util_check_EQUAL( stbbr_afterD_minus1_sha, stbbr_afterC_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_afterD_sha,  stblivD_sha, "liv label not created" )

    self.util_check_EQUAL( os.path.getsize( self.CHGLOG_D ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.FIXLOG_D ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.TKTLOG_D ), 0, "empty, chglog" )

  def test_Stabilize_02_01_LIV_YesLbl( self ):

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

    out, errCode = self.sw_ori_h.set_cfg( self.CFG_ANYREF, "True" )
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
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stabilize anyref" )


    out, errCode = self.sw_clo_h.stabilize_liv( "FAILSREGEXP" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Please specify a valid name for label LIV",
                                   "stabilize with wrong regexp" )

    out, errCode = self.sw_clo_h.stabilize_liv( "Drop.A" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Already exists a tag named",
                                   "stabilize without src" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    #note, strange, no stab never done => 
    #  create another LIV withour reporting nothing on stable, but it is possible
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize without stable branch tracked" )

    devbr_afterB_sha, devbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterB_minus1_sha, stbbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivB_sha, stblivB_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterB_sha,  stblivB_sha, "livB label not created" )


  def test_Stabilize_02_02_LIV_fromFTR( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize from another branch" )

    devbr_after_sha, devbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_after_minus1_sha, devbr_after_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_after_minus1_sha, stbbr_after_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stbliv_sha, stbliv_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_after_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_after_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_after_sha,  stbliv_sha, "liv label not created" )


  def test_Stabilize_02_03_LIV_fromDetached( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME  )
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize from another branch" )

    devbr_after_sha, devbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_after_minus1_sha, devbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_after_minus1_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stbliv_sha, stbliv_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_after_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_after_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_after_sha,  stbliv_sha, "liv label not created" )


  #
  # Test:
  #   making LIV without setting intbr either to develop or to stable
  #
  # Result:
  #   user can make LIV witout setting INTBR, very useful,
  #   BUT
  #   at least must checkout develop/stable branch 
  #    or
  #   provide it on command line
  #
  def test_Stabilize_02_04_LIV_OtherIntBr( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    #
    # intbr --> FTR
    #
    out, errCode = self.sw_clo_h.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "settinf FTR intbr")

    # stabilize from FTR (intbr FTR)
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_DENY_scenario( out, errCode,
                                   "Cannot deduce onto which branch to make stb/liv.",
                                   "stabilize from cb = FTR, with intbr = FTR, arg = None" )

    # stabilize from stable (intbr FTR)
    out, errCode = self.sw_clo_h.branch_switch_to_br( TEST_REPO_BR_STB )
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize from cb = stable, with intbr = FTR, arg = None" )

    devbr_afterB_sha, devbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterB_minus1_sha, stbbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivB_sha, stblivB_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterB_sha,  stblivB_sha, "livB label not created" )

    # go onto FTR 
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )

    #stabilize from FTR, arg = develop (intbr FTR)
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B, dstbr = TEST_REPO_BR_DEV )
    self.util_check_DENY_scenario( out, errCode,
                                   "Can create stb/liv only onto",
                                   "stabilize from cb = FTR, with intbr = FTR, arg = develop" )

    #stabilize from FTR, arg = stable (intbr FTR)
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_C, dstbr = TEST_REPO_BR_STB )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize from cb = FTR, with intbr = FTR, arg = stable" )

    devbr_afterC_sha, devbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterC_minus1_sha, devbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterC_sha, stbbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterC_minus1_sha, stbbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivC_sha, stblivC_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_C )

    self.util_check_EQUAL( devbr_afterC_minus1_sha, devbr_afterB_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterC_minus1_sha, stbbr_afterB_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_afterC_sha,  stblivC_sha, "liv label not created" )


    #
    # intbr --> INT/stable
    #
    out, errCode = self.sw_clo_h.int_branch_set( TEST_REPO_BR_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "setting stable intbr")

    # stabilize from FTR (intbr INT/stable)
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_D )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize from cb = FTR, with intbr = stable" )

    devbr_afterD_sha, devbr_afterD_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterD_minus1_sha, devbr_afterD_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterD_sha, stbbr_afterD_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterD_minus1_sha, stbbr_afterD_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivD_sha, stblivD_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_D )

    self.util_check_EQUAL( devbr_afterD_minus1_sha, devbr_afterC_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterD_minus1_sha, stbbr_afterC_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_afterD_sha,  stblivD_sha, "liv label not created" )



  def test_Stabilize_02_04_LIV_Conflict( self ):
    self.assertEqual( 1, 0, "TODO" )


  def test_Stabilize_03_00_STBLIV_NoLbl( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    #on ori move away from head (for push)
    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" )

    #on clone track stable
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )
    #out, errCode = self.sw_clo_h.branch_track( ORIG_REPO_STABLE_BRANCH )
    #self.util_check_SUCC_scenario( out, errCode, "", "tracking stable int" )

    sha_before, errCode = self.sw_clo_h.get_currsha()
    self.util_check_SUCC_scenario( out, errCode, "", "get sha before" )

    sha_stb_before, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" )

    sha_dev_before, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" )

    self.util_check_EQUAL   ( sha_before, sha_dev_before, "NOT on develop before starting stb" )
    self.assertNotEqual( sha_dev_before, sha_stb_before, "develop and stable must differ" )

    #make stb
    ################################################
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize --stb" )
    ################################################

    sha_dev_after_stb, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" )
    sha_stb_after_stb, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" )
    sha_STBDEV, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBDEV_B )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on develop" )
    sha_STBSTB, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBSTB_B )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on stable" )
    sha_LIV, errCode = self.sw_clo_h.get_currsha( self.CREATED_LIV_B )
    self.util_check_DENY_scenario( out, errCode, "", "get sha LIV" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )


    self.util_check_EQUAL   ( sha_dev_before, sha_dev_after_stb, "" )
    self.util_check_EQUAL   ( sha_STBDEV,     sha_dev_after_stb, "" )
    self.util_check_EQUAL   ( sha_STBSTB,     sha_stb_after_stb, "" )
    self.assertNotEqual( sha_stb_before, sha_stb_after_stb, "" )

    #make liv
    ################################################
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize --liv" )
    ################################################


    sha_dev_after_liv, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" )
    sha_stb_afetr_liv, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" )
    sha_STBDEV, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBDEV_B )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on develop" )
    sha_STBSTB, errCode = self.sw_clo_h.get_currsha( self.CREATED_STBSTB_B )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha STB on stable" )
    sha_LIV, errCode = self.sw_clo_h.get_currsha( self.CREATED_LIV_B )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha LIV" )

    sha_LIV_minus1, errCode = self.sw_clo_h.get_currsha( "%s~1" % self.CREATED_LIV_B )
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
    self.util_check_EQUAL( sha_LIV_minus1   , sha_STBSTB       , "" )
    self.util_check_EQUAL( sha_dev_minus1   , sha_STBDEV       , "" )
    self.util_check_EQUAL( sha_dev_minus2   , sha_LIV          , "" )

    devbr_afterB_sha, devbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterB_minus1_sha, stbbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivB_sha, stblivB_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterB_sha,  stblivB_sha, "livB label not created" )

    self.assertTrue( os.path.exists( self.CHGLOG_B ), "chg file not found" )
    self.assertTrue( os.path.exists( self.FIXLOG_B ), "fix file not found" )
    self.assertTrue( os.path.exists( self.TKTLOG_B ), "tkt file not found" )


    #file content
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( self.BUILTIN_DEV_0, self.CHGLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.BUILTIN_DEV_0 )
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( self.BUILTIN_DEV_1, self.CHGLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.BUILTIN_DEV_1 )
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( self.BUILTIN_FIX_0, self.FIXLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.BUILTIN_FIX_0 )
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"^%s$\" %s" % ( self.DDTS, self.TKTLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.DDTS )


    notexistList = [ self.LBL_B, self.CREATED_STBDEV_B, self.CREATED_STBSTB_B ]
    for t in notexistList:
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.CHGLOG_B ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.FIXLOG_B ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"^%s$\" %s" % ( t, self.TKTLOG_B ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )


    #
    # LIV without previous STB
    #
    ################################################
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_C )
    self.util_check_SUCC_scenario( out, errCode, "", "issue Another LIV without no contributes" )
    ################################################

    devbr_afterC_sha, devbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterC_minus1_sha, devbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterC_sha, stbbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterC_minus1_sha, stbbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~1" )
    stblivC_sha, stblivC_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_C )

    self.util_check_EQUAL( devbr_afterC_minus1_sha, devbr_afterB_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterC_minus1_sha, stbbr_afterB_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_afterC_sha,  stblivC_sha, "liv label not created" )

    self.util_check_EQUAL( os.path.getsize( self.CHGLOG_C ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.FIXLOG_C ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.TKTLOG_C ), 0, "empty, chglog" )

    #file content
    notexistList = [ self.BUILTIN_DEV_0, self.BUILTIN_DEV_1, self.BUILTIN_FIX_0, self.DDTS, self.LBL_B, self.CREATED_STBDEV_B, self.CREATED_STBSTB_B ]
    for t in notexistList:
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.CHGLOG_C ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.FIXLOG_C ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"^%s$\" %s" % ( t, self.TKTLOG_C ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )


  def test_Stabilize_03_01_STBLIV_Toghether( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )

    #on ori move away from head (for push)
    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merge on int" )

    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    sha_before, errCode = self.sw_clo_h.get_currsha()
    self.util_check_SUCC_scenario( out, errCode, "", "get sha before" )

    sha_stb_before, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha stable branch" )

    sha_dev_before, errCode = self.sw_clo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "get sha develop branch" )

    self.util_check_EQUAL   ( sha_before, sha_dev_before, "NOT on develop before starting stb" )
    self.assertNotEqual( sha_dev_before, sha_stb_before, "develop and stable must differ" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    #make stb liv toghether
    ################################################
    out, errCode = self.sw_clo_h.stabilize_both( self.LBL_B, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize --stb" )
    ################################################

    devbr_afterB_sha, devbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterB_minus2_sha, stbbr_afterB_minus2_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~2" )
    stblivB_sha, stblivB_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_B )

    self.util_check_EQUAL( devbr_before_sha, devbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_afterB_minus2_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterB_sha,  stblivB_sha, "livB label not created" )

    self.assertTrue( os.path.exists( self.CHGLOG_B ), "chg file not found" )
    self.assertTrue( os.path.exists( self.FIXLOG_B ), "fix file not found" )
    self.assertTrue( os.path.exists( self.TKTLOG_B ), "tkt file not found" )


    #file content
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( self.BUILTIN_DEV_0, self.CHGLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.BUILTIN_DEV_0 )
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( self.BUILTIN_DEV_1, self.CHGLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.BUILTIN_DEV_1 )
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( self.BUILTIN_FIX_0, self.FIXLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.BUILTIN_FIX_0 )
    out, errCode = self.sw_clo_h.system_unix( "grep -e \"^%s$\" %s" % ( self.DDTS, self.TKTLOG_B ) )
    self.util_check_EQUAL( errCode, 0, "must exists %s" % self.DDTS )


    notexistList = [ self.LBL_B, self.CREATED_STBDEV_B, self.CREATED_STBSTB_B ]
    for t in notexistList:
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.CHGLOG_B ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.FIXLOG_B ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"^%s$\" %s" % ( t, self.TKTLOG_B ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )


    #
    # Another stb+liv (must be same result as previous test (splitted operations)
    #
    ################################################
    out, errCode = self.sw_clo_h.stabilize_both( self.LBL_C, TEST_REPO_BR_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "issue Another LIV without no contributes" )
    ################################################

    devbr_afterC_sha, devbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    devbr_afterC_minus1_sha, devbr_afterC_minus1_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV + "~1" )
    stbbr_afterC_sha, stbbr_afterC_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    stbbr_afterC_minus2_sha, stbbr_afterC_minus2_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB + "~2" )
    stblivC_sha, stblivC_err = self.sw_clo_h.ref2sha( self.CREATED_LIV_C )

    self.util_check_EQUAL( devbr_afterC_minus1_sha, devbr_afterB_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterC_minus2_sha, stbbr_afterB_sha, "stable not moved" )
    self.util_check_EQUAL( stbbr_afterC_sha,  stblivC_sha, "liv label not created" )

    self.util_check_EQUAL( os.path.getsize( self.CHGLOG_C ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.FIXLOG_C ), 0, "empty, chglog" )
    self.util_check_EQUAL( os.path.getsize( self.TKTLOG_C ), 0, "empty, chglog" )

    #file content
    notexistList = [ self.BUILTIN_DEV_0, self.BUILTIN_DEV_1, self.BUILTIN_FIX_0, self.DDTS, self.LBL_B, self.CREATED_STBDEV_B, self.CREATED_STBSTB_B ]
    for t in notexistList:
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.CHGLOG_C ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"Ref:.*%s\" %s" % ( t, self.FIXLOG_C ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )
      out, errCode = self.sw_clo_h.system_unix( "grep -e \"^%s$\" %s" % ( t, self.TKTLOG_C ) )
      self.util_check_NOTEQ( errCode, 0, "must NOT exists %s" % t )


    #
    # Another stb+liv, now providing stable branch
    #
    out, errCode = self.sw_clo_h.stabilize_both( self.LBL_D, TEST_REPO_BR_STB )
    self.util_check_DENY_scenario( out, errCode, 
                                   "please provide --force option.", 
                                   "issue Another LIV reporting INT/stable" )

    out, errCode = self.sw_clo_h.stabilize_both( self.LBL_D, TEST_REPO_BR_STB, force = True )
    self.util_check_SUCC_scenario( out, errCode, "", "issue Another LIV reporting INT/stable" )


  def test_Stabilize_04_00_CST_YesLbl( self ):

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
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize anyref" )


    #make stb already contained
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_STABLE_BRANCH )
    self.util_check_DENY_scenario( out, errCode,
                                   "please provide --force option.",
                                   "stabilize --cst" )

    #make stb
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, self.BUILTIN_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode,
                                   "",
                                   "stabilize --cst" )

    #make same label
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode,
                                   "Already exists a tag named",
                                   "stabilize --cst same label" )


  #
  # Test:
  #   stabilize can be done from any branch
  #   Here we test what happens when current branch is FTR 
  #   In the end with FTR intbr but cb == CST it should be possible
  def test_Stabilize_04_01_CST_fromFTR( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME ) #localize
    ##################
    out, errCode = self.sw_clo_h.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "settinf FTR intbr")
    ##################

    #stabilize with FTR intbr
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot deduce onto which branch to make stb/liv.", 
                                   "stabilize from branch, with FTR intbr" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch detached head" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "Cannot deduce onto which branch to make stb/liv.", 
                                   "stabilize from detached, with FTR intbr" )

    ##################
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.MYCST_FULL_BR ) #localize
    self.util_check_SUCC_scenario( out, errCode, "", "switch onto CST" )
    ##################
    cstbr_before_sha, cstbr_err = self.sw_clo_h.ref2sha( self.MYCST_FULL_BR )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, TEST_REPO_BR_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize from another branch" )

    stbdev_sha, stbdev_err = self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )
    stbstb_sha, stbstb_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )
    stbcst_sha, stbcst_err = self.sw_clo_h.ref2sha( self.CREATED_STBCST_B )
    stbcst_minus1_sha, stbcst_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_STBCST_B + "~1" )

    self.util_check_EQUAL( stbdev_err, 1, "must NOT be craeted STB tag" )
    self.util_check_EQUAL( stbstb_err, 1, "must NOT be craeted STB tag" )
    self.util_check_EQUAL( stbcst_err, 0, "must be craeted STB tag" )

    devbr_after_sha, devbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    self.util_check_EQUAL( devbr_before_sha, devbr_after_sha,  "develop untouched" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_after_sha,  "stable untouched" )
    self.util_check_EQUAL( cstbr_before_sha, stbcst_minus1_sha,  "cst upgraded" )

    cstbr_after_sha, cstbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    cstbr_minus1_after_sha, cstbr_after_err = self.sw_clo_h.ref2sha( self.MYCST_FULL_BR + "~1" )
    self.util_check_NOTEQ( cstbr_before_sha, cstbr_after_sha, "stable not moved" )
    self.util_check_EQUAL( cstbr_before_sha, cstbr_minus1_after_sha, "stable not moved" )


  def test_Stabilize_04_02_CST_IntBrFTRR_fromDetached( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    devbr_before_sha, devbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_before_sha, stbbr_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME ) #localize
    ##################
    out, errCode = self.sw_clo_h.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "settinf FTR intbr")
    ##################

    ##################
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch detached head" )
    ##################

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, TEST_REPO_BR_DEV, self.MYCST_FULL_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "When stabilizing, target branch", 
                                   "stabilize from another branch" )

    out, errCode = self.sw_clo_h.branch_switch_to_br( self.MYCST_FULL_BR ) #localize
    self.util_check_SUCC_scenario( out, errCode, "", "switch onto CST" )
    cstbr_before_sha, cstbr_err = self.sw_clo_h.ref2sha( self.MYCST_FULL_BR )

    ##################
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.MYCST_FULL_BR + "~1" ) #go detached
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, TEST_REPO_BR_DEV, self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize from another branch" )
    ##################

    stbdev_sha, stbdev_err = self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )
    stbstb_sha, stbstb_err = self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )
    stbcst_sha, stbcst_err = self.sw_clo_h.ref2sha( self.CREATED_STBCST_B )
    stbcst_minus1_sha, stbcst_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_STBCST_B + "~1" )

    self.util_check_EQUAL( stbdev_err, 1, "must NOT be craeted STB tag" )
    self.util_check_EQUAL( stbstb_err, 1, "must NOT be craeted STB tag" )
    self.util_check_EQUAL( stbcst_err, 0, "must be craeted STB tag" )

    devbr_after_sha, devbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_DEV )
    stbbr_after_sha, stbbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )

    self.util_check_EQUAL( devbr_before_sha, devbr_after_sha,  "develop untouched" )
    self.util_check_EQUAL( stbbr_before_sha, stbbr_after_sha,  "stable untouched" )
    self.util_check_EQUAL( cstbr_before_sha, stbcst_minus1_sha,  "cst upgraded" )

    cstbr_after_sha, cstbr_after_err = self.sw_clo_h.ref2sha( TEST_REPO_BR_STB )
    cstbr_minus1_after_sha, cstbr_after_err = self.sw_clo_h.ref2sha( self.MYCST_FULL_BR + "~1" )
    self.util_check_NOTEQ( cstbr_before_sha, cstbr_after_sha, "stable not moved" )
    self.util_check_EQUAL( cstbr_before_sha, cstbr_minus1_after_sha, "stable not moved" )




  #
  # Test 1:
  #   stabilize gets a conflict in the middle
  #   resolve it
  #   re-issue with --force to complete
  #
  # Test 2:
  #   Now issue another stabilize,
  #   In order to complete we need:
  #     1. --force
  #     2. change LBL name
  #
  def test_Stabilize_04_03_CST_Conflict( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    #switch to CST
    #set CST as INT BR
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to cst" )
    out, errCode = self.sw_clo_h.int_branch_set( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "set int branch to cst" )

    #genearte conflict
    out, errCode = self.sw_clo_h.modify_repo( filename = TEST_REPO_FILE_A, msg = "modif from cst", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modif from stable" )

    out, errCode = self.sw_clo_h.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )
    out, errCode = self.sw_clo_h.modify_repo( filename = TEST_REPO_FILE_A, msg = "modif from develop" )
    self.util_check_SUCC_scenario( out, errCode, "", "modif from develop" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode, "Merge conflict", "stabilize cst will conflict" )

    #CST creates STB tag only over CST branch
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBCST_B )[1], 1, "must be craeted STB tag" )

    #resolve conflict, re-issue
    out, errCode = self.sw_clo_h.system_swgit( "add %s" % TEST_REPO_FILE_A )
    self.util_check_SUCC_scenario( out, errCode, "", "simulate resolving conflict" )
    out, errCode = self.sw_clo_h.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "committing resolved conflict" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode, "please provide --force option",
                                   "re-issue same stabilize after resolving conflict" )


    #re-issue, forced
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH, force = True )
    self.util_check_SUCC_scenario( out, errCode, "",
                                   "re-issue same stabilize after resolving conflict" )

    #CST creates STB only onver CST branch
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_B )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBCST_B )[1], 0, "must be craeted STB tag" )


    ##########
    # TEST 2


    #re-issue same same
    out, errCode = self.sw_clo_h.branch_switch_to_int()
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH )
    self.util_check_DENY_scenario( out, errCode, "please provide --force option",
                                   "re-issue same stabilize after resolving conflict" )

    #re-issue, forced
    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_B, ORIG_REPO_DEVEL_BRANCH, force = True )
    self.util_check_DENY_scenario( out, errCode,
                                   "Already exists a tag named",
                                   "re-issue same stabilize after resolving conflict" )

    out, errCode = self.sw_clo_h.stabilize_stb( self.LBL_C, ORIG_REPO_DEVEL_BRANCH, force = True )
    self.util_check_SUCC_scenario( out, errCode, "",
                                   "re-issue same stabilize after resolving conflict" )

    #CST creates STB only onver CST branch
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBDEV_C )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBSTB_C )[1], 1, "must not be craeted STB tag" )
    self.util_check_EQUAL( self.sw_clo_h.ref2sha( self.CREATED_STBCST_C )[1], 0, "must be craeted STB tag" )


  #
  # Test 1:
  #   plain CST stabilize liv
  #
  # Test 2:
  #   from first CST, stabilize liv another CST
  #
  # Test 3:
  #   comeback on CST1 and, make liv without targetB
  #
  def test_Stabilize_05_00_CST_LIV( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to FTR on origin" )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B, self.MYCST_FULL_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "When stabilizing, target branch",
                                   "liv with not tracked CST" )

    out, errCode = self.sw_clo_h.branch_track( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "tracking CST" )
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to FTR" )

    cst1br_before_sha, cst1br_err = self.sw_clo_h.ref2sha( self.MYCST_FULL_BR )

    ################################################
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B, self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize liv, cb = FTR, intbr = develop, targetB = CST1" )
    ################################################

    livBcst1_sha, livBcst1_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST_B )
    livBcst1_minu1_sha, livBcst1_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST_B + "~1" )
    self.util_check_EQUAL( cst1br_before_sha, livBcst1_minu1_sha, "CST not moved" )

    #
    # Test2
    #
    out, errCode = self.sw_clo_h.branch_track( self.MYCST2_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "tracking stable int" )

    cst2br_before_sha, cst2br_err = self.sw_clo_h.ref2sha( self.MYCST2_FULL_BR )

    ################################################
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B, self.MYCST2_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize liv, cb = CST1, targetB = cst2" )
    ################################################

    livBcst2_sha, livBcst2_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST2_B )
    livBcst2_minu1_sha, livBcst2_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST2_B + "~1" )
    self.util_check_EQUAL( cst2br_before_sha, livBcst2_minu1_sha, "CST not moved" )

    #
    # Test3
    #
    ################################################
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to cst1" )
    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_C  )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize liv, cb = CST1, intbr = develop, targetB = None" )
    ################################################

    livCcst1_sha, livCcst1_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST_C )
    livCcst1_minu1_sha, livCcst1_minus1_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST_C + "~1" )
    self.util_check_EQUAL( livBcst1_sha, livCcst1_minu1_sha, "CST not moved" )


  #
  # Test 1:
  #   plain CST stabilize stb + liv
  #
  def test_Stabilize_05_00_CST_together( self ):

    self.util_clone_repo_stabilize( self.STABILIZE_CLONE_DIR, "" )
    out, errCode = self.sw_clo_h.set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = self.sw_ori_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to FTR on origin" )

    out, errCode = self.sw_clo_h.stabilize_liv( self.LBL_B, self.MYCST_FULL_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "When stabilizing, target branch",
                                   "liv with not tracked CST" )

    out, errCode = self.sw_clo_h.branch_track( self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "tracking CST" )
    out, errCode = self.sw_clo_h.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to FTR" )

    cst1br_before_sha, cst1br_err = self.sw_clo_h.ref2sha( self.MYCST_FULL_BR )

    ################################################
    out, errCode = self.sw_clo_h.stabilize_both( self.LBL_B, TEST_REPO_BR_DEV, self.MYCST_FULL_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize both, cb = FTR, intbr = develop, targetB = CST1" )
    ################################################

    livBcst1_sha, livBcst1_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST_B )
    livBcst1_minu2_sha, livBcst1_minus2_err = self.sw_clo_h.ref2sha( self.CREATED_LIVCST_B + "~2" )
    self.util_check_EQUAL( cst1br_before_sha, livBcst1_minu2_sha, "CST not moved" )



if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()






