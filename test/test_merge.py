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

import unittest
from test_base import *

from _utils import *
from _git__utils import *
from _swgit__utils import *

class Test_Merge( Test_Base ):
  MERGE_DIR      = SANDBOX + "TEST_MERGE_CLONE"
  BRANCH_NAME    = "test_merge"
  BRANCH_NAME_SS = "side_of_side"
  
  def setUp( self ):
    super( Test_Merge, self ).setUp()

    shutil.rmtree( self.MERGE_DIR, True )
    self.swgitUtil_    = swgit__utils( self.MERGE_DIR )
    self.gitUtil_      = git__utils( self.MERGE_DIR )
    self.CREATED_BR    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, self.BRANCH_NAME )
    self.CREATED_BR_SS = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME_SS )
    self.CREATED_DEV_0   = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_DEV_1 = "%s/DEV/001" % ( self.CREATED_BR )
    self.CREATED_DEV_SS= "%s/DEV/000" % ( self.CREATED_BR_SS )
    self.MODIFY_FILE   = "%s/%s" % ( self.MERGE_DIR, ORIG_REPO_aFILE )

  def tearDown( self ):
    super( Test_Merge, self ).tearDown()
    pass

  def util_clone_createBr( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.MERGE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.MERGE_DIR ) 
    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED create branch" ) 

  def util_clone_createBr_modify( self ):
    self.util_clone_createBr()

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED modify file %s" % self.MODIFY_FILE ) 

  def util_clone_createBr_modifyFile_commit( self ):
    self.util_clone_createBr_modify()

    # commit
    out, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED committing" ) 

  def util_clone_createBr_modifyFile_commit_tag( self ):
    self.util_clone_createBr_modifyFile_commit()

    # tag
    out, errCode = self.swgitUtil_.tag_create( "DEV", msg = "modified" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED tagging" ) 


  def test_Merge_01_00_nothing( self ):
    self.util_clone_createBr()

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Already up-to-date.",
                              "FAILED merge myself on me" ) 

    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge branch" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch to int" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge branch" ) 
    
    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You already are on your current integration branch, please remove -I option",
                                   "MUST FAIL merge branch" ) 


  def test_Merge_02_00_dirtywd( self ):
    self.util_clone_createBr_modify()

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Locally modified file(s) detected.",
                                   "MUST FAIL merge myself on me with dirty wd" ) 

    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Locally modified file(s) detected.",
                                   "MUST FAIL merge myself on me with dirty wd" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Locally modified file(s) detected.",
                                   "MUST FAIL merge myself on me with dirty wd" ) 


  def test_Merge_03_00_notag( self ):
    self.util_clone_createBr_modifyFile_commit()

    sha, errCode = self.swgitUtil_.ref2sha( self.CREATED_BR )
    self.util_check_SUCC_scenario( sha, errCode, "", "FAILED retrieving my branch sha" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Already up-to-date.",
                              "FAILED merge myself on me" ) 
    out, errCode = self.swgitUtil_.merge( sha )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid label or branch",
                                   "MUST FAIL merge myself on me by sha" ) 


    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge branch" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch to int" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge branch" ) 
    
    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You already are on your current integration branch, please remove -I option",
                                   "MUST FAIL merge branch" ) 



  def test_Merge_04_00_tag_mergefromint( self ):
    self.util_clone_createBr_modifyFile_commit_tag()

    sha, errCode = self.swgitUtil_.ref2sha( self.CREATED_BR )
    self.util_check_SUCC_scenario( sha, errCode, "", "FAILED retrieving my branch sha" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch to int" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge branch" ) 
    
    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED merge DEV" ) 

    sha_after, errCode = self.swgitUtil_.get_currsha()
    self.assertNotEqual( sha, sha_after, "FAILED merge, stay on same sha - \n%s\n%s\n" % (sha, sha_after) )


  def test_Merge_05_00_tag_mergeonint( self ):
    self.util_clone_createBr_modifyFile_commit_tag()

    sha, errCode = self.swgitUtil_.ref2sha( self.CREATED_BR )
    self.util_check_SUCC_scenario( sha, errCode, "", "FAILED retrieving my branch sha" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Already up-to-date.",
                              "FAILED merge myself on me" ) 
    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Already up-to-date.",
                              "FAILED merge myself on me" ) 
    out, errCode = self.swgitUtil_.merge( sha )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid label or branch",
                                   "MUST FAIL merge myself on me by sha" ) 


    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge branch" ) 

    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED merge on int DEV" ) 

    sha_after, errCode = self.swgitUtil_.get_currsha()
    self.assertNotEqual( sha, sha_after, "FAILED merge, stay on same sha - \n%s\n%s\n" % (sha, sha_after) )


  def test_Merge_06_00_merge_FTRonintFTR( self ):
    self.util_clone_createBr()

    out, errCode = self.swgitUtil_.int_branch_set( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "int_branch_set FAILED - out:\n%s" % out )

    # create branch SS
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED create branch %s" % self.BRANCH_NAME_SS ) 

    # modify a file from SS
    out, errCode = echo_on_file( self.MODIFY_FILE, msg = "some ss contents" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED modify file %s" % self.MODIFY_FILE ) 
    out, errCode = self.swgitUtil_.commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED committing" ) 

    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "MUST FAIL merge FTR onto FTR, when is intbr" ) 

    out, errCode = self.swgitUtil_.merge_on_int( self.CREATED_DEV_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED merge DEV on FTRint" ) 


  def test_Merge_06_00_merge_FTRonFTR( self ):
    self.util_clone_createBr()

    out, errCode = self.swgitUtil_.int_branch_set( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "int_branch_set FAILED - out:\n%s" % out )

    # create branch SS
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED create branch %s" % self.BRANCH_NAME_SS ) 

    # modify a file from SS
    out, errCode = echo_on_file( self.MODIFY_FILE, msg = "some ss contents" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED modify file %s" % self.MODIFY_FILE ) 
    out, errCode = self.swgitUtil_.commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED committing" ) 

    #restore dev intbr
    out, errCode = self.swgitUtil_.int_branch_set( ORIG_REPO_DEVEL_BRANCH )
    self.assertEqual( errCode, 0, "int_branch_set FAILED - out:\n%s" % out )

    #switch onto FTR br
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch branch" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "Merging refs",
                              "FAILED merge FTR onto FTR, when it is not intbr" ) 

  def test_Merge_07_00_NOPARAM_onint( self ):
    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 

    out, errCode = self.swgitUtil_.merge( "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Without merge arguments, -I option is mandatory.",
                                   "on intbr, merge another branch" ) 

    out, errCode = self.swgitUtil_.merge_on_int( "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You already are on your current integration branch, please remove -I option",
                                   "on intbr, merge another branch" ) 
    
    
    out, errCode = self.swgitUtil_.branch_switch_to_br( "HEAD~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 

    out, errCode = self.swgitUtil_.merge( "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Without merge arguments, -I option is mandatory.",
                                   "on detached, merge another branch" ) 
    if modetest_morerepos():
      out, errCode = self.swgitUtil_.merge_on_int( "" )
      self.util_check_DENY_scenario( out, errCode, 
                                     "Cannot find a valid branch starting from this reference:",
                                     "on detached, merge another branch" ) 
    else:
      out, errCode = self.swgitUtil_.merge_on_int( "" )
      self.util_check_DENY_scenario( out, errCode, 
                                     "No DEV label found previous to HEAD.",
                                     "on detached, merge another branch" ) 




  def test_Merge_07_01_NOPARAM_onbranch( self ):
    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    out, errCode = self.swgitUtil_.merge( "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Without merge arguments, -I option is mandatory",
                                   "on ftrbr, merge no param => merge last DEV" ) 
    
    out, errCode = self.swgitUtil_.merge_on_int( "" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "First update your local repository",
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Merging refs/tags/%s into" % self.CREATED_DEV_0,
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 


  def test_Merge_07_02_NOPARAM_ondetach( self ):
    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things other" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    #go in detached
    out, errCode = self.swgitUtil_.branch_switch_to_br( "HEAD~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 

    out, errCode = self.swgitUtil_.merge( "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Without merge arguments, -I option is mandatory",
                                   "on ftrbr, merge no param => merge last DEV" ) 
    
    out, errCode = self.swgitUtil_.merge_on_int( "" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "First update your local repository",
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Merging refs/tags/%s into" % self.CREATED_DEV_0,
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 


  def test_Merge_07_03_NOPARAM_ondetach_amongdevs( self ):
    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things other" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA_dev()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A and DEV" ) 

    #go in detached
    out, errCode = self.swgitUtil_.branch_switch_to_br( "HEAD~1" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" ) 

    out, errCode = self.swgitUtil_.merge( "" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Without merge arguments, -I option is mandatory",
                                   "on ftrbr, merge no param => merge last DEV" ) 
    
    out, errCode = self.swgitUtil_.merge_on_int( "" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "First update your local repository",
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Merging refs/tags/%s into" % self.CREATED_DEV_0,
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 


  #
  # Test:
  #   Here intbr is INT/develop
  #   We create ambiguous intbr by manually setting intbr 
  #     to aBranch (both on origin and aRemote)
  #   Then merge -I
  #
  # Result:
  #   Setting newintbr will deny until a full branch is specified
  #     (with error: Multiple matches found ... )
  #   When providing full reference, it is also tracked => no problem 
  #     occurs when using merge -I
  #
  def test_Merge_08_00_ambiguous_ib( self ):

    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    #
    # try setting ambiguous inbr (some attempt)
    #
    out, errCode = self.swgitUtil_.int_branch_set( ORIG_REPO_aBRANCH_NAME )

    if modetest_morerepos():
      remote = ORIG_REPO_AREMOTE_NAME
      self.util_check_DENY_scenario( out, errCode, 
                                     "Multiple matches found, please specify one among:", 
                                     "setting ambiguous intbr" ) 

      out, errCode = self.swgitUtil_.branch_switch_to_br( ORIG_REPO_aBRANCH_NAME )
      self.util_check_DENY_scenario( out, errCode, 
                                     "Multiple matches found, please specify one among:", 
                                     "setting ambiguous intbr" ) 

      out, errCode = self.swgitUtil_.int_branch_set( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, 
                                     "Multiple matches found, please specify one among:", 
                                     "setting ambiguous intbr" ) 

      out, errCode = self.swgitUtil_.int_branch_set( remote + "/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "setting ambiguous intbr" ) 
    else:
      remote = "origin"
      self.util_check_SUCC_scenario( out, errCode, "", "setting intbr" )

    out, errCode = self.swgitUtil_.merge_on_int( "" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "First update your local repository",
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Merging refs/tags/%s into" % self.CREATED_DEV_0,
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 

  #
  # Test:
  #   Here intbr is INT/develop
  #   We go onto ambiguous ftr aBranch (both on origin and aRemote)
  #   Then merge DEV
  #
  # Result:
  #   Switch will deny until a full branch is specified
  #     (with error: Multiple matches found ... )
  #   When providing full reference, we switch
  #   BUT
  #   we are in detahced HEAD => no merge is possible
  #
  #  We need to track it (so resolving ambiguity) to proceed with merge
  #
  def test_Merge_08_01_ambiguous_targetbr( self ):

    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_br( ORIG_REPO_aBRANCH )
    if modetest_morerepos():
      remote = ORIG_REPO_AREMOTE_NAME
      self.util_check_DENY_scenario( out, errCode, 
                                     "Multiple matches found, please specify one among:", 
                                     "switching to branch on more than 1 repo" ) 
    else:
      remote = "origin"
      self.util_check_SUCC_scenario( out, errCode, "", "switching to branch" )

    out, errCode = self.swgitUtil_.branch_switch_to_br( remote + "/" + ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "switching to branch on more than 1 repo" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_0 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot merge anything into detached-head.",
                                   "on ambiguous ftrbr, merge DEV" )

    out, errCode = self.swgitUtil_.branch_track( remote + "/" + ORIG_REPO_aBRANCH )
    if modetest_morerepos():
      self.util_check_SUCC_scenario( out, errCode, "Tracking branch", "tracking branch" )
    else:
      self.util_check_SUCC_scenario( out, errCode, "Already tracked", "tracking branch" )

    out, errCode = self.swgitUtil_.branch_switch_to_br( ORIG_REPO_aBRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switching to just tracked branch" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Merging refs/tags/%s into" % self.CREATED_DEV_0,
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 


  #
  # Test:
  #   Here intbr is INT/develop, well configured and tracked
  #   Then move onto stable, ambiguous (both on origin and on remote)
  #   logib will change to stable
  #   BUT
  #   without needing to set manually set it (like previous test)
  #
  # Result:
  #   With multiple repositories, we can localize a branch only if 
  #   we track it.
  #   (also git behaves in this way: git checkout says:
  #     without remote: error: pathspec ... did not match any file(s) known to git.
  #     with remote:    gi onto detahced)
  #   So afetr localizing it, is like previous test
  #
  def test_Merge_08_03_ambiguous_logib( self ):

    self.util_clone_createBr_modifyFile_commit_tag()

    sha_dev, errCode = self.swgitUtil_.ref2sha( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( sha_dev, errCode, "", "retrieving %s sha" % self.CREATED_DEV_0 ) 

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE, "some things" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file %s" % self.MODIFY_FILE ) 
    sha, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( sha, errCode, "", "commit minus A" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_br( TEST_REPO_BR_STB )

    if modetest_morerepos():
      remote = ORIG_REPO_AREMOTE_NAME
      self.util_check_DENY_scenario( out, errCode, 
                                     "Multiple matches found, please specify one among:", 
                                     "setting ambiguous intbr" ) 
    else:
      remote = "origin"
      self.util_check_SUCC_scenario( out, errCode, "", "switch branch" )

    out, errCode = self.swgitUtil_.branch_track( remote + "/" + TEST_REPO_BR_STB )
    if modetest_morerepos():
      self.util_check_SUCC_scenario( out, errCode, "Tracking branch", "tracking branch" )
    else:
      self.util_check_SUCC_scenario( out, errCode, "Already tracked", "tracking branch" )

    out, errCode = self.swgitUtil_.branch_switch_to_br( TEST_REPO_BR_STB )
    self.util_check_SUCC_scenario( out, errCode, "", "switching to just tracked branch" ) 

    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_0 )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "First update your local repository",
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Merging refs/tags/%s into" % self.CREATED_DEV_0,
                                   "on ftrbr, merge -I no param => merge last DEV on INT" ) 



if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()



