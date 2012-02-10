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

# assertEqual()
# assertTrue()
# assertRaises()

class Test_NoIntBr( Test_Base ):
  NOINTBR_REPO_DIR  = SANDBOX + "TEST_NOINTBRDIR_REPO/"
  NOINTBR_CLONE_DIR = SANDBOX + "TEST_NOINTBRDIR_CLONE/"
  BRANCH_NAME  = "nointbr_branch"
  CREATED_BR   = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, BRANCH_NAME )

  #This method is executed before each test_*
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.NOINTBR_REPO_DIR, True )
    shutil.rmtree( self.NOINTBR_CLONE_DIR, True )
    self.sw_Ori_h  = swgit__utils( self.NOINTBR_REPO_DIR )
    self.sw_Clo_h  = swgit__utils( self.NOINTBR_CLONE_DIR )
    self.git_Ori_h = git__utils( self.NOINTBR_REPO_DIR )
    self.git_Clo_h = git__utils( self.NOINTBR_CLONE_DIR )


  #This method is executed after each test_*
  def tearDown( self ):
    #print  "tearDown"
    pass

  def util_createrepo_2commit_goondetach( self ):
    out, errCode = create_dir_some_file( self.NOINTBR_REPO_DIR )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
    out, errCode = swgit__utils.init_dir( self.NOINTBR_REPO_DIR )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
    out, errCode = self.sw_Ori_h.branch_switch_to_br( ORIG_REPO_DEVEL_BRANCH )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
    out, errCode = self.sw_Ori_h.modify_repo( TEST_REPO_FILE_A, msg = "modify to create commit and go in detach-head", gotoint = False )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
    out, errCode = self.sw_Ori_h.modify_repo( TEST_REPO_FILE_A, msg = "modify 2 to create commit and go in detach-head", gotoint = False )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
    out, errCode = self.sw_Ori_h.branch_switch_to_br( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % out )
  

  def test_IntBr_00_00_set( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.NOINTBR_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "clone" )

    if modetest_morerepos():

      # with 2 alterantives
      out, errCode = self.sw_Clo_h.int_branch_set( ORIG_REPO_aBRANCH_NAME )
      self.util_check_DENY_scenario( out, errCode, 
                                     "Multiple matches found, please specify one among:", 
                                     "track ambiguous, both remotes" )

      #
      # intbr with remote path
      #
      out, errCode = self.sw_Clo_h.int_branch_set( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, 
                                     "",
                                     "track full remotes aremote" )

      intbr, errCode = self.sw_Clo_h.get_cfg( "swgit.intbranch" )
      self.assertEqual( intbr, ORIG_REPO_aBRANCH, "" )

      CFG_GETREMOTE = "branch.%s.remote" % intbr
      remote, errCode = self.sw_Clo_h.get_cfg( CFG_GETREMOTE )
      self.assertEqual( remote, ORIG_REPO_AREMOTE_NAME, "" )

      #
      # Same branch but different remote, must change only remote info
      #
      out, errCode = self.sw_Clo_h.int_branch_set( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, 
                                     "",
                                     "track full remotes origin" )

      intbr, errCode = self.sw_Clo_h.get_cfg( "swgit.intbranch" )
      self.assertEqual( intbr, ORIG_REPO_aBRANCH, "" )

      CFG_GETREMOTE = "branch.%s.remote" % intbr
      remote, errCode = self.sw_Clo_h.get_cfg( CFG_GETREMOTE )
      self.assertEqual( remote, "origin", "" )

    else:

      # no alternatives => short works
      out, errCode = self.sw_Clo_h.int_branch_set( ORIG_REPO_aBRANCH_NAME )
      self.util_check_SUCC_scenario( out, errCode, 
                                     "",
                                     "track short name" )

      intbr, errCode = self.sw_Clo_h.get_cfg( "swgit.intbranch" )
      self.assertEqual( intbr, ORIG_REPO_aBRANCH, "" )

      CFG_GETREMOTE = "branch.%s.remote" % intbr
      remote, errCode = self.sw_Clo_h.get_cfg( CFG_GETREMOTE )
      self.assertEqual( remote, "origin", "" )



  def test_NoIntBr_01_00_onto_detahced( self ):

    self.util_createrepo_2commit_goondetach()

    cmd = "%s clone %s%s %s" % ( SWGIT, REPO_SSHACCESS, self.NOINTBR_REPO_DIR, self.NOINTBR_CLONE_DIR )
    out, errCode = myCommand( cmd )
    self.assertEqual( errCode, 0, "FAILED clone - \n%s\n" % out )

    self.assertTrue( os.path.exists( self.NOINTBR_CLONE_DIR ), "clone FAILED - %s does not exists" % self.NOINTBR_CLONE_DIR )
    self.assertTrue( os.path.exists( self.NOINTBR_CLONE_DIR + "/.git" ), "clone FAILED - %s/.git does not exists" % self.NOINTBR_CLONE_DIR )

    # in detached head (on LIV)
    out, errCode = self.git_Clo_h.current_branch()
    self.assertEqual( errCode, 0, "FAILED get current branch: \n%s\n" % out )
    self.assertEqual( out, NO_BRANCH, "FAILED get current branch, not on %s: \n%s\n" % ( NO_BRANCH , out) )

    out, errCode = self.sw_Clo_h.current_branch()
    self.assertEqual( errCode, 0, "FAILED get current branch: \n%s\n" % out )
    self.assertEqual( out, DETACH_HEAD, "FAILED get current branch, not on %s: \n%s\n" % ( DETACH_HEAD , out) )

    #no int br set
    intbr, errCode = self.sw_Clo_h.int_branch_get()
    self.assertEqual( errCode, 1, "MUST FAIL get int branch: \n%s\n" % intbr )

    sha_before, errCode = self.sw_Clo_h.get_currsha()

    #cannot create br
    out, errCode = self.sw_Clo_h.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 1, "MUST FAIL branch create - \n%s\n" % out )

    #no pull
    out, errCode = self.sw_Clo_h.pull()
    self.assertEqual( errCode, 1, "MUST FAIL pull - \n%s\n" % out )

    sha_after, errCode = self.sw_Clo_h.get_currsha()
    self.assertEqual( sha_before, sha_after, "FAILED pull, should stand on same commit \n%s\n%s" % (sha_before, sha_after) )

    #no push
    out, errCode = self.sw_Clo_h.push()
    self.util_check_SUCC_scenario( out, errCode, "in DETAHCED-HEAD only tags put-in-past will be pushed.", "push" )

    sha_after, errCode = self.sw_Clo_h.get_currsha()
    self.assertEqual( sha_before, sha_after, "FAILED push, should stand on same commit \n%s\n%s" % (sha_before, sha_after) )

    #no tag dev
    out, errCode = self.sw_Clo_h.tag_create( "dev", msg = "dev must faul" )
    self.assertEqual( errCode, 1, "MUST FAIL tag dev - \n%s\n" % out )

    #yes tag fix
    out, errCode = self.sw_Clo_h.tag_create( "fix", "1234567", msg = "dev must faul" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Label FIX cannot be put on branch type INT,",
                                   "tag fix create" )



    #can create br with src

    out, errCode = self.sw_Clo_h.branch_create_src( self.BRANCH_NAME, "HEAD" )
    self.assertEqual( errCode, 0, "FAILED branch create with src - \n%s\n" % out )

    out, errCode = self.sw_Clo_h.current_branch()
    self.assertEqual( errCode, 0, "FAILED get current branch: \n%s\n" % out )
    self.assertEqual( out, self.CREATED_BR, "FAILED get current branch, not on %s: \n%s\n" % ( self.CREATED_BR, out) )

    sha_after, errCode = self.sw_Clo_h.get_currsha()
    self.assertEqual( sha_before, sha_after, "FAILED branch create with src - \n%s\n" % out )


  def test_NoIntBr_02_00_onto_INT( self ):

    self.util_createrepo_2commit_goondetach()
    self.assertEqual( 1, 0, "TODO" )

  def test_NoIntBr_03_00_onto_FTR( self ):

    self.util_createrepo_2commit_goondetach()
    self.assertEqual( 1, 0, "TODO" )


  def test_NoIntBr_04_00_onto_CST( self ):

    self.util_createrepo_2commit_goondetach()
    self.assertEqual( 1, 0, "TODO" )



if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()

