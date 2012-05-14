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

#TODO conflicts

class Test_ProjStabilize( Test_ProjBase ):

  CFG_ANYREF = "swgit.stabilize-anyref"
  BRANCH_NAME        = "proj_stabilize"
  FULL_BRANCH_NAME   = "%s/%s/%s/FTR/%s" % (  REPO_TDM__REL, REPO_TDM__SREL, TEST_USER, BRANCH_NAME )

  CSTFS_FULL_BRANCH_NAME = "%s/%s/%s/FTR/%s" % (  REPO_FS__REL, REPO_FS__SREL, TEST_USER, BRANCH_NAME )
  DEVFS_FULL_BRANCH_NAME = "%s/%s/%s/FTR/%s" % (  REPO_FS__REL, REPO_FS__SREL, TEST_USER, BRANCH_NAME )
  DEVPLAT_FULL_BRANCH_NAME = "%s/%s/%s/FTR/%s" % (  REPO_PLAT__REL, REPO_PLAT__SREL, TEST_USER, BRANCH_NAME )
  CSTTDM_FULL_BRANCH_NAME = "%s/%s/FTR/%s" % (  CST_BRANCH_REL, TEST_USER, BRANCH_NAME )

  FULL_BRANCH_NAME_NEWTAG = "%s/NEW/BRANCH" % ( FULL_BRANCH_NAME ) 
  DDTS          = "Issue12345"
  CREATED_DEV_0  = "%s/DEV/000" % ( FULL_BRANCH_NAME )
  CREATED_FIX_0  = "%s/FIX/%s" % ( FULL_BRANCH_NAME, DDTS )

  PROJSTABILIZE_CLONE_DIR = SANDBOX + "TEST_PROJ_STABILIZE_CLONE"

  LBL_O = "Drop.O"
  LBL_B = "Drop.B"

  DEVTDM_LBL_B = "Drop.B"
  DEVTDM_CREATED_STBDEV_B = "%s/STB/%s" % ( REPO_TDM__DEVBRANCH, DEVTDM_LBL_B )
  DEVTDM_CREATED_STBSTB_B = "%s/STB/%s" % ( REPO_TDM__STBBRANCH, DEVTDM_LBL_B )
  DEVTDM_CREATED_STBFTR_B = "%s/STB/%s" % ( FULL_BRANCH_NAME, DEVTDM_LBL_B )
  DEVTDM_CREATED_LIV_B    = "%s/LIV/%s" % ( REPO_TDM__STBBRANCH, DEVTDM_LBL_B )
  DEVTDM_CHGLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.chg" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVTDM"), SWREPO_DIR, REPO_TDM__REL, REPO_TDM__SREL, DEVTDM_LBL_B )
  DEVTDM_FIXLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.fix" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVTDM"), SWREPO_DIR, REPO_TDM__REL, REPO_TDM__SREL, DEVTDM_LBL_B )
  DEVTDM_TKTLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVTDM"), SWREPO_DIR, REPO_TDM__REL, REPO_TDM__SREL, DEVTDM_LBL_B )

  DEVTDM_LBL_C = "Drop.C"

  DEVPLAT_LBL_B = "Drop.B"
  DEVPLAT_CREATED_STBDEV_B = "%s/STB/%s" % ( REPO_PLAT__DEVBRANCH, DEVPLAT_LBL_B )
  DEVPLAT_CREATED_STBSTB_B = "%s/STB/%s" % ( REPO_PLAT__STBBRANCH, DEVPLAT_LBL_B )
  DEVPLAT_CREATED_STBFTR_B = "%s/STB/%s" % ( FULL_BRANCH_NAME, DEVPLAT_LBL_B )
  DEVPLAT_CREATED_LIV_B    = "%s/LIV/%s" % ( REPO_PLAT__STBBRANCH, DEVPLAT_LBL_B )
  DEVPLAT_CHGLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.chg" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVPLAT"), SWREPO_DIR, REPO_PLAT__REL, REPO_PLAT__SREL, DEVPLAT_LBL_B )
  DEVPLAT_FIXLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.fix" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVPLAT"), SWREPO_DIR, REPO_PLAT__REL, REPO_PLAT__SREL, DEVPLAT_LBL_B )
  DEVPLAT_TKTLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVPLAT"), SWREPO_DIR, REPO_PLAT__REL, REPO_PLAT__SREL, DEVPLAT_LBL_B )

  DEVPLAT_LBL_C = "Drop.C"

  TSS100_LBL_B = "Drop.B"
  TSS100_CREATED_STBDEV_B = "%s/STB/%s" % ( REPO_TSS100__DEVBRANCH, TSS100_LBL_B )
  TSS100_CREATED_STBSTB_B = "%s/STB/%s" % ( REPO_TSS100__STBBRANCH, TSS100_LBL_B )
  TSS100_CREATED_STBFTR_B = "%s/STB/%s" % ( FULL_BRANCH_NAME, TSS100_LBL_B )
  TSS100_CREATED_LIV_B    = "%s/LIV/%s" % ( REPO_TSS100__STBBRANCH, TSS100_LBL_B )
  TSS100_CHGLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.chg" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("TSS100"), SWREPO_DIR, REPO_TSS100__REL, REPO_TSS100__SREL, TSS100_LBL_B )
  TSS100_FIXLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.fix" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("TSS100"), SWREPO_DIR, REPO_TSS100__REL, REPO_TSS100__SREL, TSS100_LBL_B )
  TSS100_TKTLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("TSS100"), SWREPO_DIR, REPO_TSS100__REL, REPO_TSS100__SREL, TSS100_LBL_B )

  TSS100_LBL_C = "Drop.C"

  CSTFS_LBL_B = "Drop.B"
  CSTFS_CREATED_STBDEV_B = "%s/STB/%s" % ( REPO_FS__DEVBRANCH, CSTFS_LBL_B )
  CSTFS_CREATED_STBSTB_B = "%s/STB/%s" % ( REPO_FS__STBBRANCH, CSTFS_LBL_B )
  CSTFS_CREATED_STBFTR_B = "%s/STB/%s" % ( FULL_BRANCH_NAME, CSTFS_LBL_B )
  CSTFS_CREATED_LIV_B    = "%s/LIV/%s" % ( REPO_FS__STBBRANCH, CSTFS_LBL_B )
  CSTFS_CHGLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.chg" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("CSTFS"), SWREPO_DIR, REPO_FS__REL, REPO_FS__SREL, CSTFS_LBL_B )
  CSTFS_FIXLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.fix" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("CSTFS"), SWREPO_DIR, REPO_FS__REL, REPO_FS__SREL, CSTFS_LBL_B )
  CSTFS_TKTLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("CSTFS"), SWREPO_DIR, REPO_FS__REL, REPO_FS__SREL, CSTFS_LBL_B )

  CSTFS_LBL_C = "Drop.C"


  srcfile = "/tmp/swgit_proj_stabilize_test.txt"

  srcobj_1_depth = {
      tss100_name2path( "TSS100"  ) : REPO_TSS100__DEVBRANCH,
      tss100_name2path( "DEVTDM"  ) : REPO_TDM__DEVBRANCH,
      tss100_name2path( "DEVPLAT" ) : REPO_PLAT__DEVBRANCH,
      #tss100_name2path( "CSTPLAT" ) : CST_BRANCH_FULLNAME,
      #tss100_name2path( "CSTTDM"  ) : CST_BRANCH_FULLNAME,
      }

  srcobj_2_depth = {
      tss100_name2path( "TSS100"  ) : REPO_TSS100__DEVBRANCH,
      tss100_name2path( "DEVTDM"  ) : REPO_TDM__DEVBRANCH,
      tss100_name2path( "DEVPLAT" ) : REPO_PLAT__DEVBRANCH,
      #tss100_name2path( "CSTPLAT" ) : REPO_PLAT__DEVBRANCH,
      #tss100_name2path( "CSTTDM"  ) : REPO_TDM__DEVBRANCH,
      tss100_name2path( "DEVFS"   ) : REPO_FS__DEVBRANCH,
      tss100_name2path( "DEVAPP"  ) : REPO_APP__DEVBRANCH,
      #tss100_name2path( "CSTFS"   ) : REPO_FS__DEVBRANCH,
      #tss100_name2path( "CSTAPP"  ) : REPO_APP__DEVBRANCH,
      }


  #This method is executed before each test_*
  def setUp( self ):
    super( Test_ProjStabilize, self ).setUp()


  #This method is executed after each test_*
  def tearDown( self ):
    super( Test_ProjStabilize, self ).tearDown()

  def SRCOBJ_2_STRLIST( self, obj ):
    return ",".join( [ "%s:%s" % ( k,v ) for k,v in obj.iteritems() ] )

  def SRCOBJ_2_FILE( self, obj, dstfile ):

    dstf = open( dstfile, 'w' )
    dstf.write( "\n".join( [ "%s:%s" % ( k,v ) for k,v in obj.iteritems() ] ) )
    dstf.close()



  # Test:
  #  Issueing a stabilize inside subrepo of project, 
  #  must have same result as inside plain repo
  #
  # Result:
  #  Here we stabilize a DEV label.
  #  We can see:
  #    1. STB label on starting point will be called like FTR/name/STB/Drop.B
  #       (note, no develop, because we use swgit tag and not git tag)
  #    2. strange merge this time because:
  #                                         
  #       develop    stable                 
  #        / |         |                      
  #     DEV--+-------->O                    
  #          |         |                    
  #          Y<--------X                    
  #       
  def test_ProjStabilize_00_00_SUBREPO_IN_PROJ( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )
    out, errCode = clo_valle_hm["DEVTDM"].stabilize_stb( self.DEVTDM_LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "only NGT labels are allowed to be stabilized",
                                   "not yet CFG_ANYREF" )

    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].stabilize_stb( self.DEVTDM_LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode, "please provide --force option.", "stabilize must work like plain repo" )

    out, errCode = clo_valle_hm["DEVTDM"].stabilize_stb( self.DEVTDM_LBL_B, "HEAD", force = True )
    self.util_check_DENY_scenario( out, errCode, "You must have a new commit to tag", "stabilize must work like plain repo" )

    out, errCode = clo_valle_hm["DEVTDM"].branch_switch_to_br( REPO_TDM__DEVBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to develop" )

    out, errCode = clo_valle_hm["DEVTDM"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    devbr_before_sha, devbr_err = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__DEVBRANCH )
    stbbr_before_sha, stbbr_err = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__STBBRANCH )
    ftrbr_before_sha, ftrbr_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME )

    ####################################
    out, errCode = clo_valle_hm["DEVTDM"].stabilize_stb( self.DEVTDM_LBL_B, "HEAD" )
    #out, errCode = clo_valle_hm["DEVTDM"].stabilize_stb( self.DEVTDM_LBL_B, self.FULL_BRANCH_NAME_NEWTAG, force = True )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize must work like plain repo" )
    ####################################

    stbdev_intra_sha, stbdev_intra_err = clo_valle_hm["DEVTDM"].ref2sha( self.DEVTDM_CREATED_STBDEV_B )
    stbstb_intra_sha, stbstb_intra_err = clo_valle_hm["DEVTDM"].ref2sha( self.DEVTDM_CREATED_STBSTB_B )
    stbftr_intra_sha, stbftr_intra_err = clo_valle_hm["DEVTDM"].ref2sha( self.DEVTDM_CREATED_STBFTR_B )
    stbftr_minus1_intra_sha, stbftr_minus1_intra_err = clo_valle_hm["DEVTDM"].ref2sha( self.DEVTDM_CREATED_STBFTR_B + "~1" )

    devbr_intra_sha, devbr_err = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__DEVBRANCH )
    stbbr_intra_sha, stbbr_err = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__STBBRANCH )
    ftrbr_intra_sha, ftrbr_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME )

    self.util_check_EQUAL( stbdev_intra_err, 1, "must NOT be craeted develop STB tag" )
    self.util_check_EQUAL( stbftr_intra_err, 0, "must be craeted feature STB tag" )
    self.util_check_EQUAL( stbstb_intra_err, 0, "must be craeted stable STB tag" )

    self.util_check_EQUAL( ftrbr_before_sha, stbftr_intra_sha,  "ftr STB tag on wrong commit" )
    self.util_check_EQUAL( stbbr_before_sha, stbftr_minus1_intra_sha,  "STB tag on wrong commit" )

    ####################################
    out, errCode = clo_valle_hm["DEVTDM"].stabilize_liv( self.DEVTDM_LBL_B )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize liv must work like plain repo" )
    ####################################

    devbr_afterB_sha, devbr_afterB_err               = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__DEVBRANCH )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__DEVBRANCH + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err               = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__STBBRANCH )
    stbbr_afterB_minus1_sha, stbbr_afterB_minus1_err = clo_valle_hm["DEVTDM"].ref2sha( REPO_TDM__STBBRANCH + "~1" )
    ftrbr_afterB_sha, ftrbr_afterB_err               = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME )
    ftrbr_afterB_minus1_sha, ftrbr_afterB_minus1_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME + "~1" )
    stblivB_sha, stblivB_err                         = clo_valle_hm["DEVTDM"].ref2sha( self.DEVTDM_CREATED_LIV_B )

    self.util_check_EQUAL( ftrbr_afterB_minus1_sha, devbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_intra_sha,  stbbr_afterB_minus1_sha, "develop not moved" )
    self.util_check_EQUAL( stbbr_afterB_sha, stblivB_sha, "livB label not created" )

    self.util_check_EQUAL( os.path.exists( self.DEVTDM_CHGLOG_B ), True, "empty, chglog" )
    self.util_check_EQUAL( os.path.exists( self.DEVTDM_FIXLOG_B ), True, "empty, fixlog" )
    self.util_check_EQUAL( os.path.exists( self.DEVTDM_TKTLOG_B ), True, "empty, tktlog" )


    #
    # Test 2
    #
    out, errCode = clo_valle_hm["DEVTDM"].branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch br" )
    out, errCode = clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev " )

    ####################################
    out, errCode = clo_valle_hm["DEVTDM"].stabilize_stb( self.DEVTDM_LBL_C, "HEAD", REPO_TDM__STBBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize with br arg must work like plain repo" )
    ####################################


  # Test:
  #  Issueing a stabilize inside root repo of project, 
  #  must have same result as inside plain repo
  #
  # Result:
  #  same as plain repo but with some proj --reset HEAD more
  #       
  def test_ProjStabilize_00_01_PROJROOT( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "HEAD" )
    self.util_check_DENY_scenario( out, errCode,
                                   "only NGT labels are allowed to be stabilized",
                                   "not yet CFG_ANYREF" )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )

    devbr_before_sha, devbr_err = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__DEVBRANCH )
    stbbr_before_sha, stbbr_err = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__STBBRANCH )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize must work like plain repo" )
    ####################################

    stbdev_intra_sha, stbdev_intra_err = clo_valle_hm["TSS100"].ref2sha( self.TSS100_CREATED_STBDEV_B )
    stbstb_intra_sha, stbstb_intra_err = clo_valle_hm["TSS100"].ref2sha( self.TSS100_CREATED_STBSTB_B )
    stbdev_minus1_intra_sha, stbdev_minus1_intra_err = clo_valle_hm["TSS100"].ref2sha( self.TSS100_CREATED_STBDEV_B + "~1" )

    devbr_intra_sha, devbr_err = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__DEVBRANCH )
    stbbr_intra_sha, stbbr_err = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__STBBRANCH )

    self.util_check_EQUAL( stbdev_intra_err, 0, "must be craeted feature STB tag" )
    self.util_check_EQUAL( stbstb_intra_err, 0, "must be craeted stable STB tag" )

    self.util_check_EQUAL( devbr_before_sha, stbdev_intra_sha,  "dev STB tag on wrong commit" )
    self.util_check_EQUAL( stbbr_before_sha, stbdev_minus1_intra_sha,  "STB tag on wrong commit" )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_liv( self.TSS100_LBL_B )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize liv must work like plain repo" )
    ####################################

    devbr_afterB_sha, devbr_afterB_err               = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__DEVBRANCH )
    devbr_afterB_minus1_sha, devbr_afterB_minus1_err = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__DEVBRANCH + "~1" )
    stbbr_afterB_sha, stbbr_afterB_err               = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__STBBRANCH )
    stbbr_afterB_minus1_sha, stbbr_afterB_minus1_err = clo_valle_hm["TSS100"].ref2sha( REPO_TSS100__STBBRANCH + "~1" )
    stblivB_sha, stblivB_err                         = clo_valle_hm["TSS100"].ref2sha( self.TSS100_CREATED_LIV_B )

    self.util_check_EQUAL( devbr_intra_sha, devbr_afterB_minus1_sha, "develop not moved one commit" )
    self.util_check_EQUAL( stbbr_intra_sha,  stbbr_afterB_minus1_sha, "stable not moved one commit" )
    self.util_check_EQUAL( stbbr_afterB_sha, stblivB_sha, "livB label not created" )

    self.util_check_EQUAL( os.path.exists( self.TSS100_CHGLOG_B ), True, "empty, chglog" )
    self.util_check_EQUAL( os.path.exists( self.TSS100_FIXLOG_B ), True, "empty, fixlog" )
    self.util_check_EQUAL( os.path.exists( self.TSS100_TKTLOG_B ), True, "empty, tktlog" )


    #
    # Test 2
    #
    out, errCode = clo_valle_hm["TSS100"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["TSS100"].modify_file( tss100_name2file("TSS100"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["TSS100"].commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev " )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_both( self.TSS100_LBL_C, "HEAD", REPO_TSS100__STBBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize with br arg must work like plain repo" )
    ####################################


  # Test:
  #  test src option with different values
  #
  def test_ProjStabilize_01_00_STB_SRC_strlist( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    #empty val
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = ""
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Wrong formatted comma-separed list at position", 
                                   "stabilize src strlist wrong val" )

    #empty key
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )
    srcstrlist += ",:HEAD"

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid path", 
                                   "stabilize src strlist wrong val" )

    #no comma
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )
    srcstrlist += ".:HEAD"

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Wrong formatted comma-separed list at position",
                                   "stabilize src strlist wrong val" )

    #parameter twice
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )
    srcstrlist += ",.:HEAD"

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "listed more than once.",
                                   "stabilize src strlist wrong val" )

    #not exists reference
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = "AAA"
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid reference.",
                                   "stabilize src strlist wrong val" )

    #not exists dir
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["ABC"] = "AAA"
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid path.",
                                   "stabilize src strlist wrong val" )

    #space in the middle
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = wrong_src_obj["."] + " "
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid branch onto which to make stb/liv.",
                                   "stabilize src strlist wrong val" )

    #all ok
    ok_src_obj = copy.deepcopy( self. srcobj_1_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( ok_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "only NGT labels are allowed to be stabilized",
                                   "stabilize src strlist wrong val" )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize src strlist wrong val" )


    out, errCode = clo_valle_hm["DEVTDM"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "please provide --force option.",
                                   "stabilize src strlist wrong val" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist, force = True )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Already exists a tag named",
                                   "stabilize src strlist wrong val" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B + "_1", srcstrlist, force = True )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize src strlist wrong val" )

  def test_ProjStabilize_01_01_STB_SRC_file( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )


    #empty val
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = ""
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid reference.",
                                   "stabilize src srcfile wrong val" )

    #empty key
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )
    os.system( "echo '\n%s' >> %s" % ( ":HEAD", self.srcfile ) )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid path", 
                                   "stabilize src srcfile wrong val" )

    #no comma
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )
    os.system( "echo '%s' >> %s" % ( ":HEAD", self.srcfile ) )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Wrong formatted line",
                                   "stabilize src srcfile wrong val" )

    #parameter twice
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )
    os.system( "echo '\n%s' >> %s" % ( ",.:HEAD", self.srcfile ) )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "listed more than once.",
                                   "stabilize src srcfile wrong val" )

    #not exists reference
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = "AAA"
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid reference.",
                                   "stabilize src srcfile wrong val" )

    #not exists dir
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["ABC"] = "AAA"
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid path.",
                                   "stabilize src srcfile wrong val" )

    #space in the middle for file works
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = " " + wrong_src_obj["."]
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "only NGT labels are allowed to be stabilized",
                                   "stabilize src srcfile wrong val" )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize src srcfile wrong val" )

  def test_ProjStabilize_01_02_00_STB_SRC_file_comments( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    #comment on line
    wrong_src_obj = copy.deepcopy( self. srcobj_1_depth )
    wrong_src_obj["."] = wrong_src_obj["."] + "# comment"
    self.SRCOBJ_2_FILE( wrong_src_obj, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize src srcfile wrong val" )

  # To test it, comment '.' line and check stabilize complains it is missing
  def test_ProjStabilize_01_02_01_STB_SRC_file_comments( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    commented_line_obj = {
        "#" + tss100_name2path( "TSS100"  ) : REPO_TSS100__DEVBRANCH,
        tss100_name2path( "DEVTDM"  ) : REPO_TDM__DEVBRANCH,
        tss100_name2path( "DEVPLAT" ) : REPO_PLAT__DEVBRANCH,
        }
    self.SRCOBJ_2_FILE( commented_line_obj, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Option -S/--source not conatining '.' entry, using HEAD", 
                                   "stabilize src srcfile wrong val" )


  # Test:
  #  test src option with different values
  #
  def test_ProjStabilize_01_03_STB_SRC_strlist_depth2( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    #empty val sec level
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    wrong_src_obj[tss100_name2path("DEVFS")] = ""
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Wrong formatted comma-separed list at position", 
                                   "stabilize src strlist wrong val" )

    #empty key
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )
    srcstrlist += ",:HEAD"

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid path", 
                                   "stabilize src strlist wrong val" )

    #no comma
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )
    srcstrlist += ".:HEAD"

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Wrong formatted comma-separed list at position",
                                   "stabilize src strlist wrong val" )

    #parameter twice sec level
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )
    srcstrlist += ",%s:HEAD" % tss100_name2path("DEVFS")

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "listed more than once.",
                                   "stabilize src strlist wrong val" )

    #not exists reference
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    wrong_src_obj[tss100_name2path("DEVFS")] = "AAA"
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid reference.",
                                   "stabilize src strlist wrong val" )

    #not exists dir sec level
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    wrong_src_obj["%s/ABC" % tss100_name2path("DEVFS")] = "AAA"
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid path.",
                                   "stabilize src strlist wrong val" )

    #space in the middle
    wrong_src_obj = copy.deepcopy( self. srcobj_2_depth )
    wrong_src_obj["."] = wrong_src_obj["."] + " "
    srcstrlist = self.SRCOBJ_2_STRLIST( wrong_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid branch onto which to make stb/liv.",
                                   "stabilize src strlist wrong val" )

    #all ok
    ok_src_obj = copy.deepcopy( self. srcobj_2_depth )
    srcstrlist = self.SRCOBJ_2_STRLIST( ok_src_obj )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not directly contained into current project.",
                                   "stabilize src strlist wrong val" )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not directly contained into current project.",
                                   "stabilize src strlist wrong val" )


    out, errCode = clo_valle_hm["DEVTDM"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    #also sec level checked for NGT
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not directly contained into current project.",
                                   "stabilize src strlist wrong val" )

    out, errCode = clo_valle_hm["DEVFS"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVAPP"].set_cfg( self.CFG_ANYREF, "True" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not directly contained into current project.",
                                   "stabilize src strlist wrong val" )

  # Test:
  #  test modifications into submodules before stabilizing
  #  test develops into DEVTDM
  #  test develops into DEVFS
  #  test provides src for 1 level only [ ., DEVTDM, DEVPLAT ]
  #
  def test_ProjStabilize_01_04_STB_checklocalstatus( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    #status on first level
    out, errCode = clo_valle_hm["DEVTDM"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Locally modified file(s) detected.",
                                   "stabilize modifiedcontent into submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   tss100_name2file( "DEVTDM" ),
                                   "stabilize modifiedcontent into submod" )

    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    #status on second level
    out, errCode = clo_valle_hm["DEVFS"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVFS"].modify_file( tss100_name2file("DEVFS"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Locally modified file(s) detected.",
                                   "stabilize modifiedcontent into sub submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   tss100_name2file( "DEVFS" ),
                                   "stabilize modifiedcontent into sub submod" )

    out, errCode = clo_valle_hm["DEVFS"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    #status on second CST level
    out, errCode = clo_valle_hm["CSTFS"].branch_create_src( self.BRANCH_NAME, REPO_FS__DEVBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["CSTFS"].modify_file( tss100_name2file("CSTFS"), msg = "a content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Locally modified file(s) detected.",
                                   "stabilize modifiedcontent into sub submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   tss100_name2file( "CSTFS" ),
                                   "stabilize modifiedcontent into sub submod" )

    out, errCode = clo_valle_hm["CSTFS"].int_branch_set( REPO_FS__DEVBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "set int branch to cst" )

    out, errCode = clo_valle_hm["CSTFS"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    #now should work
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize modifiedcontent into sub submod" )

  def test_ProjStabilize_01_05_STB_uninited( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    #un-init DEVTDM
    out, errCode = clo_valle_hm["TSS100"].proj_UNinit( tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid reference.",
                                   "stabilize modifiedcontent into submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   tss100_name2path( "DEVTDM" ),
                                   "stabilize modifiedcontent into submod" )


    self.SRCOBJ_2_FILE( self.srcobj_1_depth, self.srcfile )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, self.srcfile )
    self.util_check_DENY_scenario( out, errCode, 
                                   "invalid reference.",
                                   "stabilize src srcfile wrong val" )
    self.util_check_DENY_scenario( out, errCode, 
                                   tss100_name2path( "DEVTDM" ),
                                   "stabilize modifiedcontent into submod" )


  # Test:
  #  1.:  modify DEVTDM but do not include it into srclist => no change
  #  2.: now include it into srclist => change
  #
  # Result:
  #  Without src is like freezing only root repo
  #
  # NOTE:
  #  An option could occour asking to select ALL-HEADs when reporting
  #    (no proj --reset HEAD will be done)
  #  But like default behaviour it could be dangerous because clone 
  #    puts on develop HEAD for each DEV repo, and we do not want to 
  #    stabilize it
  #
  ##################################################################
  # Note:
  #  everithing specified is freezed in current commit
  #  everithing NOT specified: proj --reset HEAD will select for us
  ##################################################################
  def test_ProjStabilize_02_00_STB_DEVrepo( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )

    tss100_intbr_beforeB_sha, tss100_intbr_beforeB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_beforeB_err, 0, "must exists" )
    devtdm_intbr_beforeB_sha, devtdm_intbr_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_beforeB_err, 0, "must exists" )
    devplat_intbr_beforeB_sha, devplat_intbr_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_beforeB_err, 0, "must exists" )
    csttdm_intbr_beforeB_sha, csttdm_intbr_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_beforeB_err, 0, "must exists" )
    cstplat_intbr_beforeB_sha, cstplat_intbr_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_beforeB_err, 0, "must exists" )

    tss100_head_beforeB_sha, tss100_head_beforeB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_beforeB_err, 0, "must exists" )
    devtdm_head_beforeB_sha, devtdm_head_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_beforeB_err, 0, "must exists" )
    devplat_head_beforeB_sha, devplat_head_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_beforeB_err, 0, "must exists" )
    csttdm_head_beforeB_sha, csttdm_head_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_beforeB_err, 0, "must exists" )
    cstplat_head_beforeB_sha, cstplat_head_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_beforeB_err, 0, "must exists" )


    #
    # DEVTDM moves from develop, but no one provides it during satbilize => no change
    #
    CONTENT = "a content"
    out, errCode = clo_valle_hm["DEVTDM"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = CONTENT )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    #check preview
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "", f_preview = True )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod PREVIEW" )

    #first stabilize will report all modules onto stable
    repos = ( "DEVTDM"  , "DEVPLAT" , "CSTPLAT" , "CSTTDM" )
    for r in repos:
      err = "Must report default intbr for %s onto stable into file default_int_branches.cfg" % r
      self.assertTrue( "+%s:%s" % (tss100_name2path(r),tss100_name2intbr(r)) in out, err )

    #stab without lower modules
    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod" )
    ####################################

    tss100_intbr_intraB_sha, tss100_intbr_intraB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraB_err, 0, "must exists" )
    devtdm_intbr_intraB_sha, devtdm_intbr_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraB_err, 0, "must exists" )
    devplat_intbr_intraB_sha, devplat_intbr_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraB_err, 0, "must exists" )
    csttdm_intbr_intraB_sha, csttdm_intbr_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraB_err, 0, "must exists" )
    cstplat_intbr_intraB_sha, cstplat_intbr_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraB_err, 0, "must exists" )

    tss100_head_intraB_sha, tss100_head_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraB_err, 0, "must exists" )
    devtdm_head_intraB_sha, devtdm_head_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraB_err, 0, "must exists" )
    devplat_head_intraB_sha, devplat_head_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraB_err, 0, "must exists" )
    csttdm_head_intraB_sha, csttdm_head_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraB_err, 0, "must exists" )
    cstplat_head_intraB_sha, cstplat_head_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraB_err, 0, "must exists" )

    tss100_head_hat2_intraB_sha, tss100_head_hat2_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "^2" )
    self.util_check_EQUAL( tss100_head_hat2_intraB_err, 0, "must exists" )
    devtdm_ftrbr_intraB_sha, devtdm_ftrbr_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME )
    self.util_check_EQUAL( devtdm_ftrbr_intraB_err, 0, "must exists" )
    devtdm_ftrbr_minus1_intraB_sha, devtdm_ftrbr_minus1_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_EQUAL( devtdm_ftrbr_minus1_intraB_err, 0, "must exists" )

    self.util_check_EQUAL( tss100_intbr_beforeB_sha, tss100_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_beforeB_sha, devtdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_beforeB_sha, devplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_beforeB_sha, csttdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_beforeB_sha, cstplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( tss100_head_beforeB_sha, tss100_head_hat2_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_beforeB_sha, devtdm_ftrbr_minus1_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_intraB_sha, devtdm_head_beforeB_sha, "moved" )
    self.util_check_EQUAL( devplat_head_beforeB_sha, devplat_head_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_head_beforeB_sha, csttdm_head_intraB_sha, "moved" )

    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment


    #
    #test swgit proj -C
    #
    repos_heads = {
        "TSS100"  : tss100_head_intraB_sha, #this has moved instead
        "DEVTDM"  : devtdm_head_beforeB_sha,
        "DEVPLAT" : devplat_head_beforeB_sha,
        "CSTPLAT" : cstplat_head_beforeB_sha,
        "CSTTDM"  : csttdm_head_beforeB_sha,
        }
    for (reponame, repohead) in repos_heads.items():

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --get-configspec | grep -e '^\%s' | cut -d : -f 2 | cut -c 2-" % tss100_name2path(reponame) )
      self.util_check_SUCC_scenario( out, errCode, 
                                     repohead,
                                     "making diff" )



    #
    # Test 2 now merge DEVTDM on develop and provide src = DEVTDM:develop 
    #
    ####################################
    out, errCode = clo_valle_hm["DEVTDM"].branch_switch_to_br( self.FULL_BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to br" )
    out, errCode = clo_valle_hm["DEVTDM"].merge_on_int()
    self.util_check_SUCC_scenario( out, errCode, "", "merged on INT" )
    out, errCode = clo_valle_hm["TSS100"].branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to INT" )
    #srcstrlist = "%s:%s" % (tss100_name2path("DEVTDM"), tss100_name2intbr("DEVTDM"))
    srcstrlist = "%s:HEAD" % (tss100_name2path("DEVTDM"))
    ####################################

    #check preview
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_C, srcstrlist, force = True , f_preview = True)
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod PREVIEW" )

    #first stabilize will report all modules onto stable
    #second stabilize will not, so check they are no more present
    repos = ( "DEVTDM"  , "DEVPLAT" , "CSTPLAT" , "CSTTDM" )
    for r in repos:
      err = "Must report default intbr for %s onto stable into file default_int_branches.cfg" % r
      self.assertTrue( "+%s:%s" % (tss100_name2path(r),tss100_name2intbr(r)) not in out, err )

    #second stabilize will report only CONTENT
    self.assertTrue( "+%s" % CONTENT in out, "Must find this modification" )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_C, srcstrlist, force = True )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod" )
    ####################################

    tss100_intbr_intraC_sha, tss100_intbr_intraC_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraC_err, 0, "must exists" )
    devtdm_intbr_intraC_sha, devtdm_intbr_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraC_err, 0, "must exists" )
    devplat_intbr_intraC_sha, devplat_intbr_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraC_err, 0, "must exists" )
    csttdm_intbr_intraC_sha, csttdm_intbr_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraC_err, 0, "must exists" )
    cstplat_intbr_intraC_sha, cstplat_intbr_intraC_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraC_err, 0, "must exists" )

    tss100_head_intraC_sha, tss100_head_intraC_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraC_err, 0, "must exists" )
    devtdm_head_intraC_sha, devtdm_head_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraC_err, 0, "must exists" )
    devplat_head_intraC_sha, devplat_head_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraC_err, 0, "must exists" )
    csttdm_head_intraC_sha, csttdm_head_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraC_err, 0, "must exists" )
    cstplat_head_intraC_sha, cstplat_head_intraC_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraC_err, 0, "must exists" )

    devtdm_intbr_minus1_intraC_sha, devtdm_intbr_intraC_minus1_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") + "~1" )
    self.util_check_EQUAL( devtdm_intbr_intraC_minus1_err, 0, "must exists" )
    tss100_head_minus1_intraC_sha, tss100_head_minus1_intraC_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "~1" )
    self.util_check_EQUAL( tss100_head_minus1_intraC_err, 0, "must exists" )
    devtdm_ftrbr_intraC_sha, devtdm_ftrbr_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME )
    self.util_check_EQUAL( devtdm_ftrbr_intraC_err, 0, "must exists" )
    devtdm_ftrbr_minus1_intraC_sha, devtdm_ftrbr_minus1_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( self.FULL_BRANCH_NAME + "~1" )
    self.util_check_EQUAL( devtdm_ftrbr_minus1_intraC_err, 0, "must exists" )


    self.util_check_EQUAL( tss100_intbr_intraB_sha, tss100_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_intraB_sha, devtdm_intbr_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_intraB_sha, devplat_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_intraB_sha, csttdm_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_intraB_sha, cstplat_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( tss100_head_intraB_sha, tss100_head_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_intraB_sha, devtdm_ftrbr_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( devplat_head_intraB_sha, devplat_head_intraC_sha, "moved" )
    self.util_check_EQUAL( csttdm_head_intraB_sha, csttdm_head_intraC_sha, "moved" )

    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) 

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) 

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff HEAD~1 HEAD %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" ) 

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff HEAD~1 HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" ) 

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive HEAD~1 HEAD" )
    self.util_check_SUCC_scenario( out, errCode,
                                   "+Subproject commit %s" % devtdm_intbr_intraC_sha,
                                   "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" ) 


    #
    #test swgit proj -C
    #
    repos_heads = {
        "TSS100"  : tss100_head_intraC_sha,  #this has moved
        "DEVTDM"  : devtdm_intbr_intraC_sha, #this has moved
        "DEVPLAT" : devplat_head_beforeB_sha,
        "CSTPLAT" : cstplat_head_beforeB_sha,
        "CSTTDM"  : csttdm_head_beforeB_sha,
        }
    for (reponame, repohead) in repos_heads.items():

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --get-configspec | grep -e '^\%s' | cut -d : -f 2 | cut -c 2-" % tss100_name2path(reponame) )
      self.util_check_SUCC_scenario( out, errCode, 
                                     repohead,
                                     "making diff" )


  # Test:
  #  1.: modify DEVPLAT but do not include it into srclist => no change
  #  2.: now include it into srclist => change
  #
  # Result:
  #  Without src is like freezing only root repo
  #
  # NOTE:
  #  An option could occour asking to select ALL-HEADs when reporting
  #    (no proj --reset HEAD will be done)
  #  But like default behaviour it could be dangerous because clone 
  #    puts on develop HEAD for each DEV repo, and we do not want to 
  #    stabilize it
  #
  ##################################################################
  # Note:
  #  everithing specified is freezed in current commit
  #  everithing NOT specified: proj --reset HEAD will select for us
  ##################################################################
  def test_ProjStabilize_02_01_STB_DEVproj( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    tss100_intbr_beforeB_sha, tss100_intbr_beforeB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_beforeB_err, 0, "must exists" )
    devtdm_intbr_beforeB_sha, devtdm_intbr_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_beforeB_err, 0, "must exists" )
    devplat_intbr_beforeB_sha, devplat_intbr_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_beforeB_err, 0, "must exists" )
    csttdm_intbr_beforeB_sha, csttdm_intbr_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_beforeB_err, 0, "must exists" )
    cstplat_intbr_beforeB_sha, cstplat_intbr_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_beforeB_err, 0, "must exists" )

    tss100_head_beforeB_sha, tss100_head_beforeB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_beforeB_err, 0, "must exists" )
    devtdm_head_beforeB_sha, devtdm_head_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_beforeB_err, 0, "must exists" )
    devplat_head_beforeB_sha, devplat_head_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_beforeB_err, 0, "must exists" )
    csttdm_head_beforeB_sha, csttdm_head_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_beforeB_err, 0, "must exists" )
    cstplat_head_beforeB_sha, cstplat_head_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_beforeB_err, 0, "must exists" )


    #
    # DEVPLAT moves from develop, but no one provides it during satbilize => no change
    #
    CONTENT = "a content"
    out, errCode = clo_valle_hm["DEVPLAT"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = CONTENT )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVPLAT"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod" )

    tss100_intbr_intraB_sha, tss100_intbr_intraB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraB_err, 0, "must exists" )
    devtdm_intbr_intraB_sha, devtdm_intbr_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraB_err, 0, "must exists" )
    devplat_intbr_intraB_sha, devplat_intbr_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraB_err, 0, "must exists" )
    csttdm_intbr_intraB_sha, csttdm_intbr_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraB_err, 0, "must exists" )
    cstplat_intbr_intraB_sha, cstplat_intbr_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraB_err, 0, "must exists" )

    tss100_head_intraB_sha, tss100_head_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraB_err, 0, "must exists" )
    devtdm_head_intraB_sha, devtdm_head_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraB_err, 0, "must exists" )
    devplat_head_intraB_sha, devplat_head_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraB_err, 0, "must exists" )
    csttdm_head_intraB_sha, csttdm_head_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraB_err, 0, "must exists" )
    cstplat_head_intraB_sha, cstplat_head_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraB_err, 0, "must exists" )

    tss100_head_hat2_intraB_sha, tss100_head_hat2_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "^2" )
    self.util_check_EQUAL( tss100_head_hat2_intraB_err, 0, "must exists" )
    devplat_ftrbr_intraB_sha, devplat_ftrbr_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( self.DEVPLAT_FULL_BRANCH_NAME )
    self.util_check_EQUAL( devplat_ftrbr_intraB_err, 0, "must exists" )
    devplat_ftrbr_minus1_intraB_sha, devplat_ftrbr_minus1_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( self.DEVPLAT_FULL_BRANCH_NAME + "~1" )
    self.util_check_EQUAL( devplat_ftrbr_minus1_intraB_err, 0, "must exists" )

    self.util_check_EQUAL( tss100_intbr_beforeB_sha, tss100_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_beforeB_sha, devtdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_beforeB_sha, devplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_beforeB_sha, csttdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_beforeB_sha, cstplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( tss100_head_beforeB_sha, tss100_head_hat2_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_head_beforeB_sha, devplat_ftrbr_minus1_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_intraB_sha, devtdm_head_beforeB_sha, "moved" )
    self.util_check_EQUAL( devplat_head_beforeB_sha, devplat_head_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_head_beforeB_sha, csttdm_head_intraB_sha, "moved" )

    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("DEVPLAT") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment


    #
    #test swgit proj -C
    #
    repos_heads = {
        "TSS100"  : tss100_head_intraB_sha, #this has moved instead
        "DEVTDM"  : devtdm_head_beforeB_sha,
        "DEVPLAT" : devplat_head_beforeB_sha,
        "CSTPLAT" : cstplat_head_beforeB_sha,
        "CSTTDM"  : csttdm_head_beforeB_sha,
        }
    for (reponame, repohead) in repos_heads.items():

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --get-configspec | grep -e '^\%s' | cut -d : -f 2 | cut -c 2-" % tss100_name2path(reponame) )
      self.util_check_SUCC_scenario( out, errCode, 
                                     repohead,
                                     "making diff" )



    #
    # Test 2 now merge DEVPLAT on develop and provide src = DEVPLAT:develop 
    #
    ####################################
    out, errCode = clo_valle_hm["DEVPLAT"].branch_switch_to_br( self.DEVPLAT_FULL_BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to br" )
    out, errCode = clo_valle_hm["DEVPLAT"].merge_on_int()
    self.util_check_SUCC_scenario( out, errCode, "", "merged on INT" )
    out, errCode = clo_valle_hm["TSS100"].branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to INT" )
    #srcstrlist = "%s:%s" % (tss100_name2path("DEVPLAT"), tss100_name2intbr("DEVPLAT"))
    srcstrlist = "%s:HEAD" % (tss100_name2path("DEVPLAT"))
    ####################################

    #check preview
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_C, srcstrlist, force = True , f_preview = True)
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod PREVIEW" )

    #first stabilize will report all modules onto stable
    #second stabilize will not, so check they are no more present
    repos = ( "DEVTDM"  , "DEVPLAT" , "CSTPLAT" , "CSTTDM" )
    for r in repos:
      err = "Must report default intbr for %s onto stable into file default_int_branches.cfg" % r
      self.assertTrue( "+%s:%s" % (tss100_name2path(r),tss100_name2intbr(r)) not in out, err )

    #second stabilize will report only CONTENT
    self.assertTrue( "+%s" % CONTENT in out, "Must find this modification" )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_C, srcstrlist, force = True )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod" )
    ####################################

    tss100_intbr_intraC_sha, tss100_intbr_intraC_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraC_err, 0, "must exists" )
    devtdm_intbr_intraC_sha, devtdm_intbr_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraC_err, 0, "must exists" )
    devplat_intbr_intraC_sha, devplat_intbr_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraC_err, 0, "must exists" )
    csttdm_intbr_intraC_sha, csttdm_intbr_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraC_err, 0, "must exists" )
    cstplat_intbr_intraC_sha, cstplat_intbr_intraC_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraC_err, 0, "must exists" )

    tss100_head_intraC_sha, tss100_head_intraC_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraC_err, 0, "must exists" )
    devtdm_head_intraC_sha, devtdm_head_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraC_err, 0, "must exists" )
    devplat_head_intraC_sha, devplat_head_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraC_err, 0, "must exists" )
    csttdm_head_intraC_sha, csttdm_head_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraC_err, 0, "must exists" )
    cstplat_head_intraC_sha, cstplat_head_intraC_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraC_err, 0, "must exists" )

    devplat_intbr_minus1_intraC_sha, devplat_intbr_intraC_minus1_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") + "~1" )
    self.util_check_EQUAL( devplat_intbr_intraC_minus1_err, 0, "must exists" )
    tss100_head_minus1_intraC_sha, tss100_head_minus1_intraC_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "~1" )
    self.util_check_EQUAL( tss100_head_minus1_intraC_err, 0, "must exists" )
    devplat_ftrbr_intraC_sha, devplat_ftrbr_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( self.DEVPLAT_FULL_BRANCH_NAME )
    self.util_check_EQUAL( devplat_ftrbr_intraC_err, 0, "must exists" )
    devplat_ftrbr_minus1_intraC_sha, devplat_ftrbr_minus1_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( self.DEVPLAT_FULL_BRANCH_NAME + "~1" )
    self.util_check_EQUAL( devplat_ftrbr_minus1_intraC_err, 0, "must exists" )


    self.util_check_EQUAL( tss100_intbr_intraB_sha, tss100_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_intraB_sha, devtdm_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_intraB_sha, devplat_intbr_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_intraB_sha, csttdm_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_intraB_sha, cstplat_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( tss100_head_intraB_sha, tss100_head_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_intraB_sha, devtdm_head_intraC_sha, "moved" )
    self.util_check_EQUAL( devplat_head_intraB_sha, devplat_ftrbr_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( csttdm_head_intraB_sha, csttdm_head_intraC_sha, "moved" )

    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("DEVPLAT") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff HEAD~1 HEAD %s" % tss100_name2path("DEVPLAT") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff HEAD~1 HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive HEAD~1 HEAD" )
    self.util_check_SUCC_scenario( out, errCode,
                                   "+Subproject commit %s" % devplat_intbr_intraC_sha,
                                   "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" )


    #
    #test swgit proj -C
    #
    repos_heads = {
        "TSS100"  : tss100_head_intraC_sha,  #this has moved
        "DEVTDM"  : devtdm_head_beforeB_sha, 
        "DEVPLAT" : devplat_intbr_intraC_sha,#this has moved
        "CSTPLAT" : cstplat_head_beforeB_sha,
        "CSTTDM"  : csttdm_head_beforeB_sha,
        }
    for (reponame, repohead) in repos_heads.items():

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --get-configspec | grep -e '^\%s' | cut -d : -f 2 | cut -c 2-" % tss100_name2path(reponame) )
      self.util_check_SUCC_scenario( out, errCode, 
                                     repohead,
                                     "making diff" )

  # Test:
  #  1.: modify CSTTDM but do not include it into srclist => no change
  #  2.: now include it into srclist => change
  #
  # Result:
  #  Without src is like freezing only root repo
  #
  # NOTE:
  #  An option could occour asking to select ALL-HEADs when reporting
  #    (no proj --reset HEAD will be done)
  #  But like default behaviour it could be dangerous because clone 
  #    puts on develop HEAD for each DEV repo, and we do not want to 
  #    stabilize it
  #
  ##################################################################
  # Note:
  #  everithing specified is freezed in current commit
  #  everithing NOT specified: proj --reset HEAD will select for us
  ##################################################################
  def test_ProjStabilize_02_02_STB_CSTrepo( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["CSTTDM"].set_cfg( self.CFG_ANYREF, "True" )

    tss100_intbr_beforeB_sha, tss100_intbr_beforeB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_beforeB_err, 0, "must exists" )
    devtdm_intbr_beforeB_sha, devtdm_intbr_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_beforeB_err, 0, "must exists" )
    devplat_intbr_beforeB_sha, devplat_intbr_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_beforeB_err, 0, "must exists" )
    csttdm_intbr_beforeB_sha, csttdm_intbr_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_beforeB_err, 0, "must exists" )
    cstplat_intbr_beforeB_sha, cstplat_intbr_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_beforeB_err, 0, "must exists" )

    tss100_head_beforeB_sha, tss100_head_beforeB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_beforeB_err, 0, "must exists" )
    devtdm_head_beforeB_sha, devtdm_head_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_beforeB_err, 0, "must exists" )
    devplat_head_beforeB_sha, devplat_head_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_beforeB_err, 0, "must exists" )
    csttdm_head_beforeB_sha, csttdm_head_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_beforeB_err, 0, "must exists" )
    cstplat_head_beforeB_sha, cstplat_head_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_beforeB_err, 0, "must exists" )


    #
    # CSTTDM moves from develop, but no one provides it during satbilize => no change
    #
    CONTENT = "a content"
    out, errCode = clo_valle_hm["CSTTDM"].branch_create_src( self.BRANCH_NAME, tss100_name2intbr("CSTTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["CSTTDM"].modify_file( tss100_name2file("CSTTDM"), msg = CONTENT )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["CSTTDM"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod" )

    tss100_intbr_intraB_sha, tss100_intbr_intraB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraB_err, 0, "must exists" )
    devtdm_intbr_intraB_sha, devtdm_intbr_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraB_err, 0, "must exists" )
    devplat_intbr_intraB_sha, devplat_intbr_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraB_err, 0, "must exists" )
    csttdm_intbr_intraB_sha, csttdm_intbr_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraB_err, 0, "must exists" )
    cstplat_intbr_intraB_sha, cstplat_intbr_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraB_err, 0, "must exists" )

    tss100_head_intraB_sha, tss100_head_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraB_err, 0, "must exists" )
    devtdm_head_intraB_sha, devtdm_head_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraB_err, 0, "must exists" )
    devplat_head_intraB_sha, devplat_head_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraB_err, 0, "must exists" )
    csttdm_head_intraB_sha, csttdm_head_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraB_err, 0, "must exists" )
    cstplat_head_intraB_sha, cstplat_head_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraB_err, 0, "must exists" )

    tss100_head_hat2_intraB_sha, tss100_head_hat2_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "^2" )
    self.util_check_EQUAL( tss100_head_hat2_intraB_err, 0, "must exists" )
    csttdm_ftrbr_intraB_sha, csttdm_ftrbr_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( self.CSTTDM_FULL_BRANCH_NAME )
    self.util_check_EQUAL( csttdm_ftrbr_intraB_err, 0, "must exists" )
    csttdm_ftrbr_minus1_intraB_sha, csttdm_ftrbr_minus1_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( self.CSTTDM_FULL_BRANCH_NAME + "~1" )
    self.util_check_EQUAL( csttdm_ftrbr_minus1_intraB_err, 0, "must exists" )

    self.util_check_EQUAL( tss100_intbr_beforeB_sha, tss100_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_beforeB_sha, devtdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_beforeB_sha, devplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_beforeB_sha, csttdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_beforeB_sha, cstplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( tss100_head_beforeB_sha, tss100_head_hat2_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_head_beforeB_sha, devplat_head_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_beforeB_sha, devtdm_head_intraB_sha, "moved" )
    #moved back by proj --reset during stabilize
    self.util_check_EQUAL( csttdm_head_beforeB_sha, csttdm_head_intraB_sha, "moved" )
    self.util_check_EQUAL( cstplat_head_beforeB_sha, cstplat_head_intraB_sha, "moved" )

    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("CSTTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment


    #
    #test swgit proj -C
    #
    repos_heads = {
        "TSS100"  : tss100_head_intraB_sha, #this has moved instead
        "DEVTDM"  : devtdm_head_beforeB_sha,
        "DEVPLAT" : devplat_head_beforeB_sha,
        "CSTPLAT" : cstplat_head_beforeB_sha,
        "CSTTDM"  : csttdm_head_beforeB_sha,
        }
    for (reponame, repohead) in repos_heads.items():

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --get-configspec | grep -e '^\%s' | cut -d : -f 2 | cut -c 2-" % tss100_name2path(reponame) )
      self.util_check_SUCC_scenario( out, errCode, 
                                     repohead,
                                     "making diff" )



    #
    # Test 2 now merge CSTTDM on develop and provide src = CSTTDM:develop 
    #
    ####################################
    out, errCode = clo_valle_hm["CSTTDM"].branch_switch_to_br( self.CSTTDM_FULL_BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to br" )
    out, errCode = clo_valle_hm["CSTTDM"].merge_on_int()
    self.util_check_SUCC_scenario( out, errCode, "", "merged on INT" )
    out, errCode = clo_valle_hm["TSS100"].branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to INT" )

    #srcstrlist = "%s:%s" % (tss100_name2path("CSTTDM"), tss100_name2intbr("CSTTDM"))
    srcstrlist = "%s:HEAD" % (tss100_name2path("CSTTDM"))
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_C, srcstrlist, force = True )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into submod" )
    ####################################

    tss100_intbr_intraC_sha, tss100_intbr_intraC_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraC_err, 0, "must exists" )
    devtdm_intbr_intraC_sha, devtdm_intbr_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraC_err, 0, "must exists" )
    devplat_intbr_intraC_sha, devplat_intbr_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraC_err, 0, "must exists" )
    csttdm_intbr_intraC_sha, csttdm_intbr_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraC_err, 0, "must exists" )
    cstplat_intbr_intraC_sha, cstplat_intbr_intraC_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraC_err, 0, "must exists" )

    tss100_head_intraC_sha, tss100_head_intraC_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraC_err, 0, "must exists" )
    devtdm_head_intraC_sha, devtdm_head_intraC_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraC_err, 0, "must exists" )
    devplat_head_intraC_sha, devplat_head_intraC_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraC_err, 0, "must exists" )
    csttdm_head_intraC_sha, csttdm_head_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraC_err, 0, "must exists" )
    cstplat_head_intraC_sha, cstplat_head_intraC_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraC_err, 0, "must exists" )

    csttdm_intbr_minus1_intraC_sha, csttdm_intbr_intraC_minus1_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") + "~1" )
    self.util_check_EQUAL( csttdm_intbr_intraC_minus1_err, 0, "must exists" )
    tss100_head_minus1_intraC_sha, tss100_head_minus1_intraC_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "~1" )
    self.util_check_EQUAL( tss100_head_minus1_intraC_err, 0, "must exists" )
    csttdm_ftrbr_intraC_sha, csttdm_ftrbr_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( self.CSTTDM_FULL_BRANCH_NAME )
    self.util_check_EQUAL( csttdm_ftrbr_intraC_err, 0, "must exists" )
    csttdm_ftrbr_minus1_intraC_sha, csttdm_ftrbr_minus1_intraC_err = clo_valle_hm["CSTTDM"].ref2sha( self.CSTTDM_FULL_BRANCH_NAME + "~1" )
    self.util_check_EQUAL( csttdm_ftrbr_minus1_intraC_err, 0, "must exists" )


    self.util_check_EQUAL( tss100_intbr_intraB_sha, tss100_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_intraB_sha, devtdm_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_intraB_sha, devplat_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_intraB_sha, csttdm_intbr_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_intraB_sha, cstplat_intbr_intraC_sha, "moved" )
    self.util_check_EQUAL( tss100_head_intraB_sha, tss100_head_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_intraB_sha, devtdm_head_intraC_sha, "moved" )
    self.util_check_EQUAL( devplat_head_intraB_sha, devplat_head_intraC_sha, "moved" )
    self.util_check_EQUAL( csttdm_head_intraB_sha, csttdm_ftrbr_minus1_intraC_sha, "moved" )
    self.util_check_EQUAL( cstplat_head_intraB_sha, cstplat_head_intraC_sha, "moved" )

    #self.util_check_EQUAL( devplat_head_intraB_sha, devplat_ftrbr_minus1_intraC_sha, "moved" )
    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("CSTTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff HEAD~1 HEAD %s" % tss100_name2path("CSTTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff HEAD~1 HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" ) #this will be true in a moment

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive HEAD~1 HEAD" )
    self.util_check_SUCC_scenario( out, errCode,
                                   "+Subproject commit %s" % csttdm_intbr_intraC_sha,
                                   "making diff" )
    self.assertTrue( "+%s" % CONTENT in out, "Must not find modificcations" ) #this will be true in a moment


    #
    #test swgit proj -C
    #
    repos_heads = {
        "TSS100"  : tss100_head_intraC_sha,  #this has moved
        "DEVTDM"  : devtdm_head_beforeB_sha, 
        "DEVPLAT" : devplat_head_beforeB_sha,
        "CSTPLAT" : cstplat_head_beforeB_sha,
        "CSTTDM"  : csttdm_intbr_intraC_sha, #this has moved
        }
    for (reponame, repohead) in repos_heads.items():

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --get-configspec | grep -e '^\%s' | cut -d : -f 2 | cut -c 2-" % tss100_name2path(reponame) )
      self.util_check_SUCC_scenario( out, errCode, 
                                     repohead,
                                     "making diff" )


  #  I'm freezing on stable something not aligned (not clean), 
  #  because DEVPLAT marks new commits under it
  #
  #  This is like when I stabilize a contained project, but referencing a change 
  #   into its sub module only suitable for my project
  #
  #  vvvvvvvvvvvvvvvvvvvvv
  #  This is not possible: ONLY 1st LEVEL repos can be registered inside stabilzie
  #  ^^^^^^^^^^^^^^^^^^^^^
  #       Only 1 level submodules are sored inside proj repo
  #
  #  Also if i would freeze proj containing SUB SUBmod, where to do this, on which branch?
  #
  #
  #  If I proj --update after this:
  #   when subsubrepo is under CST -> ok, my local project will continue selecting it and never move
  #   when subsubrepo is under DEV -> I will go onto develop HEAD for that repo:
  #        this could be bad : maybe that commit shift during stabilize was done 
  #                            because develop was wrong =>
  #                            stable is now safe:
  #                                any proj --reset INT/stable will restore right commit
  #                                any proj --update will move onto subsubrepo devevlop HEAD
  #                            but this means develop must be restored as soon as possible.
  #                                it is not a proj --update problem, 
  #                                it is a developer committing that wrong commit problem
  #
  def test_ProjStabilize_02_03_STB_SUBSUB_DEVrepo( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVFS"].set_cfg( self.CFG_ANYREF, "True" )

    tss100_intbr_beforeB_sha, tss100_intbr_beforeB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_beforeB_err, 0, "must exists" )
    devtdm_intbr_beforeB_sha, devtdm_intbr_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_beforeB_err, 0, "must exists" )
    devplat_intbr_beforeB_sha, devplat_intbr_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_beforeB_err, 0, "must exists" )
    devfs_intbr_beforeB_sha, devfs_intbr_beforeB_err = clo_valle_hm["DEVFS"].ref2sha( tss100_name2intbr("DEVFS") )
    self.util_check_EQUAL( devfs_intbr_beforeB_err, 0, "must exists" )
    csttdm_intbr_beforeB_sha, csttdm_intbr_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_beforeB_err, 0, "must exists" )
    cstplat_intbr_beforeB_sha, cstplat_intbr_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_beforeB_err, 0, "must exists" )

    tss100_head_beforeB_sha, tss100_head_beforeB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_beforeB_err, 0, "must exists" )
    devtdm_head_beforeB_sha, devtdm_head_beforeB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_beforeB_err, 0, "must exists" )
    devplat_head_beforeB_sha, devplat_head_beforeB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_beforeB_err, 0, "must exists" )
    devfs_head_beforeB_sha, devfs_head_beforeB_err = clo_valle_hm["DEVFS"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devfs_head_beforeB_err, 0, "must exists" )
    csttdm_head_beforeB_sha, csttdm_head_beforeB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_beforeB_err, 0, "must exists" )
    cstplat_head_beforeB_sha, cstplat_head_beforeB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_beforeB_err, 0, "must exists" )


    #
    # DEVFS moves from develop, but no one provides it during satbilize => no change
    #
    CONTENT = "a content"
    out, errCode = clo_valle_hm["DEVFS"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVFS"].modify_file( tss100_name2file("DEVFS"), msg = CONTENT )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVFS"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )

    devfs_ftrbr_beforeB_sha, devfs_ftrbr_beforeB_err = clo_valle_hm["DEVFS"].ref2sha( self.DEVFS_FULL_BRANCH_NAME )
    self.util_check_EQUAL( devfs_ftrbr_beforeB_err, 0, "must exists" )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "%s:HEAD" % tss100_name2path("DEVFS") )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not directly contained into current project.", 
                                   "stabilize modifiedcontent into SUB SUBmod" )
    ####################################

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, "" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize modifiedcontent into SUB SUBmod" )

    tss100_intbr_intraB_sha, tss100_intbr_intraB_err = clo_valle_hm["TSS100"].ref2sha( tss100_name2intbr("TSS100") )
    self.util_check_EQUAL( tss100_intbr_intraB_err, 0, "must exists" )
    devtdm_intbr_intraB_sha, devtdm_intbr_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( tss100_name2intbr("DEVTDM") )
    self.util_check_EQUAL( devtdm_intbr_intraB_err, 0, "must exists" )
    devplat_intbr_intraB_sha, devplat_intbr_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( tss100_name2intbr("DEVPLAT") )
    self.util_check_EQUAL( devplat_intbr_intraB_err, 0, "must exists" )
    csttdm_intbr_intraB_sha, csttdm_intbr_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( tss100_name2intbr("CSTTDM") )
    self.util_check_EQUAL( csttdm_intbr_intraB_err, 0, "must exists" )
    cstplat_intbr_intraB_sha, cstplat_intbr_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( tss100_name2intbr("CSTPLAT") )
    self.util_check_EQUAL( cstplat_intbr_intraB_err, 0, "must exists" )

    tss100_head_intraB_sha, tss100_head_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" )
    self.util_check_EQUAL( tss100_head_intraB_err, 0, "must exists" )
    devtdm_head_intraB_sha, devtdm_head_intraB_err = clo_valle_hm["DEVTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devtdm_head_intraB_err, 0, "must exists" )
    devplat_head_intraB_sha, devplat_head_intraB_err = clo_valle_hm["DEVPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( devplat_head_intraB_err, 0, "must exists" )
    csttdm_head_intraB_sha, csttdm_head_intraB_err = clo_valle_hm["CSTTDM"].ref2sha( "HEAD" )
    self.util_check_EQUAL( csttdm_head_intraB_err, 0, "must exists" )
    cstplat_head_intraB_sha, cstplat_head_intraB_err = clo_valle_hm["CSTPLAT"].ref2sha( "HEAD" )
    self.util_check_EQUAL( cstplat_head_intraB_err, 0, "must exists" )

    tss100_head_hat2_intraB_sha, tss100_head_hat2_intraB_err = clo_valle_hm["TSS100"].ref2sha( "HEAD" + "^2" )
    self.util_check_EQUAL( tss100_head_hat2_intraB_err, 0, "must exists" )

    self.util_check_EQUAL( tss100_intbr_beforeB_sha, tss100_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_intbr_beforeB_sha, devtdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_intbr_beforeB_sha, devplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_intbr_beforeB_sha, csttdm_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( cstplat_intbr_beforeB_sha, cstplat_intbr_intraB_sha, "moved" )
    self.util_check_EQUAL( tss100_head_beforeB_sha, tss100_head_hat2_intraB_sha, "moved" )
    self.util_check_EQUAL( devtdm_head_beforeB_sha, devtdm_head_intraB_sha, "moved" )
    self.util_check_EQUAL( devplat_head_beforeB_sha, devplat_head_intraB_sha, "moved" )
    self.util_check_EQUAL( csttdm_head_beforeB_sha, csttdm_head_intraB_sha, "moved" )
    self.util_check_EQUAL( cstplat_head_beforeB_sha, cstplat_head_intraB_sha, "moved" )

    #
    #test swgit proj -D
    #
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff %s" % tss100_name2path("DEVFS") )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository", 
                                   "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "proj --diff --recursive" )
    self.util_check_SUCC_scenario( out, errCode, "", "making diff" )
    self.assertTrue( "+%s" % CONTENT not in out, "Must not find modificcations" )



  # Result:
  #  DEVFS (second level) cannot be directly freezed. 
  #        (see Test_ProjStabilize.test_ProjStabilize_02_03_STB_SUBSUB_DEVrepo)
  #  Here we stabilize inside DEVPLAT and then inside TSS100
  # 
  def test_ProjStabilize_02_04_STB_DEVproj_DEVrepo( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    shamap_intbr_va_clonetime = self.util_map2_tss100intbrshas( clo_valle_hm )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVFS"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    #stabilize first time all submodules into DEVPLAT
    strlist = "%s:%s" % ( plat_name2path("DEVFS"), tss100_name2intbr("DEVFS") )
    out, errCode = clo_valle_hm["DEVPLAT"].stabilize_both( self.LBL_O, strlist, force = True, f_preview = True )
    self.util_check_DENY_scenario( out, errCode, "Not found valid version for subrepo", "stabilize DEVPLAT" )
    out, errCode = clo_valle_hm["DEVPLAT"].stabilize_both( self.LBL_O, strlist, force = True, f_preview = False )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize DEVPLAT" )

    #stabilize first time all submodules into TSS100 (DEVPLAT not mentioned into srclist)
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.LBL_O, "" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize project" )

    shamap_intbr_va_afterO = self.util_map2_tss100intbrshas( clo_valle_hm )
    shamap_heads_va_afterO = self.util_map2_currshas( clo_valle_hm )

    # check from TSS100 by specifying DEVFS -> error because is depth2
    #
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.LBL_O, "%s:HEAD" % tss100_name2path("DEVFS"), force = True, f_preview = True )
    self.util_check_DENY_scenario( out, errCode,
                                   "is not directly contained into current project", 
                                   "stabilize modifiedcontent into TSS100 submod PREVIEW" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.LBL_O, "%s:HEAD" % tss100_name2path("DEVFS"), f_preview = False )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not directly contained into current project.", 
                                   "stabilize modifiedcontent into TSS100 submod PREVIEW" )



    # DEVrepo d2 (depth2) contribute
    CONTENT = "a content"
    out, errCode = clo_valle_hm["DEVFS"].branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "swith to int br" )
    out, errCode = clo_valle_hm["DEVFS"].branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create br" )
    out, errCode = clo_valle_hm["DEVFS"].modify_file( tss100_name2file("DEVFS"), msg = CONTENT )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = clo_valle_hm["DEVFS"].commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" )
    out, errCode = clo_valle_hm["DEVFS"].merge_on_int()
    self.util_check_SUCC_scenario( out, errCode, "", "merged on INT" )

    devfs_ftrbr_beforeB_sha, devfs_ftrbr_beforeB_err = clo_valle_hm["DEVFS"].ref2sha( self.DEVFS_FULL_BRANCH_NAME )
    self.util_check_EQUAL( devfs_ftrbr_beforeB_err, 0, "must exists" )


    #
    #stabilize DEVFS int DEVPLAT
    #
    out, errCode = clo_valle_hm["DEVPLAT"].branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "swith to int br" )

    strlist = "%s:%s" % ( plat_name2path("DEVFS"), tss100_name2intbr("DEVFS") )
    out, errCode = clo_valle_hm["DEVPLAT"].stabilize_both( self.LBL_B, strlist, force = True, f_preview = True )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize DEVPLAT" )
    self.assertTrue( "+%s" % CONTENT in out, "stabilizing contribute into DEVFS" )

    ####################################
    out, errCode = clo_valle_hm["DEVPLAT"].stabilize_both( self.LBL_B, strlist, force = True, f_preview = False )
    ####################################
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize DEVPLAT" )

    liv_after_platB_sha, liv_after_platB_err = clo_valle_hm["DEVPLAT"].ref2sha( self.DEVPLAT_CREATED_LIV_B )
    self.util_check_EQUAL( liv_after_platB_err, 0, "must exists" )

    shamap_intbr_va_after_platB = self.util_map2_tss100intbrshas( clo_valle_hm )
    shamap_heads_va_after_platB = self.util_map2_currshas( clo_valle_hm )

    self.util_assert_EQ_UNEQ_maps( shamap_heads_va_afterO, 
                                   shamap_heads_va_after_platB, 
                                   [], # empty => all
                                   [ "DEVPLAT", "DEVFS" ],
                                   "FAILED stabilize inside DEVPLAT to freeze DEFVS"
                                 )

    #
    #stabilize TSS100 referring DEVPLAT just created label
    #
    out, errCode = clo_valle_hm["TSS100"].branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "swith to int br" )

    strlist = "%s:%s" % (tss100_name2path("DEVPLAT"), self.DEVPLAT_CREATED_LIV_B)

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.LBL_B, strlist, force = True, f_preview = True )
    ####################################
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize tss100 with DEVFS upgrage (by upgrading DEVPLAT)" )
    self.assertTrue( "+%s" % CONTENT in out, "stabilizing DEVFS contribute into TSS100" )

    submod_upgrade = "+Subproject commit %s" % shamap_intbr_va_after_platB["DEVFS"]
    self.assertTrue( submod_upgrade in out, "stabilizing DEVFS contribute into TSS100" )

    shamap_intbr_va_after_tss100B = self.util_map2_tss100intbrshas( clo_valle_hm )
    shamap_heads_va_after_tss100B = self.util_map2_currshas( clo_valle_hm )

    self.util_assert_EQ_UNEQ_maps( shamap_heads_va_after_platB, 
                                   shamap_heads_va_after_tss100B, 
                                   [], # empty => all
                                   [ "TSS100" ],
                                   "FAILED stabilize inside TSS100 to freeze DEFVS passing by DEVPLAT"
                                 )

    ####################################
    out, errCode = clo_valle_hm["TSS100"].stabilize_liv( self.LBL_B )
    ####################################
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize LIV tss100 with DEVFS upgrage (by upgrading DEVPLAT)" )



  #
  # LIV is identical to any plain repo, all work is done during --stb.
  #
  def test_ProjStabilize_03_00_LIV( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize superproj" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_liv( self.TSS100_LBL_B )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize modifiedcontent into sub submod" )

    liv_afterB_sha, liv_afterB_err = clo_valle_hm["TSS100"].ref2sha( self.TSS100_CREATED_LIV_B )
    self.util_check_EQUAL( liv_afterB_err, 0, "must exists" )


  def test_ProjStabilize_04_00_BOTH( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_both( self.TSS100_LBL_B, srcstrlist )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize superproj" )

    liv_afterB_sha, liv_afterB_err = clo_valle_hm["TSS100"].ref2sha( self.TSS100_CREATED_LIV_B )
    self.util_check_EQUAL( liv_afterB_err, 0, "must exists" )


    
  #
  # Test:
  #   after LIV, make an update
  #
  def test_ProjStabilize_05_00_Update( self ):
    self.assertEqual( 1, 0, "TODO" )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()




