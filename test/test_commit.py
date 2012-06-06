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

class Test_Commit( Test_Base ):
  COMMIT_DIR     = SANDBOX + "TEST_COMMIT_CLONE"
  BRANCH_NAME    = "prova_commit"
  BRANCH_NAME_SS   = "side_of_side"
  BRANCH_NAME_SS_2 = "side_of_side_2"
  
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.COMMIT_DIR, True )
    self.swgitUtil_    = swgit__utils( self.COMMIT_DIR )
    self.gitUtil_      = git__utils( self.COMMIT_DIR )
    self.CREATED_BR    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, self.BRANCH_NAME )
    self.CREATED_BR_SS   = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME_SS )
    self.CREATED_BR_SS_2 = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME_SS_2 )
    self.CREATED_DEV   = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_DEV_SS   = "%s/DEV/000" % ( self.CREATED_BR_SS )
    self.CREATED_DEV_SS_2 = "%s/DEV/000" % ( self.CREATED_BR_SS_2 )
    self.DDTS          = "Issue12345"
    self.CREATED_FIX   = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS )
    self.MODIFY_FILE   = "%s/%s" % ( self.COMMIT_DIR, ORIG_REPO_aFILE )

  def tearDown( self ):
    pass

  def createBr_modifyFile( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.COMMIT_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )



  def test_Commit_01_00_00_nothing( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.COMMIT_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % out )

    # commit nothing
    out, errCode = self.swgitUtil_.commit()
    self.assertNotEqual( errCode, 0, "swgitUtil_.commit FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % out )

    self.assertEqual( sha_before, sha_after, "swgitUtil_.commit FAILED - after commit no-op, not same sha as before\n%s\n" % out )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )


  def test_Commit_01_00_01_nothing_allow_empty( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.COMMIT_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % out )

    # commit nothing
    out, errCode = self.swgitUtil_.commit( allow_empty = True)
    self.assertEqual( errCode, 0, "commit allow_empty FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % out )
    sha_after_minus1, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % out )

    self.assertNotEqual( sha_before, sha_after, "commit FAILED - after commit no-op, not same sha as before\n%s\n" % out )
    self.assertEqual( sha_before, sha_after_minus1, "commit FAILED - after commit no-op, not same sha as before\n%s\n" % out )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )



  def test_Commit_01_01_00_noAdd( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit but not added
    out, errCode = self.swgitUtil_.commit()
    self.assertNotEqual( errCode, 0, "swgitUtil_.commit FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertEqual( sha_before, sha_after, "swgitUtil_.commit FAILED - after commit no-op, not same sha as before\n%s\n" % sha_after )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )


  def test_Commit_01_01_00_noAdd_allow_empty( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit but not added
    out, errCode = self.swgitUtil_.commit(allow_empty=True)
    self.util_check_SUCC_scenario( out, errCode, 
                                  "Without -a option these files will not be committed", 
                                  "FAILED committing" )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )
    sha_after_minus1, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % out )

    self.assertNotEqual( sha_before, sha_after, "commit FAILED - after commit no-op, not same sha as before\n%s\n" % out )
    self.assertEqual( sha_before, sha_after_minus1, "commit FAILED - after commit no-op, not same sha as before\n%s\n" % out )


    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )




  def test_Commit_01_02_manuallyAdd( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # add file to index
    out, errCode = self.swgitUtil_.add( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "swgitUtil_.add FAILED - \n%s\n" % out )

    # commit
    out, errCode = self.swgitUtil_.commit()
    self.assertEqual( errCode, 0, "swgitUtil_.commit FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_.commit_minusA FAILED - after commit SAME sha as before\n%s\n" % sha_after )

    # getsha previous HEAD
    sha_minusOne, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_minusOne )

    self.assertEqual( sha_before, sha_minusOne, "swgitUtil_.commit FAILED - sha_minusOne not same as sha_before\n%s\n" % sha_minusOne )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )



  def test_Commit_01_03_minusA( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA()
    self.assertEqual( errCode, 0, "swgitUtil_.commit_minusA FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_.commit_minusA FAILED - after commit SAME sha as before\n%s\n" % sha_after )

    # getsha previous HEAD
    sha_minusOne, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_minusOne )

    self.assertEqual( sha_before, sha_minusOne, "swgitUtil_.commit_minusA FAILED - sha_minusOne not same as sha_before\n%s\n" % sha_minusOne )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )



  def test_Commit_01_04_onDevelop( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.COMMIT_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA()
    self.assertNotEqual( errCode, 0, "swgitUtil_.commit_minusA must FAIL on develop - \n%s\n" % out )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )



  def test_Commit_02_00_Dev( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA_dev()
    self.assertEqual( errCode, 0, "swgitUtil_.commit_minusA_dev FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_.commit_minusA_dev FAILED - after commit SAME sha as before\n%s\n" % sha_after )

    # getsha previous HEAD
    sha_minusOne, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_minusOne )

    self.assertEqual( sha_before, sha_minusOne, "swgitUtil_.commit_minusA_dev FAILED - sha_minusOne not same as sha_before\n%s\n" % sha_minusOne )

    # check TAG exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertEqual( errCode, 0, "gitUtil_.tag_get( DEV ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_DEV, "gitUtil_.commit_minusA_dev FAILED not put DEV label - \n%s\n" % self.CREATED_DEV )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )


  def test_Commit_03_00_Fix_NoDdts( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA_fix( "\"\"" )
    self.assertNotEqual( errCode, 0, "swgitUtil_.commit_minusA_fix MUST FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertEqual( sha_before, sha_after, "swgitUtil_.commit_minusA FAILED - after commit must be same as before\n%s\n" % sha_after )

    # check TAG DOES NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )



  def test_Commit_03_01_Fix_WrongDdts( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA_fix( "ISSUE12345" )
    self.assertNotEqual( errCode, 0, "swgitUtil_.commit_minusA_fix MUST FAILED - \n%s\n" % out )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA_fix( "Issue123456" )
    self.assertNotEqual( errCode, 0, "swgitUtil_.commit_minusA_fix MUST FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertEqual( sha_before, sha_after, "swgitUtil_.commit_minusA FAILED - after commit must be same as before\n%s\n" % sha_after )

    # check TAG DOES NOT exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )




  def test_Commit_03_02_Fix_Ok( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA_fix( self.DDTS )
    self.assertEqual( errCode, 0, "swgitUtil_.commit_minusA_fix FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_.commit_minusA FAILED - after commit SAME sha as before\n%s\n" % sha_after )

    # getsha previous HEAD
    sha_minusOne, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_minusOne )

    self.assertEqual( sha_before, sha_minusOne, "swgitUtil_.commit_minusA_fix FAILED - sha_minusOne not same as sha_before\n%s\n" % sha_minusOne )

    # check FIX TAG exists on HEAD
    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertEqual( errCode, 0, "gitUtil_.tag_get( FIX ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_FIX, "gitUtil_.commit_minusA_dev FAILED not put DEV label - \n%s\n" % self.CREATED_FIX )

    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )


  def test_Commit_04_00_Dev_Fix( self ):
    self.createBr_modifyFile()

    # getsha before commit
    sha_before, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.assertEqual( errCode, 0, "swgitUtil_.commit_minusA_fix FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_.commit_minusA FAILED - after commit SAME sha as before\n%s\n" % sha_after )

    # getsha previous HEAD
    sha_minusOne, errCode = self.gitUtil_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_.get_currsha FAILED - \n%s\n" % sha_minusOne )

    self.assertEqual( sha_before, sha_minusOne, "swgitUtil_.commit_minusA_fix FAILED - sha_minusOne not same as sha_before\n%s\n" % sha_minusOne )

    # check DEV and FIX TAG exist on HEAD
    tag, errCode = self.gitUtil_.tag_get( "DEV" )
    self.assertEqual( errCode, 0, "gitUtil_.tag_get( DEV ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_DEV, "gitUtil_.commit_minusA_dev FAILED not put DEV label - \n%s\n" % self.CREATED_FIX )

    tag, errCode = self.gitUtil_.tag_get( "FIX" )
    self.assertEqual( errCode, 0, "gitUtil_.tag_get( FIX ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_FIX, "gitUtil_.commit_minusA_dev FAILED not put FIX label - \n%s\n" % self.CREATED_FIX )


  def test_Commit_05_00_IntBr_FTR( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.COMMIT_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch and set as intbr
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED creating branch" )

    out, errCode = self.swgitUtil_.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode,
                              "Setting INTEGRATION branch to", 
                              "FAILED set int br" )

    # create branch side_side branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED creating branch %s" % self.BRANCH_NAME_SS )

    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "FAILED echo on file - \n%s\n" % out )
    out, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED to commit on side side branch, why?" )

    #switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "FAILED switch to int - out:\n%s" % ( out ) )

    #mod and commit, not allowed on intbr
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "FAILED echo on file - \n%s\n" % out )
    out, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot issue this command on integration branches except for",
                                   "MUST FAIL committing on intbr also if it is FTR" )

    ##simulate Merge conflict
    #out, errCode = self.swgitUtil_.system_unix( "touch .git/MERGE_HEAD" )

    ##now is possible to commit
    #out, errCode = self.swgitUtil_.commit_minusA()
    #self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit" ) 



  def test_Commit_05_00_IntBr_FTR_conflict( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.COMMIT_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch and set as intbr
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "creating branch" )

    out, errCode = self.swgitUtil_.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "set int br" )

    # create branch side_side branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "creating branch %s" % self.BRANCH_NAME_SS )

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_SS_2 )
    self.util_check_SUCC_scenario( out, errCode, "", "creating branch %s" % self.BRANCH_NAME_SS_2 )

    #commit on br1 and merge
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "swicth to branch %s" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, msg = "from side_side" )
    self.util_check_SUCC_scenario( out, errCode, "", "swicth to branch %s" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_.commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "committing on branch %s" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )
    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "merge %s" % self.CREATED_DEV_SS )

    #commit on br2 and merge
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.BRANCH_NAME_SS_2 )
    self.util_check_SUCC_scenario( out, errCode, "", "swicth to branch %s" % self.BRANCH_NAME_SS_2 )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, msg = "from side_side_2" )
    self.util_check_SUCC_scenario( out, errCode, "", "swicth to branch %s" % self.BRANCH_NAME_SS_2 )
    out, errCode = self.swgitUtil_.commit_minusA_dev()
    self.util_check_SUCC_scenario( out, errCode, "", "committing on branch %s" % self.BRANCH_NAME_SS_2 )
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )
    out, errCode = self.swgitUtil_.merge( self.CREATED_BR_SS_2 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly merge a branch into integration branch",
                                   "merge branch into develop" )
    out, errCode = self.swgitUtil_.merge( self.CREATED_DEV_SS_2 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "CONFLICT (content)", 
                                   "merge %s. Must create conflict" % self.CREATED_DEV_SS_2 )

    out, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on file", 
                                   "commit after resolving conflicts" )

    #now is possible to commit
    out, errCode = self.swgitUtil_.system_swgit( "add %s" % ORIG_REPO_aFILE )
    self.util_check_SUCC_scenario( out, errCode, "", "simulate resolving conflict, adding to index" )

    out, errCode = self.swgitUtil_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "commit after resolving conflicts" )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()


