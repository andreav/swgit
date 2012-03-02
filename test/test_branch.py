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

class Test_Branch( Test_Base ):
  BRANCH_DIR    = SANDBOX + "TEST_BRANCH_REPO"
  BRANCH_NAME   = "prova_branch"
  BRANCH_NAME_2 = "prova_branch_2"
  
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.BRANCH_DIR, True )
    self.swgitUtil_ = swgit__utils( self.BRANCH_DIR )
    self.gitUtil_   = git__utils( self.BRANCH_DIR )
    self.DDTS             = "Issue12345"
    self.CREATED_BR       = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, self.BRANCH_NAME )
    self.CREATED_BR_NEWBR = "%s/NEW/BRANCH" % ( self.CREATED_BR )
    self.CREATED_BR_DEV   = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_BR_FIX   = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS )
    self.CREATED_BR_RDY   = "%s/RDY/000" % ( self.CREATED_BR )
    self.CREATED_BR_2 = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, self.BRANCH_NAME_2 )
    self.LIV          = "%s/%s/%s/INT/stable/LIV/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, ORIG_REPO_GITUSER, TEST_REPO_LIV )
    self.DEV          = "%s/DEV/000" % ORIG_REPO_aBRANCH
    self.CREATED_CHK  = "%s/%s/%s/CHK/LIV_DROP.%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, TEST_REPO_LIV )
    self.TRACK_BR     = "1/0/%s/%s/INT/develop" % ( ORIG_REPO_SUBREL, ORIG_REPO_GITUSER )

  def tearDown( self ):
    pass

  def check_repo_git_swgit_alignment( self ):
    br_develop = "origin/" + ORIG_REPO_DEVEL_BRANCH
    br_stable  = "origin/" + ORIG_REPO_STABLE_BRANCH

    # remote branches at least develop, stable (git)
    out_rem_git, errCode = self.gitUtil_.remote_branches()
    self.assertEqual( errCode, 0, "self.gitUtil_.remote_branches FAILED - out: %s " % out_rem_git )
    self.assertTrue( br_develop in out_rem_git.splitlines() , \
        "self.gitUtil_.remote_branches FAILED - not present  %s inside out\n%s" % ( br_develop, out_rem_git) )
    self.assertTrue( br_stable in out_rem_git.splitlines() , \
        "self.gitUtil_.remote_branches FAILED - not present  %s inside out\n%s" % ( br_stable, out_rem_git) )


    # remote branches at least develop, stable (swgit)
    out_rem_sw, errCode = self.swgitUtil_.remote_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.remote_branches FAILED - out: %s " % out_rem_sw )
    self.assertTrue( br_develop in out_rem_sw.splitlines() , \
        "self.swgitUtil_.remote_branches FAILED - not present  %s inside out\n%s" % ( br_develop, out_rem_sw) )
    self.assertTrue( br_stable in out_rem_sw.splitlines() , \
        "self.swgitUtil_.remote_branches FAILED - not present  %s inside out\n%s" % ( br_stable, out_rem_sw) )

    out_loc_git, errCode = self.gitUtil_.local_branches()
    out_loc_sw,  errCode = self.swgitUtil_.local_branches()

    # remote branches comparison
    out_rem_git.replace( "remotes/", "" ) #git and swgit have different output
    for b in out_rem_git.splitlines():
      if b.find( "master" ) != -1: #master is not deleted no more
        continue
      self.assertTrue( b in out_rem_sw.splitlines() , "branch [%s] not found inside swgit branches\n%s" % ( b, out_rem_sw ) )

    # local branches comparison
    for b in out_loc_git.splitlines():
      self.assertTrue( b in out_loc_sw.splitlines() , "branch [%s] not found inside swgit branches\n%s" % ( b, out_loc_sw ) )

    # user hudson (git)
    out_loc_git_hudson, errCode = self.gitUtil_.local_branches_byuser( ORIG_REPO_GITUSER )
    self.assertEqual( errCode, 0, "self.gitUtil_.local_branches_byuser FAILED - out: %s " % out_loc_git_hudson )
    self.assertEqual( len( out_loc_git_hudson.splitlines() ), 1, \
        "self.gitUtil_.local_branches_byuser not just 1 local branch for user %s - \nout\n%s" % ( ORIG_REPO_GITUSER, out_loc_git_hudson ) )
    self.assertEqual( out_loc_git_hudson.splitlines()[0], ORIG_REPO_DEVEL_BRANCH, \
        "self.gitUtil_.local_branches_byuser user %s not on branch %s - \nout\n%s" % ( ORIG_REPO_GITUSER, ORIG_REPO_DEVEL_BRANCH, out_loc_git_hudson ) )

    # user hudson (swgit)
    out_loc_sw_hudson, errCode = self.swgitUtil_.local_branches_byuser( ORIG_REPO_GITUSER )
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches_byuser FAILED - out: %s " % out_loc_sw_hudson )
    self.assertEqual( len( out_loc_sw_hudson.splitlines() ), 1, \
        "self.swgitUtil_.local_branches_byuser not just 1 local branch for user %s - \nout\n%s" % ( ORIG_REPO_GITUSER, out_loc_sw_hudson ) )
    self.assertEqual( out_loc_sw_hudson.splitlines()[0], ORIG_REPO_DEVEL_BRANCH, \
        "self.swgitUtil_.local_branches_byuser user %s not on branch %s - \nout\n%s" % ( ORIG_REPO_GITUSER, ORIG_REPO_DEVEL_BRANCH, out_loc_sw_hudson ) )

  
  def test_Branch_01_00_List( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # on branch develop (git)
    out, errCode = self.gitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.gitUtil_.current_branch FAILED - out: %s " % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "self.gitUtil_.current_branch - not on develop - out: %s " % out )

    # on branch develop (swgit)
    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out: %s " % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "self.swgitUtil_.current_branch FAILED - not on develop - out: %s " % out )

    # only 1 local branch (git)
    out_loc_git, errCode = self.gitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.gitUtil_.local_branches FAILED - out: %s " % out_loc_git )
    self.assertEqual( len( out_loc_git.splitlines() ), 1, "self.gitUtil_.local_branches FAILED - more/less than 1 branch - %s" % out_loc_git )

    # only 1 local branch (swgit)
    out_loc_sw, errCode = self.swgitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches FAILED - out: %s " % out_loc_sw )
    self.assertEqual( len( out_loc_sw.splitlines() ), 1, "self.swgitUtil_.local_branches FAILED - more/less than 1 branch - %s" % out_loc_sw )

    # git <--> swgit
    self.check_repo_git_swgit_alignment()

  def create_branch_and_check( self, numBranch=2, src = "" ):
    # create branch
    if src == "":
      out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
      self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )
    else:
      out, errCode = self.swgitUtil_.branch_create_src( self.BRANCH_NAME, src )
      self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.CREATED_BR, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( self.BRANCH_NAME, out) )

    # git <--> swgit
    self.check_repo_git_swgit_alignment()

    # 2 local branches
    out_loc_sw, errCode = self.swgitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches FAILED - out: %s " % out_loc_sw )
    self.assertEqual( len( out_loc_sw.splitlines() ), numBranch, "self.swgitUtil_.local_branches FAILED - more/less than 2 branch - %s" % out_loc_sw )
  
  
  #TODO check tags
  def test_Branch_02_00_Create( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    self.create_branch_and_check()

  def test_Branch_03_00_Switch_to_int( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.CREATED_BR, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( self.CREATED_BR, out ) )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "self.swgitUtil_.current_branch - not on develop - out:\n%s" % out )


  def test_Branch_03_01_Create_Switch( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.CREATED_BR, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( self.CREATED_BR, out ) )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "self.swgitUtil_.current_branch - not on develop - out:\n%s" % out )

    # re-create same branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertNotEqual( errCode, 0, "swgitUtil_.branch_create CREATED an ALREADY created branch - \n%s\n" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "self.swgitUtil_.current_branch - not on develop - out:\n%s" % out )


    # switch to new craeted branch
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.CREATED_BR )
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_br( %s ) FAILED - out:\n%s" % ( self.CREATED_BR, out ) )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.CREATED_BR, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( self.CREATED_BR, out ) )


    # re-switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, ORIG_REPO_DEVEL_BRANCH, "self.swgitUtil_.current_branch - not on develop - out:\n%s" % out )


  def test_Branch_03_02_Create_Switch( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    # create another branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_2 )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME_2, out ) )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.CREATED_BR_2, "self.swgitUtil_.current_branch() - not on %s - out:\n%s" % ( self.CREATED_BR_2, out) )

    # git <--> swgit
    self.check_repo_git_swgit_alignment()

    # 2 local branches
    out_loc_sw, errCode = self.swgitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches FAILED - out: %s " % out_loc_sw )
    self.assertEqual( len( out_loc_sw.splitlines() ), 3, "self.swgitUtil_.local_branches FAILED - NOT exactly 3 branch - %s" % out_loc_sw )

    
  def test_Branch_04_00_Delete_nonExistent( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # delete non existing it
    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.assertNotEqual( errCode, 0, "swgitUtil_.branch_create DELETED a non existet branch?? - \n%s\n" % out )


  def test_Branch_04_01_Delete_whileOnIt( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    # delete it while you are on it
    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.assertNotEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) DONE, but you are on that branch!?!? - \n%s\n" % ( self.BRANCH_NAME, out ) )


  def test_Branch_04_02_00_Delete_Nonexisting( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "does not exists", "delete not existing branch" )

    out, errCode = self.swgitUtil_.branch_delete_D( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "does not exists", "delete not existing branch" )

    out, errCode = self.swgitUtil_.branch_delete_E( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "does not exists", "delete not existing branch" )

    out, errCode = self.swgitUtil_.branch_delete_e( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "does not exists", "delete not existing branch" )




  def test_Branch_04_02_01_Delete_OnlyLocal_d( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    out, errCode = self.swgitUtil_.branch_delete_E( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "Not existing remote branch, try using -d/-D option instead", "deleteing only local branch" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

    out, errCode = self.swgitUtil_.branch_delete_e( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "Not existing remote branch, try using -d/-D option instead", "deleteing only local branch" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

    out, errCode = self.swgitUtil_.branch_delete_d( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "deleteing only local branch" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 1, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

  def test_Branch_04_02_02_Delete_OnlyLocal_D( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    out, errCode = self.swgitUtil_.branch_delete_E( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "Not existing remote branch, try using -d/-D option instead", "deleteing only local branch" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

    out, errCode = self.swgitUtil_.branch_delete_e( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "Not existing remote branch, try using -d/-D option instead", "deleteing only local branch" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

    out, errCode = self.swgitUtil_.branch_delete_D( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "deleteing only local branch" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 1, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 1, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 1, "get sha %s" % self.CREATED_BR_FIX )


  def test_Branch_04_02_03_Delete_OnlyRemote_e( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_d( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_d( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_d( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )

    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_NEWBR )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV0 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV0 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV1 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV1 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_FIX )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_FIX )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_D( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )

    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_NEWBR )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV0 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV0 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV1 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV1 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_FIX )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_FIX )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_e( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_e( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_e( ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_NEWBR )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV0 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV0 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV1 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV1 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_FIX )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_FIX )


  def test_Branch_04_02_04_Delete_OnlyRemote_E( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_d( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_d( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_d( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )

    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_NEWBR )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV0 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV0 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV1 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV1 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_FIX )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_FIX )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_d( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "deleteing only remote branch" )

    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_NEWBR )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV0 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV0 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV1 )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_DEV1 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_FIX )[1], 0, "get sha %s" % ORIG_REPO_aBRANCH_FIX )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_E( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_NEWBR )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV0 )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH_DEV0 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_DEV1 )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH_DEV1 )
    self.assertEqual( self.sw_origrepo_h.ref2sha( ORIG_REPO_aBRANCH_FIX )[1], 1, "get sha %s" % ORIG_REPO_aBRANCH_FIX )



  def test_Branch_04_03_Delete_Local_byShortName( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #
    # delete branch with contributes
    #
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "re-create same branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "delete br with contributes" )

    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR )[1], 1, "must not found %s" % self.CREATED_BR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "must not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR_DEV )[1], 1, "must not not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR_FIX )[1], 1, "must not not found %s" % self.CREATED_BR_FIX )



  def test_Branch_04_04_Delete_Local_D_byShortName( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    #
    # delete branch with contributes
    #
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "re-create same branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete -D  a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_D( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "delete -D br with contributes" )

    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Why found %s" % self.CREATED_BR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Why found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must not found %s" % self.CREATED_BR_FIX )

    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR )[1], 1, "must not found %s" % self.CREATED_BR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "must not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR_DEV )[1], 1, "must not not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.sw_origrepo_h.ref2sha( self.CREATED_BR_FIX )[1], 1, "must not not found %s" % self.CREATED_BR_FIX )



  def test_Branch_04_05_Delete_Local_E_byShortName( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    #
    # delete branch with contributes
    #
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "re-create same branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete -D  a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_E( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "Not existing remote branch", "delete -D br with contributes" )


  def test_Branch_04_06_Delete_LocalRemote_byShortName( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "origin switch to br" )
    if modetest_morerepos():
      #push on aRemote, just to test ... 
      out, errCode = self.swgitUtil_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_d( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Not found %s" % self.CREATED_BR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "not not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "not not found %s" % self.CREATED_BR_FIX )


  def test_Branch_04_07_Delete_LocalRemote_D_byShortName( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )
    if modetest_morerepos():
      #push on aRemote, just to test ... 
      out, errCode = self.swgitUtil_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    self.util_check_SUCC_scenario( out, errCode, "", "push" )
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_D( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Must Not found %s" % self.CREATED_BR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Must Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must Not found %s" % self.CREATED_BR_FIX )

    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 0, "not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "not not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "not not found %s" % self.CREATED_BR_FIX )


  def test_Branch_04_08_Delete_LocalRemote_e_byShortName( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )
    if modetest_morerepos():
      #push on aRemote, just to test ... 
      out, errCode = self.swgitUtil_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    self.util_check_SUCC_scenario( out, errCode, "", "push" )
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_e( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Must Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Must Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Must Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Must Not found %s" % self.CREATED_BR_FIX )

    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 1, "must not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "must not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 0, "must not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 0, "must not found %s" % self.CREATED_BR_FIX )




  def test_Branch_04_09_Delete_LocalRemote_E_byShortName( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch" )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_E( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Must Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Must Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must Not found %s" % self.CREATED_BR_FIX )

    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 1, "must not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "must not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 1, "must not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 1, "must not found %s" % self.CREATED_BR_FIX )


  def test_Branch_04_10_Delete_LocalRemote_E_withLocalTags( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #create file labels and push
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.swgitUtil_.tag_create( "rdy", msg = "message for RDY tag" )
    self.util_check_SUCC_scenario( out, errCode, "", "tag rdy" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch" )

    remote = ""
    remote_h = self.sw_origrepo_h
    if modetest_morerepos():
      remote   = ORIG_REPO_AREMOTE_NAME
      remote_h = self.sw_aremoterepo_h

    out, errCode = self.swgitUtil_.push_with_merge( remote )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )

    # delete a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_E( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.BRANCH_NAME, out ) )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Must Not found %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Must Not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Must Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Must Not found %s" % self.CREATED_BR_FIX )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_RDY )[1], 1, "Must Not found %s" % self.CREATED_BR_RDY )

    self.assertEqual( remote_h.ref2sha( self.CREATED_BR )[1], 1, "must not found %s" % self.CREATED_BR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "must not found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_DEV )[1], 1, "must not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_FIX )[1], 1, "must not found %s" % self.CREATED_BR_FIX )
    self.assertEqual( remote_h.ref2sha( self.CREATED_BR_RDY )[1], 1, "must not found %s" % self.CREATED_BR_RDY )




  def test_Branch_04_10_Delete_byLongName( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_int FAILED - out:\n%s" % out )

    # delete a branch whith long name
    out, errCode = self.swgitUtil_.branch_delete_d( self.CREATED_BR )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_delete_d( %s ) FAILED - \n%s\n" % ( self.CREATED_BR, out ) )

    # delete remote branch
    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_d( ORIG_REPO_STABLE_BRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among", "delete remote branch" )
    else:
      out, errCode = self.swgitUtil_.branch_delete_d( ORIG_REPO_STABLE_BRANCH )
      self.util_check_DENY_scenario( out, errCode, "Not existing local branch, try using -e/-E option instead", "delete remote branch" )

    #
    # delete branch with contributes
    #
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "re-create same branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )


    # delete -D  a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_d( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "delete -D br with contributes" )

    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Why found %s" % self.CREATED_BR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Why found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "Not found %s" % self.CREATED_BR_FIX )

    out, errCode = self.swgitUtil_.system_unix( "git tag -d %s" % self.CREATED_BR_DEV )
    out, errCode = self.swgitUtil_.system_unix( "git tag -d %s" % self.CREATED_BR_FIX )

    #
    # erase branch with contributes
    #
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "re-create same branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    # switch to int
    out, errCode = self.swgitUtil_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "switch to int" )


    # delete -D  a branch whith short name
    out, errCode = self.swgitUtil_.branch_delete_D( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "erasing -E br with contributes" )

    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR )[1], 1, "Why found %s" % self.CREATED_BR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 1, "Why found %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 1, "Not found %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.gitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 1, "Not found %s" % self.CREATED_BR_FIX )


  def test_Branch_05_00_Move_denies( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )


    WRONG_SLASH = "1/2/3/4/%s/FTR/%s/aaa" % ( TEST_USER, self.BRANCH_NAME )
    out, errCode = self.swgitUtil_.branch_move_m( WRONG_SLASH )
    self.util_check_DENY_scenario( out, errCode, "Only local branch names allowed", "wrong slash" )

    WRONG_REL = "111/2/3/44/%s/FTR/%s" % ( TEST_USER, self.BRANCH_NAME )
    out, errCode = self.swgitUtil_.branch_move_m( WRONG_REL )
    self.util_check_DENY_scenario( out, errCode, "Please specify a valid release number:", "wrong rel" )

    WRONG_USER = "11/2/3/44/AA1/FTR/%s" % ( self.BRANCH_NAME )
    out, errCode = self.swgitUtil_.branch_move_m( WRONG_USER )
    self.util_check_DENY_scenario( out, errCode, "Invalid user name,", "wrong user" )

    WRONG_BRTYPE = "11/2/3/44/AAA/FIX/%s" % ( self.BRANCH_NAME )
    out, errCode = self.swgitUtil_.branch_move_m( WRONG_BRTYPE )
    self.util_check_DENY_scenario( out, errCode, "Cannot change branch type.", "change type" )

    WRONG_BRNAME = "11/2/3/44/AAA/FTR/aa22_@"
    out, errCode = self.swgitUtil_.branch_move_m( WRONG_BRNAME )
    self.util_check_DENY_scenario( out, errCode, "Please specify a branch name respecting this regexp:", "wrong name" )

    out, errCode = self.swgitUtil_.branch_move_m( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "Already exists a branch named", "wrong position" )

    out, errCode = self.swgitUtil_.branch_switch_to_br( self.LIV )
    self.util_check_SUCC_scenario( out, errCode, "", "change branch" )

    DETACHED = "1/2/3/4/AAA/FTR/aa"
    out, errCode = self.swgitUtil_.branch_move_m( DETACHED )
    self.util_check_DENY_scenario( out, errCode, "not in detahced head", "wrong position" )


  def test_Branch_05_01_Move_m( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

    NEWREL = "1/1/1/1" 
    out, errCode = self.swgitUtil_.branch_move_M( "%s/%s/FTR/%s" % (NEWREL,TEST_USER,self.BRANCH_NAME) )
    self.util_check_DENY_scenario( out, errCode, "Not existing remote branch, try using -m option instead.", "-M on local branch" )

    out, errCode = self.swgitUtil_.branch_move_m( "%s/%s/FTR/%s" % (NEWREL,TEST_USER,self.BRANCH_NAME) )
    self.util_check_SUCC_scenario( out, errCode, "", "change rel" )

    for r in [ self.CREATED_BR, self.CREATED_BR_NEWBR, self.CREATED_BR_DEV, self.CREATED_BR_FIX ]:

      newr = r.replace( "%s/%s" % (ORIG_REPO_REL, ORIG_REPO_SUBREL), NEWREL )

      self.assertEqual( self.swgitUtil_.ref2sha( newr )[1], 0, "get sha %s" % newr )
      self.assertEqual( self.swgitUtil_.ref2sha( r    )[1], 1, "get sha %s" % r )



  def test_Branch_05_02_Move_M( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "move origin" )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    #sys.exit( 1 )

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_DEV )[1], 0, "get sha %s" % self.CREATED_BR_DEV )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_FIX )[1], 0, "get sha %s" % self.CREATED_BR_FIX )

    NEWREL = "1/1/1/1" 
    out, errCode = self.swgitUtil_.branch_move_M( "%s/%s/FTR/%s" % (NEWREL,TEST_USER,self.BRANCH_NAME) )
    self.util_check_SUCC_scenario( out, errCode, "", "change rel" )

    for oldr in [ self.CREATED_BR, self.CREATED_BR_NEWBR, self.CREATED_BR_DEV, self.CREATED_BR_FIX ]:

      newr = oldr.replace( "%s/%s" % (ORIG_REPO_REL, ORIG_REPO_SUBREL), NEWREL )

      self.assertEqual( self.swgitUtil_.ref2sha( newr )[1], 0, "get sha %s" % newr )
      self.assertEqual( self.swgitUtil_.ref2sha( oldr )[1], 1, "get sha %s" % oldr )

      self.assertEqual( remote_h.ref2sha( newr )[1], 0, "get sha %s" % newr )
      self.assertEqual( remote_h.ref2sha( oldr )[1], 1, "get sha %s" % oldr )



  def test_Branch_06_00_CHK_Create_from_liv( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    # create branch
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.LIV )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    out, errCode = self.gitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, NO_BRANCH, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( NO_BRANCH, out ) )
    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, DETACH_HEAD, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( DETACH_HEAD, out ) )

    # git <--> swgit
    self.check_repo_git_swgit_alignment()

    # 2 local branches
    out_loc_sw, errCode = self.swgitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches FAILED - out: %s " % out_loc_sw )
    self.assertEqual( len( out_loc_sw.splitlines() ), 1, "self.swgitUtil_.local_branches FAILED - more/less than 1 branch - %s" % out_loc_sw )

  def test_Branch_06_01_CHK_Create_from_dev( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    #get a DEV from repo
    self.assertEqual( self.gitUtil_.ref2sha( self.DEV )[1], 0, "Label %s from which to start does no exists" % self.DEV )

    # create branch
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.DEV )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    self.CREATED_CHK_2  = "%s/%s/%s/CHK/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_USER, self.gitUtil_.ref2sha( self.DEV )[0][0:8] )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, DETACH_HEAD , "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( DETACH_HEAD, out ) )
    out, errCode = self.gitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, NO_BRANCH , "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( NO_BRANCH, out ) )

    # git <--> swgit
    self.check_repo_git_swgit_alignment()

    # 2 local branches
    out_loc_sw, errCode = self.swgitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches FAILED - out: %s " % out_loc_sw )
    self.assertEqual( len( out_loc_sw.splitlines() ), 1, "self.swgitUtil_.local_branches FAILED - more/less than 1 branch - %s" % out_loc_sw )

  def test_Branch_07_00_Create_from_CHK( self ):
    self.test_Branch_06_00_CHK_Create_from_liv()
    self.create_branch_and_check(numBranch=2, src = self.LIV )

 
  def test_Branch_07_01_Create_CHK_and_switch( self ):
    self.test_Branch_06_00_CHK_Create_from_liv()
    self.create_branch_and_check(numBranch=2, src = self.LIV )
    # switch to FTR craeted
    out, errCode = self.swgitUtil_.branch_switch_to_br( self.CREATED_BR )
    self.assertEqual( errCode, 0, "self.swgitUtil_.branch_switch_to_br( %s ) FAILED - out:\n%s" % ( self.CREATED_BR, out ) )


  def test_Branch_07_02_Create_fail( self ):
    self.test_Branch_02_00_Create()
    # create branch
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME_2 )
    self.assertNotEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.CREATED_BR, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( self.BRANCH_NAME, out) )

    # git <--> swgit
    self.check_repo_git_swgit_alignment()

    # 2 local branches
    out_loc_sw, errCode = self.swgitUtil_.local_branches()
    self.assertEqual( errCode, 0, "self.swgitUtil_.local_branches FAILED - out: %s " % out_loc_sw )
    self.assertEqual( len( out_loc_sw.splitlines() ), 2, "self.swgitUtil_.local_branches FAILED - more/less than 2 branch - %s" % out_loc_sw )
  
  def test_Branch_08_00_track( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )
    
    out, errCode = self.swgitUtil_.branch_track( self.TRACK_BR )
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )

    out, errCode = self.swgitUtil_.branch_switch_to_br( self.TRACK_BR )
    self.assertEqual( errCode, 0, "swgitUtil_.branch_create FAILED - \n%s\n" % out )

    out, errCode = self.swgitUtil_.current_branch()
    self.assertEqual( errCode, 0, "self.swgitUtil_.current_branch FAILED - out:\n%s" % out )
    self.assertEqual( out, self.TRACK_BR, "self.swgitUtil_.current_branch - not on %s - out:\n%s" % ( self.TRACK_BR, out) )


  def test_Branch_09_00_INTBR_yesLocal_yesRemote_yesTracked( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    oldIntBr = self.swgitUtil_.int_branch_get()[0]

    self.assertNotEqual( oldIntBr, self.TRACK_BR, "to run this test, specify different TRACK_BR" )

    out, errCode = self.swgitUtil_.branch_track( self.TRACK_BR )
    self.assertEqual( errCode, 0, "branch_track FAILED - out:\n%s" % out )

    out, errCode = self.swgitUtil_.int_branch_set( self.TRACK_BR )
    self.assertEqual( errCode, 0, "int_branch_set FAILED - out:\n%s" % out )

    newIntBr = self.swgitUtil_.int_branch_get()[0]
    self.assertEqual( newIntBr, self.TRACK_BR, "int br NOT set\n%s\n%s" % ( newIntBr, self.TRACK_BR ) )
    self.assertNotEqual( oldIntBr, newIntBr, "int br NOT set\n%s\n%s" % ( oldIntBr, newIntBr ) )


  def test_Branch_09_01_INTBR_yesLocal_yesRemote_noTracked( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    oldIntBr = self.swgitUtil_.int_branch_get()[0]

    out, errCode = self.swgitUtil_.int_branch_set( self.TRACK_BR )
    self.assertEqual( errCode, 0, "int_branch_set FAILED - out:\n%s" % out )

    newIntBr = self.swgitUtil_.int_branch_get()[0]
    self.assertEqual( newIntBr, self.TRACK_BR, "int br NOT set\n%s\n%s" % ( newIntBr, self.TRACK_BR ) )
    self.assertNotEqual( oldIntBr, newIntBr, "int br NOT set\n%s\n%s" % ( oldIntBr, newIntBr ) )


  def test_Branch_09_02_INTBR_yesLocal_noRemote( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    oldIntBr = self.swgitUtil_.int_branch_get()[0]

    #create local br
    self.assertNotEqual( oldIntBr, self.BRANCH_NAME, "to run this test, specify different BRANCH_NAME" )
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "branch_create FAILED - \n%s\n" % out )

    orig_helper = git__utils( self.BRANCH_DIR )

    #move origin HEAD away from develop (otherwisepush fails)
    orig_util = git__utils( TEST_ORIG_REPO )
    out, errCode = orig_util.branch_create( self.BRANCH_NAME_2 )
    self.assertEqual( errCode, 0, "branch_create FAILED - \n%s\n" % out )

    #set new int
    out, errCode = self.swgitUtil_.int_branch_set( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "int_branch_set FAILED - out:\n%s" % out )

    newIntBr = self.swgitUtil_.int_branch_get()[0]
    self.assertEqual( newIntBr, self.CREATED_BR, "int br NOT set\n%s\n%s" % ( newIntBr, self.CREATED_BR ) )
    self.assertNotEqual( oldIntBr, newIntBr, "int br NOT set\n%s\n%s" % ( oldIntBr, newIntBr ) )


  def test_Branch_09_03_INTBR_noLocal_noRemote( self ):
    # clone
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_scripts_repo" )

    oldIntBr = self.swgitUtil_.int_branch_get()[0]

    out, errCode = self.swgitUtil_.int_branch_set( "abcd" )
    self.assertNotEqual( errCode, 0, "MUST FAIL set int br to abcd - out:\n%s" % out )

    newIntBr = self.swgitUtil_.int_branch_get()[0]

    self.assertEqual( oldIntBr, newIntBr, "MUST NOT change int br\n%s\n%s" % ( oldIntBr, newIntBr ) )


  def test_Branch_10_00_Create_Src_nocandidates( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.BRANCH_DIR ) 
  
    out, errCode = self.swgitUtil_.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 

    #delete all labels
    # with more remotes, must delete 2 branches and move away from 2 repos
    if modetest_morerepos():

      out, errCode = self.sw_aremoterepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
      self.util_check_SUCC_scenario( out, errCode, "", "moving away 2" ) 

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_E( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_DEVEL_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

    else:

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting branch and all tags" ) 


    out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 

    out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_STABLE_BRANCH )

    if modetest_morerepos():
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found", "deleting INT branch and all tags" ) 

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_STABLE_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 
    else:
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 

    #craete 
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "Without integration branch set, plese specify --source", "create br from detahced" ) 

    #craete 
    out, errCode = self.swgitUtil_.branch_create_src( self.BRANCH_NAME, src = "HEAD" )
    self.util_check_DENY_scenario( out, errCode, "Not found any reference containing", "create br from detahced" ) 


  def test_Branch_10_01_Create_Src_OnlyRemote( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.BRANCH_DIR ) 
  
    out, errCode = self.swgitUtil_.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 

    #delete all labels
    #delete all labels
    # with more remotes, must delete 2 branches and move away from 2 repos
    if modetest_morerepos():

      out, errCode = self.sw_aremoterepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
      self.util_check_SUCC_scenario( out, errCode, "", "moving away 2" ) 

      out, errCode = self.swgitUtil_.branch_delete_E( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

      #
      #this -E must not delete local copy!!! Because local copy points to origin, nly remote must be deleted
      #
      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_DEVEL_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleteing only remote branch" )

    else:

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting branch and all tags" ) 

    out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 

    #craete 
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "In 'detached head', plese specify --source", "create br from detahced" ) 

    #craete 
    out, errCode = self.swgitUtil_.branch_create_src( self.BRANCH_NAME, src = "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "create br from detahced" ) 

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )


  def test_Branch_10_02_Create_Src_FromTag( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.BRANCH_DIR ) 
  
    out, errCode = self.swgitUtil_.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 

    #delete all labels
    out, errCode = self.swgitUtil_.tag_delete( ORIG_REPO_aBRANCH_DEV0 )
    self.util_check_DENY_scenario( out, errCode, "Cannot delete a tag already pushed on origin", "deleting tag" ) 

    #sys.exit( 1 )

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_track( ORIG_REPO_aBRANCH_NAME )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "track to understand which remote" ) 
      out, errCode = self.swgitUtil_.branch_track( ORIG_REPO_AREMOTE_NAME + "/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "track to understand which remote" ) 

    out, errCode = self.swgitUtil_.tag_delete_e( ORIG_REPO_aBRANCH_DEV0 )
    self.util_check_SUCC_scenario( out, errCode, "", "deleting tag" ) 
    out, errCode = self.swgitUtil_.tag_delete_e( ORIG_REPO_aBRANCH_DEV1 )
    self.util_check_SUCC_scenario( out, errCode, "", "deleting tag" ) 
    out, errCode = self.swgitUtil_.tag_delete_e( ORIG_REPO_aBRANCH_FIX )
    self.util_check_SUCC_scenario( out, errCode, "", "deleting tag" ) 
    out, errCode = self.swgitUtil_.tag_delete_e( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_DENY_scenario( out, errCode, "'NEW' tags can be deleted only by deleting associated branch", "deleting tag" ) 

    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_AREMOTE_NAME + "/" +  ORIG_REPO_DEVEL_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 
    else:
      out, errCode = self.swgitUtil_.branch_delete_D( ORIG_REPO_DEVEL_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 

    #craete 
    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
      self.util_check_DENY_scenario( out, errCode, "Without integration branch set, plese specify --source while creating branch.", "create br from detahced" ) 
    else:
      out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
      self.util_check_DENY_scenario( out, errCode, "In 'detached head', plese specify --source", "create br from detahced" ) 

    #craete 
    out, errCode = self.swgitUtil_.branch_create_src( self.BRANCH_NAME, src = "HEAD" )
    self.util_check_SUCC_scenario( out, errCode, "", "create br from detahced" ) 

    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR )[1], 0, "get sha %s" % self.CREATED_BR )
    self.assertEqual( self.swgitUtil_.ref2sha( self.CREATED_BR_NEWBR )[1], 0, "get sha %s" % self.CREATED_BR_NEWBR )

    
  def test_Branch_10_03_Create_Src_NoValid( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.BRANCH_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED cloning repo into %s" % self.BRANCH_DIR ) 
  
    #mark develop with a tag to avoid loosing that tip
    PLACEHOLDER = "ciccio"
    out, errCode = self.swgitUtil_.system_unix( "git tag %s %s" %  (PLACEHOLDER, ORIG_REPO_DEVEL_BRANCH) )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 

    out, errCode = self.swgitUtil_.branch_switch_to_br( PLACEHOLDER )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( ORIG_REPO_aBRANCH_NEWBR )
    self.util_check_SUCC_scenario( out, errCode, "", "moving away" ) 

    #delete all labels
    if modetest_morerepos():
      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH_NAME )
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found, please specify one among:", "deleting branch and all tags" ) 

      out, errCode = self.swgitUtil_.branch_delete_E( "origin/" + ORIG_REPO_aBRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting branch and all tags" ) 

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_AREMOTE_NAME + "/" +  ORIG_REPO_DEVEL_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 

    else:

      out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_aBRANCH_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting branch and all tags" ) 

    out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_DEVEL_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 

    out, errCode = self.swgitUtil_.branch_delete_E( ORIG_REPO_STABLE_BRANCH )
    if modetest_morerepos():
      self.util_check_DENY_scenario( out, errCode, "Multiple matches found", "deleting INT branch and all tags" ) 

      out, errCode = self.swgitUtil_.branch_delete_E( "origin/" + ORIG_REPO_STABLE_BRANCH )
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 
    else:
      self.util_check_SUCC_scenario( out, errCode, "", "deleting INT branch and all tags" ) 


    #craete 
    out, errCode = self.swgitUtil_.branch_create( self.BRANCH_NAME )
    self.util_check_DENY_scenario( out, errCode, "Without integration branch set, plese specify --source", "create br from detahced" ) 

    #craete 
    out, errCode = self.swgitUtil_.branch_create_src( self.BRANCH_NAME, src = "HEAD" )
    self.util_check_DENY_scenario( out, errCode, "but not a valid swgit reference", "create br from detahced" ) 

    
if __name__ == '__main__':

  manage_debug_opt( sys.argv )
  unittest.main()
