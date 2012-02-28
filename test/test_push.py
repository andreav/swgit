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

class Test_Push( Test_Base ):
  PUSH_REPO_DIR    = SANDBOX + "TEST_PUSH__REPO/"
  PUSH_CLONE_DIR   = SANDBOX + "TEST_PUSH__CLONE/"
  BRANCH_NAME   = "prova_push"
  BRANCH_NAME_SS = "side_of_side"

  DETACH_HEAD_ERROR = "FAILED - Cannot push in DETAHCED-HEAD."
  
  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

    super( Test_Push, self ).setUp()

    shutil.rmtree( self.PUSH_REPO_DIR, True ) #ignore errors
    shutil.rmtree( self.PUSH_CLONE_DIR, True ) #ignore errors

    # utilities for repo
    self.swgitUtil_Repo_ = swgit__utils( self.PUSH_REPO_DIR )
    self.gitUtil_Repo_   = git__utils( self.PUSH_REPO_DIR )


    # utilities for clone
    self.swgitUtil_Clone_ = swgit__utils( self.PUSH_CLONE_DIR )
    self.gitUtil_Clone_   = git__utils( self.PUSH_CLONE_DIR )

    # locals
    self.CREATED_BR     = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME )
    self.CREATED_BR_SS  = "%s/%s/%s/FTR/%s" % ( TEST_REPO_R, TEST_REPO_S, TEST_USER, self.BRANCH_NAME_SS )
    self.CREATED_BR_REM = "origin/%s" % self.CREATED_BR
    self.CREATED_BR_NEWBR = "%s/NEW/BRANCH" % ( self.CREATED_BR )
    self.CREATED_BR_FIX   = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS )
    self.CREATED_BR_DEV   = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_DEV_0  = "%s/DEV/000" % ( self.CREATED_BR )
    self.CREATED_DEV_1  = "%s/DEV/001" % ( self.CREATED_BR )
    self.CREATED_DEV_2  = "%s/DEV/002" % ( self.CREATED_BR )
    self.DDTS_0         = "Issue00000"
    self.DDTS_1         = "Issue11111"
    self.DDTS_2         = "Issue22222"
    self.CREATED_FIX_0  = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_0 )
    self.CREATED_FIX_1  = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_1 )
    self.CREATED_FIX_2  = "%s/FIX/%s" % ( self.CREATED_BR, self.DDTS_2 )
    self.MODIFY_FILE    = "%s/%s" % ( self.PUSH_REPO_DIR, ORIG_REPO_aFILE )


  def tearDown( self ):
    super( Test_Push, self ).tearDown()
    pass

  def clone_repo( self ):
    #first create repo
    create_dir_some_file( self.PUSH_REPO_DIR )
    out, errCode = swgit__utils.init_dir( self.PUSH_REPO_DIR )
    self.assertEqual( errCode, 0, "SWGIT init FAILED - swgit__utils.init_dir - \n%s\n" % out )

    #clone
    out, errCode = swgit__utils.clone_repo( self.PUSH_REPO_DIR, self.PUSH_CLONE_DIR )
    self.assertEqual( errCode, 0, "SWGIT clone FAILED - swgit__utils.clone_repo - \n%s\n" % out )

    # switch to int
    #out, errCode = self.gitUtil_Repo_.checkout( TEST_REPO_BR_DEV )
    #self.assertEqual( errCode, 0, "self.gitUtil_Repo_.checkout FAILED - out:\n%s" % out )


  def test_Push_01_00_Nothing( self ):
    self.clone_repo()

    # push
    out, errCode = self.swgitUtil_Clone_.push()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                      self.gitUtil_Clone_.get_currsha()[0], \
                      "Not on same commit FAILED - \n%s\n%s\n" % (self.gitUtil_Repo_.get_currsha()[0],self.gitUtil_Clone_.get_currsha()[0]) )

    #return A
    return self.gitUtil_Repo_.get_currsha()[0]

  # create this
  #  clone           
  #    |             
  #    A             
  #     \           
  #      B branch    
  #
  def clone_createBr_modifyFile_commit( self ):
    #clone
    self.clone_repo()
    A_repo = self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0]

    # create branch
    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.commit_minusA FAILED - \n%s\n" % out )

    # modify a file
    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"modification on repo\"" )
    self.assertEqual( errCode, 0, "_utils.echo_on_file FAILED - \n%s\n" % out )

    # commit (usign git because swgit does not work on origin)
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "swgitUtil_Clone_.commit_minusA FAILED - \n%s\n" % out )

    B_clone = self.gitUtil_Clone_.get_currsha()[0]

    self.assertNotEqual( B_clone, \
                         A_repo, \
                         "A has moved?\n%s\n%s\n" % (B_clone,A_repo) )
    self.assertNotEqual( B_clone, \
                         self.gitUtil_Clone_.ref2sha( "HEAD~1" )[0], \
                         "Commit but no moved?\n%s\n%s\n" % (B_clone,self.gitUtil_Clone_.ref2sha( "HEAD~1" )[0]) )
    self.assertEqual( A_repo, \
                      self.gitUtil_Clone_.ref2sha( "HEAD~1" )[0], \
                      "Commit not equals?\n%s\n%s\n" % (A_repo,self.gitUtil_Clone_.ref2sha( "HEAD~1" )[0]) )

    return A_repo, B_clone

  # create this:
  #
  #  repo  
  #    |   
  #    A   
  #    |\  
  #    | B 
  #    |/  
  #    C   
  def clone_createBr_modifyFile_commit_mergeOnDev( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    # switch to int
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.gitUtil_Repo_.checkout FAILED - out:\n%s" % out )

    # merge on develop
    out, errCode = self.gitUtil_Clone_.merge( B_clone )
    self.assertEqual( errCode, 0, "self.gitUtil_Clone_.merge FAILED - out:\n%s" % out )

    #return A,B,C
    return A_repo, B_clone, self.gitUtil_Clone_.get_currsha()[0]



  #  repo       clone           
  #    |          |             
  #    A          A             
  #                \           
  #                 B branch    
  #
  def test_Push_02_00_fromDevel_Commit_Tag_but_NoMergeOnDevel( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    # tag clone
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    # tag clone
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    # tag clone
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_1 )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )

    # switch to int
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "self.gitUtil_Repo_.checkout FAILED - out:\n%s" % out )

    # no merge branch!!!

    # push
    out, errCode = self.swgitUtil_Clone_.push()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )


    #nothing must be put on repo
    #no moved local branch
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_BR )[0], \
                      B_clone, \
                      "B has moved?\n%s\n%s\n" % (self.gitUtil_Clone_.ref2sha( self.CREATED_BR)[0] ,B_clone) )

    #no commit on origin
    self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                      A_repo, \
                      "A_repo has moved? - \n%s\n%s\n" % (self.gitUtil_Repo_.get_currsha()[0],A_repo) )


    #no branch on origin
    self.assertTrue( self.CREATED_BR not in self.swgitUtil_Repo_.local_branches()[0], \
        "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.local_branches()[0] ) )
    self.assertTrue( self.CREATED_BR not in self.swgitUtil_Repo_.remote_branches()[0], \
        "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.remote_branches()[0] ) )

    #no labels on origin
    self.assertTrue( self.CREATED_DEV_0 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_DEV_0 not in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 not in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 not in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )




  #  repo        clone           
  #    |           |            
  #    A           A            
  #    |\          | \          
  #    | B   <--   |  B  branch 
  #    |/          | /          
  #    C           C            
  def test_Push_02_01_fromDevel_BranchMerged( self ):
    A_repo, B_clone, C_clone = self.clone_createBr_modifyFile_commit_mergeOnDev()

    ######
    # push
    ######
    for i in (1,2):
      if i == 1:
        out, errCode = self.swgitUtil_Clone_.push()
        self.assertEqual( errCode, 0, "FAILED push from develop - \n%s\n" % out )
      else:
        out, errCode = self.swgitUtil_Clone_.push_with_merge()
        self.assertEqual( errCode, 0, "FAILED push from develop with -I - \n%s\n" % out )

      # repo not moved (always on slave)
      self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                        A_repo, \
                        "repo has moved?? Must stay on slave! - \n%s\n%s\n" % \
                        (self.gitUtil_Repo_.get_currsha()[0], A_repo) )

      # develop repo and develop clone on same commit
      self.assertEqual( self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0], \
                        self.gitUtil_Clone_.ref2sha( TEST_REPO_BR_DEV )[0], \
                        "Develop on repo is not same as develop on clone %s - %s" % \
                        ( self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0], self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )[0]) ) 

      # commit reported on origin
      self.assertEqual( self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0], \
                        C_clone, \
                        "C_clone not reported? - \n[%s]\n[%s]\n" % (self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0],C_clone) )


     # # branch reported on origin
     # self.assertTrue( self.CREATED_BR in self.swgitUtil_Repo_.local_branches()[0], \
     #     "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.local_branches()[0] ) )
     # self.assertTrue( self.CREATED_BR not in self.swgitUtil_Repo_.remote_branches()[0], \
     #     "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.remote_branches()[0] ) )

      #no labels on origin
      self.assertTrue( self.CREATED_DEV_0 not in self.gitUtil_Clone_.tag_list()[0], \
          "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
      self.assertTrue( self.CREATED_FIX_0 not in self.gitUtil_Clone_.tag_list()[0], \
          "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
      self.assertTrue( self.CREATED_FIX_1 not in self.gitUtil_Clone_.tag_list()[0], \
          "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
      self.assertTrue( self.CREATED_DEV_0 not in self.gitUtil_Repo_.tag_list()[0], \
          "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
      self.assertTrue( self.CREATED_FIX_0 not in self.gitUtil_Repo_.tag_list()[0], \
          "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
      self.assertTrue( self.CREATED_FIX_1 not in self.gitUtil_Repo_.tag_list()[0], \
          "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )





  #  repo       clone           
  #    |          |             
  #    A          A             
  #                \           
  #                 B branch    
  #
  def test_Push_03_00_fromSide_NoDevOnsideBr( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #
    # push from side! => no dev => MUST fail
    #
    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.assertNotEqual( errCode, 0, "SWGIT pull MUST FAILED - swgit__utils.pull - \n%s\n" % out )

    # repo not moved (always on slave)
    self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                      A_repo, \
                      "repo has moved?? Must stay on slave! - \n%s\n%s\n" % \
                      (self.gitUtil_Repo_.get_currsha()[0], A_repo) )

    #nothing must be put on repo
    #no moved local branch
    self.assertEqual( self.gitUtil_Clone_.ref2sha( self.CREATED_BR )[0], \
                      B_clone, \
                      "B has moved?\n%s\n%s\n" % (self.gitUtil_Clone_.ref2sha( self.CREATED_BR)[0] ,B_clone) )

    #local HEAD on develop
    self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                      A_repo, \
                      "A has moved?\n%s\n%s\n" % (self.gitUtil_Repo_.get_currsha()[0] ,A_repo) )

    #no commit on origin
    self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                      A_repo, \
                      "A_repo has moved? - \n%s\n%s\n" % (self.gitUtil_Repo_.get_currsha()[0],A_repo) )


    #no branch on origin
    self.assertTrue( self.CREATED_BR not in self.swgitUtil_Repo_.local_branches()[0], \
        "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.local_branches()[0] ) )
    self.assertTrue( self.CREATED_BR not in self.swgitUtil_Repo_.remote_branches()[0], \
        "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.remote_branches()[0] ) )

    #no labels on origin, nor in local
    self.assertTrue( self.CREATED_DEV_0 not in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 not in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 not in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_DEV_0 not in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 not in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 not in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )



  # repo                clone
  #   |                   |
  #   A                   A    DEV   
  #   | \                 |\   DEV     
  #   |  B       <--      | B  FIX     
  #   | /                 |/   FIX    
  #   C                   C            
  def test_Push_03_01_fromSide_YesDevOnSideBr( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    # tag clone
    out, errCode = self.swgitUtil_Clone_.tag_dev()
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    # tag clone
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_0 )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )
    # tag clone
    out, errCode = self.swgitUtil_Clone_.tag_fix( self.DDTS_1 )
    self.assertEqual( errCode, 0, "gitUtil_Repo_.tag_put_on_commit FAILED - \n%s\n" % out )


    #
    # push from side! => merge and push
    #
    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.assertEqual( errCode, 0, "SWGIT pull FAILED - swgit__utils.pull - \n%s\n" % out )

    C_clone = self.gitUtil_Clone_.ref2sha( TEST_REPO_BR_DEV )[0]
    #C_clone must be a new commit
    self.assertNotEqual( A_repo, \
                         C_clone, \
                         "C_clone same as A_repo? - \n[%s]\n[%s]\n" % (A_repo,C_clone) )
    self.assertNotEqual( B_clone, \
                         C_clone, \
                         "C_clone same as B_clone? - \n[%s]\n[%s]\n" % (B_clone,C_clone) )

    # repo not moved (always on slave)
    self.assertEqual( self.gitUtil_Repo_.get_currsha()[0], \
                      A_repo, \
                      "repo has moved?? Must stay on slave! - \n%s\n%s\n" % \
                      (self.gitUtil_Repo_.get_currsha()[0], A_repo) )

    # develop repo and develop clone on same commit
    self.assertEqual( self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0], \
                      self.gitUtil_Clone_.ref2sha( TEST_REPO_BR_DEV )[0], \
                      "Develop on repo is not same as develop on clone %s - %s" % \
                      ( self.gitUtil_Repo_.ref2sha( TEST_REPO_BR_DEV )[0], self.gitUtil_Clone_.ref2sha( self.CREATED_DEV_0 )[0]) ) 


    # branch reported on origin
    #self.assertTrue( self.CREATED_BR in self.swgitUtil_Repo_.local_branches()[0], \
    #    "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.local_branches()[0] ) )
    #self.assertTrue( self.CREATED_BR not in self.swgitUtil_Repo_.remote_branches()[0], \
    #    "FAILED local branch pushed on origin, %s in %s" % (self.CREATED_BR, self.swgitUtil_Repo_.remote_branches()[0] ) )

    # labels on origin
    self.assertTrue( self.CREATED_DEV_0 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 in self.gitUtil_Clone_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Clone_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_DEV_0 in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_0 in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )
    self.assertTrue( self.CREATED_FIX_1 in self.gitUtil_Repo_.tag_list()[0], \
        "NOT local dev %s in\n%s" % ( self.CREATED_DEV_0, self.gitUtil_Repo_.tag_list()[0] ) )


  def test_Push_04_00_CustomTags_push( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #create pushable and non pushable custom label
    YESPUSHabel_label = copy.deepcopy( CUSTTAG_NAME )
    YESPUSHabel_label["tagtype"]  = "NUMTAG_YES_PUSHABLE"

    NONPUSHabel_label = copy.deepcopy( CUSTTAG_NAME )
    NONPUSHabel_label["tagtype"]  = "NUMTAG_NON_PUSHABLE"
    NONPUSHabel_label["push_on_origin"]  = "False"
    self.swgitUtil_Clone_.tag_define_custom_tag( YESPUSHabel_label )
    self.swgitUtil_Clone_.tag_define_custom_tag( NONPUSHabel_label )

    # commit changes
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit_minusA - \n%s\n" % out )

    tagname = "1234567"
    out, errCode = self.swgitUtil_Clone_.tag_create( YESPUSHabel_label["tagtype"], tagname, msg = "yes pushable" )
    self.assertEqual( errCode, 0, "FAILED create CUSTTAG NAME pushable - \n%s\n" % out )

    out, errCode = self.swgitUtil_Clone_.tag_create( NONPUSHabel_label["tagtype"], tagname, msg = "non pushable" )
    self.assertEqual( errCode, 0, "FAILED create CUSTTAG NAME NON pushable - \n%s\n" % out )

    created_yespush_custtag_label = "%s/%s/%s" % ( self.CREATED_BR, YESPUSHabel_label["tagtype"], tagname )
    created_nonpush_custtag_label = "%s/%s/%s" % ( self.CREATED_BR, NONPUSHabel_label["tagtype"], tagname )

    yespush_tag_sha, errCode = self.gitUtil_Clone_.ref2sha( created_yespush_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_yespush_custtag_label, yespush_tag_sha) )

    nonpush_tag_sha, errCode = self.gitUtil_Clone_.ref2sha( created_nonpush_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_nonpush_custtag_label, nonpush_tag_sha) )


    #
    # Push
    #
    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.assertEqual( errCode, 1, "MUST FAIL push without DEV - \n%s\n" % out )
    self.util_check_DENY_scenario( out, errCode, 
                                   "No DEV label found on branch",
                                   "MUST FAIL push without DEV" )

    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "pushable custom tag test" )
    self.assertEqual( errCode, 0, "FAILED create DEV lable - \n%s\n" % out )

    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push with DEV - \n%s\n" % out )

    #check labels on remote
    origin_yespush_tag_sha, errCode = self.gitUtil_Repo_.ref2sha( created_yespush_custtag_label )
    self.assertEqual( errCode, 0, "FAILED retrieving tag %s - \n%s\n" % (created_yespush_custtag_label, origin_yespush_tag_sha) )
    self.assertEqual( yespush_tag_sha, origin_yespush_tag_sha, "FAILED - origin and local label %s must be on ame sha %s vs %s - \n%s\n" %
                      (created_yespush_custtag_label, yespush_tag_sha, origin_yespush_tag_sha, origin_yespush_tag_sha ) )

    origin_nonpush_tag_sha, errCode = self.gitUtil_Repo_.ref2sha( created_nonpush_custtag_label )
    self.assertEqual( errCode, 1, "MUST FAIL retrieving tag %s on origin (non pushable) - \n%s\n" % 
                      (created_nonpush_custtag_label, origin_nonpush_tag_sha) )


  def test_Push_05_00_DetachedHead( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #make another commit
    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"2. modification on repo\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )

    #on br, no dev
    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot directly push a develop branch",
                                   "MUST FAIL push from detach" )

    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "No DEV label found on branch",
                                   "MUST FAIL push from br witout DEV with -I" )

    #on detach head on devel br
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED switch to HEAD~1 - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "DONE - No tags found.",
                                   "push from detached head" )

    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "DONE - No tags found.",
                                   "push from detached head also with -I" )

    #on detach head on int br
    #make another commit
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.assertEqual( errCode, 0, "FAILED switch to int - out:\n%s" % ( out ) )
    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"2. modification on repo\"" )
    self.assertEqual( errCode, 0, "FAILED echo_on_file - \n%s\n" % out )
    out, errCode = self.gitUtil_Clone_.commit_minusA()
    self.assertEqual( errCode, 0, "FAILED commit - \n%s\n" % out )
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( "HEAD~1" )
    self.assertEqual( errCode, 0, "FAILED switch to HEAD~1 - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "DONE - No tags found.",
                                   "MUST FAIL push from detached head" )

    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "DONE - No tags found.",
                                   "MUST FAIL push from detached head also with -I" )

  def test_Push_06_00_NoIntBr( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #unset intbr
    saved_intbr, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.assertEqual( errCode, 0, "FAILED getting intbr - out:\n%s" % ( saved_intbr ) )
    out, errCode = self.swgitUtil_Clone_.set_cfg( "swgit.intbranch", SWCFG_TEST_UNSET )
    self.assertEqual( errCode, 0, "FAILED manually unsettin intbr - out:\n%s" % ( out ) )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_DENY_scenario( out, errCode, 
                                   "No int branch set for this repo.",
                                   "MUST FAIL getintbr after manually unsetting" )

    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot push without an integration branch set.",
                                   "MUST FAIL push without an integration branch set" )

    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot push without an integration branch set.",
                                   "MUST FAIL push without an integration branch set also with -I" )


    #make another commit (temporary reset intbr to allow committing)
    out, errCode = self.swgitUtil_Clone_.int_branch_set( saved_intbr )
    self.assertEqual( errCode, 0, "FAILED manually setting intbr - out:\n%s" % ( out ) )

    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"2. modification on repo\"" )
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

    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "DONE - No tags found.",
                                   "MUST FAIL push from detached head" )

    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, 
                                   "DONE - No tags found.",
                                   "MUST FAIL push from detached head also with -I" )




  def test_Push_06_01_IntBrOnlyLocal_pushItNow_fromintbr( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #check br not existing on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving remote branch %s" % self.BRANCH_NAME_SS )


    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode,
                              "Setting INTEGRATION branch to", 
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_SUCC_scenario( out, errCode,
                              self.CREATED_BR,
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode,
                              "Creating branch %s" % self.CREATED_BR_SS,
                              "FAILED creating br %s" % self.CREATED_BR_SS )

    #modify from side_of_side
    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"side_of_side\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED echo on file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit minus A" )
    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "will be pushed from side of side" )
    self.util_check_SUCC_scenario( out, errCode, "DEV/000", "FAILED create dev" )

    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )

    #
    # swith to int and merge
    #
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED swith to int" )
    out, errCode = self.swgitUtil_Clone_.merge( "%s/DEV/000" % self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED merge" )
    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED push" )
    #second push must not fail if previous push also has tracked new intbr
    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED push" )

    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )


  def test_Push_06_01_IntBrOnlyLocal_pushItNow_fromintbr_reversepushorder( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #check br not existing on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving remote branch %s" % self.BRANCH_NAME_SS )


    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode,
                              "Setting INTEGRATION branch to", 
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_SUCC_scenario( out, errCode,
                              self.CREATED_BR,
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode,
                              "Creating branch %s" % self.CREATED_BR_SS,
                              "FAILED creating br %s" % self.CREATED_BR_SS )

    #modify from side_of_side
    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"side_of_side\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED echo on file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit minus A" )
    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "will be pushed from side of side" )
    self.util_check_SUCC_scenario( out, errCode, "DEV/000", "FAILED create dev" )

    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )

    #
    # swith to int nd merge
    #
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED swith to int" )
    out, errCode = self.swgitUtil_Clone_.merge( "%s/DEV/000" % self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED merge" )
    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED push" )
    #second push must not fail if previous push also has tracked new intbr
    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED push" )

    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )




  def test_Push_06_01_IntBrOnlyLocal_pushItNow_fromside( self ):
    A_repo, B_clone = self.clone_createBr_modifyFile_commit()

    #check br not existing on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving remote branch %s" % self.BRANCH_NAME_SS )


    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode,
                              "Setting INTEGRATION branch to", 
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.int_branch_get()
    self.util_check_SUCC_scenario( out, errCode,
                              self.CREATED_BR,
                              "FAILED set int br" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode,
                              "Creating branch %s" % self.CREATED_BR_SS,
                              "FAILED creating br %s" % self.CREATED_BR_SS )

    #modify from side_of_side
    out, errCode = echo_on_file( self.PUSH_CLONE_DIR + TEST_REPO_FILE_A, "\"side_of_side\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED echo on file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED commit minus A" )
    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "will be pushed from side of side" )
    self.util_check_SUCC_scenario( out, errCode, "DEV/000", "FAILED create dev" )

    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )

    out, errCode = self.swgitUtil_Clone_.push()
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL simple push" )

    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_DENY_scenario( out, errCode, "", "MUST FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )


    out, errCode = self.swgitUtil_Clone_.push_with_merge()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED push with -I" )


    #no branch no devs on origin
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Repo_.ref2sha( self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED retrieving branch %s on origin" % self.BRANCH_NAME_SS )
    out, errCode = self.swgitUtil_Repo_.ref2sha( "%s/DEV/000" % self.CREATED_BR_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "FAIL retrieving label %s/DEV/000 on origin" % self.BRANCH_NAME_SS )


  def test_Push_07_00_Push_TagInPast_PushFromBr( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )

    #define custom tag
    TAG_NUM_ECHO_NOPAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_NOPAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_NOPAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_NOPAST["tag_in_past"]  = "True"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_NOPAST )

    #some commits
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_repo( TEST_REPO_FILE_A, msg = "something", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modify repo" )
    out, errCode = self.swgitUtil_Clone_.modify_repo( TEST_REPO_FILE_A, msg = "something", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modify repo" )


    #switch back in past, but local
    DETACH = "HEAD~1"
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to HEAD~1" )

    #create tag
    BASEBR = self.CREATED_BR
    created_custtag_label_1 = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_NOPAST["tagtype"] )
    created_custtag_PAST_label_1 = "PAST/%s" % created_custtag_label_1

    #check labels non existence
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    #create tag
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past" )

    #come back on HEAD
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to %s" % self.BRANCH_NAME )
    out, errCode = self.swgitUtil_Clone_.tag_create( "dev", msg = "local dev" )
    self.assertEqual( errCode, 0, "FAILED tag DEV - \n%s\n" % out )

    #check labels existence
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    #push
    out, errCode = self.sw_origrepo_h.branch_switch_to_br( TEST_REPO_TAG_LIV )
    if modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.push_with_merge( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_Clone_.push_with_merge()
      self.util_check_SUCC_scenario( out, errCode, "", "push" )
      remote_h = self.sw_origrepo_h

    #check labels existence
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )
    out, errCode = remote_h.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    tagPast_sha, errCode = remote_h.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )




  def test_Push_07_00_PushInPast( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )

    #define custom tag
    TAG_NUM_ECHO_NOPAST = copy.deepcopy( CUSTTAG_NUM )
    script_comment = "comment: ABCD"
    TAG_NUM_ECHO_NOPAST["tagtype"]             = "TAGINPAST"
    TAG_NUM_ECHO_NOPAST["hook_pretag_script"]  = "echo \"%s\"" % script_comment
    TAG_NUM_ECHO_NOPAST["tag_in_past"]  = "True"
    self.swgitUtil_Clone_.tag_define_custom_tag( TAG_NUM_ECHO_NOPAST )

    #some commits
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_repo( TEST_REPO_FILE_A, msg = "something", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modify repo" )
    out, errCode = self.swgitUtil_Clone_.modify_repo( TEST_REPO_FILE_A, msg = "something", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modify repo" )


    #switch back in past, but local
    DETACH = "HEAD~1"
    out, errCode = self.swgitUtil_Clone_.branch_switch_to_br( DETACH )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to HEAD~1" )


    #push
    if modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.push( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, 
                                     "DONE - No tags found.",
                                     "push in past, with no labels in past" )
    else:
      out, errCode = self.swgitUtil_Clone_.push()
      self.util_check_SUCC_scenario( out, errCode, 
                                     "DONE - No tags found.",
                                     "push in past, with no labels in past" )


    #tag names
    BASEBR = self.CREATED_BR
    created_custtag_label_0 = "%s/%s/000" % ( BASEBR, TAG_NUM_ECHO_NOPAST["tagtype"] )
    created_custtag_PAST_label_0 = "PAST/%s" % created_custtag_label_0
    created_custtag_label_1 = "%s/%s/001" % ( BASEBR, TAG_NUM_ECHO_NOPAST["tagtype"] )
    created_custtag_PAST_label_1 = "PAST/%s" % created_custtag_label_1

    #check labels not existence
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_0 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )


    #create tag
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past" )
    out, errCode = self.swgitUtil_Clone_.tag_create( TAG_NUM_ECHO_NOPAST["tagtype"] )
    self.util_check_SUCC_scenario( out, errCode, 
                                   "Tagging in past also creates tag PAST/",
                                   "tagging in past" )

    #check labels not existence
    #on clone
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_0 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    #on origin
    out, errCode = self.sw_origrepo_h.ref2sha( created_custtag_label_0 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_0 )
    out, errCode = self.sw_origrepo_h.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )
    out, errCode = self.sw_origrepo_h.ref2sha( created_custtag_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    out, errCode = self.sw_origrepo_h.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )


    #push
    if modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.push( ORIG_REPO_AREMOTE_NAME )
      self.util_check_SUCC_scenario( out, errCode, 
                                     "in DETAHCED-HEAD only tags put-in-past will be pushed",
                                     "push in past" )
      remote_h = self.sw_aremoterepo_h
    else:
      out, errCode = self.swgitUtil_Clone_.push()
      self.util_check_SUCC_scenario( out, errCode, 
                                     "in DETAHCED-HEAD only tags put-in-past will be pushed",
                                     "push in past" )
      remote_h = self.sw_origrepo_h


    #check labels not existence
    #on clone
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_0 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_0 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    out, errCode = self.swgitUtil_Clone_.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )

    #on origin
    out, errCode = remote_h.ref2sha( created_custtag_label_0 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_0 )
    out, errCode = remote_h.ref2sha( created_custtag_PAST_label_0 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_0 )
    out, errCode = remote_h.ref2sha( created_custtag_label_1 )
    self.util_check_SUCC_scenario( out, errCode, "", "retrieving %s" % created_custtag_label_1 )
    out, errCode = remote_h.ref2sha( created_custtag_PAST_label_1 )
    self.util_check_DENY_scenario( out, errCode, "", "retrieving %s" % created_custtag_PAST_label_1 )


  def test_Push_08_00_NewRel_LIV( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )

    MYINT_REL  = "1/1"
    MYINT_NAME = "myint"
    MYINT_DEV  = "%s/%s/%s/INT/%s_develop" % ( MYINT_REL, ORIG_REPO_SUBREL, TEST_USER, MYINT_NAME )
    MYINT_STB  = "%s/%s/%s/INT/%s_stable" % ( MYINT_REL, ORIG_REPO_SUBREL, TEST_USER, MYINT_NAME )
    MYINT_DEV_STB  = "%s/STB/%s" % ( MYINT_DEV, TEST_REPO_LIV )
    MYINT_STB_LIV  = "%s/LIV/%s" % ( MYINT_STB, TEST_REPO_LIV )
    MYINT_STB_STB  = "%s/STB/%s" % ( MYINT_STB, TEST_REPO_LIV )
    out, errCode = self.swgitUtil_Clone_.init_dir( self.PUSH_CLONE_DIR, 
                                                   "1/1", 
                                                   u = TEST_USER, 
                                                   c = MYINT_NAME,
                                                   src = "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % MYINT_DEV )

    #only local
    intdev, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_DEV )
    self.util_check_SUCC_scenario( intdev, errCode, "", "retrieving local %s" % MYINT_DEV )
    intstb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB )
    self.util_check_SUCC_scenario( intstb, errCode, "", "retrieving local %s" % MYINT_STB )

    intdev_stb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_DEV_STB )
    self.util_check_SUCC_scenario( intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    intstb_liv, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB_LIV )
    self.util_check_SUCC_scenario( intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    intstb_stb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB_STB )
    self.util_check_SUCC_scenario( intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )

    devminus1, errCode = self.swgitUtil_Clone_.ref2sha( "%s~1" % MYINT_DEV )
    self.util_check_SUCC_scenario( devminus1, errCode, "", "retrieving local %s~1" % MYINT_DEV )
    stbminus1, errCode = self.swgitUtil_Clone_.ref2sha( "%s~1" % MYINT_STB )
    self.util_check_SUCC_scenario( stbminus1, errCode, "", "retrieving local %s~1" % MYINT_STB )
    src, errCode = self.swgitUtil_Clone_.ref2sha( "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( src, errCode, "", "retrieving local origin/%s" % ORIG_REPO_STABLE_BRANCH )

    self.assertEqual( intdev, intstb, "must be equal" )
    self.assertEqual( devminus1, src, "must be equal" )
    self.assertEqual( stbminus1, src, "must be equal" )


    rem_intdev, errCode = self.sw_origrepo_h.ref2sha( MYINT_DEV )
    self.util_check_DENY_scenario( rem_intdev, errCode, "", "retrieving remote %s" % MYINT_DEV )
    rem_intstb, errCode = self.sw_origrepo_h.ref2sha( MYINT_STB )
    self.util_check_DENY_scenario( rem_intstb, errCode, "", "retrieving local %s" % MYINT_STB )
    rem_intdev_stb, errCode = self.sw_origrepo_h.ref2sha( MYINT_DEV_STB )
    self.util_check_DENY_scenario( rem_intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    rem_intstb_liv, errCode = self.sw_origrepo_h.ref2sha( MYINT_STB_LIV )
    self.util_check_DENY_scenario( rem_intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    rem_intstb_stb, errCode = self.sw_origrepo_h.ref2sha( MYINT_STB_STB )
    self.util_check_DENY_scenario( rem_intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )

    remote = ""
    remote_h = self.sw_origrepo_h
    if modetest_morerepos():
      remote   = ORIG_REPO_AREMOTE_NAME
      remote_h = self.sw_aremoterepo_h

    #
    #push in detach does nothing
    #
    intdev, errCode = self.swgitUtil_Clone_.push( remote )
    self.util_check_SUCC_scenario( intdev, errCode, 
                                   "in DETAHCED-HEAD only tags put-in-past will be pushed.", 
                                   "pushing in detach" )

    rem_intdev, errCode = remote_h.ref2sha( MYINT_DEV )
    self.util_check_DENY_scenario( rem_intdev, errCode, "", "retrieving remote %s" % MYINT_DEV )
    rem_intstb, errCode = remote_h.ref2sha( MYINT_STB )
    self.util_check_DENY_scenario( rem_intstb, errCode, "", "retrieving local %s" % MYINT_STB )
    rem_intdev_stb, errCode = remote_h.ref2sha( MYINT_DEV_STB )
    self.util_check_DENY_scenario( rem_intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    rem_intstb_liv, errCode = remote_h.ref2sha( MYINT_STB_LIV )
    self.util_check_DENY_scenario( rem_intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    rem_intstb_stb, errCode = remote_h.ref2sha( MYINT_STB_STB )
    self.util_check_DENY_scenario( rem_intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )



    #
    #switch and push
    #
    intdev, errCode = self.swgitUtil_Clone_.branch_switch_to_br( MYINT_STB )
    self.util_check_SUCC_scenario( intdev, errCode, "", "switch to %s" % MYINT_STB )
    intdev, errCode = self.swgitUtil_Clone_.push( remote )
    self.util_check_SUCC_scenario( intdev, errCode, "", "pushing from stable" )

    #local and remote
    intdev, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_DEV )
    self.util_check_SUCC_scenario( intdev, errCode, "", "retrieving local %s" % MYINT_DEV )
    intstb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB )
    self.util_check_SUCC_scenario( intstb, errCode, "", "retrieving local %s" % MYINT_STB )

    rem_intdev, errCode = remote_h.ref2sha( MYINT_DEV )
    self.util_check_SUCC_scenario( rem_intdev, errCode, "", "retrieving remote %s" % MYINT_DEV )
    rem_intstb, errCode = remote_h.ref2sha( MYINT_STB )
    self.util_check_SUCC_scenario( rem_intstb, errCode, "", "retrieving local %s" % MYINT_STB )

    rem_intdev_stb, errCode = remote_h.ref2sha( MYINT_DEV_STB )
    self.util_check_SUCC_scenario( rem_intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    rem_intstb_liv, errCode = remote_h.ref2sha( MYINT_STB_LIV )
    self.util_check_SUCC_scenario( rem_intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    rem_intstb_stb, errCode = remote_h.ref2sha( MYINT_STB_STB )
    self.util_check_SUCC_scenario( rem_intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )




  def test_Push_08_01_NewRel_noLIV( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )

    MYINT_REL  = "1/1"
    MYINT_NAME = "myint"
    MYINT_DEV  = "%s/%s/%s/INT/%s_develop" % ( MYINT_REL, ORIG_REPO_SUBREL, TEST_USER, MYINT_NAME )
    MYINT_STB  = "%s/%s/%s/INT/%s_stable" % ( MYINT_REL, ORIG_REPO_SUBREL, TEST_USER, MYINT_NAME )
    MYINT_DEV_STB  = "%s/STB/%s" % ( MYINT_DEV, TEST_REPO_LIV )
    MYINT_STB_LIV  = "%s/LIV/%s" % ( MYINT_STB, TEST_REPO_LIV )
    MYINT_STB_STB  = "%s/STB/%s" % ( MYINT_STB, TEST_REPO_LIV )
    out, errCode = self.swgitUtil_Clone_.init_dir( self.PUSH_CLONE_DIR, 
                                                   "1/1", 
                                                   u = TEST_USER, 
                                                   l= "", 
                                                   c = MYINT_NAME,
                                                   src = "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % MYINT_DEV )

    #only local
    intdev, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_DEV )
    self.util_check_SUCC_scenario( intdev, errCode, "", "retrieving local %s" % MYINT_DEV )
    intstb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB )
    self.util_check_SUCC_scenario( intstb, errCode, "", "retrieving local %s" % MYINT_STB )

    intdev_stb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_DEV_STB )
    self.util_check_DENY_scenario( intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    intstb_liv, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB_LIV )
    self.util_check_DENY_scenario( intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    intstb_stb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB_STB )
    self.util_check_DENY_scenario( intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )

    devminus1, errCode = self.swgitUtil_Clone_.ref2sha( "%s~1" % MYINT_DEV )
    self.util_check_SUCC_scenario( devminus1, errCode, "", "retrieving local %s~1" % MYINT_DEV )
    stbminus1, errCode = self.swgitUtil_Clone_.ref2sha( "%s~1" % MYINT_STB )
    self.util_check_SUCC_scenario( stbminus1, errCode, "", "retrieving local %s~1" % MYINT_STB )
    src, errCode = self.swgitUtil_Clone_.ref2sha( "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( src, errCode, "", "retrieving local origin/%s" % ORIG_REPO_STABLE_BRANCH )

    self.assertEqual( intdev, intstb, "must be equal" )
    self.assertEqual( devminus1, src, "must be equal" )
    self.assertEqual( stbminus1, src, "must be equal" )


    rem_intdev, errCode = self.sw_origrepo_h.ref2sha( MYINT_DEV )
    self.util_check_DENY_scenario( rem_intdev, errCode, "", "retrieving remote %s" % MYINT_DEV )
    rem_intstb, errCode = self.sw_origrepo_h.ref2sha( MYINT_STB )
    self.util_check_DENY_scenario( rem_intstb, errCode, "", "retrieving local %s" % MYINT_STB )
    rem_intdev_stb, errCode = self.sw_origrepo_h.ref2sha( MYINT_DEV_STB )
    self.util_check_DENY_scenario( rem_intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    rem_intstb_liv, errCode = self.sw_origrepo_h.ref2sha( MYINT_STB_LIV )
    self.util_check_DENY_scenario( rem_intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    rem_intstb_stb, errCode = self.sw_origrepo_h.ref2sha( MYINT_STB_STB )
    self.util_check_DENY_scenario( rem_intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )


    #
    # push
    #
    remote = ""
    remote_h = self.sw_origrepo_h
    if modetest_morerepos():
      remote   = ORIG_REPO_AREMOTE_NAME
      remote_h = self.sw_aremoterepo_h

    intdev, errCode = self.swgitUtil_Clone_.push( remote )
    self.util_check_SUCC_scenario( intdev, errCode, "", "pushing from stable" )

    #local and remote
    intdev, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_DEV )
    self.util_check_SUCC_scenario( intdev, errCode, "", "retrieving local %s" % MYINT_DEV )
    intstb, errCode = self.swgitUtil_Clone_.ref2sha( MYINT_STB )
    self.util_check_SUCC_scenario( intstb, errCode, "", "retrieving local %s" % MYINT_STB )

    rem_intdev, errCode = remote_h.ref2sha( MYINT_DEV )
    self.util_check_SUCC_scenario( rem_intdev, errCode, "", "retrieving remote %s" % MYINT_DEV )
    rem_intstb, errCode = remote_h.ref2sha( MYINT_STB )
    self.util_check_SUCC_scenario( rem_intstb, errCode, "", "retrieving local %s" % MYINT_STB )

    rem_intdev_stb, errCode = remote_h.ref2sha( MYINT_DEV_STB )
    self.util_check_DENY_scenario( rem_intdev_stb, errCode, "", "retrieving local %s" % MYINT_DEV_STB )
    rem_intstb_liv, errCode = remote_h.ref2sha( MYINT_STB_LIV )
    self.util_check_DENY_scenario( rem_intstb_liv, errCode, "", "retrieving local %s" % MYINT_STB_LIV )
    rem_intstb_stb, errCode = remote_h.ref2sha( MYINT_STB_STB )
    self.util_check_DENY_scenario( rem_intstb_stb, errCode, "", "retrieving local %s" % MYINT_STB_STB )




  def test_Push_08_02_NewCst_LIV( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )

    MYCST_REL  = "1/1"
    MYCST_NAME = "mycst"
    MYCST  = "%s/%s/%s/CST/%s" % ( MYCST_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST_NAME )
    MYCST_LIV  = "%s/LIV/%s" % ( MYCST, TEST_REPO_LIV )
    out, errCode = self.swgitUtil_Clone_.init_dir( self.PUSH_CLONE_DIR, 
                                                   "1/1", 
                                                   u = TEST_USER, 
                                                   c = MYCST_NAME,
                                                   cst = True, 
                                                   src = "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % MYCST )

    #only local
    cstsha, errCode = self.swgitUtil_Clone_.ref2sha( MYCST )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "retrieving local %s" % MYCST )

    cstsha_liv, errCode = self.swgitUtil_Clone_.ref2sha( MYCST_LIV )
    self.util_check_SUCC_scenario( cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )

    devminus1, errCode = self.swgitUtil_Clone_.ref2sha( "%s~1" % MYCST )
    self.util_check_SUCC_scenario( devminus1, errCode, "", "retrieving local %s~1" % MYCST )
    src, errCode = self.swgitUtil_Clone_.ref2sha( "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( src, errCode, "", "retrieving local origin/%s" % ORIG_REPO_STABLE_BRANCH )

    self.assertEqual( cstsha, cstsha_liv, "must be equal" )
    self.assertEqual( devminus1, src, "must be equal" )


    rem_cstsha, errCode = self.sw_origrepo_h.ref2sha( MYCST )
    self.util_check_DENY_scenario( rem_cstsha, errCode, "", "retrieving remote %s" % MYCST )
    rem_cstsha_liv, errCode = self.sw_origrepo_h.ref2sha( MYCST_LIV )
    self.util_check_DENY_scenario( rem_cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )

    remote = ""
    remote_h = self.sw_origrepo_h
    if modetest_morerepos():
      remote   = ORIG_REPO_AREMOTE_NAME
      remote_h = self.sw_aremoterepo_h

    #
    # push
    #
    cstsha, errCode = self.swgitUtil_Clone_.push( remote )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "pushing from CST" )

    #local and remote
    cstsha, errCode = self.swgitUtil_Clone_.ref2sha( MYCST )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "retrieving local %s" % MYCST )

    rem_cstsha, errCode = remote_h.ref2sha( MYCST )
    self.util_check_SUCC_scenario( rem_cstsha, errCode, "", "retrieving remote %s" % MYCST )

    rem_cstsha_liv, errCode = remote_h.ref2sha( MYCST_LIV )
    self.util_check_SUCC_scenario( rem_cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )




  def test_Push_08_03_NewCst_noLIV( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )

    MYCST_REL  = "1/1"
    MYCST_NAME = "mycst"
    MYCST  = "%s/%s/%s/CST/%s" % ( MYCST_REL, ORIG_REPO_SUBREL, TEST_USER, MYCST_NAME )
    MYCST_LIV  = "%s/LIV/%s" % ( MYCST, TEST_REPO_LIV )
    out, errCode = self.swgitUtil_Clone_.init_dir( self.PUSH_CLONE_DIR, 
                                                   "1/1", 
                                                   u = TEST_USER, 
                                                   c = MYCST_NAME,
                                                   l = "",
                                                   cst = True, 
                                                   src = "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( out, errCode, "", "creating %s" % MYCST )

    #only local
    cstsha, errCode = self.swgitUtil_Clone_.ref2sha( MYCST )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "retrieving local %s" % MYCST )

    cstsha_liv, errCode = self.swgitUtil_Clone_.ref2sha( MYCST_LIV )
    self.util_check_DENY_scenario( cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )

    devminus1, errCode = self.swgitUtil_Clone_.ref2sha( "%s~1" % MYCST )
    self.util_check_SUCC_scenario( devminus1, errCode, "", "retrieving local %s~1" % MYCST )
    src, errCode = self.swgitUtil_Clone_.ref2sha( "origin/" + ORIG_REPO_STABLE_BRANCH )
    self.util_check_SUCC_scenario( src, errCode, "", "retrieving local origin/%s" % ORIG_REPO_STABLE_BRANCH )

    self.assertEqual( devminus1, src, "must be equal" )


    rem_cstsha, errCode = self.sw_origrepo_h.ref2sha( MYCST )
    self.util_check_DENY_scenario( rem_cstsha, errCode, "", "retrieving remote %s" % MYCST )
    rem_cstsha_liv, errCode = self.sw_origrepo_h.ref2sha( MYCST_LIV )
    self.util_check_DENY_scenario( rem_cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )

    remote = ""
    remote_h = self.sw_origrepo_h
    if modetest_morerepos():
      remote   = ORIG_REPO_AREMOTE_NAME
      remote_h = self.sw_aremoterepo_h

    #
    # push
    #
    cstsha, errCode = self.swgitUtil_Clone_.push( remote )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "pushing from CST" )

    #local and remote
    cstsha, errCode = self.swgitUtil_Clone_.ref2sha( MYCST )
    self.util_check_SUCC_scenario( cstsha, errCode, "", "retrieving local %s" % MYCST )

    rem_cstsha, errCode = remote_h.ref2sha( MYCST )
    self.util_check_SUCC_scenario( rem_cstsha, errCode, "", "retrieving remote %s" % MYCST )

    rem_cstsha_liv, errCode = remote_h.ref2sha( MYCST_LIV )
    self.util_check_DENY_scenario( rem_cstsha_liv, errCode, "", "retrieving local %s" % MYCST_LIV )


  def test_Push_09_00_MoreRemotes( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "clone" )

    if not modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.remote_add( ORIG_REPO_AREMOTE_NAME, ORIG_REPO_AREMOTE_URL )
      self.util_check_SUCC_scenario( out, errCode, "", "add remote" )

    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_SUCC_scenario( out, errCode, "", "pull" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.swgitUtil_Clone_.push_with_merge( remote = ORIG_REPO_AREMOTE_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "push" )

    for r in ( self.CREATED_BR, self.CREATED_BR_DEV, self.CREATED_BR_FIX, self.CREATED_BR_NEWBR ):
      self.assertEqual( self.swgitUtil_Clone_.ref2sha( r )[1], 0, "get sha %s" % r )
      self.assertEqual( self.sw_aremoterepo_h.ref2sha( r )[1], 0, "get sha %s" % r )
      self.assertEqual( self.sw_origrepo_h.ref2sha( r )[1]   , 1, "get sha %s" % r )


  #
  # Test:
  #  push onto repo 1 a    new branch
  #  push onto repo 2 same new branch
  #  re-push onto repo 1, but now remote branch exists but is NOT correctly tracked
  #
  # Result:
  #  everithing works because pull --all will be satisfied from tracked branch.
  #
  # Note:
  #  Behaviour here is ok.
  #  We were looking for crashing push. It could happen only when we 
  #  push with an integartion branch remote but not tracked, and this should not possible
  #  Next test will force it manually.
  #
  def test_Push_09_01_MoreRemotes_CrossPush( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "clone" )

    if not modetest_morerepos():
      out, errCode = self.swgitUtil_Clone_.remote_add( ORIG_REPO_AREMOTE_NAME, ORIG_REPO_AREMOTE_URL )
      self.util_check_SUCC_scenario( out, errCode, "", "add remote" )

    out, errCode = self.swgitUtil_Clone_.pull()
    self.util_check_SUCC_scenario( out, errCode, "", "pull" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )
    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "Setting INTEGRATION branch to", "set int br to just create file" )
    out, errCode = self.swgitUtil_Clone_.push_with_merge( remote = "origin" )
    self.util_check_SUCC_scenario( out, errCode, "", "push to origin" )
    out, errCode = self.swgitUtil_Clone_.push_with_merge( remote = ORIG_REPO_AREMOTE_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "push to remote" )

    out, errCode = self.swgitUtil_Clone_.modify_repo( ORIG_REPO_aFILE, "ddd", gotoint = False )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.push_with_merge( remote = "origin" )
    self.util_check_SUCC_scenario( out, errCode, "", "push to origin" )


  def test_Push_09_02_Remote_track_new_intbr( self ):
    out, errCode = swgit__utils.clone_scripts_repo( self.PUSH_CLONE_DIR )
    self.util_check_SUCC_scenario( out, errCode, "", "clone" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.int_branch_set( self.BRANCH_NAME )
    self.util_check_SUCC_scenario( out, errCode, "Setting INTEGRATION branch to", "set int br to just create file" )

    out, errCode = self.swgitUtil_Clone_.branch_create( self.BRANCH_NAME_SS )
    self.util_check_SUCC_scenario( out, errCode, "", "create branch" )
    out, errCode = self.swgitUtil_Clone_.modify_file( ORIG_REPO_aFILE, "ccc" )
    self.util_check_SUCC_scenario( out, errCode, "", "modify file" )
    out, errCode = self.swgitUtil_Clone_.commit_minusA_dev_fix( self.DDTS )
    self.util_check_SUCC_scenario( out, errCode, "", "commmit" )

    out, errCode = self.swgitUtil_Clone_.branch_list_track()
    self.assertTrue( self.CREATED_BR not in out, "Must be untracked branch" )

    # first push will track
    #########################################################
    out, errCode = self.swgitUtil_Clone_.push_with_merge( "origin" )
    self.util_check_SUCC_scenario( out, errCode, "", "push to origin" )
    #########################################################

    out, errCode = self.swgitUtil_Clone_.branch_list_track()
    self.assertTrue( self.CREATED_BR in out, "Must be tracked branch" )

    #must be possible pushing because intbr has just been tracked
    # Once there was this error (because not right tracked branch)
    #		Fetching tags only, you probably meant:
		#   git fetch --tags
    out, errCode = self.swgitUtil_Clone_.push_with_merge( "origin" )
    self.util_check_SUCC_scenario( out, errCode, "", "push to origin" )

    #manually untrack branch
    out, errCode = self.swgitUtil_Clone_.system_unix( "git config  --unset branch.%s.merge" % self.CREATED_BR )
    
    out, errCode = self.swgitUtil_Clone_.branch_list_track()
    self.assertTrue( self.CREATED_BR not in out, "Must be untracked branch" )

    #########################################################
    out, errCode = self.swgitUtil_Clone_.push_with_merge( "origin" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Your current integration branch remotely exists but is not tracked.", 
                                   "push to origin" )
    #########################################################

    out, errCode = self.swgitUtil_Clone_.branch_track( "origin/%s" % self.CREATED_BR )
    self.util_check_SUCC_scenario( out, errCode, "", "track branch" )

    out, errCode = self.swgitUtil_Clone_.branch_list_track()
    self.assertTrue( self.CREATED_BR in out, "Must be tracked branch" )

    #########################################################
    out, errCode = self.swgitUtil_Clone_.push_with_merge( "origin" )
    self.util_check_SUCC_scenario( out, errCode, "", "push to origin" )
    #########################################################


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()
