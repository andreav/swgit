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

from _utils import *
from _git__utils import *
from _swgit__utils import *

class Test_Checkout( unittest.TestCase ):
  CHECKOUT_DIR     = SANDBOX + "TEST_CHECKOUT_REPO"
  BRANCH_NAME      = "br_checkout"
  CREATED_BR       = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, BRANCH_NAME )
  BRANCH_NAME_2    = "br_checkout_2"
  BFILE_ONCLONE    = "%s/%s" % (CHECKOUT_DIR, TEST_REPO_FILE_B)

  
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.CHECKOUT_DIR, True )
    self.swgith_ = swgit__utils( self.CHECKOUT_DIR )
    self.gith_   = git__utils( self.CHECKOUT_DIR )
    self.CREATED_BR   = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, self.BRANCH_NAME )

  def tearDown( self ):
    pass

  def test_Checkout_01_00_BranchCreate( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.CHECKOUT_DIR )
    self.assertEqual( errCode, 0, "FAILED clone to %s - out:\n%s" % (self.CHECKOUT_DIR, out) )

    #create
    SUBCMD_CREATEBR = "checkout -b %s %s" % ( self.BRANCH_NAME, ORIG_REPO_DEVEL_BRANCH )

    out, errCode = self.swgith_.system_swgit( SUBCMD_CREATEBR )
    self.assertEqual( errCode, 1, "MUST FAILED create branch with checkout [%s] - out:\n%s" % (SUBCMD_CREATEBR, out) )

    #create from non exists src
    SUBCMD_CREATEBR_WRONG_SRC = "checkout -b %s %s_notexist" % ( self.BRANCH_NAME_2, ORIG_REPO_DEVEL_BRANCH )

    out, errCode = self.swgith_.system_swgit( SUBCMD_CREATEBR_WRONG_SRC )
    self.assertEqual( errCode, 1, "MUST FAIL create branch with checkout (wrong src) [%s] - out:\n%s" % (SUBCMD_CREATEBR_WRONG_SRC, out) )

    #create with bad name
    SUBCMD_CREATEBR_WRONG_BNAME = "checkout -b %s/a %s" % ( self.BRANCH_NAME_2, ORIG_REPO_DEVEL_BRANCH )

    out, errCode = self.swgith_.system_swgit( SUBCMD_CREATEBR_WRONG_BNAME )
    self.assertEqual( errCode, 1, "MUST FAIL create branch with checkout (wrong bname) [%s] - out:\n%s" % (SUBCMD_CREATEBR_WRONG_BNAME, out) )

    #create with dirty working dir
    out, errCode = echo_on_file( self.BFILE_ONCLONE )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )

    SUBCMD_CREATEBR_WRONG_DIRTYWD = "checkout -b %s %s" % ( self.BRANCH_NAME_2, ORIG_REPO_DEVEL_BRANCH )

    out, errCode = self.swgith_.system_swgit( SUBCMD_CREATEBR_WRONG_BNAME )
    self.assertEqual( errCode, 1, "MUST FAIL create branch with checkout (dirty WD) [%s] - out:\n%s" % (SUBCMD_CREATEBR_WRONG_BNAME, out) )


  def test_Checkout_02_00_FileUndo( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.CHECKOUT_DIR )
    self.assertEqual( errCode, 0, "FAILED clone to %s - out:\n%s" % (self.CHECKOUT_DIR, out) )
  
    #copy bkp
    CMD_BACKUP_FILE = "cp %s %s.before" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED command [%s] - out:\n%s" % (CMD_BACKUP_FILE, out) )

    #modif
    out, errCode = echo_on_file( self.BFILE_ONCLONE )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )

    #diff with bkp
    CMD_DIFF = "diff %s.before %s" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_DIFF )
    self.assertEqual( errCode, 1, "MUST FAIL command [%s] - out:\n%s" % (CMD_DIFF, out) )

    #undo
    CMD_CHECKOUT_UNDO = "checkout HEAD %s" % ( self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_swgit( CMD_CHECKOUT_UNDO )
    self.assertEqual( errCode, 0, "FAILED undo by checkout, command [%s] - out:\n%s" % (CMD_CHECKOUT_UNDO, out) )

    #diff with bkp
    CMD_DIFF = "diff %s.before %s" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED diff after undo, command [%s] - out:\n%s" % (CMD_DIFF, out) )

    #modif
    out, errCode = echo_on_file( self.BFILE_ONCLONE )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )

    #undo with --
    CMD_CHECKOUT_UNDO = "checkout HEAD -- %s" % ( self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_swgit( CMD_CHECKOUT_UNDO )
    self.assertEqual( errCode, 0, "FAILED undo by checkout, command [%s] - out:\n%s" % (CMD_CHECKOUT_UNDO, out) )

    #diff with bkp
    CMD_DIFF = "diff %s.before %s" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED diff after undo, command [%s] - out:\n%s" % (CMD_DIFF, out) )

    #modif
    out, errCode = echo_on_file( self.BFILE_ONCLONE )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )

    #undo with -- and 2 files
    CMD_CHECKOUT_UNDO = "checkout HEAD  %s %s" % ( TEST_REPO_FILE_A, TEST_REPO_FILE_B )
    out, errCode = self.swgith_.system_swgit( CMD_CHECKOUT_UNDO )
    self.assertEqual( errCode, 0, "FAILED undo by checkout, command [%s] - out:\n%s" % (CMD_CHECKOUT_UNDO, out) )

    #diff with bkp
    CMD_DIFF = "diff %s.before %s" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED diff after undo, command [%s] - out:\n%s" % (CMD_DIFF, out) )

    #modif
    out, errCode = echo_on_file( self.BFILE_ONCLONE )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )

    #undo to another version
    CMD_CHECKOUT_UNDO = "checkout HEAD~1 %s" % ( TEST_REPO_FILE_B )
    out, errCode = self.swgith_.system_swgit( CMD_CHECKOUT_UNDO )
    self.assertEqual( errCode, 0, "FAILED undo by checkout to another version, command [%s] - out:\n%s" % (CMD_CHECKOUT_UNDO, out) )

    #diff with bkp
    CMD_DIFF = "diff %s.before %s" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED diff after undo, command [%s] - out:\n%s" % (CMD_DIFF, out) )



  def test_Checkout_03_00_ChangeHead( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.CHECKOUT_DIR )
    self.assertEqual( errCode, 0, "FAILED clone to %s - out:\n%s" % (self.CHECKOUT_DIR, out) )
  
    sha_before, errCode = self.swgith_.get_currsha()
    sha_headtildeone, errCode = self.swgith_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED get_currsha - out:\n%s" % (out) )

    #change HEAD with dirty working dir
    out, errCode = echo_on_file( self.BFILE_ONCLONE )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )
  
    SUBCMD_CHNAGEHEAD = "checkout HEAD~1"
    out, errCode = self.swgith_.system_swgit( SUBCMD_CHNAGEHEAD )
    self.assertEqual( errCode, 1, "MUST FAIL change HEAD with dirty WD [%s] - out:\n%s" % (SUBCMD_CHNAGEHEAD, out) )
  
    #file undo + change with clean
    SUBCMD_UNDO = "checkout HEAD %s" % ( self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_swgit( SUBCMD_UNDO )
    self.assertEqual( errCode, 0, "FAILED undo [%s] - out:\n%s" % (SUBCMD_UNDO, out) )
  
    SUBCMD_CHNAGEHEAD = "checkout HEAD~1"
    out, errCode = self.swgith_.system_swgit( SUBCMD_CHNAGEHEAD )
    self.assertEqual( errCode, 0, "FAILED changing head to [%s] - out:\n%s" % (SUBCMD_CHNAGEHEAD, out) )
  
    sha_after, errCode = self.swgith_.get_currsha()
    self.assertEqual( errCode, 0, "FAILED get_currsha - out:\n%s" % (out) )
  
    #must change
    self.assertNotEqual( sha_before, sha_after, "FAILED change HEAD, not changed currsha" )
    self.assertEqual( sha_after, sha_headtildeone, "FAILED change HEAD, not changed currsha" )

  
  def test_Checkout_04_00_ConflictResolution( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.CHECKOUT_DIR )
    self.assertEqual( errCode, 0, "FAILED clone to %s - out:\n%s" % (self.CHECKOUT_DIR, out) )
  
    #create branche 1 modify commit
    out, errCode = self.swgith_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "FAILED create branch [%s] - out:\n%s" % (self.BRANCH_NAME, out) )
    out, errCode = echo_on_file( self.BFILE_ONCLONE, msg = "frombr1" )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )
    out, errCode = self.swgith_.commit_minusA()
    #copy bkp
    CMD_BACKUP_FILE = "cp %s %s.1" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED command [%s] - out:\n%s" % (CMD_BACKUP_FILE, out) )
    self.assertEqual( errCode, 0, "FAILED commit minus A - out:\n%s" % (out) )

    #create branche 2 modify commit
    out, errCode = self.swgith_.branch_create_src( self.BRANCH_NAME_2, ORIG_REPO_DEVEL_BRANCH )
    self.assertEqual( errCode, 0, "FAILED create branch [%s] --src [%s] - out:\n%s" % (self.BRANCH_NAME_2, ORIG_REPO_DEVEL_BRANCH, out) )
    out, errCode = echo_on_file( self.BFILE_ONCLONE, msg = "frombr2" )
    self.assertEqual( errCode, 0, "FAILED modify file %s - \n%s\n" % (self.BFILE_ONCLONE,out) )
    out, errCode = self.swgith_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit minus A - out:\n%s" % (out) )
    #copy bkp
    CMD_BACKUP_FILE = "cp %s %s.2" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED command [%s] - out:\n%s" % (CMD_BACKUP_FILE, out) )

    #merge other branch
    out, errCode = self.swgith_.merge( self.CREATED_BR )
    self.assertEqual( errCode, 1, "MUST FAIL merge with conflicts - out:\n%s" % (out) )

    SUBCMD_RESOLVEMERGE = "checkout --ours %s" % TEST_REPO_FILE_B
    out, errCode = self.swgith_.system_swgit( SUBCMD_RESOLVEMERGE )
    self.assertEqual( errCode, 0, "FAILED resolving mege with checkout [%s] - out:\n%s" % (SUBCMD_RESOLVEMERGE, out) )
  
    #diff with bkp
    CMD_DIFF = "diff %s %s.2" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED diff merge coonflict resolution, command [%s] - out:\n%s" % (CMD_DIFF, out) )

    #reset hard to retry
    SUBCMD_RESETHARD = "reset --hard HEAD"
    out, errCode = self.swgith_.system_swgit( SUBCMD_RESETHARD )
    self.assertEqual( errCode, 0, "FAILED reset hard command [%s] - out:\n%s" % (SUBCMD_RESETHARD, out) )

    #
    #re-merge other branch 
    #
    out, errCode = self.swgith_.merge( self.CREATED_BR )
    self.assertEqual( errCode, 1, "MUST FAIL merge with conflicts - out:\n%s" % (out) )

    SUBCMD_RESOLVEMERGE = "checkout --theirs %s" % TEST_REPO_FILE_B
    out, errCode = self.swgith_.system_swgit( SUBCMD_RESOLVEMERGE )
    self.assertEqual( errCode, 0, "FAILED resolving mege with checkout [%s] - out:\n%s" % (SUBCMD_RESOLVEMERGE, out) )

    #diff with bkp
    CMD_DIFF = "diff %s %s.1" % ( self.BFILE_ONCLONE, self.BFILE_ONCLONE )
    out, errCode = self.swgith_.system_unix( CMD_BACKUP_FILE )
    self.assertEqual( errCode, 0, "FAILED diff merge coonflict resolution, command [%s] - out:\n%s" % (CMD_DIFF, out) )

  
  
    
if __name__ == '__main__':

  manage_debug_opt( sys.argv )
  unittest.main()

