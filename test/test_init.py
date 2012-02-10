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

class Test_Init( Test_Base ):
  INIT_REPO_DIR     = SANDBOX + "TEST_INIT__REPO/"
  INIT_CLONE_DIR    = SANDBOX + "TEST_INIT__CLONE/"
  
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    shutil.rmtree( self.INIT_REPO_DIR, True ) #ignore errors
    self.swgitUtil_Repo_ = swgit__utils( self.INIT_REPO_DIR )
    self.gitUtil_Repo_   = git__utils( self.INIT_REPO_DIR )

    shutil.rmtree( self.INIT_CLONE_DIR, True ) #ignore errors
    self.swgitUtil_Clone_ = swgit__utils( self.INIT_CLONE_DIR )
    self.gitUtil_Clone_   = git__utils( self.INIT_CLONE_DIR )


  def tearDown( self ):
    pass

  def test_Init_00_00_WrongValues( self ):
    create_dir_some_file( self.INIT_REPO_DIR )

    # init
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, r = "a" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid release", 
                                   "init wrong rel" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, s = "a.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid release", 
                                   "init wrong subrel" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, l = "a.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "please enter -l argument respecting",
                                   "init wrong liv" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, u = "a.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid user name",
                                   "init wrong users" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "aaa_-" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a branch name respecting this regexp:",
                                   "init wrong br name" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "aaa", cst = True )
    self.util_check_DENY_scenario( out, errCode, 
                                   "src option is mandatory.",
                                   "init and create cst no src" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "aaa", cst = True, src = "bbb" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "init and create cst wrong src" ) 


    #now inside native git repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = self.swgitUtil_Repo_.system_unix( "git init" )
    self.util_check_SUCC_scenario( out, errCode, "", "initializing native git repo" ) 



    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, r = "a" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid release", 
                                   "init wrong rel" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, s = "a.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid release", 
                                   "init wrong subrel" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, l = "a.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "please enter -l argument respecting",
                                   "init wrong liv" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, u = "a.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid user name",
                                   "init wrong users" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "aaa_-" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a branch name respecting this regexp:",
                                   "init wrong br name" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "aaa", cst = True )
    self.util_check_DENY_scenario( out, errCode, 
                                   "src option is mandatory.",
                                   "init and create cst no src" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "aaa", cst = True, src = "bbb" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "init and create cst wrong src" ) 




  def test_Init_01_00_WithLiv( self ):
    create_dir_some_file( self.INIT_REPO_DIR )

    # init
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    # 1 commit an nothing else
    root_sha, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % root_sha )
    nonExist_sha, errCode = self.gitUtil_Repo_.get_currsha( "HEAD~1" )
    self.assertNotEqual( errCode, 0, "gitUtil_Repo_.get_currsha MUST FAILED - \n%s\n" % nonExist_sha )

    # all tags on same commit
    stbdev_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_DEV )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.ref2sha FAILED - \n%s\n" % stbdev_sha )
    self.assertEqual( root_sha, stbdev_sha, "FAILED - \n%s\n%s\n" % ( root_sha, stbdev_sha ) )

    stbstb_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_STB )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.ref2sha FAILED - \n%s\n" % stbstb_sha )
    self.assertEqual( root_sha, stbstb_sha, "FAILED - \n%s\n%s\n" % ( root_sha, stbstb_sha ) )
    self.assertEqual( stbdev_sha, stbstb_sha, "FAILED - \n%s\n%s\n" % ( stbdev_sha, stbstb_sha ) )

    liv_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_LIV )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.ref2sha FAILED - \n%s\n" % liv_sha )
    self.assertEqual( root_sha, liv_sha, "FAILED - \n%s\n%s\n" % ( root_sha, liv_sha ) )
    self.assertEqual( stbdev_sha, liv_sha, "FAILED - \n%s\n%s\n" % ( stbdev_sha, liv_sha ) )
    self.assertEqual( stbstb_sha, liv_sha, "FAILED - \n%s\n%s\n" % ( stbstb_sha, liv_sha ) )

    #NEWBR
    devnewbr_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_DEV_NEWBR )
    self.assertEqual( errCode, 0, "Label %s does no exists" % TEST_REPO_TAG_DEV_NEWBR )
    stbnewbr_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_NEWBR )
    self.assertEqual( errCode, 0, "Label %s does no exists" % TEST_REPO_TAG_STB_NEWBR )
    self.assertEqual( devnewbr_sha, stbnewbr_sha, "FAILED - \n%s\n%s\n" % ( devnewbr_sha, stbnewbr_sha ) )


    # on detahced head
    out, errCode = self.gitUtil_Repo_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.current_branch out: %s " % out )
    self.assertEqual( out, NO_BRANCH, "FAILED not on no-brach - \n%s\n" % (out) )

    out, errCode = self.swgitUtil_Repo_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.current_branch out: %s " % out )
    self.assertEqual( out, DETACH_HEAD, "FAILED not on DETACHED HEAD - \n%s\n" % (out) )

    #master
    master_sha, errCode = self.gitUtil_Repo_.ref2sha( "master" )
    self.assertEqual( errCode, 1, "branch master MUST not exists" )



  def test_Init_01_01_WithLiv_IssueTwice( self ):
    create_dir_some_file( self.INIT_REPO_DIR )

    # init
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "init once" ) 

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.util_check_DENY_scenario( out, errCode, "ERROR", "init twice" ) 



  def test_Init_01_01_WithoutLiv( self ):
    create_dir_some_file( self.INIT_REPO_DIR )

    # init
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR , l = "" ) #without LIV
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    # 1 commit an nothing esle
    root_sha, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % root_sha )
    nonExist_sha, errCode = self.gitUtil_Repo_.get_currsha( "HEAD~1" )
    self.assertNotEqual( errCode, 0, "gitUtil_Repo_.get_currsha MUST FAILED - \n%s\n" % nonExist_sha )

    # all tags on same commit
    stbdev_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_DEV )
    self.assertNotEqual( errCode, 0, "Tag %s SHULD NOT EXIST - \n%s\n" % (TEST_REPO_TAG_STB_DEV,stbdev_sha) )

    stbdev_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_STB )
    self.assertNotEqual( errCode, 0, "Tag %s SHULD NOT EXIST - \n%s\n" % (TEST_REPO_TAG_STB_STB,stbdev_sha) )

    stbdev_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_LIV )
    self.assertNotEqual( errCode, 0, "Tag %s SHULD NOT EXIST - \n%s\n" % (TEST_REPO_TAG_LIV,stbdev_sha) )

    #Not on branch CHK
    out, errCode = self.gitUtil_Repo_.current_branch()
    self.assertNotEqual( out, TEST_REPO_CHK_LIV, "FAILED not on CHK LABEL %s - \n%s\n" % (TEST_REPO_CHK_LIV,out) )



  def test_Init_02_00_NativeGit_int( self ):
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = self.swgitUtil_Repo_.system_unix( "git init && git commit -a -m 'first' --allow-empty" )
    self.util_check_SUCC_scenario( out, errCode, "", "initializing native git repo" ) 


    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "from native git repo to swgit repo" ) 


    # 1 commit an nothing else
    root_sha, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % root_sha )
    root1_sha, errCode = self.gitUtil_Repo_.get_currsha( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED - \n%s\n" % root1_sha )
    nonExist_sha, errCode = self.gitUtil_Repo_.get_currsha( "HEAD~2" )
    self.assertEqual( errCode, 1, "FAILED - \n%s\n" % nonExist_sha )

    # all tags on same commit
    stbdev_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_DEV )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.ref2sha FAILED - \n%s\n" % stbdev_sha )
    self.assertEqual( root_sha, stbdev_sha, "FAILED - \n%s\n%s\n" % ( root_sha, stbdev_sha ) )

    stbstb_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_STB )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.ref2sha FAILED - \n%s\n" % stbstb_sha )
    self.assertEqual( root_sha, stbstb_sha, "FAILED - \n%s\n%s\n" % ( root_sha, stbstb_sha ) )
    self.assertEqual( stbdev_sha, stbstb_sha, "FAILED - \n%s\n%s\n" % ( stbdev_sha, stbstb_sha ) )

    liv_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_LIV )
    self.assertEqual( errCode, 0, "swgitUtil_Repo_.ref2sha FAILED - \n%s\n" % liv_sha )
    self.assertEqual( root_sha, liv_sha, "FAILED - \n%s\n%s\n" % ( root_sha, liv_sha ) )
    self.assertEqual( stbdev_sha, liv_sha, "FAILED - \n%s\n%s\n" % ( stbdev_sha, liv_sha ) )
    self.assertEqual( stbstb_sha, liv_sha, "FAILED - \n%s\n%s\n" % ( stbstb_sha, liv_sha ) )

    #NEWBR
    devnewbr_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_DEV_NEWBR )
    self.assertEqual( errCode, 0, "Label %s does no exists" % TEST_REPO_TAG_DEV_NEWBR )
    stbnewbr_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_NEWBR )
    self.assertEqual( errCode, 0, "Label %s does no exists" % TEST_REPO_TAG_STB_NEWBR )
    self.assertEqual( devnewbr_sha, stbnewbr_sha, "FAILED - \n%s\n%s\n" % ( devnewbr_sha, stbnewbr_sha ) )


    # on detahced head
    out, errCode = self.gitUtil_Repo_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.current_branch out: %s " % out )
    self.assertEqual( out, NO_BRANCH, "FAILED not on no-brach - \n%s\n" % (out) )

    out, errCode = self.swgitUtil_Repo_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.current_branch out: %s " % out )
    self.assertEqual( out, DETACH_HEAD, "FAILED not on DETACHED HEAD - \n%s\n" % (out) )

    #master
    master_sha, errCode = self.gitUtil_Repo_.ref2sha( "master" )
    self.assertEqual( errCode, 0, "master MUST exists because it was created before swgit init " )


  def test_Init_02_01_NativeGit_cst( self ):
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = self.swgitUtil_Repo_.system_unix( "git init && git commit -a -m 'first' --allow-empty" )
    self.util_check_SUCC_scenario( out, errCode, "", "initializing native git repo" ) 

    # with LIV

    MYCST_REL  = "1/1"
    MYCST_NAME = "mycst"
    MYCST  = "%s/%s/%s/CST/%s" % ( MYCST_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST_NAME )
    MYCST_LIV  = "%s/LIV/%s" % ( MYCST, TEST_REPO_LIV )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, cst = True, src = "master", r = MYCST_REL, c = MYCST_NAME, u = TEST_USER  )
    self.util_check_SUCC_scenario( out, errCode, "", "from native git repo to swgit repo" ) 

    cstsha, errCode = self.swgitUtil_Repo_.ref2sha( MYCST )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "retrieving local %s" % MYCST )
    cstsha_liv, errCode = self.swgitUtil_Repo_.ref2sha( MYCST_LIV )
    self.util_check_SUCC_scenario( cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )

    # another no LIV

    MYCST_REL  = "2/0"
    MYCST_NAME = "mycst"
    MYCST  = "%s/%s/%s/CST/%s" % ( MYCST_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST_NAME )
    MYCST_LIV  = "%s/LIV/%s" % ( MYCST, TEST_REPO_LIV )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, 
                                          cst = True, 
                                          src = "master", 
                                          l = "",
                                          r = MYCST_REL, 
                                          c = MYCST_NAME, 
                                          u = TEST_USER  )
    self.util_check_SUCC_scenario( out, errCode, "", "from native git repo to swgit repo" ) 

    cstsha, errCode = self.swgitUtil_Repo_.ref2sha( MYCST )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "retrieving local %s" % MYCST )
    cstsha_liv, errCode = self.swgitUtil_Repo_.ref2sha( MYCST_LIV )
    self.util_check_DENY_scenario( cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )



  def test_Init_03_00_Modify_Commit( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    # switch to int
    out, errCode = self.gitUtil_Repo_.checkout( TEST_REPO_BR_DEV )
    self.assertEqual( errCode, 0, "self.gitUtil_Repo_.checkout FAILED - out:\n%s" % out )

    # getsha before commit
    sha_before, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_before )

    stbdev_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_DEV )
    stbstb_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_DEV )
    liv_sha, errCode = self.gitUtil_Repo_.ref2sha( TEST_REPO_TAG_STB_DEV )

    # modify a file
    out, errCode = echo_on_file( self.INIT_REPO_DIR + TEST_REPO_FILE_A, "ciccio" )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    # commit
    out, errCode = self.gitUtil_Repo_.commit_minusA()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.commit_minusA FAILED - \n%s\n" % out )

    # getsha after commit
    sha_after, errCode = self.gitUtil_Repo_.get_currsha()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.get_currsha FAILED - \n%s\n" % sha_after )

    self.assertNotEqual( sha_before, sha_after, "swgitUtil_Repo_.commit_minusA FAILED - after commit SAME sha as before\n%s\n%s\n" % (sha_before,sha_after) )
    self.assertNotEqual( sha_after, stbdev_sha, "FAILED - \n%s\n%s\n" % ( sha_after, stbdev_sha ) )
    self.assertNotEqual( sha_after, stbstb_sha, "FAILED - \n%s\n%s\n" % ( sha_after, stbstb_sha ) )
    self.assertNotEqual( sha_after, liv_sha, "FAILED - \n%s\n%s\n" % ( sha_after, liv_sha ) )


  def test_Init_04_00_Clone( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    #clone
    out, errCode = swgit__utils.clone_repo( self.INIT_REPO_DIR, self.INIT_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo - \n%s\n" % out )

    # on branch develop
    out, errCode = self.gitUtil_Clone_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.current_branch out: %s " % out )
    self.assertEqual( out, TEST_REPO_BR_DEV, "SWGIT branch not cloned - gitUtil_Clone_.current_branch out: %s " % out )

    # no other local branches
    out, errCode = self.gitUtil_Clone_.local_branches()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.local_branches out: %s " % out )
    self.assertEqual( len( out.splitlines() ), 1, "SWGIT more/less than 1 local branch created - gitUtil_Clone_.local_branches out: %s  " % out )



  def test_Init_04_01_and_Clone_integrator( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    #clone
    out, errCode = swgit__utils.clone_repo_integrator( self.INIT_REPO_DIR, self.INIT_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo - \n%s\n" % out )

    # on branch develop
    out, errCode = self.gitUtil_Clone_.current_branch()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.current_branch out: %s " % out )
    self.assertEqual( out, TEST_REPO_BR_DEV, "SWGIT branch not cloned - gitUtil_Clone_.current_branch out: %s " % out )

    # develop, stable
    out, errCode = self.gitUtil_Clone_.local_branches()
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - gitUtil_Clone_.local_branches out: %s " % out )
    self.assertEqual( len( out.splitlines() ), 2, "SWGIT more/less than 2 local branch created - gitUtil_Clone_.local_branches out: %s  " % out )


  def test_Init_05_00_CST_branch_onOrigin( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "testsss", cst = True, src = "bbb" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, cst = True, src = TEST_REPO_LIV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "-c/--create option is mandatory",
                                   "not a valid reference" )

    CSTNAME =  "mycustomer"

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV, c = CSTNAME, r = "1.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "create CST %s" % CSTNAME )

    #reissue
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV, c = CSTNAME, r = "1.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already exists",
                                   "recreate same CST" )

    #change release
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV, c = CSTNAME, r = "2.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "recreate another CST" )

    ref = "2/0/0/0/%s/INT/develop" % ( ORIG_REPO_GITUSER )
    develop, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( develop, errCode, "", "get %s " % ref )

    ref = "1/0/0/0/%s/CST/%s" % ( ORIG_REPO_GITUSER, CSTNAME )
    cst1, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( cst1, errCode, "", "get %s " % ref )

    ref = "2/0/0/0/%s/CST/%s" % ( ORIG_REPO_GITUSER, CSTNAME )
    cst2, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( cst2, errCode, "", "get %s " % ref )

    self.assertNotEqual( cst1, cst2, "MUST not be the same" )
    self.assertNotEqual( cst1, develop, "MUST not be the same" )
    self.assertNotEqual( cst2, develop, "MUST not be the same" )



  def test_Init_05_01_CST_branch_onClone( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    #clone
    out, errCode = swgit__utils.clone_repo( self.INIT_REPO_DIR, self.INIT_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo - \n%s\n" % out )


    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, c = "testsss", cst = True, src = "bbb" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, cst = True, src = TEST_REPO_LIV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "-c/--create option is mandatory",
                                   "not a valid reference" )

    CSTNAME =  "mycustomer"

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV, c = CSTNAME, r = "1.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "create CST" )

    #reissue
    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV, c = CSTNAME, r = "1.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already exists",
                                   "recreate same CST" )

    #change release
    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, cst = True, src = TEST_REPO_TAG_STB_DEV, c = CSTNAME, r = "2.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "recreate another CST" )

    ref = "2/0/0/0/%s/INT/develop" % ( ORIG_REPO_GITUSER )
    develop, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( develop, errCode, "", "get %s " % ref )

    ref = "1/0/0/0/%s/CST/%s" % ( ORIG_REPO_GITUSER, CSTNAME )
    cst1, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( cst1, errCode, "", "get %s " % ref )

    ref = "2/0/0/0/%s/CST/%s" % ( ORIG_REPO_GITUSER, CSTNAME )
    cst2, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( cst2, errCode, "", "get %s " % ref )

    self.assertNotEqual( cst1, cst2, "MUST not be the same" )
    self.assertNotEqual( cst1, develop, "MUST not be the same" )
    self.assertNotEqual( cst2, develop, "MUST not be the same" )


  def test_Init_06_00_NEWREL_onOrigin( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, c = "testsss", src = "bbb" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, src = TEST_REPO_LIV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, src = TEST_REPO_TAG_STB_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already exists",
                                   "re-create same INT br" )

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, src = TEST_REPO_TAG_STB_DEV, s = "2.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "create new INT br" )

    INTNAME =  "mynewint"

    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, src = TEST_REPO_TAG_STB_DEV, c = INTNAME, r = "1.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "create INT %s" % INTNAME )

    #reissue
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, src = TEST_REPO_TAG_STB_DEV, c = INTNAME, r = "1.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already exists",
                                   "recreate same INT" )

    #change release
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR, src = TEST_REPO_TAG_STB_DEV, c = INTNAME, r = "2.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "recreate another INT" )

    ref = "2/0/0/0/%s/INT/develop" % ( ORIG_REPO_GITUSER )
    develop, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( develop, errCode, "", "get %s " % ref )
    ref = "2/0/0/0/%s/INT/stable" % ( ORIG_REPO_GITUSER )
    stable, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( stable, errCode, "", "get %s " % ref )

    ref = "1/0/0/0/%s/INT/%s_develop" % ( ORIG_REPO_GITUSER, INTNAME )
    dev1, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( dev1, errCode, "", "get %s " % ref )
    ref = "1/0/0/0/%s/INT/%s_stable" % ( ORIG_REPO_GITUSER, INTNAME )
    stb1, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( stb1, errCode, "", "get %s " % ref )

    ref = "2/0/0/0/%s/INT/%s_develop" % ( ORIG_REPO_GITUSER, INTNAME )
    dev2, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( dev2, errCode, "", "get %s " % ref )
    ref = "2/0/0/0/%s/INT/%s_stable" % ( ORIG_REPO_GITUSER, INTNAME )
    stb2, errCode = self.swgitUtil_Repo_.ref2sha( ref )
    self.util_check_SUCC_scenario( stb2, errCode, "", "get %s " % ref )

    self.assertNotEqual( dev1, dev2, "MUST not be the same" )
    self.assertNotEqual( dev1, develop, "MUST not be the same" )
    self.assertNotEqual( dev2, develop, "MUST not be the same" )

    self.assertEqual( dev1, stb1, "MUST be the same" )
    self.assertEqual( dev2, stb2, "MUST be the same" )
    self.assertEqual( develop, stable, "MUST be the same" )


  def test_Init_06_01_NEWREL_onClone( self ):
    #first create repo
    create_dir_some_file( self.INIT_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.INIT_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    #clone
    out, errCode = swgit__utils.clone_repo( self.INIT_REPO_DIR, self.INIT_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo - \n%s\n" % out )


    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, c = "testsss", src = "bbb" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, src = TEST_REPO_LIV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid source reference",
                                   "not a valid reference" )

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, src = TEST_REPO_TAG_STB_DEV )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already exists",
                                   "re-create same INT br" )

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, src = TEST_REPO_TAG_STB_DEV, s = "2.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "create new INT br" )

    INTNAME =  "mynewint"

    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, src = TEST_REPO_TAG_STB_DEV, c = INTNAME, r = "1.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "create INT %s" % INTNAME )

    #reissue
    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, src = TEST_REPO_TAG_STB_DEV, c = INTNAME, r = "1.0" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "already exists",
                                   "recreate same INT" )

    #change release
    out, errCode = swgit__utils.init_dir( self.INIT_CLONE_DIR, src = TEST_REPO_TAG_STB_DEV, c = INTNAME, r = "2.0" )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "",
                                   "recreate another INT" )

    ref = "2/0/0/0/%s/INT/develop" % ( ORIG_REPO_GITUSER )
    develop, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( develop, errCode, "", "get %s " % ref )
    #stable does not exists because not track all
    ref = "2/0/0/0/%s/INT/stable" % ( ORIG_REPO_GITUSER )
    stable, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_DENY_scenario( stable, errCode, "", "get %s " % ref )

    ref = "1/0/0/0/%s/INT/%s_develop" % ( ORIG_REPO_GITUSER, INTNAME )
    dev1, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( dev1, errCode, "", "get %s " % ref )
    ref = "1/0/0/0/%s/INT/%s_stable" % ( ORIG_REPO_GITUSER, INTNAME )
    stb1, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( stb1, errCode, "", "get %s " % ref )

    ref = "2/0/0/0/%s/INT/%s_develop" % ( ORIG_REPO_GITUSER, INTNAME )
    dev2, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( dev2, errCode, "", "get %s " % ref )
    ref = "2/0/0/0/%s/INT/%s_stable" % ( ORIG_REPO_GITUSER, INTNAME )
    stb2, errCode = self.swgitUtil_Clone_.ref2sha( ref )
    self.util_check_SUCC_scenario( stb2, errCode, "", "get %s " % ref )

    self.assertNotEqual( dev1, dev2, "MUST not be the same" )
    self.assertNotEqual( dev1, develop, "MUST not be the same" )
    self.assertNotEqual( dev2, develop, "MUST not be the same" )

    self.assertEqual( dev1, stb1, "MUST be the same" )
    self.assertEqual( dev2, stb2, "MUST be the same" )
    #self.assertEqual( develop, stable, "MUST be the same" )




if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()

