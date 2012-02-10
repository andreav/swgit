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

# assertEqual()
# assertTrue()
# assertRaises()

class Test_Clone( unittest.TestCase ):
  CLONE_DIR    = SANDBOX + "TEST_CLONE_REPO"

  #This method is executed before each test_*
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    if os.path.exists( self.CLONE_DIR ):
      shutil.rmtree( self.CLONE_DIR, True ) #ignore errors

    self.swgitUtil_ = swgit__utils( self.CLONE_DIR )
    self.gitUtil_   = git__utils( self.CLONE_DIR )

  #This method is executed after each test_*
  def tearDown( self ):
    #print  "tearDown"
    pass
  
  #Every test_* is executed when Test_Clone is runned
  def test_Clone_00_00_NonExistingRepo( self ):
    cmd = "%s clone %s%s %s -b %s" % ( SWGIT, REPO_SSHACCESS, ORIG_REPO_DIR + ORIG_REPO_NAME + "BLA", self.CLONE_DIR, ORIG_REPO_DEVEL_BRANCH )
    out, errCode = myCommand( cmd )
    self.assertNotEqual( errCode, 0, "SWGIT cloned DONE?? - %s" % cmd )


  def test_Clone_00_01_ScriptsRepo_allOptions( self ):
    self.assertFalse( os.path.exists( self.CLONE_DIR ), "SWGIT clone FAILED - %s already exists" % self.CLONE_DIR )

    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - _swgit__utils.clone_scripts_repo" )

    self.assertTrue( os.path.exists( self.CLONE_DIR ), "SWGIT clone FAILED - %s does not exists" % self.CLONE_DIR )


    # on branch develop
    out, errCode = self.gitUtil_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - git__utils.current_branch out: %s " % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "SWGIT branch not cloned - git__utils.current_branch out: %s " % out )

    # no other local branches
    out, errCode = self.gitUtil_.local_branches()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - git__utils.local_branches out: %s " % out )
    self.assertEqual( len( out.splitlines() ), 1, "SWGIT more/less than 1 local branch created - git__utils.local_branches out: %s  " % out )

  
  def test_Clone_01_00_ScriptsRepo_integrator( self ):
    self.assertFalse( os.path.exists( self.CLONE_DIR ), "SWGIT clone FAILED - %s already exists" % self.CLONE_DIR )

    # clone
    out, errCode = swgit__utils.clone_scripts_repo_integrator( self.CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone --integrator FAILED - _utils.clone_scripts_repo" )

    self.assertTrue( os.path.exists( self.CLONE_DIR ), "SWGIT clone FAILED - %s does not exists" % self.CLONE_DIR )

    # on branch develop
    out, errCode = self.gitUtil_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - git__utils.current_branch out: %s " % out )
    self.assertEqual( out[out.rfind("/")+1:], "develop", "SWGIT branch not cloned - git__utils.current_branch out: %s " % out )

    # develop, stable and slave branches
    for b in (ORIG_REPO_DEVEL_BRANCH, ORIG_REPO_STABLE_BRANCH):
      out, errCode = self.gitUtil_.branch_exists( b )
      self.assertEqual( self.gitUtil_.branch_exists( b )[1], 0, \
          "SWGIT clone integrator FAILED - branch does not exists: %s " % b )

  def test_Clone_01_01_ScriptsRepo_integrator_withBranchName( self ):
    self.assertFalse( os.path.exists( self.CLONE_DIR ), "SWGIT clone FAILED - %s already exists" % self.CLONE_DIR )

    # clone
    out, errCode = swgit__utils.clone_scripts_repo_integrator( self.CLONE_DIR, append=" -b %s" % ORIG_REPO_DEVEL_BRANCH )
    self.assertEqual( errCode, 0, "SWGIT clone --integrator FAILED - _utils.clone_scripts_repo" )

    self.assertTrue( os.path.exists( self.CLONE_DIR ), "SWGIT clone FAILED - %s does not exists" % self.CLONE_DIR )

    # on branch develop
    out, errCode = self.gitUtil_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - git__utils.current_branch out: %s " % out )
    self.assertEqual( out[out.rfind("/")+1:], "develop", "SWGIT branch not cloned - git__utils.current_branch out: %s " % out )

    # develop, stable and slave branches
    for b in (ORIG_REPO_DEVEL_BRANCH, ORIG_REPO_STABLE_BRANCH):
      out, errCode = self.gitUtil_.branch_exists( b )
      self.assertEqual( self.gitUtil_.branch_exists( b )[1], 0, \
          "SWGIT clone integratintegrator FAILED - branch does not exists: %s " % b )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()


