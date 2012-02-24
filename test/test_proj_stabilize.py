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

  FULL_BRANCH_NAME_NEWTAG = "%s/NEW/BRANCH" % ( FULL_BRANCH_NAME ) 
  DDTS          = "Issue12345"
  CREATED_DEV_0  = "%s/DEV/000" % ( FULL_BRANCH_NAME )
  CREATED_FIX_0  = "%s/FIX/%s" % ( FULL_BRANCH_NAME, DDTS )

  PROJSTABILIZE_CLONE_DIR = SANDBOX + "TEST_PROJ_STABILIZE_CLONE"

  DEVTDM_LBL_B = "Drop.B"
  DEVTDM_CREATED_STBDEV_B = "%s/STB/%s" % ( REPO_TDM__DEVBRANCH, DEVTDM_LBL_B )
  DEVTDM_CREATED_STBSTB_B = "%s/STB/%s" % ( REPO_TDM__STBBRANCH, DEVTDM_LBL_B )
  DEVTDM_CREATED_STBFTR_B = "%s/STB/%s" % ( FULL_BRANCH_NAME, DEVTDM_LBL_B )
  DEVTDM_CREATED_LIV_B    = "%s/LIV/%s" % ( REPO_TDM__STBBRANCH, DEVTDM_LBL_B )
  DEVTDM_CHGLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.chg" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVTDM"), SWREPO_DIR, REPO_TDM__REL, REPO_TDM__SREL, DEVTDM_LBL_B )
  DEVTDM_FIXLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.fix" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVTDM"), SWREPO_DIR, REPO_TDM__REL, REPO_TDM__SREL, DEVTDM_LBL_B )
  DEVTDM_TKTLOG_B = "%s/%s/%s/changelog/%s/%s/LIV_%s.tkt" % ( PROJSTABILIZE_CLONE_DIR, tss100_name2path("DEVTDM"), SWREPO_DIR, REPO_TDM__REL, REPO_TDM__SREL, DEVTDM_LBL_B )

  DEVTDM_LBL_C = "Drop.C"

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
      #tss100_name2path( "CSTPLAT" ) : REPO_PLAT__DEVBRANCH,
      #tss100_name2path( "CSTTDM"  ) : REPO_TDM__DEVBRANCH,
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
    self.util_check_DENY_scenario( out, errCode, 
                                   "only NGT labels are allowed to be stabilized",
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



  # Test:
  #  test modifications into submodules before stabilizing
  #  test develops into DEVTDM
  #  test develops into DEVFS
  #  test provides src for [ ., DEVTDM, DEVPLAT ]
  #
  # Result:
  #  DEVFS is freezed on current HEAD because it is not provided into src list.
  #  but DEVPLAT is freezed by src.
  #  I'm freezing on stable something not aligned (clean), 
  #  because DEVPLAT marks new commits under it
  #
  #  This is like when I stabilize a contained project, but referencing a change 
  #   into its sub module only suitable for my project
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
  def test_ProjStabilize_02_00_STB_checklocalstatus( self ):
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

    #TODO check an test this situation:
    #stabilize:
    # DEVTDM has specified value into srcstrlist (no change)
    # DEVFS is not specified into srcstrlist => HEAD is taken => changes because test develops there



  def test_ProjStabilize_03_00_LIV( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.PROJSTABILIZE_CLONE_DIR, f_integrator = True )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.PROJSTABILIZE_CLONE_DIR )

    out, errCode = clo_valle_hm["TSS100"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVTDM"].set_cfg( self.CFG_ANYREF, "True" )
    out, errCode = clo_valle_hm["DEVPLAT"].set_cfg( self.CFG_ANYREF, "True" )

    srcstrlist = self.SRCOBJ_2_STRLIST( self.srcobj_1_depth )

    out, errCode = clo_valle_hm["TSS100"].stabilize_stb( self.TSS100_LBL_B, srcstrlist )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize modifiedcontent into sub submod" )

    out, errCode = clo_valle_hm["TSS100"].stabilize_liv( self.TSS100_LBL_B )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "stabilize modifiedcontent into sub submod" )



  def test_ProjStabilize_04_00_STBLIV( self ):
    self.assertEqual( 1, 0, "TODO" )

    
  #
  # Test:
  #   after LIV, make an update
  #
  def test_ProjStabilize_05_00_Update( self ):
    self.assertEqual( 1, 0, "TODO" )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()




