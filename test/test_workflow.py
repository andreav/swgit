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


class Test_Workflow( Test_ProjBase ):
  WORKFLOW_CLONE_DIR    = SANDBOX + "TEST_WORKFLOW_CLONE"
  WORKFLOW_CLONE_2_DIR  = SANDBOX + "TEST_WORKFLOW_CLONE_2"
  BRANCH_NAME         = "test_workflow"
  FULL_BRANCH_NAME    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, BRANCH_NAME )

  FEATURE_BRANCH_NAME = "feature"
  FULL_FEATURE_BRANCH_NAME_DEV    = "%s/%s/%s/INT/%s_develop" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, FEATURE_BRANCH_NAME )
  FULL_FEATURE_BRANCH_NAME_STB    = "%s/%s/%s/INT/%s_stable" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, FEATURE_BRANCH_NAME )
  FEATURE_LIV_NAME      = "Drop.G"
  FEATURE_LIV_FULL_NAME = "%s/LIV/%s" % ( FULL_FEATURE_BRANCH_NAME_STB, FEATURE_LIV_NAME )

  MODIF_BRANCH_NAME = "modif"
  FULL_MODIF_BRANCH_NAME    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, MODIF_BRANCH_NAME )

  #This method is executed before each test_*
  def setUp( self ):
    super( Test_Workflow, self ).setUp()

    self.sw_clonerepo_h      = swgit__utils( self.WORKFLOW_CLONE_DIR )
    self.sw_clonerepo_2_h    = swgit__utils( self.WORKFLOW_CLONE_2_DIR )

    shutil.rmtree( self.WORKFLOW_CLONE_DIR, True )
    shutil.rmtree( self.WORKFLOW_CLONE_2_DIR, True )
    

  #This method is executed after each test_*
  def tearDown( self ):
    super( Test_Workflow, self ).tearDown()

  def test_workflow_01_00_cloneOfClone( self ):
    self.assertEqual( 1, 0, "TODO" )

  #
  # Test:
  #   testing shared feature repo:
  #     clone repo
  #     create branch
  #     set as int-br
  #     push on origin
  #
  def test_workflow_02_00_teamFeature_sharedBranch( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.WORKFLOW_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.WORKFLOW_CLONE_DIR ) 

    # create shared branch
    out, errCode = self.sw_clonerepo_h.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED create branch" ) 

    out, errCode = self.sw_clonerepo_h.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "setting shared branch as int" ) 

    out, errCode = self.sw_clonerepo_h.push()
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    out, errCode = self.sw_origrepo_h.get_currsha( self.FULL_BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "check origin has %s" % self.FULL_BRANCH_NAME )

    #check is also tracked
    out, errCode = self.sw_clonerepo_h.branch_list_track()
    self.assertTrue( self.FULL_BRANCH_NAME in out, "branch not tracked" )


  #
  # Test:
  #   testing feature INT branches:
  #     clone repo
  #     init new branche features
  #     push on origin
  #
  #   clone 2 will develop, stabilize, merge on mainstream
  #
  #
  def test_workflow_02_01_teamFeature_newINTpair_plainMerge( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.WORKFLOW_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.WORKFLOW_CLONE_DIR ) 

    out, errCode = self.sw_clonerepo_h.init_src( ORIG_REPO_DEVEL_BRANCH, c = self.FEATURE_BRANCH_NAME, )
    self.util_check_SUCC_scenario( out, errCode, "", "creating feature INT branches" ) 

    out, errCode = self.sw_clonerepo_h.push()
    self.util_check_DENY_scenario( out, errCode, "Cannot directly push a develop branch.", "push" )

    out, errCode = self.sw_clonerepo_h.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, "is empty, no-op", "push with merge" )

    out, errCode = self.sw_clonerepo_h.int_branch_set( self.FULL_FEATURE_BRANCH_NAME_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "restoring old INT branch" )

    out, errCode = self.sw_clonerepo_h.push()
    self.util_check_SUCC_scenario( out, errCode, "", "push new iNT branch" )

    out, errCode = self.sw_origrepo_h.get_currsha( self.FULL_FEATURE_BRANCH_NAME_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "check origin has %s" % self.FULL_FEATURE_BRANCH_NAME_DEV )
    out, errCode = self.sw_origrepo_h.get_currsha( self.FULL_FEATURE_BRANCH_NAME_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "check origin has %s" % self.FULL_FEATURE_BRANCH_NAME_STB )

    #check is also tracked
    out, errCode = self.sw_clonerepo_h.branch_list_track()
    self.assertTrue( self.FULL_FEATURE_BRANCH_NAME_DEV in out, "branch not tracked" )
    self.assertTrue( self.FULL_FEATURE_BRANCH_NAME_STB not in out, "branch not tracked" )

    #
    # clone 2
    #
    sha_dev_orig_beforeclone2, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    #clone integartor
    out, errCode = swgit__utils.clone_scripts_repo_integrator( self.WORKFLOW_CLONE_2_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.WORKFLOW_CLONE_2_DIR ) 

    #set int br manually after
    out, errCode = self.sw_clonerepo_2_h.int_branch_set( self.FULL_FEATURE_BRANCH_NAME_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "setting wnew INT branch as integration branch" ) 

    #create topic branch
    out, errCode = self.sw_clonerepo_2_h.branch_switch_to_int()
    out, errCode = self.sw_clonerepo_2_h.branch_create( self.MODIF_BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED create branch" ) 

    #push mofic and check nothing happened on INT/develop
    out, errCode = self.sw_clonerepo_2_h.modify_file( ORIG_REPO_aFILE, "modif for feature" )
    out, errCode = self.sw_clonerepo_2_h.commit_minusA_dev( "commit feature" )
    out, errCode = self.sw_clonerepo_2_h.push_with_merge( remote )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED pushing on origin" ) 

    sha_dev_orig_afterclone2push, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    self.assertEqual( sha_dev_orig_beforeclone2,
                      sha_dev_orig_afterclone2push,
                      "orig/ INT/develop must NOT change after clone2 push" )

    #stabilize this feature
    out, errCode = self.sw_clonerepo_2_h.set_cfg( "swgit.stabilize-anyref", "True" )
    out, errCode = self.sw_clonerepo_2_h.branch_switch_to_int()
    out, errCode = self.sw_clonerepo_2_h.stabilize_stb( self.FEATURE_LIV_NAME, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize STB feature develop" ) 
    out, errCode = self.sw_clonerepo_2_h.stabilize_liv( self.FEATURE_LIV_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize LIV feature develop" ) 

    sha_dev_orig_afterclone2stabilize, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    self.assertEqual( sha_dev_orig_beforeclone2,
                      sha_dev_orig_afterclone2stabilize,
                      "orig/ INT/develop must NOT change afetr clone2 stabilize" )

    #imagine we want to merge last feature LIV

    #restore old intbr
    out, errCode = self.sw_clonerepo_2_h.int_branch_set( ORIG_REPO_DEVEL_BRANCH)
    self.util_check_SUCC_scenario( out, errCode, "", "restoring old INT branch" )
    out, errCode = self.sw_clonerepo_2_h.branch_switch_to_int()

    #merge liv
    out, errCode = self.sw_clonerepo_2_h.merge( self.FEATURE_LIV_FULL_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merging last feature LIV" )
    
    #push, will fail due to checkout develop
    out, errCode = self.sw_clonerepo_2_h.push( )
    self.util_check_DENY_scenario( out, errCode, "refusing to update checked out branch:", "push" )

    #re-push
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_STABLE_BRANCH )
    out, errCode = self.sw_clonerepo_2_h.push( )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    sha_dev_orig_afterclone2mergepush, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    sha_dev_clo2_afterclone2mergepush, errCode = self.sw_clonerepo_2_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    self.assertEqual( sha_dev_orig_afterclone2mergepush,
                      sha_dev_clo2_afterclone2mergepush,
                      "orig/ INT/develop must change afetr clone2 push" )

    sha_devFath2_orig_afterclone2mergepush, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH + "^2")
    sha_ftrdev_clo2_afterclone2mergepush, errCode = self.sw_clonerepo_2_h.get_currsha( self.FEATURE_LIV_FULL_NAME )

    self.assertEqual( sha_devFath2_orig_afterclone2mergepush,
                      sha_ftrdev_clo2_afterclone2mergepush,
                      "orig/ INT/develop must be same as INT/feature_develop" )

  #
  # Test:
  #   like test_workflow_02_01_teamFeature_newINTpair
  #   but
  #   clone 2 will merge with push -I
  #
  # Result:
  #
  #   push -I works but do nothing here: just pushes develop (because cb = INT)
  #   tagging DEV on INT(/develop) is not allowed
  #   merging INT/feature_develop into INT/develop is not allowed
  #   So, only way is choosing a LIV from INT/stable
  #
  #   I like it:
  #     if you choose INT pair way, behave correctly and use LIV labels
  #     If you choosed FTR shared branch, you have no stable branch => no LIV.
  #        create DEV labels and use them to merge
  #
  def test_workflow_02_02_teamFeature_newINTpair_pushMinusI( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.WORKFLOW_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.WORKFLOW_CLONE_DIR ) 

    out, errCode = self.sw_clonerepo_h.init_src( ORIG_REPO_DEVEL_BRANCH, c = self.FEATURE_BRANCH_NAME, )
    self.util_check_SUCC_scenario( out, errCode, "", "creating feature INT branches" ) 


    out, errCode = self.sw_clonerepo_h.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, "", "push with merge" )

    out, errCode = self.sw_origrepo_h.get_currsha( self.FULL_FEATURE_BRANCH_NAME_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "check origin has %s" % self.FULL_FEATURE_BRANCH_NAME_DEV )
    out, errCode = self.sw_origrepo_h.get_currsha( self.FULL_FEATURE_BRANCH_NAME_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "check origin has %s" % self.FULL_FEATURE_BRANCH_NAME_STB )

    #check is also tracked
    out, errCode = self.sw_clonerepo_h.branch_list_track()
    self.assertTrue( self.FULL_FEATURE_BRANCH_NAME_DEV in out, "branch not tracked" )
    self.assertTrue( self.FULL_FEATURE_BRANCH_NAME_STB not in out, "branch not tracked" )

    #
    # clone 2
    #
    sha_dev_orig_beforeclone2, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    #clone integartor
    out, errCode = swgit__utils.clone_scripts_repo_integrator( self.WORKFLOW_CLONE_2_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.WORKFLOW_CLONE_2_DIR ) 

    #set int br manually after
    out, errCode = self.sw_clonerepo_2_h.int_branch_set( self.FULL_FEATURE_BRANCH_NAME_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "setting wnew INT branch as integration branch" ) 

    #create topic branch
    out, errCode = self.sw_clonerepo_2_h.branch_switch_to_int()
    out, errCode = self.sw_clonerepo_2_h.branch_create( self.MODIF_BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED create branch" ) 

    #push mofic and check nothing happened on INT/develop
    out, errCode = self.sw_clonerepo_2_h.modify_file( ORIG_REPO_aFILE, "modif for feature" )
    out, errCode = self.sw_clonerepo_2_h.commit_minusA_dev( "commit feature" )
    out, errCode = self.sw_clonerepo_2_h.push_with_merge( remote )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED pushing on origin" ) 

    sha_dev_orig_afterclone2push, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    self.assertEqual( sha_dev_orig_beforeclone2,
                      sha_dev_orig_afterclone2push,
                      "orig/ INT/develop must NOT change after clone2 push" )

    #stabilize this feature
    out, errCode = self.sw_clonerepo_2_h.set_cfg( "swgit.stabilize-anyref", "True" )
    out, errCode = self.sw_clonerepo_2_h.branch_switch_to_int()
    out, errCode = self.sw_clonerepo_2_h.stabilize_stb( self.FEATURE_LIV_NAME, "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize STB feature develop" ) 
    out, errCode = self.sw_clonerepo_2_h.stabilize_liv( self.FEATURE_LIV_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "stabilize LIV feature develop" ) 

    sha_dev_orig_afterclone2stabilize, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    self.assertEqual( sha_dev_orig_beforeclone2,
                      sha_dev_orig_afterclone2stabilize,
                      "orig/ INT/develop must NOT change afetr clone2 stabilize" )

    #restore old intbr
    out, errCode = self.sw_clonerepo_2_h.int_branch_set( ORIG_REPO_DEVEL_BRANCH)
    self.util_check_SUCC_scenario( out, errCode, "", "restoring old INT branch" )

    #tagging DEV on INT/feature_develop not possible
    out, errCode = self.sw_clonerepo_2_h.tag_create( "dev", msg = "feature finished, tagging an INT branch with DEV" )
    self.util_check_DENY_scenario( out, errCode, "", "tagging DEV on INT branch must be denied" )

    # push -I will not fail, but will do nothing: just push INT/faeture_develop
    #         no merge because cb is /INT/ => behave like integartion branch
    ######################################################
    out, errCode = self.sw_clonerepo_2_h.push_with_merge()
    ######################################################
    self.util_check_SUCC_scenario( out, errCode, "Everything up-to-date", "side push with cb = INT => only pushing cb, no side merge" )

    sha_dev_orig_afterclone2mergepush, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )
    sha_dev_clo2_afterclone2mergepush, errCode = self.sw_clonerepo_2_h.get_currsha( ORIG_REPO_DEVEL_BRANCH )

    self.assertEqual( sha_dev_orig_afterclone2mergepush,
                      sha_dev_clo2_afterclone2mergepush,
                      "orig/ INT/develop must change afetr clone2 push" )

    #merge feature_develop on develop will fail, need a valid label
    out, errCode = self.sw_clonerepo_2_h.branch_switch_to_int()
    out, errCode = self.sw_clonerepo_2_h.merge( self.FULL_FEATURE_BRANCH_NAME_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "merging feature_develop on develop" )

    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_STABLE_BRANCH )
    out, errCode = self.sw_clonerepo_2_h.merge( self.FEATURE_LIV_FULL_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "merging feature LIV on INT/develop" )
    
    out, errCode = self.sw_clonerepo_2_h.push()
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    sha_devFath2_orig_afterclone2mergepush, errCode = self.sw_origrepo_h.get_currsha( ORIG_REPO_DEVEL_BRANCH + "^2")
    sha_ftrdev_clo2_afterclone2mergepush, errCode = self.sw_clonerepo_2_h.get_currsha( self.FEATURE_LIV_FULL_NAME )

    self.assertEqual( sha_devFath2_orig_afterclone2mergepush,
                      sha_ftrdev_clo2_afterclone2mergepush,
                      "orig/ INT/develop must be same as INT/feature_develop" )


  def test_workflow_03_00_multisite_supportedbyCST( self ):
    self.assertEqual( 1, 0, "TODO" )

  def test_workflow_03_01_multisite_supportedbyTAG( self ):
    self.assertEqual( 1, 0, "TODO" )

  def test_workflow_03_02_multisite_notsupported_TrackBr( self ):
    self.assertEqual( 1, 0, "TODO" )

  def test_workflow_03_02_multisite_notsupported_AddRepoOnClone( self ):
    self.assertEqual( 1, 0, "TODO" )

  def test_workflow_04_00_proj_repogitnative( self ):
    self.assertEqual( 1, 0, "TODO" )




if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()





