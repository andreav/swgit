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

class Test_Tag( Test_Base ):
  TAG_CLONE_DIR   = SANDBOX + "TEST_TAG_CLONE/"
  TAG_CLONE_DIR_2 = SANDBOX + "TEST_TAG_CLONE_2/"
  TAG_REPO_DIR    = SANDBOX + "TEST_TAG_REPO/"
  BRANCH_NAME          = "prova_tag"
  ORIG_MOD_BRANCH      = "orig_modbr"
  ORIG_MOD_FULL_BRANCH = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER, ORIG_MOD_BRANCH )
  ORIG_MOD_DEV         = "%s/DEV/000" % ( ORIG_MOD_FULL_BRANCH )
  
  DDTS            = "Issue12345"

  CREATED_BR       = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, BRANCH_NAME )
  CREATED_BR_NEWBR = "%s/NEW/BRANCH" % ( CREATED_BR )
  CREATED_BR_DEV   = "%s/DEV/000" % ( CREATED_BR )
  CREATED_BR_FIX   = "%s/FIX/%s" % ( CREATED_BR, DDTS )

  REMOTE_2_NAME    = "aRemote"
  REMOTE_2_URL     = "%s%s" % (REPO_SSHACCESS, TAG_CLONE_DIR_2)

  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.TAG_REPO_DIR, True )
    shutil.rmtree( self.TAG_CLONE_DIR, True )
    shutil.rmtree( self.TAG_CLONE_DIR_2, True )
    self.swgitUtil_Repo_   = swgit__utils( self.TAG_REPO_DIR )
    self.swgitUtil_Clone_  = swgit__utils( self.TAG_CLONE_DIR )
    self.swgitUtil_Clone_2 = swgit__utils( self.TAG_CLONE_DIR_2 )
    self.gitUtil_Repo_   = git__utils( self.TAG_REPO_DIR )
    self.gitUtil_Clone_  = git__utils( self.TAG_CLONE_DIR )

    self.CREATED_BR  = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME )
    self.CREATED_DEV_0 = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_DEV_1 = "%s/DEV/001" % ( self.CREATED_BR )
    self.CREATED_DEV_2 = "%s/DEV/002" % ( self.CREATED_BR )
    self.DDTS_0        = "Issue00000"
    self.DDTS_1        = "Issue11111"
    self.DDTS_2        = "Issue22222"
    self.CREATED_FIX_0 = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_0 )
    self.CREATED_FIX_1 = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_1 )
    self.CREATED_FIX_2 = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_2 )
    self.MODIFY_FILE   = "%s/a.txt" % ( self.TAG_CLONE_DIR )

    self.G2C_NAME      = "export"
    self.CREATED_G2C   = "%s/G2C/%s" % ( TEST_REPO_BR_DEV, self.G2C_NAME )
    self.SLC_LIV       = "LIV.A.40"
    self.PLAT_LIV      = "PLAT.10"
    self.FLC_LIV       = "LIV.4.0.0.DROP.AH"
    self.ZIC_LIV       = "ZIC.10"


  def tearDown( self ):
    pass

  def clone_createBr_modify( self, somecommmitondev = False ):
    #first create repo
    create_dir_some_file( self.TAG_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.TAG_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    if somecommmitondev:
      #create also an empty commit on develop
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "d.", gotoint = False )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "d.", gotoint = False )

      #create a  commit usefull for some tests
      out, errCode = self.swgitUtil_Repo_.branch_create_src( self.ORIG_MOD_BRANCH, ORIG_REPO_DEVEL_BRANCH )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "1. modify to create commit", gotoint = False )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "2. modify to create commit", gotoint = False )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.tag_create( "DEV", msg = "some modifications on origin" )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.branch_switch_to_br( ORIG_REPO_DEVEL_BRANCH )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.merge( self.ORIG_MOD_DEV )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )

    # clone
    out, errCode = swgit__utils.clone_repo( self.TAG_REPO_DIR, self.TAG_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo" )

    # create branch
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.branch_create FAILED - \n%s\n" % out )

    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

  def clone_createBr( self, somecommmitondev = False, integrator = False ):
    #first create repo
    create_dir_some_file( self.TAG_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.TAG_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    if somecommmitondev:
      #create also an empty commit on develop
      out, errCode = self.swgitUtil_Repo_.branch_switch_to_br( ORIG_REPO_DEVEL_BRANCH )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "d. da develop", gotoint = False )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "d. da develop", gotoint = False )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )

      #create a  commit usefull for some tests
      out, errCode = self.swgitUtil_Repo_.branch_create_src( self.ORIG_MOD_BRANCH, ORIG_REPO_DEVEL_BRANCH )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "1. modify to create commit", gotoint = False )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.modify_repo( TEST_REPO_FILE_A, msg = "2. modify to create commit", gotoint = False )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.tag_create( "DEV", msg = "some modifications on origin" )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.branch_switch_to_br( ORIG_REPO_DEVEL_BRANCH )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
      out, errCode = self.swgitUtil_Repo_.merge( self.ORIG_MOD_DEV )
      self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )


    # clone
    if not integrator:
      out, errCode = swgit__utils.clone_repo( self.TAG_REPO_DIR, self.TAG_CLONE_DIR )
      self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo" )
    else:
      out, errCode = swgit__utils.clone_repo_integrator( self.TAG_REPO_DIR, self.TAG_CLONE_DIR )
      self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo" )

    # create branch
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.branch_create FAILED - \n%s\n" % out )


  def modify_and_commit( self, alsotags = True ):
    # modify a file
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    #create all custom tags
    if alsotags:
      self.swgitUtil_Clone_.tag_define_all_100_custom()

    # getsha before commit
    sha_before, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_before )
    
    # commit
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.commit_minusA FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_Clone_.commit_minusA FAILED - after commit SAME sha as before\n%s\n" % sha_after )

    # getsha previous HEAD
    sha_minusOne, errCode = self.gitUtil_Clone_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_minusOne )

    self.assertEqual( sha_before, sha_minusOne, "swgitUtil_Clone_.commit_minusA FAILED - sha_minusOne not same as sha_before\n%s\n" % sha_minusOne )


  
  def test_Tag_01_00_nothingDone( self ):
    #first create repo
    create_dir_some_file( self.TAG_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.TAG_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )


    # clone
    out, errCode = swgit__utils.clone_repo( self.TAG_REPO_DIR, self.TAG_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo" )

    # create branch
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.branch_create FAILED - \n%s\n" % out )

    # getsha before commit
    sha_before, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % out )

    # tag nothing
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_dev MUST FAILED (tagging on branch just created without changes) - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % out )

    self.assertEqual( sha_before, sha_after, "swgitUtil_Clone_.tag_dev FAILED - after commit no-op, not same sha as before\n%s\n" % out )

    # tag nothing
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_fix MUST FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % out )

    self.assertEqual( sha_before, sha_after, "swgitUtil_Clone_.tag_fix FAILED - after commit no-op, not same sha as before\n%s\n" % out )

  
  
  def test_Tag_01_01_noAdd( self ):
    self.clone_createBr_modify()

    # getsha before commit
    sha_before, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_before )

    # commit but not added
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_dev MUST FAILED (tagging dev on branch with changes not added to index)- \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertEqual( sha_before, sha_after, "swgitUtil_Clone_.tag_dev FAILED - after commit no-op, not same sha as before\n%s\n" % sha_after )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )


    # commit but not added
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_fix MUST FAILED (tagging fix on branch with changes not added to index)- \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertEqual( sha_before, sha_after, "swgitUtil_Clone_.tag_fix FAILED - after commit no-op, not same sha as before\n%s\n" % sha_after )

    # check TAG MUST NOT exists on HEAD
    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )

  
  def test_Tag_02_00_DEV( self ):
    self.clone_createBr()
    self.modify_and_commit()

    commit_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit_sha )

    # tag dev
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # check TAG exists on HEAD, FIX does not exist
    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_DEV_0, "gitUtil_Clone_.tag_dev FAILED not put DEV label - \n%s\n" % self.CREATED_DEV_0 )

    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag0_sha )

    #
    # Another loop
    #
    self.modify_and_commit()

    commit1_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit1_sha )
    self.assertNotEqual( commit_sha, commit1_sha, "self.modify_and_commit FAILED (not different commits) - \n%s\n" % commit1_sha )

    # tag dev
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # check TAG exists on HEAD
    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_DEV_1, "gitUtil_Clone_.tag_dev FAILED not put DEV label - \n%s\n" % self.CREATED_DEV_1 )

    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )

    tag1_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_1 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag1_sha )
    self.assertEqual( commit1_sha, tag1_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag1_sha )



    #
    # Another loop
    #
    self.modify_and_commit()
    commit2_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit2_sha )
    self.assertNotEqual( commit_sha, commit1_sha, "self.modify_and_commit FAILED (not different commits) - \n%s\n" % commit1_sha )
    self.assertNotEqual( commit_sha, commit2_sha, "self.modify_and_commit FAILED (not different commits) - \n%s\n" % commit2_sha )
    self.assertNotEqual( commit1_sha, commit2_sha, "self.modify_and_commit FAILED (not different commits) - \n%s\n" % commit2_sha )

    # tag dev
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # check TAG exists on HEAD
    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_DEV_2, "gitUtil_Clone_.tag_dev FAILED not put DEV label - \n%s\n" % self.CREATED_DEV_2 )

    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) MUST FAILED - \n%s\n" % tag )

    tag2_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_2 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag2_sha )
    self.assertEqual( commit2_sha, tag2_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag2_sha )

  
  def test_Tag_02_01_DEV_on_DEV( self ):
    self.clone_createBr()
    self.modify_and_commit()

    # tag dev
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # re-tag dev
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_dev MUST FAILED (Already a DEV on this commit)- \n%s\n" % out )


  def test_Tag_03_00_FIX_WrongsParams( self ):
    self.clone_createBr()
    self.modify_and_commit()

    out, errCode = self.swgitUtil_Clone_.tag_fix( "\"\"" )
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_dev MUST FAILED (no ddts passed) - \n%s\n" % out )

    out, errCode = self.swgitUtil_Clone_.tag_fix( "ISSUE12345" )
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_dev MUST FAILED (no regexp satisfied) - \n%s\n" % out )


  def test_Tag_03_01_FIX( self ):
    self.clone_createBr()
    self.modify_and_commit()

    # tag fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # check TAG exists on HEAD, DEV does not exist
    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_FIX_0, "gitUtil_Clone_.tag_fix FAILED not put FIX label - \n%s\n" % self.CREATED_FIX_0 )

    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    #
    # Another loop
    #
    self.modify_and_commit()
    # tag fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_1 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # check TAG exists on HEAD, DEV does not exist
    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_FIX_1, "gitUtil_Clone_.tag_fix FAILED not put FIX label - \n%s\n" % self.CREATED_FIX_1 )

    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )

    #
    # Another loop
    #
    self.modify_and_commit()
    # tag fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_2 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    # check TAG exists on HEAD, DEV does not exist
    tag, errCode = self.gitUtil_Clone_.tag_get( "FIX" )
    self.assertEqual( errCode, 0, "gitUtil_Clone_.tag_get( FIX ) FAILED - \n%s\n" % tag )
    self.assertEqual( tag, self.CREATED_FIX_2, "gitUtil_Clone_.tag_fix FAILED not put FIX label - \n%s\n" % self.CREATED_FIX_2 )

    tag, errCode = self.gitUtil_Clone_.tag_get( "DEV" )
    self.assertNotEqual( errCode, 0, "gitUtil_Clone_.tag_get( DEV ) MUST FAILED - \n%s\n" % tag )


  def test_Tag_03_02_FIX_on_same_FIX( self ):
    self.clone_createBr()
    self.modify_and_commit()

    commit_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit_sha )

    # tag fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag0_sha )


    # re-tag same fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertNotEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag0_sha )



  def test_Tag_03_03_FIX_on_other_FIX( self ):
    self.clone_createBr()
    self.modify_and_commit()

    commit_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit_sha )

    # tag fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag0_sha )

    # re-tag different fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_1 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag0 sha - \n%s\n" % tag0_sha )

    tag1_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_1 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag1_sha )
    self.assertEqual( commit_sha, tag1_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag1 sha - \n%s\n" % tag1_sha )
    self.assertEqual( tag0_sha, tag1_sha, "swgitUtil_Clone_.tag_fix FAILED (*tag0 sha different from *tag1 sha - \n%s\n" % tag1_sha )


    # re-tag different fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_2 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag0 sha - \n%s\n" % tag0_sha )

    tag1_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_1 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag1_sha )
    self.assertEqual( commit_sha, tag1_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag1 sha - \n%s\n" % tag1_sha )
    self.assertEqual( tag0_sha, tag1_sha, "swgitUtil_Clone_.tag_fix FAILED (*tag0 sha different from *tag1 sha - \n%s\n" % tag1_sha )

    tag2_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_2 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag2_sha )
    self.assertEqual( commit_sha, tag2_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag2 sha - \n%s\n" % tag2_sha )
    self.assertEqual( tag0_sha, tag1_sha, "swgitUtil_Clone_.tag_fix FAILED (*tag0 sha different from *tag1 sha - \n%s\n" % tag1_sha )
    self.assertEqual( tag0_sha, tag2_sha, "swgitUtil_Clone_.tag_fix FAILED (*tag0 sha different from *tag2 sha - \n%s\n" % tag2_sha )
    self.assertEqual( tag1_sha, tag2_sha, "swgitUtil_Clone_.tag_fix FAILED (*tag1 sha different from *tag2 sha - \n%s\n" % tag2_sha )

  def test_Tag_03_04_LIV_cloneIntegrator( self ):
    self.clone_createBr( integrator = True )
    self.modify_and_commit()

    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "swicth to stable" )
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.util_check_SUCC_scenario( out, errCode, "", "modif file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA( )
    self.util_check_SUCC_scenario( out, errCode, "", "commit minua A on stable" )

    out, errCode = self.swgitUtil_Clone_.tag_create( "LIV", "Drop.B", msg = "Droppppp" )
    self.util_check_SUCC_scenario( out, errCode, "", 
                                   "LIV inside integration repo" )



  def test_Tag_03_05_LIV_RepoConvertedIntoIntegrator( self ):
    self.clone_createBr()
    self.modify_and_commit()

    out, errCode = self.swgitUtil_Clone_.tag_create( "LIV", "Drop.B", msg = "Droppppp" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Tag LIV can be created/deleted only on", 
                                   "LIV inside NOT integration repo" )

    #transform repo into integrator
    self.swgitUtil_Clone_.set_cfg( "swgit.integrator", "True" )

    #some cheks only for this particualr repo....
    out, errCode = self.swgitUtil_Clone_.tag_create( "LIV", "Drop.B", msg = "Droppppp" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Label LIV cannot be put on branch type FTR",
                                   "LIV inside NOT integration repo" )


    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "swicth to stable" )

    out, errCode = self.swgitUtil_Clone_.tag_create( "LIV", "Drop.B", msg = "Droppppp" )
    self.util_check_DENY_scenario( out, errCode, 
                                   #"You already have a LIV label on this commit:",
                                   "You must have a new commit to tag",
                                   "LIV inside NOT integration repo" )


    #create commit on stable
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.util_check_SUCC_scenario( out, errCode, "", "modif file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA( )
    self.util_check_SUCC_scenario( out, errCode, "", "commit minua A on stable" )


    out, errCode = self.swgitUtil_Clone_.tag_create( "LIV", "Drop.B", msg = "Droppppp" )
    self.util_check_SUCC_scenario( out, errCode, "", "LIV inside integration repo" )




  def test_Tag_04_00_Replace_DEV( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )


    # tag dev
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit0_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag0_sha )

    # modify, commit
    self.modify_and_commit()
    commitrep_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commitrep_sha )


    # move tag
    out, errCode = self.swgitUtil_Clone_.tag_dev_replace()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev_replace FAILED - \n%s\n" % out )

    tagrep_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tagrep_sha )
    self.assertEqual( commit0_sha, tag0_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commit sha different from *tag0 sha - \n%s\n" % tag0_sha )
    self.assertEqual( commitrep_sha, tagrep_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha different from *tagrep sha - \n%s\n" % tagrep_sha )
    self.assertNotEqual( commitrep_sha, commit0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha MUST be different from commit0_sha sha - \n%s\n" % commitrep_sha )
    self.assertNotEqual( tagrep_sha, tag0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (*tagrep_sha sha MUST be different from *tag0_sha sha - \n%s\n" % tagrep_sha )


    #
    # Another loop
    #
    self.modify_and_commit()
    commitrep2_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commitrep2_sha )


    # move tag
    out, errCode = self.swgitUtil_Clone_.tag_dev_replace()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_dev_replace FAILED - \n%s\n" % out )

    tagrep2_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tagrep2_sha )
    self.assertEqual( commit0_sha, tag0_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commit sha different from *tag0 sha - \n%s\n" % tag0_sha )
    self.assertEqual( commitrep_sha, tagrep_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha different from *tagrep sha - \n%s\n" % tagrep_sha )
    self.assertNotEqual( commitrep_sha, commit0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha MUST be different from commit0_sha sha - \n%s\n" % commitrep_sha )
    self.assertNotEqual( tagrep_sha, tag0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (*tagrep_sha sha MUST be different from *tag0_sha sha - \n%s\n" % tagrep_sha )

    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tagrep2_sha )
    self.assertEqual( commit0_sha, tag0_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commit0 sha different from *tag0 sha - \n%s\n" % tag0_sha )
    self.assertEqual( commitrep_sha, tagrep_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commit1 sha different from *tagrep sha - \n%s\n" % tagrep_sha )
    self.assertEqual( commitrep2_sha, tagrep2_sha, "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha different from *tagrep sha - \n%s\n" % tagrep2_sha )
    self.assertNotEqual( commitrep2_sha, commit0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha MUST be different from commit0_sha sha - \n%s\n" % commitrep2_sha )
    self.assertNotEqual( commitrep2_sha, commitrep_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep2 sha MUST be different from commitrep sha - \n%s\n" % commitrep2_sha )
    self.assertNotEqual( commitrep_sha, commit0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (commitrep sha MUST be different from commit0 sha - \n%s\n" % commitrep2_sha )
    self.assertNotEqual( tagrep2_sha, tag0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (*tagrep2_sha sha MUST be different from *tag0_sha sha - \n%s\n" % tagrep2_sha )
    self.assertNotEqual( tagrep2_sha, tagrep_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (*tagrep2_sha sha MUST be different from *tagrep sha - \n%s\n" % tagrep2_sha )
    self.assertNotEqual( tagrep_sha, tag0_sha, \
        "swgitUtil_Clone_.tag_dev_replace FAILED (*tagrep_sha sha MUST be different from *tag0_sha sha - \n%s\n" % tagrep2_sha )


  def test_Tag_04_01_Replace_FIX( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )


    # tag fix
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_fix FAILED - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tag0_sha )
    self.assertEqual( commit0_sha, tag0_sha, "swgitUtil_Clone_.tag_fix FAILED (commit sha different from *tag sha - \n%s\n" % tag0_sha )

    # modify, commit
    self.modify_and_commit()
    commitrep_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commitrep_sha )


    # move tag
    out, errCode = self.swgitUtil_Clone_.tag_fix_replace( self.DDTS_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.tag_fix_replace FAILED - \n%s\n" % out )

    tagrep_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_FIX_0 )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.ref2sha FAILED - \n%s\n" % tagrep_sha )
    self.assertEqual( commit0_sha, tag0_sha, "swgitUtil_Clone_.tag_fix_replace FAILED (commit sha different from *tag0 sha - \n%s\n" % tag0_sha )
    self.assertEqual( commitrep_sha, tagrep_sha, "swgitUtil_Clone_.tag_fix_replace FAILED (commitrep sha different from *tagrep sha - \n%s\n" % tagrep_sha )
    self.assertNotEqual( commitrep_sha, commit0_sha, \
        "swgitUtil_Clone_.tag_fix_replace FAILED (commitrep sha MUST be different from commit0_sha sha - \n%s\n" % commitrep_sha )
    self.assertNotEqual( tagrep_sha, tag0_sha, \
        "swgitUtil_Clone_.tag_fix_replace FAILED (*tagrep_sha sha MUST be different from *tag0_sha sha - \n%s\n" % tagrep_sha )


  def test_Tag_05_00_DEV_on_INT( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.TAG_CLONE_DIR )

    out, errCode = echo_on_file( self.TAG_CLONE_DIR + ORIG_REPO_aFILE )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot issue this command on integration branches except for",
                                   "MUST FAIL commit" )

    #simulate erge conflict
    out, errCode = self.swgitUtil_Clone_.system_unix( "touch .git/MERGE_HEAD" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, 
                              "",
                              "FAILED commit" )

    #tag create
    out, errCode = self.swgitUtil_Clone_.tag_create( "DEV", msg = "some modifications on origin" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Label DEV cannot be put on branch type INT",
                                   "FAILED commit" )


  def test_Tag_05_01_DEV_on_FTR_asINTbr( self ):

    self.clone_createBr_modify()

    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED set int br %s" % self.CREATED_BR )
 
    # commit must fail except for resolve conflict
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot issue this command on integration branches except for",
                                   "MUST FAIL commit" )

    #simulate erge conflict, commit must go
    out, errCode = self.swgitUtil_Clone_.system_unix( "touch .git/MERGE_HEAD" )

    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit" )

    #tag create, allow it on FTR.
    out, errCode = self.swgitUtil_Clone_.tag_create( "DEV", msg = "some modifications on origin" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED tagging DEV on FTR" )



  def test_Tag_06_00_CustomTags_SimpleTag( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    out, errCode = self.swgitUtil_Clone_.tag_create( "NOTEXISTS", msg = "something" )
    self.assertEqual( errCode, 1, "MUST FAIL creation of not existing label - \n%s\n" % out )

    #define custom tags
    self.swgitUtil_Clone_.tag_define_custom_tag( CUSTTAG_NUM )
    self.swgitUtil_Clone_.tag_define_custom_tag( CUSTTAG_NAME )

    # verify always can ypu put a DEV (default labels must never disappear)
    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "createring tag dev" )
    self.assertEqual( errCode, 0, "FAILED tag DEV - \n%s\n" % out )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )
    self.assertEqual( errCode, 0, "FAILED retrieving DEV - \n%s\n" % tag0_sha )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    #simple numtag, with val without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], "avalue" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM plus value - \n%s\n" % out )

    #simple numtag, with val and with msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], "avalue", msg = "something" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM plus value - \n%s\n" % out )

    #simple numtag, without val and without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], "avalue" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM without msg and hook - \n%s\n" % out )

    #simple numtag correct
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], msg = "something" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NUM creation - \n%s\n" % out )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, CUSTTAG_NUM["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    #simple nametag, without val without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME without value - \n%s\n" % out )

    #simple nametag, without val with msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], msg = "someother" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME without value - \n%s\n" % out )

    #simple nametag, with val without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME without message - \n%s\n" % out )

    #simple nametag correct
    value = "DropAB_2"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], value, msg = "someother first regexp" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NAME respecting FIRST regexp - \n%s\n" % out )

    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, 
        "FAILED creating tag CUSTTAG_NAME with first regexp commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    value = "Issue12345"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], value , msg = "someother second regexp" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NAME respecting SECOND regexp - \n%s\n" % out )

    created_custtag_label_2 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_2 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_2, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, 
        "FAILED creating tag CUSTTAG_NAME with second regexp commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )


  def test_Tag_06_01_CustomTags_SimpleTag_WrongValues( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #define custom tags
    wrong_num_custtag_push = copy.deepcopy( CUSTTAG_NUM )
    wrong_name_custtag_push = copy.deepcopy( CUSTTAG_NAME )

    wrong_num_custtag_push["push_on_origin"]  = "CICCIO"
    wrong_name_custtag_push["push_on_origin"] = "CICCIO"
    self.swgitUtil_Clone_.tag_define_custom_tag( wrong_num_custtag_push )
    self.swgitUtil_Clone_.tag_define_custom_tag( wrong_name_custtag_push )

    #must fail creation
    out, errCode = self.swgitUtil_Clone_.tag_create( wrong_num_custtag_push["tagtype"], msg = "something" )
    self.assertEqual( errCode, 1, "MUST FAIL WRONG val \"push\" CUSTTAG NUM creation - \n%s\n" % out )

    #check not exists label
    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, wrong_num_custtag_push["tagtype"] )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST NOT EXISTS tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #must fail creation
    value = "DropAB_2"
    out, errCode = self.swgitUtil_Clone_.tag_create( wrong_name_custtag_push["tagtype"], value, msg = "someother first regexp" )
    self.assertEqual( errCode, 1, "MUST FAIL WRONG val \"push\" CUSTTAG NAME creation - \n%s\n" % out )

    #check not exists label
    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, wrong_name_custtag_push["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )


  def test_Tag_06_02_CustomTags_Hook_PreTag_Local( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #
    # local script
    #

    #define custom tags
    pretag_custtag_ECHO_num   = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_NOECHO_num = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_ECHO_BUTFAILS_num   = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_NOECHO_ANDFAILS_num = copy.deepcopy( CUSTTAG_NUM )

    script_comment = "comment: ABCD"
    out_ssh_string = "Executing pre-tag hook"
    pretag_custtag_ECHO_num["tagtype"]  = "NUMTAG_PREHOOK_ECHO"
    pretag_custtag_ECHO_num["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    pretag_custtag_NOECHO_num["tagtype"] = "NAMETAG_PREHOOK_NOECHO"
    pretag_custtag_NOECHO_num["hook_pretag_script"] = "echo \"AAA\" > /dev/null"

    pretag_custtag_ECHO_BUTFAILS_num["tagtype"]  = "NUMTAG_PREHOOK_ECHO_BUTFAILS"
    pretag_custtag_ECHO_BUTFAILS_num["hook_pretag_script"]  = "echo \"%s\" && return 1" % script_comment
    pretag_custtag_NOECHO_ANDFAILS_num["tagtype"] = "NAMETAG_PREHOOK_NOECHO_AND_FAILS"
    pretag_custtag_NOECHO_ANDFAILS_num["hook_pretag_script"] = "echo \"AAA\" > /dev/null && return 1"

    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_ECHO_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_NOECHO_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_ECHO_BUTFAILS_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_NOECHO_ANDFAILS_num )

    #pretag ECHO numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHO_num["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   out_ssh_string,
                                   "tagging, local echo script" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   script_comment,
                                   "tagging, local echo script" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHO_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag comment for %s - \n%s\n" % (created_custtag_label, tag_comment) )
    self.assertTrue( script_comment in tag_comment, "FAILED creating tag: comment wothout %s inside %s" % ( script_comment, tag_comment) )

    #pretag ECHO numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHO_num["tagtype"], msg = user_comment )
    self.util_check_SUCC_scenario( out, errCode, 
                                   out_ssh_string,
                                   "tagging , echo script with message" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   script_comment,
                                   "tagging , echo script with message" )

    created_custtag_label_1 = "%s/%s/001" % ( self.CREATED_BR, pretag_custtag_ECHO_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag comment for %s - \n%s\n" % (created_custtag_label_1, tag_comment) )
    self.assertTrue( script_comment in tag_comment, "FAILED creating tag: comment without hook output %s inside %s" % ( script_comment, tag_comment) )
    self.assertTrue( user_comment in tag_comment, "FAILED creating tag: comment without user output %s inside %s" % ( user_comment, tag_comment) )


    #pretag NOECHO numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHO_num["tagtype"] )
    self.assertTrue( out_ssh_string in out, "FAILED tagging over ssh, noecho script" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "returned empty string. Please specify at least -m option",
                                   "tagging, noecho script" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHO_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag NOECHO numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHO_num["tagtype"], msg = user_comment )
    self.util_check_SUCC_scenario( out, errCode, 
                                   out_ssh_string,
                                   "tagging ,local  echo script with message" )
    self.assertTrue( script_comment not in out, "FAILED tagging, noecho script" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHO_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag comment for %s - \n%s\n" % (created_custtag_label_1, tag_comment) )
    self.assertTrue( script_comment not in tag_comment, "FAILED creating tag: comment without hook output %s inside %s" % ( script_comment, tag_comment) )
    self.assertTrue( user_comment in tag_comment, "FAILED creating tag: comment without user output %s inside %s" % ( user_comment, tag_comment) )


    #pretag ECHO + FAILS numtag, without msg
    # do not consider script output
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHO_BUTFAILS_num["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "returned error.",
                                   "tagging with local pre-tag echo nomsg returning error" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHO_BUTFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag ECHO + FAILS numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHO_BUTFAILS_num["tagtype"], msg = user_comment )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NUMTAG_PREHOOK_ECHO_BUTFAILS pre-tag hook",
                                   "tagging with local pre-tag numbered returning error" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHO_BUTFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving failed tag" )



    #pretag NOECHO + FAILS numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHO_ANDFAILS_num["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "returned error.",
                                   "tagging with local pre-tag numtag noecho returning error" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHO_ANDFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag NOECHO = FAILS numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHO_ANDFAILS_num["tagtype"], msg = user_comment )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NAMETAG_PREHOOK_NOECHO_AND_FAILS pre-tag hook",
                                   "tagging with local pre-tag named returning error" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHO_ANDFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving failed tag" )


  def test_Tag_06_03_CustomTags_Hook_PreTag_OverSsh( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #
    # remote scripts
    #

    #define custom tags
    pretag_custtag_ECHOSSH_num   = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_NOECHOSSH_num = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_ECHOSSH_BUTFAILS_num   = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_NOECHOSSH_ANDFAILS_num = copy.deepcopy( CUSTTAG_NUM )

    script_comment = "comment: ABCD"
    out_ssh_string = "Executing pre-tag hook %s@%s" % (TEST_USER_SSH,TEST_ADDR)
    pretag_custtag_ECHOSSH_num["tagtype"]  = "NUMTAG_PREHOOK_ECHOSSH"
    pretag_custtag_ECHOSSH_num["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    pretag_custtag_ECHOSSH_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_ECHOSSH_num["hook_pretag_sshaddr"]  = TEST_ADDR
    pretag_custtag_NOECHOSSH_num["tagtype"] = "NAMETAG_PREHOOK_NOECHOSSH"
    pretag_custtag_NOECHOSSH_num["hook_pretag_script"] = "echo \"AAA\" > /dev/null"
    pretag_custtag_NOECHOSSH_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_NOECHOSSH_num["hook_pretag_sshaddr"]  = TEST_ADDR

    pretag_custtag_ECHOSSH_BUTFAILS_num["tagtype"]  = "NUMTAG_PREHOOK_ECHOSSH_BUTFAILS"
    pretag_custtag_ECHOSSH_BUTFAILS_num["hook_pretag_script"]  = "echo \"%s\" && return 1" % script_comment
    pretag_custtag_ECHOSSH_BUTFAILS_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_ECHOSSH_BUTFAILS_num["hook_pretag_sshaddr"]  = TEST_ADDR
    pretag_custtag_NOECHOSSH_ANDFAILS_num["tagtype"] = "NAMETAG_PREHOOK_NOECHOSSH_AND_FAILS"
    pretag_custtag_NOECHOSSH_ANDFAILS_num["hook_pretag_script"] = "echo \"AAA\" > /dev/null && return 1"
    pretag_custtag_NOECHOSSH_ANDFAILS_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_NOECHOSSH_ANDFAILS_num["hook_pretag_sshaddr"]  = TEST_ADDR

    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_ECHOSSH_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_NOECHOSSH_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_ECHOSSH_BUTFAILS_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_NOECHOSSH_ANDFAILS_num )

    #pretag ECHOSSH numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_num["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   out_ssh_string,
                                   "tagging over ssh, echo script" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   script_comment,
                                   "tagging over ssh, echo script" )


    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag comment for %s - \n%s\n" % (created_custtag_label, tag_comment) )
    self.assertTrue( script_comment in tag_comment, "FAILED creating tag: comment wothout %s inside %s" % ( script_comment, tag_comment) )


    #pretag ECHOSSH numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_num["tagtype"], msg = user_comment )
    self.util_check_SUCC_scenario( out, errCode, 
                                   out_ssh_string,
                                   "tagging over ssh, echo script with message" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   script_comment,
                                   "tagging over ssh, echo script with message" )

    created_custtag_label_1 = "%s/%s/001" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag comment for %s - \n%s\n" % (created_custtag_label_1, tag_comment) )
    self.assertTrue( script_comment in tag_comment, "FAILED creating tag: comment without hook output %s inside %s" % ( script_comment, tag_comment) )
    self.assertTrue( user_comment in tag_comment, "FAILED creating tag: comment without user output %s inside %s" % ( user_comment, tag_comment) )


    #pretag NOECHOSSH numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_num["tagtype"] )
    self.assertTrue( out_ssh_string in out, "FAILED tagging over ssh, noecho script" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "returned empty string. Please specify at least -m option",
                                   "tagging over ssh, noecho script" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag NOECHOSSH numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_num["tagtype"], msg = user_comment )
    self.util_check_SUCC_scenario( out, errCode, 
                                   out_ssh_string,
                                   "tagging over ssh, no echo script with message" )
    self.assertTrue( out_ssh_string in out, "FAILED tagging over ssh, noecho script with message" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, "FAILED creating tag: commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag comment for %s - \n%s\n" % (created_custtag_label_1, tag_comment) )
    self.assertTrue( script_comment not in tag_comment, "FAILED creating tag: comment without hook output %s inside %s" % ( script_comment, tag_comment) )
    self.assertTrue( user_comment in tag_comment, "FAILED creating tag: comment without user output %s inside %s" % ( user_comment, tag_comment) )


    #pretag ECHOSSH + FAILS numtag, without msg
    # do not consider script output
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_BUTFAILS_num["tagtype"] )
    self.assertTrue( out_ssh_string in out, "FAILED tagging over ssh, echo script, but fails" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NUMTAG_PREHOOK_ECHOSSH_BUTFAILS pre-tag hook",
                                   "tagging over ssh, echo script, but fails" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_BUTFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag ECHOSSH + FAILS numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_BUTFAILS_num["tagtype"], msg = user_comment )
    self.assertTrue( out_ssh_string in out, "FAILED tagging over ssh, noecho script, but fails" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NUMTAG_PREHOOK_ECHOSSH_BUTFAILS pre-tag hook",
                                   "tagging over ssh, noecho script, but fails" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_BUTFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NUMTAG_PREHOOK_ECHOSSH_BUTFAILS pre-tag hook",
                                   "tagging with ssh pre-tag numbered returning error" )


    #pretag NOECHOSSH + FAILS numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_ANDFAILS_num["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM without msg and with noecho hook - \n%s\n" % out )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_ANDFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag NOECHOSSH = FAILS numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_ANDFAILS_num["tagtype"], msg = user_comment )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM with msg and with noecho hook - \n%s\n" % out )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_ANDFAILS_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NAMETAG_PREHOOK_NOECHOSSH_AND_FAILS pre-tag hook",
                                   "tagging with ssh pre-tag numbered returning error" )
   

  def test_Tag_06_04_CustomTags_Hook_PreTag_OverSsh_WrongVals( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #
    # remote wrong scripts
    #

    #
    # ssh custom tag WITHOUT IP
    #   must always fail
    #
    pretag_custtag_ECHOSSH_noip_num   = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_NOECHOSSH_noip_num = copy.deepcopy( CUSTTAG_NUM )

    script_comment = "comment: ABCD"
    pretag_custtag_ECHOSSH_noip_num["tagtype"]  = "NUMTAG_PREHOOK_ECHOSSH_NOIP"
    pretag_custtag_ECHOSSH_noip_num["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    pretag_custtag_ECHOSSH_noip_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_ECHOSSH_noip_num["hook_pretag_sshaddr"]  = ""
    pretag_custtag_NOECHOSSH_noip_num["tagtype"] = "NAMETAG_PREHOOK_NOECHOSSH_NOIP"
    pretag_custtag_NOECHOSSH_noip_num["hook_pretag_script"] = "echo \"AAA\" > /dev/null"
    pretag_custtag_NOECHOSSH_noip_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_NOECHOSSH_noip_num["hook_pretag_sshaddr"]  = ""

    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_ECHOSSH_noip_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_NOECHOSSH_noip_num )

    #pretag ECHOSSH noip numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_noip_num["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM without msg but with echo hook and no ip - \n%s\n" % out )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_noip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag ECHOSSH noip numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_noip_num["tagtype"], msg = user_comment )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM with msg and with echo hook and no ip - \n%s\n" % out )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_noip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )


    #pretag NOECHOSSH noip numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_noip_num["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM without msg and with noecho hook and no ip - \n%s\n" % out )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_noip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag NOECHOSSH noip numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_noip_num["tagtype"], msg = user_comment )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM with msg and with noecho hook and no ip - \n%s\n" % out )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_noip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )

    #
    # ssh custom tag with WRONG IP
    #   when -m is provisioned, it is enough
    #
    pretag_custtag_ECHOSSH_wrongip_num   = copy.deepcopy( CUSTTAG_NUM )
    pretag_custtag_NOECHOSSH_wrongip_num = copy.deepcopy( CUSTTAG_NUM )

    script_comment = "comment: ABCD"
    pretag_custtag_ECHOSSH_wrongip_num["tagtype"]  = "NUMTAG_PREHOOK_ECHOSSH_WRONGIP"
    pretag_custtag_ECHOSSH_wrongip_num["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    pretag_custtag_ECHOSSH_wrongip_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_ECHOSSH_wrongip_num["hook_pretag_sshaddr"]  = "127"  #invalid IP
    pretag_custtag_NOECHOSSH_wrongip_num["tagtype"] = "NAMETAG_PREHOOK_NOECHOSSH_WRONGIP"
    pretag_custtag_NOECHOSSH_wrongip_num["hook_pretag_script"] = "echo \"AAA\" > /dev/null"
    pretag_custtag_NOECHOSSH_wrongip_num["hook_pretag_sshuser"]  = TEST_USER_SSH
    pretag_custtag_NOECHOSSH_wrongip_num["hook_pretag_sshaddr"]  = "127"

    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_ECHOSSH_wrongip_num )
    self.swgitUtil_Clone_.tag_define_custom_tag( pretag_custtag_NOECHOSSH_wrongip_num )

    #pretag ECHOSSH wrongip numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_wrongip_num["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM without msg but with echo hook and wrong ip - \n%s\n" % out )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_wrongip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag ECHOSSH wrongip numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_ECHOSSH_wrongip_num["tagtype"], msg = user_comment )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NUMTAG_PREHOOK_ECHOSSH_WRONGIP pre-tag hook",
                                   "tagging pretag_custtag_ECHOSSH_wrongip_num, with message" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_ECHOSSH_wrongip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )


    #pretag NOECHOSSH wrongip numtag, without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_wrongip_num["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NAMETAG_PREHOOK_NOECHOSSH_WRONGIP pre-tag",
                                   "tagging pretag_custtag_NOECHOSSH_wrongip_num, no message" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_wrongip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #pretag NOECHOSSH wrongip numtag, with msg
    user_comment = "MESSAGE IN A BOTTLE"
    out, errCode = self.swgitUtil_Clone_.tag_create( pretag_custtag_NOECHOSSH_wrongip_num["tagtype"], msg = user_comment )
    self.util_check_DENY_scenario( out, errCode, 
                                   "FAILED - NAMETAG_PREHOOK_NOECHOSSH_WRONGIP pre-tag hook",
                                   "tagging pretag_custtag_NOECHOSSH_wrongip_num, with message" )

    created_custtag_label_1 = "%s/%s/000" % ( self.CREATED_BR, pretag_custtag_NOECHOSSH_wrongip_num["tagtype"] )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )



  def test_Tag_07_00_CustomTags_Overload_list_regexp( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #define custom tags
    self.swgitUtil_Clone_.tag_define_custom_tag( CUSTTAG_NUM )
    self.swgitUtil_Clone_.tag_define_custom_tag( CUSTTAG_NAME )

    basekey_num  = "swgit.%s." % CUSTTAG_NUM["tagtype"]
    basekey_name = "swgit.%s." % CUSTTAG_NAME["tagtype"]

    #chenge regexp
    self.swgitUtil_Clone_.set_cfg( basekey_num  + "regexp", "^[a-z]{3}$" )
    self.swgitUtil_Clone_.set_cfg( basekey_name + "regexp", "^[a-z]{3}$" )

    #
    # NUM NOW BECOMES A NAMED!!!
    #
    #simple numtag, with val without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], "avalue" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM now NAME plus value (wrong regexp) - \n%s\n" % out )
    #simple numtag, with val and with msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], "avalue", msg = "something" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM now NAME plus value (wrong regexp) - \n%s\n" % out )
    #simple numtag, without val and without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], "avalue" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM now NAME without msg and hook name (wrong regexp) - \n%s\n" % out )
    #simple numtag NOW FAILS TOO
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], msg = "something" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM now NAME creation without name - \n%s\n" % out )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, CUSTTAG_NUM["tagtype"] )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #OLD NUM now NAME can be created with msg and right name
    value = "abc"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM["tagtype"], value, msg = "old num now named tag" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NUM now NAME respecting regexp - \n%s\n" % out )

    created_custtag_label_0 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NUM["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_0, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, 
        "FAILED creating tag CUSTTAG_NAME with first regexp commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )



    #
    #NAME CHANGED
    #
    #simple nametag, without val without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME without value - \n%s\n" % out )
    #simple nametag, without val with msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], msg = "someother" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME without value - \n%s\n" % out )
    #simple nametag, with val without msg
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"] )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME without message - \n%s\n" % out )

    #simple nametag correct AND ALL OLD REGEXP MUST FAIL
    value = "abc"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], value, msg = "someother first regexp" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NAME respecting FIRST regexp - \n%s\n" % out )

    created_custtag_label_0 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_0, tag0_sha) )
    self.assertEqual( commit0_sha, tag0_sha, 
        "FAILED creating tag CUSTTAG_NAME with first regexp commit sha (%s) different from tag sha (%s)" % ( commit0_sha, tag0_sha) )

    value = "DropAB_2"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], value, msg = "someother first regexp" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME respecting FIRST regexp, now overloaded with config - \n%s\n" % out )

    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )

    value = "Issue12345"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME["tagtype"], value , msg = "someother second regexp" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME respecting SECOND regexp, now overloaded with config - \n%s\n" % out )

    created_custtag_label_2 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_2 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_2, tag0_sha) )


  def test_Tag_07_01_CustomTags_Overload_bool_oneXcommit( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #
    # NOFIRST CREATE LABELS ONE_X_COMMIT = True
    #
    CUSTTAG_NUM_ONEXCOMMIT   = copy.deepcopy( CUSTTAG_NUM )
    CUSTTAG_NAME_ONEXCOMMIT  = copy.deepcopy( CUSTTAG_NAME )
    CUSTTAG_NUM_ONEXCOMMIT["one_x_commit"]  = "True"
    CUSTTAG_NAME_ONEXCOMMIT["one_x_commit"] = "True"
    self.swgitUtil_Clone_.tag_define_custom_tag( CUSTTAG_NUM_ONEXCOMMIT )
    self.swgitUtil_Clone_.tag_define_custom_tag( CUSTTAG_NAME_ONEXCOMMIT )

    #
    # create 2 labels, must fail second
    #
    #NUM0
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM_ONEXCOMMIT["tagtype"], msg = "something num" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NUM - \n%s\n" % out )
    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, CUSTTAG_NUM_ONEXCOMMIT["tagtype"] )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #NUM1
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM_ONEXCOMMIT["tagtype"], msg = "something num second" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM on same commit - \n%s\n" % out )
    created_custtag_label = "%s/%s/001" % ( self.CREATED_BR, CUSTTAG_NUM_ONEXCOMMIT["tagtype"] )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #NAME0
    value = "Issue12345"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value , msg = "someother name" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NAME respecting SECOND regexp - \n%s\n" % out )
    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )

    #NAME1
    value = "Issue77777"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value , msg = "someother name second" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME second on same - \n%s\n" % out )
    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )


    #
    # NOW OVERLOAD ONE_X_COMMIT BUT WITH WRONG BOOL VALUE = Falseeeee
    #
    basekey_num  = "swgit.%s." % CUSTTAG_NUM["tagtype"]
    basekey_name = "swgit.%s." % CUSTTAG_NAME["tagtype"]

    #chenge regexp
    self.swgitUtil_Clone_.set_cfg( basekey_num  + "one-x-commit", "Falseeee" )
    self.swgitUtil_Clone_.set_cfg( basekey_name + "one-x-commit", "Falseeee" )

    #NUM1
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM_ONEXCOMMIT["tagtype"], msg = "something num second" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NUM on same commit - \n%s\n" % out )
    created_custtag_label = "%s/%s/001" % ( self.CREATED_BR, CUSTTAG_NUM_ONEXCOMMIT["tagtype"] )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #NAME1
    value = "Issue77777"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value , msg = "someother name second" )
    self.assertEqual( errCode, 1, "MUST FAIL CUSTTAG NAME second on same - \n%s\n" % out )
    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )

    #
    # NOW OVERLOAD ONE_X_COMMIT = False
    #
    basekey_num  = "swgit.%s." % CUSTTAG_NUM["tagtype"]
    basekey_name = "swgit.%s." % CUSTTAG_NAME["tagtype"]

    #chenge regexp
    self.swgitUtil_Clone_.set_cfg( basekey_num  + "one-x-commit", "False" )
    self.swgitUtil_Clone_.set_cfg( basekey_name + "one-x-commit", "False" )

    #NUM1
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NUM_ONEXCOMMIT["tagtype"], msg = "something num second" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NUM on same commit after overriding one-x-commit = False - \n%s\n" % out )
    created_custtag_label = "%s/%s/001" % ( self.CREATED_BR, CUSTTAG_NUM_ONEXCOMMIT["tagtype"] )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label, tag0_sha) )

    #NAME1
    value = "Issue77777"
    out, errCode = self.swgitUtil_Clone_.tag_create( CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value , msg = "someother name second" )
    self.assertEqual( errCode, 0, "FAILED CUSTTAG NAME second on same commit after overriding one-x-commit = False - \n%s\n" % out )
    created_custtag_label_1 = "%s/%s/%s" % ( self.CREATED_BR, CUSTTAG_NAME_ONEXCOMMIT["tagtype"], value )
    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_custtag_label_1, tag0_sha) )


  def test_Tag_08_00_Delete( self ):
    self.clone_createBr()
    self.modify_and_commit()
    commit0_sha, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Clone_.get_currsha FAILED - \n%s\n" % commit0_sha )

    #dev only local
    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "local dev" )
    self.assertEqual( errCode, 0, "FAILED tag DEV - \n%s\n" % out )

    #simulate a tag previously pushed
    origin_dev = "origin/" + ORIG_REPO_DEVEL_BRANCH
    out, errCode = self.gitUtil_Clone_.tag_put_on_commit( self.CREATED_DEV_1, origin_dev )
    self.assertEqual( errCode, 0, "FAILED tag DEV in past, on refernce %s - \n%s\n" % (origin_dev, out) )

    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_DEV_0 )
    self.assertEqual( errCode, 0, "FAILED tag delete of %s - \n%s\n" % (self.CREATED_DEV_0, out) )

    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_DEV_1 )
    self.assertEqual( errCode, 1, "MUST FAIL tag delete of already pushed tag (%s) - \n%s\n" % (self.CREATED_DEV_1, out) )

    out, errCode = self.swgitUtil_Clone_.tag_delete( TEST_REPO_TAG_LIV )
    self.assertEqual( errCode, 1, "MUST FAIL tag delete of LIV label on NON integrator repo (%s) - \n%s\n" % (TEST_REPO_TAG_LIV,  out) )



  def test_Tag_08_01_DeleteRemote_mine( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.TAG_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    #new must be denied
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "tags can be deleted only by deleting associated branch", "delete tag" )

    #push
    if modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_Clone_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    #move afterwards
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ddd" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "commit" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # check tag existence remote
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # delete not forced no-op
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_DEV )
    self.util_check_DENY_scenario( out, errCode, "Cannot delete a tag already pushed on origin", "delete tag" )

    # delete not forced no-op
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_FIX )
    self.util_check_DENY_scenario( out, errCode, "Cannot delete a tag already pushed on origin", "delete tag" )

    # delete not forced no-op
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "tags can be deleted only by deleting associated branch", "delete tag" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # check tag existence remote
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )


    #
    # forced delete DEV
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_DEV )
    self.util_check_SUCC_scenario( out, errCode, "Deleting also remote tag", "delete tag -D" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not exists %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # check tag existence remote
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not find %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    #
    # re-forced delete DEV
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid tag to be deleted", 
                                   "re-delete tag -D" )

    #
    # forced delete FIX
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_FIX )
    self.util_check_SUCC_scenario( out, errCode, "Deleting also remote tag", "delete tag -D" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not exists %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must not exists %s" % self.CREATED_BR_FIX )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )

    #
    # forced delete NEW
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "tags can be deleted only by deleting associated branch", "delete NEW" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not exists %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must not exists %s" % self.CREATED_BR_FIX )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )



  def test_Tag_08_02_DeleteRemote_mine_fromDetached( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.TAG_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    #new must be denied
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "tags can be deleted only by deleting associated branch", "delete tag" )

    #push
    if modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_Clone_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    #move detached
    shaStable, err = self.swgitUtil_Clone_.ref2sha( "origin/" + ORIG_REPO_STABLE_BRANCH )
    out, errCode = remote_h.branch_switch_to_br( shaStable )
    self.util_check_SUCC_scenario( out, errCode, "", "go detached" )


    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # check tag existence remote
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # delete not forced no-op
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_DEV )
    self.util_check_DENY_scenario( out, errCode, "Cannot delete a tag already pushed on origin", "delete tag" )

    # delete not forced no-op
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_FIX )
    self.util_check_DENY_scenario( out, errCode, "Cannot delete a tag already pushed on origin", "delete tag" )

    # delete not forced no-op
    out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "tags can be deleted only by deleting associated branch", "delete tag" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # check tag existence remote
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )


    #
    # forced delete DEV
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_DEV )
    self.util_check_SUCC_scenario( out, errCode, "Deleting also remote tag", "delete tag -D" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not exists %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    # check tag existence remote
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not find %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    #
    # re-forced delete DEV
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid tag to be deleted", 
                                   "re-delete tag -D" )

    #
    # forced delete FIX
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_FIX )
    self.util_check_SUCC_scenario( out, errCode, "Deleting also remote tag", "delete tag -D" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not exists %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must not exists %s" % self.CREATED_BR_FIX )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )

    #
    # forced delete NEW
    out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "tags can be deleted only by deleting associated branch", "delete NEW" )

    # check tag existence local
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not exists %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must not exists %s" % self.CREATED_BR_FIX )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_Clone_.ref2sha( self.CREATED_BR )[1], 0, "Not found %s" % self.CREATED_BR )


  def test_Tag_08_03_DeleteRemote_NotPushed( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.TAG_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    out, errCode = self.gitUtil_Clone_.ref2sha( self.CREATED_BR_DEV )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving local %s" % self.CREATED_BR_DEV )
    out, errCode = self.sw_origrepo_h.ref2sha( self.CREATED_BR_DEV )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving remote %s" % self.CREATED_BR_DEV )

    #
    # forced delete DEV
    if modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_DEV )
      self.util_check_DENY_scenario( out, errCode, "No remote branch found for branch name", "delete tag -e" )
      out, errCode = self.swgitUtil_Clone_.tag_delete( self.CREATED_BR_DEV )
      self.util_check_SUCC_scenario( out, errCode, "", "delete tag -d" )
    else:
      out, errCode = self.swgitUtil_Clone_.tag_delete_e( self.CREATED_BR_DEV )
      self.util_check_SUCC_scenario( out, errCode, "Deleting also remote tag", "delete tag -e" )




  #  HERE IS IN PAST FOR EVERYONE BUT ON CLONE POINT
  #
  #  repo                     
  #    |                      
  #    A
  #    |\                     
  #    | B 
  #    | |                 
  #    | C <-- orig_modbr 
  #    |/                        vvvv    
  #    D   <-- o/dev and dev and HEAD
  #     \                        ^^^^
  #      E    <-- prova_tag
  #
  def test_Tag_09_00_TagInPast_OnClonePoint( self ):
    self.clone_createBr( somecommmitondev = True )
    self.modify_and_commit()

    sha_clonetime, errCode = self.gitUtil_Clone_.get_currsha( "origin/%s" % ORIG_REPO_DEVEL_BRANCH  )

    #goto int
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "FAILED switch to int - out:\n%s" % out )

    sha_intbr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( sha_clonetime, sha_intbr, "FAILED switch to int , another place %s- out:\n%s" % (sha_intbr,out) )

    #define custom tag
    TAG_NUM_ECHO_NOPAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_NOPAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_NOPAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_NOPAST["tag_in_past"]  = "falSe"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_NOPAST )

    #create tag
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Commit you are tagging is already pushed on origin",
                                   "tagging in past a nopast label" )


    #overload option to allow tagging
    basekey_num  = "swgit.%s." % TAG_NUM_ECHO_NOPAST["tagtype"]
    self.swgitUtil_Clone_.set_cfg( basekey_num  + "tag-in-past", "TRue" )

    #create tag
    # NOTE: on INT MUST BE INT develop the tag base
    BASEBR = ORIG_REPO_DEVEL_BRANCH
    created_custtag_label = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_NOPAST["tagtype"] )
    created_custtag_PAST_label = "PAST/%s" % created_custtag_label

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )

    #commit and clone int br
    out, errCode = self.gitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "commit on INT" )
    out, errCode = self.swgitUtil_Repo_.branch_switch_to_br( self.ORIG_MOD_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )
    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    #check tag existenge and not
    out, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )
    out, errCode = self.gitUtil_Repo_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s on origin" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Repo_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s on origin" % created_custtag_PAST_label )


  #  HERE IS IN PAST FOR EVERYONE BUT NOT IN DETACHED
  #
  #  repo                     
  #    |                      
  #    A
  #    |\                     
  #    | B 
  #    | |                    vvvv   
  #    | C <-- orig_modbr and HEAD
  #    |/                     ^^^^  
  #    D   <-- o/dev and dev
  #     \                        
  #      E    <-- prova_tag
  #
  def test_Tag_09_01_TagInPast_OnOriginBranch( self ):
    self.clone_createBr( somecommmitondev = True )
    self.modify_and_commit()

    ORIGBR_INPAST = "origin/%s" % self.ORIG_MOD_FULL_BRANCH
    sha_origbr, errCode = self.gitUtil_Clone_.get_currsha( ORIGBR_INPAST )

    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( self.ORIG_MOD_BRANCH )
    self.assertEqual( errCode, 0, "FAILED switch to br %s - out:\n%s" % ( self.ORIG_MOD_BRANCH, out) )

    sha_curr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( sha_curr, sha_origbr, "FAILED switch to br, another place %s- out:\n%s" % (self.ORIG_MOD_BRANCH,out) )

    #define custom tag
    TAG_NUM_ECHO_NOPAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_NOPAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_NOPAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_NOPAST["tag_in_past"]  = "falSe"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_NOPAST )

    #create tag
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Commit you are tagging is already pushed on origin",
                                   "tagging in past a nopast label" )


    #overload option to allow tagging
    basekey_num  = "swgit.%s." % TAG_NUM_ECHO_NOPAST["tagtype"]
    self.swgitUtil_Clone_.set_cfg( basekey_num  + "tag-in-past", "TRue" )

    #create tag
    BASEBR = self.ORIG_MOD_FULL_BRANCH
    created_custtag_label = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_NOPAST["tagtype"] )
    created_custtag_PAST_label = "PAST/%s" % created_custtag_label

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )



  #  HERE IS IN PAST FOR EVERYONE (BEFORE ORIG/DEVELOP)
  #
  #  repo                     
  #    |                      
  #    A
  #    |\       vvvv          
  #    | B  <-- HEAD
  #    | |      ^^^^         
  #    | C <-- orig_modbr
  #    |/
  #    D   <-- o/dev and dev  
  #     \ 
  #      E    <-- prova_tag
  #
  def test_Tag_09_02_TagInPast_DetachedHead_PastForAll( self ):
    self.clone_createBr( somecommmitondev = True )
    self.modify_and_commit()

    DETACH_INPAST = "origin/%s~1" % self.ORIG_MOD_FULL_BRANCH
    sha_detachpoint, errCode = self.gitUtil_Clone_.get_currsha( DETACH_INPAST )

    #goto detached point in past
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACH_INPAST )
    self.assertEqual( errCode, 0, "FAILED switch to br %s - out:\n%s" % ( DETACH_INPAST, out) )

    sha_curr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( sha_curr, sha_detachpoint, "FAILED switch to point, another place %s- out:\n%s" % (sha_detachpoint,out) )

    #define custom tag
    TAG_NUM_ECHO_PAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_PAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_PAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_PAST["tag_in_past"]  = "tRuE"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_PAST )

    #overload option to NOT allow tagging
    basekey_num  = "swgit.%s." % TAG_NUM_ECHO_PAST["tagtype"]
    tag_cfg = basekey_num  + "tag-in-past"
    self.swgitUtil_Clone_.set_cfg( tag_cfg, "FAlse" )

    #create tag
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not configured to be put in past.",
                                   "tagging in past a nopast label" )

    #unset deny
    out, errCode = self.swgitUtil_Clone_.set_cfg( tag_cfg, SWCFG_TEST_UNSET )
    self.assertEqual( errCode, 0, "FAILED manually unsettin cfg - out:\n%s" % ( out ) )


    #create tag
    BASEBR = self.ORIG_MOD_FULL_BRANCH
    created_custtag_label = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_PAST["tagtype"] )
    created_custtag_PAST_label = "PAST/%s" % created_custtag_label

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )



  #  HERE IS IN PAST ONLY FOR ME (AFTER ORIG/DEVELOP)
  #       NOT PUSHED NOTHING TO ORIGIN
  #
  #  repo                     
  #    |                      
  #    A
  #    |\                     
  #    | B
  #    | |                   
  #    | C <-- orig_modbr
  #    |/
  #    D   <-- o/dev and dev  
  #     \      vvvv
  #      E <-- HEAD    << N.B. HERE is in past, but only for me (not already pushed) >>
  #      |     ^^^^
  #      F  <-- prova_tag
  #
  def test_Tag_09_03_TagInPast_DetachedHead_PastOnlyForMe( self ):
    self.clone_createBr( somecommmitondev = True )
    self.modify_and_commit()
    self.modify_and_commit()

    DETACH_INPAST = "%s~1" % self.CREATED_BR
    sha_detachpoint, errCode = self.gitUtil_Clone_.get_currsha( DETACH_INPAST )

    #goto detached point in past
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACH_INPAST )
    self.assertEqual( errCode, 0, "FAILED switch to br %s - out:\n%s" % ( DETACH_INPAST, out) )

    sha_curr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( sha_curr, sha_detachpoint, "FAILED switch to point, another place %s- out:\n%s" % (sha_detachpoint,out) )

    #define custom tag
    TAG_NUM_ECHO_PAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_PAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_PAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_PAST["tag_in_past"]  = "tRuE"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_PAST )

    #overload option to NOT allow tagging
    basekey_num  = "swgit.%s." % TAG_NUM_ECHO_PAST["tagtype"]
    tag_cfg = basekey_num  + "tag-in-past"
    self.swgitUtil_Clone_.set_cfg( tag_cfg, "FAlse" )

    #create tag
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "is not configured to be put in past.",
                                   "tagging in past a nopast label" )

    #unset deny
    out, errCode = self.swgitUtil_Clone_.set_cfg( tag_cfg, SWCFG_TEST_UNSET )
    self.assertEqual( errCode, 0, "FAILED manually unsettin cfg - out:\n%s" % ( out ) )


    #create tag
    BASEBR = self.CREATED_BR
    created_custtag_label = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_PAST["tagtype"] )
    created_custtag_PAST_label = "PAST/%s" % created_custtag_label

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )


  def test_Tag_09_04_TagInPast_AlreadyTaggedDownstream( self ):
    self.clone_createBr( somecommmitondev = True )

    #define custom tag
    TAG_NUM_ECHO_PAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_PAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_PAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_PAST["tag_in_past"]  = "tRuE"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_PAST )

    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit" )

    self.modify_and_commit( alsotags = False )
    self.modify_and_commit( alsotags = False )


    #create tag (this is not in past)
    BASEBR = self.CREATED_BR
    created_custtag_label_0 = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_PAST["tagtype"] )
    created_custtag_PAST_label_0 = "PAST/%s" % created_custtag_label_0

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.util_check_DENY_scenario( tag0_sha, errCode, "", "retrieving %s" % created_custtag_label_0 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_DENY_scenario( tagPast_sha, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, "",
                                   "tagging in past a past label" )
    self.assertTrue( "Tagging in past also creates tag" not in out,
                     "FAILED tagging not in past with a past-label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.util_check_SUCC_scenario( tag0_sha, errCode, "", "retrieving %s" % created_custtag_label_0 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_DENY_scenario( tagPast_sha, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )

    DETACH_INPAST = "%s~1" % self.CREATED_BR
    sha_detachpoint, errCode = self.gitUtil_Clone_.get_currsha( DETACH_INPAST )

    #goto detached point in past
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACH_INPAST )
    self.assertEqual( errCode, 0, "FAILED switch to br %s - out:\n%s" % ( DETACH_INPAST, out) )
    sha_curr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( sha_curr, sha_detachpoint, "FAILED switch to point, another place %s- out:\n%s" % (sha_detachpoint,out) )


    #create tag (this is in past)
    BASEBR = self.CREATED_BR
    created_custtag_label_1 = "%s/%s/001" % ( BASEBR, TAG_NUM_ECHO_PAST["tagtype"] )
    created_custtag_PAST_label_1 = "PAST/%s" % created_custtag_label_1

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    #re-create tag (this is in past)
    BASEBR = self.CREATED_BR
    created_custtag_label_1 = "%s/%s/002" % ( BASEBR, TAG_NUM_ECHO_PAST["tagtype"] )
    created_custtag_PAST_label_1 = "PAST/%s" % created_custtag_label_1

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode,
                                   "Tagging in past also creates tag",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    #now force 1 per commit, same previous re-create, now must fails
    basekey_num  = "swgit.%s." % TAG_NUM_ECHO_PAST["tagtype"]
    tag_cfg = basekey_num  + "one-x-commit"
    self.swgitUtil_Clone_.set_cfg( tag_cfg, "true" )

    #re-re-create tag (this is in past), but max 1 per commit
    BASEBR = self.CREATED_BR
    created_custtag_label_1 = "%s/%s/003" % ( BASEBR, TAG_NUM_ECHO_PAST["tagtype"] )
    created_custtag_PAST_label_1 = "PAST/%s" % created_custtag_label_1

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_PAST["tagtype"] )
    self.util_check_DENY_scenario( out, errCode,
                                   "You already have a",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )


  # This test try what happens when a branch comes first that INT/develop
  #  and in past this can happen
  #  git describe should choice orig_mod before orig/develop, and creates a unwanted name 
  #  Very difficult to chage behaviour...
  #  or
  #  to understand what the user want when tagging there...
  #  keep it in this way for the moment
  #
  #  repo                     
  #    |       vvvv              
  #    A  <--  HEAD
  #    |\      ^^^^              
  #    | B
  #    | |                   
  #    | C <-- orig_modbr
  #    |/
  #    D   <-- o/dev and dev  
  #     \ 
  #      E 
  #      |
  #      F  <-- prova_tag
  #
  def test_Tag_09_05_TagInPast_onOriginDev_abranchInMiddle( self ):
    self.clone_createBr( somecommmitondev = True )
    self.modify_and_commit()

    sha_clonetime,  errCode = self.gitUtil_Clone_.get_currsha()

    #goto int
    DETACHED_POINT = "%s/NEW/BRANCH~1" % self.ORIG_MOD_FULL_BRANCH
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACHED_POINT )
    self.assertEqual( errCode, 0, "FAILED switch to br - out:\n%s" % out )

    sha_intbr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertNotEqual( sha_clonetime, sha_intbr, "FAILED switch to int , another place %s- out:\n%s" % (sha_intbr,out) )

    #define custom tag
    TAG_NUM_ECHO_NOPAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_NOPAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_NOPAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_NOPAST["tag_in_past"]  = "True"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_NOPAST )

    #create tag
    # NOTE: this will choose nearest...
    #       not nice...
    #BASEBR = ORIG_REPO_DEVEL_BRANCH
    BASEBR = self.ORIG_MOD_FULL_BRANCH
    created_custtag_label = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_NOPAST["tagtype"] )
    created_custtag_PAST_label = "PAST/%s" % created_custtag_label

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past a past label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label )
    self.util_check_SUCC_scenario



  def test_Tag_09_06_TagInPast_NotPushOnOrigin( self ):
    self.clone_createBr( somecommmitondev = True )

    #define custom tag
    TAG_NOPUSH = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NOPUSH["tagtype"]             = "TAGINPAST"
    TAG_NOPUSH["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NOPUSH["tag_in_past"]  = "tRuE"
    TAG_NOPUSH["push_on_origin"]  = "false"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NOPUSH )

    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit" )

    self.modify_and_commit( alsotags = False )

    DETACH_INPAST = "HEAD~1"
    sha_detachpoint, errCode = self.gitUtil_Clone_.get_currsha( DETACH_INPAST )

    #goto detached point in past
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACH_INPAST )
    self.assertEqual( errCode, 0, "FAILED switch to br %s - out:\n%s" % ( DETACH_INPAST, out) )
    sha_curr, errCode = self.gitUtil_Clone_.get_currsha()
    self.assertEqual( sha_curr, sha_detachpoint, "FAILED switch to point, another place %s- out:\n%s" % (sha_detachpoint,out) )


    #create tag
    BASEBR = self.CREATED_BR
    created_custtag_label_1 = "%s/%s/000" % ( BASEBR, TAG_NOPUSH["tagtype"] )
    created_custtag_PAST_label_1 = "PAST/%s" % created_custtag_label_1

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NOPUSH["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, "",
                                   "tagging in past a past label" )
    self.assertTrue( "Tagging in past also creates tag" not in out, "FAILED also created PAST tag for a not push on origin label" )

    tag0_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.gitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )



  def test_Tag_10_00_ReuseComment( self ):
    self.clone_createBr()
    out, errCode = echo_on_file( self.MODIFY_FILE )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED echo" ) 
    TEST_MSG = "TEST COMMIT MESSAGE"
    out, errCode = self.swgitUtil_Clone_.commit_minusA( msg = TEST_MSG )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit" ) 

    #define custom tag no echo 
    TAG_NOECHO = copy.deepcopy( CUSTTAG_NUM )
    TAG_NOECHO["tagtype"] = "TAG_NOECHO"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NOECHO )

    #define custom tag echo 
    TAG_ECHO = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "TAG comment: ABCD"
    TAG_ECHO["tagtype"]             = "TAG_ECHO"
    TAG_ECHO["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_ECHO )

    #if test
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NOECHO["tagtype"], msg = "", reuse = False )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify option -m or -M or",
                                   "MUST FAIL, without -M, -m, noecho" )
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NOECHO["tagtype"], msg = "a msg", reuse = True )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify only one among",
                                   "MUST FAIL, with -M and -m" )
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_ECHO["tagtype"], msg = "", reuse = False )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED, without -M, -m, but yes echo" )
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_ECHO["tagtype"], msg = "a msg", reuse = True )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify only one among",
                                   "MUST FAIL, with -M and -m" )

    #paylod test

    #
    #echo => -M goes into body tag
    #
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_ECHO["tagtype"], reuse = True )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED, with -M, echo" )

    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, TAG_ECHO["tagtype"] )
    tag_comment, errCode = self.gitUtil_Clone_.tag_get_body( created_custtag_label )
    self.util_check_SUCC_scenario( tag_comment, errCode, 
                              TEST_MSG,
                              "FAILED, get_comment" )
    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label )
    self.util_check_SUCC_scenario( tag_comment, errCode, 
                              script_comment,
                              "FAILED, get_comment" )

    #
    #noecho => -M goes into subject tag
    #
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NOECHO["tagtype"], reuse = True )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED, with -M, noecho" )
    created_custtag_label = "%s/%s/000" % ( self.CREATED_BR, TAG_NOECHO["tagtype"] )
    tag_comment, errCode = self.gitUtil_Clone_.tag_get_subject( created_custtag_label )
    self.util_check_SUCC_scenario( tag_comment, errCode, 
                              TEST_MSG,
                              "FAILED, get_comment" )
    tag_comment, errCode = self.gitUtil_Clone_.tag_get_body( created_custtag_label )
    self.assertTrue( script_comment not in tag_comment, "FAILED, get_comment" )






if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()
