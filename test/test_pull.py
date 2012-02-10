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

class Test_Pull( Test_Base ):
  PULL_REPO_DIR    = SANDBOX + "TEST_PULL__REPO/"
  PULL_CLONE_DIR   = SANDBOX + "TEST_PULL__CLONE/"
  BRANCH_NAME      = "prova_pull"
  BRANCH_NAME_CLO  = "clo_branch"
  BRANCH_NAME_SS   = "side_of_side"

  DETACH_HEAD_ERROR = "FAILED - Cannot pull in DETAHCED-HEAD."
  
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.PULL_REPO_DIR, True ) #ignore errors
    shutil.rmtree( self.PULL_CLONE_DIR, True ) #ignore errors

    # utilities for repo
    self.swgitUtil_Repo_ = swgit__utils( self.PULL_REPO_DIR )
    self.gitUtil_Repo_   = git__utils( self.PULL_REPO_DIR )

    # utilities for clone
    self.swgitUtil_Clone_ = swgit__utils( self.PULL_CLONE_DIR )
    self.gitUtil_Clone_   = git__utils( self.PULL_CLONE_DIR )

    # locals
    self.CREATED_BR     = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME )
    self.CREATED_BR_CLO = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME_CLO )
    self.CREATED_BR_SS  = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME_SS )
    self.CREATED_BR_REM = "origin/%s" % self.CREATED_BR
    self.CREATED_DEV_0  = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_DEV_1  = "%s/DEV/001" % ( self.CREATED_BR )
    self.CREATED_DEV_2  = "%s/DEV/002" % ( self.CREATED_BR )
    self.DDTS_0         = "Issue00000"
    self.DDTS_1         = "Issue11111"
    self.DDTS_2         = "Issue22222"
    self.CREATED_FIX_0  = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_0 )
    self.CREATED_FIX_1  = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_1 )
    self.CREATED_FIX_2  = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_2 )
    self.MODIFY_FILE    = "%s/%s" % ( self.PULL_REPO_DIR, ORIG_REPO_aFILE )


  def tearDown( self ):
    pass

  def clone_repo( self ):
    #first create repo
    create_dir_some_file( self.PULL_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.PULL_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    #clone
    out, errCode = swgit__utils.clone_repo( self.PULL_REPO_DIR, self.PULL_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo - \n%s\n" % out )

    # switch to inty
    out, errCode = self.gitUtil_Repo_.checkout( TEST_REPO_BR_DEV )
    self.assertEqual( errCode, 0, "self.gitUtil_Repo_.checkout FAILED - out:\n%s" % out )


  def test_Pull_01_00_Nothing( self ):
    self.clone_repo()

    # getsha before pull
    sha_before_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_before_repo )
    sha_before_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_before_clone )

    #pull Already-up-toDate
    out, errCode = self.swgitUtil_Clone_.pull()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    # getsha after pull
    sha_after_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after_repo )
    sha_after_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_after_clone )

    self.assertEqual( sha_before_clone, sha_after_clone, "swgitUtil_Clone_.pull FAILED - after pull NOT SAME sha as before\n%s\n%s\n" % (sha_before_clone,sha_after_clone) )
    self.assertEqual( sha_before_repo, sha_after_repo, "swgitUtil_Clone_.pull FAILED - after pull NOT SAME sha as before\n%s\n%s\n" % (sha_before_repo,sha_after_repo) )
    self.assertEqual( sha_before_clone, sha_after_repo, "swgitUtil_Clone_.pull FAILED - after pull NOT SAME sha as before\n%s\n%s\n" % (sha_before_clone,sha_after_repo) )
    self.assertEqual( sha_after_clone, sha_before_repo, "swgitUtil_Clone_.pull FAILED - after pull NOT SAME sha as before\n%s\n%s\n" % (sha_after_clone,sha_before_repo) )


  def test_Pull_02_00_JustDevelop( self ):
    #clone
    self.clone_repo()

    # getsha before commit and pull
    sha_before_repo, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_before_repo )
    sha_before_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_before_clone )

    # modify a file
    out, errCode = echo_on_file( self.PULL_REPO_DIR + TEST_REPO_FILE_A, "\"modification on repo\"" )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    # commit (usign git because swgit does not work on origin)
    out, errCode = self.gitUtil_Repo_.commit_minusA()
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.commit_minusA FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after_commit_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after_commit_repo )
    self.assertNotEqual( sha_before_repo, sha_after_commit_repo, "swgitUtil_Repo_.commit_minusA FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_before_repo,sha_after_commit_repo) )

    # pull
    out, errCode = self.swgitUtil_Clone_.pull()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    # getsha after commit
    sha_after_pull_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after_pull_repo )
    sha_after_pull_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_after_pull_clone )

    self.assertEqual( sha_after_pull_clone, sha_after_commit_repo, \
        "swgitUtil_Clone_.pull FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_after_pull_clone,sha_after_commit_repo) )
    self.assertEqual( sha_after_pull_clone, sha_after_pull_repo, \
        "swgitUtil_Clone_.pull FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_after_pull_clone,sha_after_pull_repo) )

  # repo            clone
  #   |               |
  #   A               A
  #     \           
  #      B branch     
  #
  def test_Pull_03_00_BranchNotMerged( self ):
    #clone
    self.clone_repo()

    # getsha before commit and pull
    sha_before_repo, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_before_repo )
    sha_before_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_before_clone )

    # create branch
    out, errCode = self.gitUtil_Repo_.branch_create( self.CREATED_BR )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.branch_create( %s ) FAILED - \n%s\n" % ( self.CREATED_BR, out ) )

    # modify a file
    out, errCode = echo_on_file( self.PULL_REPO_DIR + TEST_REPO_FILE_A, "\"modification on repo\"" )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    # commit (usign git because swgit does not work on origin)
    out, errCode = self.gitUtil_Repo_.commit_minusA()
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.commit_minusA FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after_commit_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after_commit_repo )
    self.assertNotEqual( sha_before_repo, sha_after_commit_repo, "swgitUtil_Repo_.commit_minusA FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_before_repo,sha_after_commit_repo) )

    br_sha, errCode = self.gitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.ref2sha FAILED - \n%s\n" % br_sha )
    self.assertEqual( sha_after_commit_repo, br_sha, \
        "swgitUtil_Repo_.branch_create( %s ) FAILED (commit sha different from *br sha - \n%s\n%s\n" % ( self.CREATED_BR,sha_after_commit_repo, br_sha ) )

    # pull
    out, errCode = self.swgitUtil_Clone_.pull()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    # getsha after commit
    sha_after_pull_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after_pull_repo )
    sha_after_pull_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_after_pull_clone )

    # branch is not pulled down because is not merged on develop
    self.assertNotEqual( sha_after_pull_clone, sha_after_commit_repo, \
        "swgitUtil_Clone_.pull FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_after_pull_clone,sha_after_commit_repo) )
    self.assertEqual( sha_after_pull_clone, sha_before_repo, \
        "swgitUtil_Clone_.pull FAILED - after commit NOT SAME sha as before\n%s\n%s\n" % (sha_after_pull_clone,sha_before_repo) )

    # branch must not exist on clone
    cb, errCode = self.swgitUtil_Clone_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_Clone_ FAILED - \n%s\n" % cb )
    self.assertEqual( cb, TEST_REPO_BR_DEV, "FAILED not on develop: - \n%s\n" % cb )



  def clone_createBr_modifyFile_commit_mergeOnDev( self ):
    #clone
    self.clone_repo()

    # getsha before commit and pull
    sha_before_repo, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_before_repo )
    sha_before_clone, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_before_clone )

    # create branch
    out, errCode = self.gitUtil_Repo_.branch_create( self.CREATED_BR )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.branch_create( %s ) FAILED - \n%s\n" % ( self.CREATED_BR, out ) )

    # modify a file
    out, errCode = echo_on_file( self.PULL_REPO_DIR + TEST_REPO_FILE_A, "\"modification on repo\"" )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    # commit (usign git because swgit does not work on origin)
    out, errCode = self.gitUtil_Repo_.commit_minusA()
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.commit_minusA FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after_commit_repo, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after_commit_repo )
    self.assertNotEqual( sha_before_repo, sha_after_commit_repo, "swgitUtil_Repo_.commit_minusA FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_before_repo,sha_after_commit_repo) )

    br_sha, errCode = self.gitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.ref2sha FAILED - \n%s\n" % br_sha )
    self.assertEqual( sha_after_commit_repo, br_sha, \
        "swgitUtil_Repo_.branch_create( %s ) FAILED (commit sha different from *br sha - \n%s\n%s\n" % ( self.CREATED_BR,sha_after_commit_repo, br_sha ) )

    # switch to int
    out, errCode = self.gitUtil_Repo_.checkout( TEST_REPO_BR_DEV )
    self.assertEqual( errCode, 0, "self.gitUtil_Repo_.checkout FAILED - out:\n%s" % out )

    # merge on develop
    out, errCode = self.gitUtil_Repo_.merge( br_sha )
    self.assertEqual( errCode, 0, "self.gitUtil_Repo_.merge FAILED - out:\n%s" % out )

    #return A,B,C
    return sha_before_repo, sha_after_commit_repo, self.gitUtil_Repo_.get_currsha()


  # repo                clone
  #   |                   |
  #   A                   A
  #   | \                 |\
  #   |  B  branch  -->   | B
  #   | /                 |/
  #   C                   C
  def test_Pull_03_01_BranchMerged( self ):
    A_repo, B_repo, C_repo = self.clone_createBr_modifyFile_commit_mergeOnDev()

    ######
    # pull
    ######
    out, errCode = self.swgitUtil_Clone_.pull()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    # repo and clone on same commit
    self.assertEqual( self.gitUtil_Repo_.get_currsha(), \
                      self.gitUtil_Clone_.get_currsha(), \
                      "repo and clone not on same commit - \n%s\n%s\n" % \
                      (self.gitUtil_Repo_.get_currsha(),self.gitUtil_Clone_.get_currsha()) )


    # branch must exist on clone, but only as remote one
    self.assertTrue( self.CREATED_BR not in self.swgitUtil_Clone_.local_branches()[0], \
        "FAILED local branch %s in %s" % (self.CREATED_BR, self.swgitUtil_Clone_.local_branches()[0] ) )
    self.assertTrue( self.CREATED_BR in self.swgitUtil_Clone_.remote_branches()[0], \
        "NOT remote branch %s in %s" % (self.CREATED_BR, self.swgitUtil_Clone_.local_branches()[0] ) )
    self.assertEqual( self.swgitUtil_Clone_.current_branch()[0], \
                      TEST_REPO_BR_DEV, \
                      "NOT develop current branch - %s" % self.swgitUtil_Clone_.current_branch()[0] )
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_BR_REM )[0], \
                      B_repo, \
                      "branch %s not on right commit %s - %s" % (self.CREATED_BR, self.gitUtil_Clone_.ref2sha( self.CREATED_BR_REM )[0], B_repo ) ) 


  # repo                clone
  #   |                   |
  #   A     DEV           A
  #   | \   DEV           |\
  #   |  B  FIX   -->     | B
  #   | /   FIX           |/
  #   C                   C
  def test_Pull_03_02_BranchMerged_DevLabel( self ):
    A_repo, B_repo, C_repo = self.clone_createBr_modifyFile_commit_mergeOnDev()

    #Tag repo
    out, errCode = self.gitUtil_Repo_.tag_put_on_commit( self.CREATED_DEV_0, B_repo )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    #Tag repo
    out, errCode = self.gitUtil_Repo_.tag_put_on_commit( self.CREATED_DEV_1, B_repo )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    #Tag repo
    out, errCode = self.gitUtil_Repo_.tag_put_on_commit( self.CREATED_FIX_0, B_repo )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    #Tag repo
    out, errCode = self.gitUtil_Repo_.tag_put_on_commit( self.CREATED_FIX_1, B_repo )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )


    ######
    # pull
    ######
    out, errCode = self.swgitUtil_Clone_.pull()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    # repo and clone on same commit
    self.assertEqual( self.gitUtil_Repo_.get_currsha(), \
                      self.gitUtil_Clone_.get_currsha(), \
                      "repo and clone not on same commit - \n%s\n%s\n" % \
                      (self.gitUtil_Repo_.get_currsha(),self.gitUtil_Clone_.get_currsha()) )


    # branch must exist on clone, but only as remote one
    self.assertTrue( self.CREATED_BR not in self.swgitUtil_Clone_.local_branches()[0], \
        "FAILED local branch %s in %s" % (self.CREATED_BR, self.swgitUtil_Clone_.local_branches()[0] ) )
    self.assertTrue( self.CREATED_BR in self.swgitUtil_Clone_.remote_branches()[0], \
        "NOT remote branch %s in %s" % (self.CREATED_BR, self.swgitUtil_Clone_.local_branches()[0] ) )
    self.assertEqual( self.swgitUtil_Clone_.current_branch()[0], \
                      TEST_REPO_BR_DEV, \
                      "NOT develop current branch - %s" % self.swgitUtil_Clone_.current_branch()[0] )
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_BR_REM )[0], \
                      B_repo, \
                      "branch %s not on right commit %s - %s" % ( self.CREATED_BR, self.gitUtil_Clone_.ref2sha( self.CREATED_BR_REM )[0], B_repo ) ) 

    # tags must exist on clone
    self.assertTrue( self.CREATED_DEV_0 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_DEV_1 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_1, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local fix %s in\n%s" % ( self.CREATED_FIX_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local fix %s in\n%s" % ( self.CREATED_FIX_1, self.gitUtil_Clone_.tag_list()[0] ) )

    # tags must be on the right sha
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )[0], \
                      B_repo, \
                      "label %s not on right commit %s - %s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )[0], B_repo ) ) 
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_1 )[0], \
                      B_repo, \
                      "label %s not on right commit %s - %s" % ( self.CREATED_DEV_1, self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_1 )[0], B_repo ) ) 
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )[0], \
                      B_repo, \
                      "label %s not on right commit %s - %s" % ( self.CREATED_FIX_0, self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )[0], B_repo ) ) 
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_1 )[0], \
                      B_repo, \
                      "label %s not on right commit %s - %s" % ( self.CREATED_FIX_1, self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_1 )[0], B_repo ) ) 


  def test_Pull_04_00_DetachedHead( self ):
    A_repo, B_repo, C_repo = self.clone_createBr_modifyFile_commit_mergeOnDev()

    #create branch and make some commit
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_CLO )
    self.assertEqual( errCode, 0, "FAILED create branch %s - \n%s\n" % ( self.CREATED_BR_CLO, out ) )
    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"modification on clone\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )
    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"another modification on clone\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )

    #side br pull must fail
    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly pull a develop branch.",
                                   "MUST FAIL side pull without -I" )

    #
    # go detached head
    #
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED switch to HEAD~1 - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   self.DETACH_HEAD_ERROR,
                                   "MUST FAIL side pull without -I" )

    out, errCode = self.swgitUtil_Clone_.pull_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   self.DETACH_HEAD_ERROR,
                                   "MUST FAIL pull from br witout DEV with -I" )

    #on detach head on int br
    #make another commit
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "FAILED switch to int - out:\n%s" % ( out ) )
    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"2. modification on repo\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.gitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED switch to HEAD~1 - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   self.DETACH_HEAD_ERROR, 
                                   "MUST FAIL pull from detached head" )

    out, errCode = self.swgitUtil_Clone_.pull_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   self.DETACH_HEAD_ERROR, 
                                   "MUST FAIL pull from detached head also with -I" )


  def test_Pull_05_00_NoIntBr( self ):
    A_repo, B_repo, C_repo = self.clone_createBr_modifyFile_commit_mergeOnDev()

    #create branch and make some commit
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_CLO )
    self.assertEqual( errCode, 0, "FAILED create branch %s - \n%s\n" % ( self.CREATED_BR_CLO, out ) )
    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"modification on clone\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )

    #
    #unset intbr
    #
    saved_intbr, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.assertEqual( errCode, 0, "FAILED getting intbr - out:\n%s" % ( saved_intbr ) )
    out, errCode = self.swgitUtil_Clone_.set_cfg( "swgit.intbranch", SWCFG_TEST_UNSET )
    self.assertEqual( errCode, 0, "FAILED manually unsettin intbr - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_DENY_scenario( out, errCode, 
                                   "No int branch set for this repo.",
                                   "MUST FAIL getintbr after manually unsetting" )

    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot pull without an integration branch set.",
                                   "MUST FAIL pull without an integration branch set" )

    out, errCode = self.swgitUtil_Clone_.pull_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot pull without an integration branch set.",
                                   "MUST FAIL pull without an integration branch set also with -I" )


    #make another commit (temporary reset intbr to allow committing)
    out, errCode = self.swgitUtil_Clone_.int_branch_set( saved_intbr )
    self.assertEqual( errCode, 0, "FAILED manually setting intbr - out:\n%s" % ( out ) )

    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"2. modification on repo\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )

    out, errCode = self.swgitUtil_Clone_.set_cfg( "swgit.intbranch", SWCFG_TEST_UNSET )
    self.assertEqual( errCode, 0, "FAILED manually unsettin intbr - out:\n%s" % ( out ) )
    

    #move to deatched head
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED switch to HEAD~1 - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.current_branch()
    self.util_check_SUCC_scenario( out, errCode, 
                              "(detached-head)",
                              "FAILED getCurrBr" )

    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   self.DETACH_HEAD_ERROR, 
                                   "MUST FAIL push from detached head" )

    out, errCode = self.swgitUtil_Clone_.pull_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   self.DETACH_HEAD_ERROR, 
                                   "MUST FAIL push from detached head also with -I" )


  def test_Pull_05_01_IntBrOnlyLocal_fromIntBr( self ):
    A_repo, B_repo, C_repo = self.clone_createBr_modifyFile_commit_mergeOnDev()

    #create branch and make some commit
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_CLO )
    self.assertEqual( errCode, 0, "FAILED create branch %s - \n%s\n" % ( self.CREATED_BR_CLO, out ) )
    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"modification on clone\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )


    #check br not existing on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_CLO )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving remote branch %s" % self.CREATED_BR_CLO )


    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.CREATED_BR_CLO )
    self.util_check_SUCC_scenario( out, errCode,
                              "Setting INTEGRATION branch to", 
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_SUCC_scenario( out, errCode,
                              self.CREATED_BR_CLO,
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode,
                              "Creating branch %s" % self.CREATED_BR_SS,
                              "FAILED creating br %s" % self.CREATED_BR_SS )

    #
    # swith to int and pull
    #
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED swith to int" )
    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Your current integration branch is only a local branch",
                                   "MUST FAIL pull" )
    #second push must not fail if previous push also has tracked new intbr
    out, errCode = self.swgitUtil_Clone_.pull_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Your current integration branch is only a local branch",
                                   "MUST FAIL pull" )



  def test_Pull_05_01_IntBrOnlyLocal_fromSideBr( self ):
    A_repo, B_repo, C_repo = self.clone_createBr_modifyFile_commit_mergeOnDev()

    #create branch and make some commit
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_CLO )
    self.assertEqual( errCode, 0, "FAILED create branch %s - \n%s\n" % ( self.CREATED_BR_CLO, out ) )
    out, errCode = echo_on_file( self.PULL_CLONE_DIR + TEST_REPO_FILE_A, "\"modification on clone\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )


    #check br not existing on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_CLO )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving remote branch %s" % self.CREATED_BR_CLO )


    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.CREATED_BR_CLO )
    self.util_check_SUCC_scenario( out, errCode,
                              "Setting INTEGRATION branch to", 
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_SUCC_scenario( out, errCode,
                              self.CREATED_BR_CLO,
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode,
                              "Creating branch %s" % self.CREATED_BR_SS,
                              "FAILED creating br %s" % self.CREATED_BR_SS )

    #
    # stay on side and pull
    #
    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly pull a develop branch.",
                                   "MUST FAIL pull" )
    #second push must not fail if previous push also has tracked new intbr
    out, errCode = self.swgitUtil_Clone_.pull_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Your current integration branch is only a local branch",
                                   "MUST FAIL pull" )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()
