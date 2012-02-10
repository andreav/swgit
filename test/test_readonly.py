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
import grp
import pwd

class Test_ReadOnly( Test_ProjBase ):
  #
  # USER MGT
  #
  stat_info = os.stat(TESTDIR)
  READWRITE_uid = stat_info.st_uid
  READWRITE_gid = stat_info.st_gid
  TEST_READWRITE_USER = pwd.getpwuid( READWRITE_uid )[0]
  TEST_READONLY_USER  = pwd.getpwuid( os.getuid() )[0]

  READONLY_uid = os.getuid()
  READONLY_gid = os.getgid()

  #print READWRITE_uid, READWRITE_gid
  #print READONLY_uid, READONLY_gid

  #
  # TEST constants
  #
  READONLY_REPO_DIR    = SANDBOX_777 + "TEST_READONLY_REPO"
  READONLY_CLONE_DIR   = SANDBOX_777 + "TEST_READONLY_CLONE"
  READONLY_CLONE_2_DIR = SANDBOX_777 + "TEST_READONLY_CLONE_2"
  READONLY_CLOCLO_DIR = SANDBOX_777 + "TEST_READONLY_CLOCLO"
  READWRITE_CLONE_DIR = SANDBOX + "TEST_READWRITE_CLONE"
  BRANCH_NAME        = "test_readonly"
  CREATED_BR    = "%s/%s/%s/FTR/%s" % ( ORIG_REPO_REL, ORIG_REPO_SUBREL, TEST_READWRITE_USER, BRANCH_NAME )

  BUILTIN_DEV_0  = "%s/DEV/000" % ( ORIG_REPO_aBRANCH )
  BUILTIN_DEV_1  = "%s/DEV/001" % ( ORIG_REPO_aBRANCH )
  BUILTIN_FIX_0  = "%s/FIX/000" % ( ORIG_REPO_aBRANCH )

  DDTS          = "Issue12345"
  CREATED_FIX   = "%s/FIX/%s"  % ( CREATED_BR, DDTS )
  CREATED_DEV_0 = "%s/DEV/000" % ( CREATED_BR )
  CREATED_DEV_1 = "%s/DEV/001" % ( CREATED_BR )

  REPO_RO__ORI_URL     = "ssh://%s@%s%s" % ( TEST_READONLY_USER, TEST_ADDR, READONLY_REPO_DIR )
  REPO_RO__DEVBRANCH     = "%s/%s/%s/INT/develop" % (ORIG_REPO_REL, ORIG_REPO_SUBREL, ORIG_REPO_GITUSER )
  ROPROJ__BI = [ "ROUSER_REPO",
                 REPO_RO__ORI_URL,
                 REPO_RO__DEVBRANCH,
                 False
                 ]

  ROPROJ__INFO     = ( READONLY_REPO_DIR,
                       ORIG_REPO_REL,
                       ORIG_REPO_SUBREL,
                       "RO"    ,
                       "ro.txt",
                       ORIG_REPO_GITUSER, 
                       None,
                       None,
                       None,
                       None
                       )
  sw_ori_FS_h   = swgit__utils( REPO_FS__ORI_DIR )
  sw_ori_APP_h  = swgit__utils( REPO_APP__ORI_DIR )


  def exe_READWRITE_user( self, cmd ):
    #print cmd
    ret = os.system( "%s/run_as_user.bin %s '%s'" % (TESTDIR, self.READWRITE_uid, cmd) )
    self.assertEqual( ret, 0, "FAILED executing '%s' as the READWRITE user %s (id:%s)" % (cmd,self.TEST_READWRITE_USER,self.READWRITE_uid) )


  def setUp( self ):
    #recreate protorepo (push can have broken it)
    self.exe_READWRITE_user( "%s/util_prepare_sandbox.py -p" % TESTDIR )
    self.exe_READWRITE_user( "%s/util_prepare_sandbox.py -r" % TESTDIR )

    #check user executing this tests is:
    # 1. not the user having cloned this repo
    # 2. in the same group as the user having cloned this repo
    self.assertTrue( os.path.exists( TEST_ORIG_REPO ), \
                     "To run this test must have created %s as user %s" % (TEST_ORIG_REPO, self.TEST_READWRITE_USER) )

    self.assertTrue( os.access( TEST_ORIG_REPO, os.R_OK ), 
                     "USER RUNNING THIS TEST MUST HAVE READ PERMISSIONS on dir %s" % TEST_ORIG_REPO )

    self.assertNotEqual( self.READWRITE_uid, self.READONLY_uid,
                         "USER RUNNING THIS TEST MUST HAVE DIFFERENT UID as %s" % self.TEST_READWRITE_USER )
    self.assertEqual( self.READWRITE_gid, self.READONLY_gid,
                     "USER RUNNING THIS TEST MUST HAVE SAME GID as %s" % self.TEST_READWRITE_USER )

    self.assertFalse( os.access( TEST_ORIG_REPO, os.W_OK ), 
                      "USER RUNNING THIS TEST MUST NOT HAVE WRITE PERMISSIONS on dir %s" % TEST_ORIG_REPO )

    #logs
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )


    shutil.rmtree( self.READONLY_REPO_DIR, True )
    shutil.rmtree( self.READONLY_CLONE_DIR, True )
    shutil.rmtree( self.READONLY_CLONE_2_DIR, True )
    shutil.rmtree( self.READONLY_CLOCLO_DIR, True )

    self.sw_ori_h = swgit__utils( self.READONLY_REPO_DIR )
    self.sw_clo_h = swgit__utils( self.READONLY_CLONE_DIR )

    self.sw_testrepo_ori_h    = swgit__utils( TEST_ORIG_REPO )
    self.sw_testrepo_shared_h = swgit__utils( TEST_ORIG_REPO_SHARED )



  def tearDown( self ):
    pass
    #os.system( "chmod 777 %s -R" % SANDBOX_777 )


  def test_ReadOnly_01_00_ClonePush( self ):

    out, errCode = swgit__utils.clone_repo( TEST_ORIG_REPO, 
                                            self.READONLY_CLONE_DIR, 
                                            br = "", 
                                            user = self.TEST_READONLY_USER, 
                                            addr = TEST_ADDR )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "cloning repo %s into %s as %s user" % \
                                   ( TEST_ORIG_REPO, self.READONLY_CLONE_DIR, self.TEST_READONLY_USER) )

    #ORIG only files of RW user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( TEST_ORIG_REPO, self.TEST_READWRITE_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READWRITE_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READWRITE_USER,out) )

    #CLONE only files of RO user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( self.READONLY_CLONE_DIR, self.TEST_READONLY_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READONLY_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READONLY_USER,out) )

    #CLONE modify
    out, errCode = self.sw_clo_h.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME ) 
    out, errCode = self.sw_clo_h.modify_file( TEST_REPO_FILE_A, msg = "some content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" ) 
    out, errCode = self.sw_clo_h.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" ) 

    #push RO
    out, errCode = self.sw_clo_h.push_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "insufficient permission for adding an object to repository database", 
                                   "push" ) 


    #not corrupted origin

    #ORIG only files of RW user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( TEST_ORIG_REPO, self.TEST_READWRITE_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READWRITE_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READWRITE_USER,out) )

    #CLONE only files of RO user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( self.READONLY_CLONE_DIR, self.TEST_READONLY_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READONLY_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READONLY_USER,out) )


  #
  # I'm a read only user having my project
  # I add some other user repo (like any library)
  #
  #-------------------------------------------------------------------
  #     user A         |      read only user     |     clone of ro
  #-------------------------------------------------------------------
  # 
  #                              ORIG RO     <-------- CLOofCLO
  #                                 +                      +
  #    OTHER REPO   <---------- ANOTHER REPO  <-------- clo of this
  # 
  # 
  #-------------------------------------------------------------------
  def test_ReadOnly_02_00_MyProj_add_OtherUserRepo( self ):

    out, errCode = swgit__utils.create_repo_withbkp( self.ROPROJ__INFO )
    self.util_check_SUCC_scenario( out, errCode, "", "creating a RO user proj" )

    out, errCode = swgit__utils.clone_repo( self.READONLY_REPO_DIR, self.READONLY_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "cloning proj %s into %s" % \
                                   (self.READONLY_REPO_DIR, self.READONLY_CLONE_DIR) )


    out, errCode = self.sw_clo_h.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME ) 

    #both are READWRITE USER repos
    self.util_addrepo_2proj( self.sw_clo_h, PROJ_PLAT_DESCRIPTION[1] )


    #push RO
    out, errCode = self.sw_clo_h.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "push" ) 

    #check DEV fs
    repo_bi = PROJ_PLAT_DESCRIPTION[1][0]
    fs_clone_helper = swgit__utils( self.READONLY_CLONE_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.sw_clo_h, fs_clone_helper,
                                                      self.sw_ori_h, self.sw_ori_FS_h,
                                                      repo_bi )

    #check DEV app
    repo_bi = PROJ_PLAT_DESCRIPTION[1][1]
    app_clone_helper = swgit__utils( self.READONLY_CLONE_DIR + "/" + repo_bi[0] )
    app_orig_helper = swgit__utils( REPO_PLAT__ORI_DIR + "/" + PROJ_PLAT_DESCRIPTION[1][1][0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.sw_clo_h, app_clone_helper,
                                                      self.sw_ori_h, self.sw_ori_APP_h,
                                                      repo_bi )



    #ORIG only files of RW user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( TEST_ORIG_REPO, self.TEST_READWRITE_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READWRITE_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READWRITE_USER,out) )

    #CLONE only files of RO user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( self.READONLY_CLONE_DIR, self.TEST_READONLY_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READONLY_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READONLY_USER,out) )


    ###################################################
    #clone another time, now cloning project with repos
    #
    out, errCode = swgit__utils.clone_repo( self.READONLY_REPO_DIR, self.READONLY_CLONE_2_DIR )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "cloning proj %s into %s" % \
                                   (self.READONLY_REPO_DIR, self.READONLY_CLONE_2_DIR) )


    ###################################################
    #clone another time, now cloning the clone project
    #
    out, errCode = swgit__utils.clone_repo( self.READONLY_CLONE_2_DIR, self.READONLY_CLOCLO_DIR )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "cloning proj %s into %s" % \
                                   (self.READONLY_CLONE_2_DIR, self.READONLY_CLOCLO_DIR) )




  #
  # I'm a read only user cloning a repo
  # I add some repo in order to create MY OWN PROJECT based on remote one
  # I cannot push (i'm RO user)
  # But someone can clone my repo.
  # I will continue keeping my proj repo up-to-date by pulling from RW repo.
  #
  # strange (usually i will create my proj and ADD another user repo)
  # that case is covered in test 02_00
  #
  # This case could be used for 'branching off' a project, 
  #      and develop on it like it becomes my MAIN repo
  #
  #
  #-------------------------------------------------------------------
  #     user A         |      read only user     |     clone of ro
  #-------------------------------------------------------------------
  # 
  #    OTHER REPO   <----------- CLONE RO     <-------- CLOofCLO
  #                                 +                      +
  #                             ANOTHER REPO  <-------- clo of this
  #                                 |
  #                                 |
  #                                 v
  #                             local repo
  # 
  #-------------------------------------------------------------------
  #
  # clone TEST_ORIG_REPO                 <--- repo owned by READWRITE
  # create ROPROJ__INFO                  <--- repo owned by READONLY
  # add ROPROJ__INFO to TEST_ORIG_REPO   <--- add RO to RW
  #
  #  push will fail
  #  clone of clone will have all projects added
  #
  def test_ReadOnly_03_00_OtherUserRepo_add_myProj( self ):
    #create repo of RO
    out, errCode = swgit__utils.create_repo_withbkp( self.ROPROJ__INFO )
    self.util_check_SUCC_scenario( out, errCode, "", "creating a RO user proj" )


    #clone repo of RW
    out, errCode = swgit__utils.clone_repo( TEST_ORIG_REPO, 
                                            self.READONLY_CLONE_DIR, 
                                            br = "", 
                                            user = self.TEST_READONLY_USER, 
                                            addr = TEST_ADDR )
    self.util_check_SUCC_scenario( out, errCode, "", 
                                   "cloning repo %s into %s as %s user" % \
                                   ( TEST_ORIG_REPO, self.READONLY_CLONE_DIR, self.TEST_READONLY_USER) )

    #add repo RO to proj RW
    out, errCode = self.sw_clo_h.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME ) 
    self.util_addrepo_2proj( self.sw_clo_h, [ self.ROPROJ__BI ] )


    #check repo added correctly
    sw_ori_proj_h = swgit__utils( TEST_ORIG_REPO )
    sw_ori_repo_h = swgit__utils( self.ROPROJ__INFO[0] )
    repo_bi = self.ROPROJ__BI
    ro_clone_helper = swgit__utils( self.READONLY_CLONE_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.sw_clo_h, ro_clone_helper,
                                                      sw_ori_proj_h, sw_ori_repo_h,
                                                      repo_bi )

    #push proj must fail
    out, errCode = self.sw_clo_h.push_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "insufficient permission for adding an object to repository database", 
                                   "push" ) 


    out, errCode = swgit__utils.clone_repo( self.READONLY_CLONE_DIR, self.READONLY_CLOCLO_DIR )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "cloning proj %s into %s" % \
                                   (self.READONLY_CLONE_DIR, self.READONLY_CLOCLO_DIR) )


  def test_ReadOnly_04_00_OriginShared( self ):

    #RO clones shared repo
    out, errCode = swgit__utils.clone_repo( TEST_ORIG_REPO_SHARED, 
                                            self.READONLY_CLONE_DIR, 
                                            br = "", 
                                            user = self.TEST_READONLY_USER, 
                                            addr = TEST_ADDR )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "", 
                                   "cloning repo %s into %s as %s user" % \
                                   ( TEST_ORIG_REPO_SHARED, self.READONLY_CLONE_DIR, self.TEST_READONLY_USER) )

    #RW clones shared repo
    url = "ssh://%s@%s%s" % ( self.TEST_READWRITE_USER, TEST_ADDR, TEST_ORIG_REPO_SHARED )
    ret = self.exe_READWRITE_user( "cd %s && %s clone %s %s" % (SANDBOX, SWGIT, url, self.READWRITE_CLONE_DIR ) )
    #ret = self.exe_READWRITE_user( "cd %s && git clone %s %s" % (SANDBOX, url, self.READWRITE_CLONE_DIR ) )


    #ORIG only files of RW user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( TEST_ORIG_REPO_SHARED, self.TEST_READWRITE_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READWRITE_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READWRITE_USER,out) )

    #CLONE only files of RO user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( self.READONLY_CLONE_DIR, self.TEST_READONLY_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READONLY_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READONLY_USER,out) )

    #CLONE modify
    out, errCode = self.sw_clo_h.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch %s" % self.BRANCH_NAME ) 
    out, errCode = self.sw_clo_h.modify_file( TEST_REPO_FILE_A, msg = "some content" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" ) 
    out, errCode = self.sw_clo_h.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commit dev fix" ) 

    #push RO (before move HEAD away into origin)
    ret = self.exe_READWRITE_user( "cd %s && %s branch -s %s" % (TEST_ORIG_REPO_SHARED, SWGIT, TEST_REPO_BR_STB ) )

    #
    # push now runs
    #
    out, errCode = self.sw_clo_h.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, "Files updated:", "push" ) 


    #ORIG mixed files of RW and RO user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( TEST_ORIG_REPO_SHARED, self.TEST_READWRITE_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READWRITE_USER )
    self.assertNotEqual( out, "", "NOT FOUND files not of %s:\n%s" % (self.TEST_READWRITE_USER,out) )

    #CLONE only files of RO user
    out, errCode = self.sw_clo_h.system_unix( "find %s -not -user %s" % ( self.READONLY_CLONE_DIR, self.TEST_READONLY_USER ) )
    self.util_check_SUCC_scenario( out, errCode, "", "Looking for files not of %s" % self.TEST_READONLY_USER )
    self.assertEqual( out, "", "Found files not of %s:\n%s" % (self.TEST_READONLY_USER,out) )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()







