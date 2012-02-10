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
from test_proj_util import *

import copy

from _utils import *
from _git__utils import *
from _swgit__utils import *

class Test_Proj( Test_ProjBase ):
  REPO_PROJ_ABC_ORIGIN_DIR = SANDBOX + "TEST_PROJ_ABC_ORIGIN"
  REPO_PROJ_ABC_ORIGIN_URL = "%s%s" % ( TESTER_SSHACCESS, REPO_PROJ_ABC_ORIGIN_DIR )
  REPO_PROJ_ABC_ORIGIN_MAP = SANDBOX + "TEST_PROJ_ABC_ORIGIN" + "/" + PROJMAP
  REPO_PROJ_ABC_CLONE_DIR  = SANDBOX + "TEST_PROJ_ABC_CLONE"
  REPO_PROJ_ABC_CLONE_MAP  = SANDBOX + "TEST_PROJ_ABC_CLONE" + "/" + PROJMAP

  LABEL_NEW = "%s/%s/%s/MYLBL/A_DUMMY_LABEL" % ( REPOS_INFOS[0][1],  REPOS_INFOS[0][2], TEST_USER )

  MOD_BRANCH = "MODIFY_PROJ_BR"
  BR_CONFLICT_1 = "BR_CONF_1"
  BR_CONFLICT_2 = "BR_CONF_2"
  REPO_PROJ_A_CLONE_DIR      = REPO_A + "_CLONE"
  REPO_PROJ_B_CLONE_DIR      = REPO_B + "_CLONE"
  REPO_PROJ_C_CLONE_DIR      = REPO_C + "_CLONE"
  REPO_PROJ_S_CLONE_DIR      = REPO_S + "_CLONE"

  REPO_PROJ_ABC_A_CLONE_DIR      = REPO_PROJ_ABC_CLONE_DIR + "/" + MAP_INFOS[0][0]
  REPO_PROJ_ABC_B_CLONE_DIR      = REPO_PROJ_ABC_CLONE_DIR + "/" + MAP_INFOS[1][0]
  REPO_PROJ_ABC_C_CLONE_DIR      = REPO_PROJ_ABC_CLONE_DIR + "/" + MAP_INFOS[2][0]
  REPO_PROJ_ABC_S_CLONE_DIR      = REPO_PROJ_ABC_CLONE_DIR + "/" + MAP_INFOS[3][0]

  ALL_REPOS_2 = ( REPO_A, REPO_B, REPO_C, REPO_S, REPO_PROJ_ABC_ORIGIN_DIR, REPO_PROJ_ABC_CLONE_DIR, REPO_PROJ_A_CLONE_DIR, REPO_PROJ_B_CLONE_DIR, REPO_PROJ_C_CLONE_DIR, REPO_PROJ_S_CLONE_DIR  )

  #This method is executed before each test_*
  def setUp( self ):
    super( Test_Proj, self ).setUp()

    for r in self.ALL_REPOS_2:
      shutil.rmtree( r, True ) #ignore errors

    self.swgitUtil_A       = swgit__utils( REPO_A )
    self.gitUtil_A         = git__utils( REPO_A )
    self.swgitUtil_B       = swgit__utils( REPO_B )
    self.gitUtil_B         = git__utils( REPO_B )
    self.swgitUtil_C       = swgit__utils( REPO_C )
    self.gitUtil_C         = git__utils( REPO_C )
    self.swgitUtil_ABC_ORI = swgit__utils( self.REPO_PROJ_ABC_ORIGIN_DIR )
    self.gitUtil_ABC_ORI   = git__utils( self.REPO_PROJ_ABC_ORIGIN_DIR )
    self.swgitUtil_ABC_CLO = swgit__utils( self.REPO_PROJ_ABC_CLONE_DIR )
    self.gitUtil_ABC_CLO   = git__utils( self.REPO_PROJ_ABC_CLONE_DIR )

    self.swgitUtil_A_CLO   = swgit__utils( self.REPO_PROJ_A_CLONE_DIR )
    self.gitUtil_A_CLO     = git__utils( self.REPO_PROJ_A_CLONE_DIR )
    self.swgitUtil_B_CLO   = swgit__utils( self.REPO_PROJ_B_CLONE_DIR )
    self.gitUtil_B_CLO     = git__utils( self.REPO_PROJ_B_CLONE_DIR )
    self.swgitUtil_C_CLO   = swgit__utils( self.REPO_PROJ_C_CLONE_DIR )
    self.gitUtil_C_CLO     = git__utils( self.REPO_PROJ_C_CLONE_DIR )

    self.swgitUtil_ABC_A_CLO   = swgit__utils( self.REPO_PROJ_ABC_A_CLONE_DIR )
    self.gitUtil_ABC_A_CLO     = git__utils( self.REPO_PROJ_ABC_A_CLONE_DIR )
    self.swgitUtil_ABC_B_CLO   = swgit__utils( self.REPO_PROJ_ABC_B_CLONE_DIR )
    self.gitUtil_ABC_B_CLO     = git__utils( self.REPO_PROJ_ABC_B_CLONE_DIR )
    self.swgitUtil_ABC_C_CLO   = swgit__utils( self.REPO_PROJ_ABC_C_CLONE_DIR )
    self.gitUtil_ABC_C_CLO     = git__utils( self.REPO_PROJ_ABC_C_CLONE_DIR )
    self.swgitUtil_ABC_S_CLO   = swgit__utils( self.REPO_PROJ_ABC_S_CLONE_DIR )
    self.gitUtil_ABC_S_CLO     = git__utils( self.REPO_PROJ_ABC_S_CLONE_DIR )


  #This method is executed after each test_*
  def tearDown( self ):
    #print  "tearDown"
    super( Test_Proj, self ).tearDown()
    pass
  

  def util_createrepos_cloneproj_createBr( self ):
    #create ORIG
    swgit__utils.create_default_repos( )
    out, errCode = self.swgitUtil_ABC_ORI.proj_create()
    self.assertEqual( errCode, 0, "FAILED create repo for project %s - \n%s\n" % ( self.REPO_PROJ_ABC_ORIGIN_DIR, out) )

    #clone the empty origin proj
    swgit__utils.clone_repo_url( self.REPO_PROJ_ABC_ORIGIN_URL, self.REPO_PROJ_ABC_CLONE_DIR, TEST_REPO_BR_DEV )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s ) FAILED - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, self.REPO_PROJ_ABC_CLONE_DIR, out) )

    # direcotries
    self.assertTrue( os.path.exists( self.REPO_PROJ_ABC_CLONE_DIR ), "not created directory %s" % self.REPO_PROJ_ABC_CLONE_DIR )

    #create branch
    out, errCode = self.swgitUtil_ABC_CLO.branch_create( self.MOD_BRANCH )
    self.assertEqual( errCode, 0, "FAILED creating branch for adding repo to proj %s - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out) )

  def util_createrepos_cloneproj_createBr_addentry_commit_push( self, entrylist ):
    self.util_createrepos_cloneproj_createBr()

    for e in entrylist:

      out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ e ] )
      self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % \
                        ( e, self.REPO_PROJ_ABC_CLONE_DIR, out ) )

      out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = e[0] )
      self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                        ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )




  def test_Proj_00_00_CreateProj( self ):

    #create REPOS that will build the project
    swgit__utils.create_default_repos( )

    #create PROJECT MAP
    out, errCode = self.swgitUtil_ABC_ORI.proj_create()
    self.assertEqual( errCode, 0, "FAILED create poject %s - \n%s\n" % ( self.REPO_PROJ_ABC_ORIGIN_DIR, out) )

    #general checks ( dir exists, map exists, .gitignore exists)
    out, errCode = self.swgitUtil_ABC_ORI.proj_check_dir_is_proj( checkmappresence = False )
    self.assertEqual( errCode, 0, "Project not craeted correctly %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )


  def test_Proj_01_00_AddOneEntry_DEVRepo_onOrigin( self ):

    #create REPOS that will build the project
    swgit__utils.create_default_repos( )

    #create PROJECT MAP
    out, errCode = self.swgitUtil_ABC_ORI.proj_create()
    self.assertEqual( errCode, 0, "FAILED create repo for project %s - \n%s\n" % ( self.REPO_PROJ_ABC_ORIGIN_DIR, out) )

    #create branch, fails on origin
    out, errCode = self.swgitUtil_ABC_ORI.branch_create( self.MOD_BRANCH )
    self.assertEqual( errCode, 1, "MUST FAIL creating branch on origin without INT branch set %s - \n%s\n" % ( self.REPO_PROJ_ABC_ORIGIN_DIR, out) )

    #set int branch and re-try create branch
    out, errCode = self.swgitUtil_ABC_ORI.int_branch_set( ORIG_REPO_DEVEL_BRANCH )
    self.assertEqual( errCode, 0, "FAILED setting INT br %s on origin (repo %s) - \n%s\n" % ( ORIG_REPO_DEVEL_BRANCH, self.REPO_PROJ_ABC_ORIGIN_DIR, out) )

    #create branch
    out, errCode = self.swgitUtil_ABC_ORI.branch_create_src( self.MOD_BRANCH, ORIG_REPO_DEVEL_BRANCH )
    self.assertEqual( errCode, 0, "FAILED creating branch for adding repo to proj %s - \n%s\n" % ( self.REPO_PROJ_ABC_ORIGIN_DIR, out) )


    #add one entry
    out, errCode = self.swgitUtil_ABC_ORI.proj_add( [ MAP_INFOS[0] ] )
    self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )


    out, errCode = self.swgitUtil_ABC_ORI.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )


    #check map values, by unix (grep ... )
    out, errCode = self.swgitUtil_ABC_ORI.proj_check_map_unix( MAP_INFOS[0] )
    self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )



  def test_Proj_01_01_AddOneEntry_DEVRepo_onClone( self ):
    self.util_createrepos_cloneproj_createBr()

    #add one entry
    out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ MAP_INFOS[0] ] )
    self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # check project is not damaged, every file is there
    #

    #general checks ( dir exists, map exists, .gitignore exists)
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj()
    self.assertEqual( errCode, 0, "Project %s has been damage while adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )

    #check map values, by unix (grep ... )
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_map_unix( MAP_INFOS[0] )
    self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # push
    #
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )



  def test_Proj_01_02_AddOneEntry_CSTRepo_OnClone( self ):
    self.util_createrepos_cloneproj_createBr()

    # create CST branch on A clone, starting from develop
    out, errCode = swgit__utils.clone_repo_url( MAP_INFOS[0][1], self.REPO_PROJ_A_CLONE_DIR, MAP_INFOS[0][2] )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s ) FAILED - \n%s\n" % \
                      ( MAP_INFOS[0][1], self.REPO_PROJ_A_CLONE_DIR, out) )

    out, errCode = self.swgitUtil_A_CLO.init_cst( MAP_INFOS[0][2], CST_BRANCH_NAME, CST_BRANCH_REL )
    self.assertEqual( errCode, 0, "FAILED creating CST branch %s starting from %s into proj %s - \n%s\n" % \
                      ( CST_BRANCH_NAME,  MAP_INFOS[0][2], self.REPO_PROJ_ABC_CLONE_DIR, out) )
    out, errCode = self.gitUtil_A_CLO.branch_exists( CST_BRANCH_FULLNAME )
    self.assertEqual( errCode, 0, "FAILED creating CST branch %s into proj %s - \n%s\n" % \
                      ( CST_BRANCH_FULLNAME, REPO_A, out) )

    # no more need to push
    #out, errCode = self.swgitUtil_A_CLO.commit_minusA_dev_repolist( repolist = self.REPO_PROJ_ABC_A_CLONE_DIR )
    #self.assertNotEqual( errCode, 0, "MUST FAIL commit with --repo-list, for proj: %s - \n%s\n" % \
    #                     ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    # push branch CST
    out, errCode = self.swgitUtil_A_CLO.push()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    # add one entry
    Arepo_info_with_cst = copy.deepcopy( MAP_INFOS[0] )
    Arepo_info_with_cst[2] = CST_BRANCH_FULLNAME

    out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ Arepo_info_with_cst ] )
    self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s with CST %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_CLONE_DIR, CST_BRANCH_FULLNAME, out ) )

    #
    # check project is not damaged, every file is there
    #

    #general checks ( dir exists, map exists, .gitignore exists)
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj()
    self.assertEqual( errCode, 0, "Project %s has been damage while adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )

    #check map values, by unix (grep ... )
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_map_unix( Arepo_info_with_cst )
    self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                      ( Arepo_info_with_cst, self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # commit must be done with --repo-list
    #
    out, errCode = self.swgitUtil_ABC_CLO.commit()
    self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # push
    #
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )




  def test_Proj_01_03_AddManyEntries( self ):
    self.util_createrepos_cloneproj_createBr()

    #add entries
    for m in MAP_INFOS:

      #add one entry
      out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ m ] )
      self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % \
                        ( m, self.REPO_PROJ_ABC_CLONE_DIR, out ) )

      #
      # check project is not damaged, every file is there
      #

      #general checks ( dir exists, map exists, .gitignore exists)
      out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj()
      self.assertEqual( errCode, 0, "Project %s has been damage while adding section %s - \n%s\n" % \
                        ( self.REPO_PROJ_ABC_CLONE_DIR, m, out ) )

      #check map values, by unix (grep ... )
      out, errCode = self.swgitUtil_ABC_CLO.proj_check_map_unix( m )
      self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                        ( m, self.REPO_PROJ_ABC_CLONE_DIR, out ) )

      #
      # commit must be done with --repo-list
      #
      out, errCode = self.swgitUtil_ABC_CLO.commit()
      self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
                        ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

      out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = m[0] )
      self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                        ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # push
    #
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )



  def test_Proj_01_04_AddEntry_reAddSameEntry( self ):
    self.util_createrepos_cloneproj_createBr()

    #add one entry
    out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ MAP_INFOS[0] ] )
    self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % ( MAP_INFOS[0], self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )

    #re-add same entry
    out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ MAP_INFOS[0] ] )
    self.assertNotEqual( errCode, 0, "MUST FAIL editing repo before committing into project %s - \n%s\n" % \
                         ( self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )


    #
    # check project is not damaged, every file is there
    #

    #general checks ( dir exists, map exists, .gitignore exists)
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj()
    self.assertEqual( errCode, 0, "Project %s has been damage while adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )

    #check map values, by unix (grep ... )
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_map_unix( MAP_INFOS[0] )
    self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # commit must be done with --repo-list
    #
    out, errCode = self.swgitUtil_ABC_CLO.commit()
    self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    # push
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # re-add same entry after committing
    #
    out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ MAP_INFOS[0] ] )
    self.assertNotEqual( errCode, 0, "MUST FAIL editing repo before committing into project %s - \n%s\n" % \
                         ( self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )

    #
    # check project is not damaged, every file is there
    #

    #general checks ( dir exists, map exists, .gitignore exists)
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj()
    self.assertEqual( errCode, 0, "Project %s has been damage while adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )

    #check map values, by unix (grep ... )
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_map_unix( MAP_INFOS[0] )
    self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                      ( MAP_INFOS[0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # commit must be done with --repo-list
    #
    out, errCode = self.swgitUtil_ABC_CLO.commit()
    self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.assertNotEqual( errCode, 0, "MUST FAIL commit with --repo-list of re-added section, for proj: %s - \n%s\n" % \
                         ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )



  def test_Proj_01_05_AddOneEntry_WrongsParams( self ):
    self.util_createrepos_cloneproj_createBr()

    # User cannot be tested because ssh generation is interactive
    #wronguser = copy.deepcopy( MAP_INFOS[0] )
    #wronguser[1] = "ssh://%s@%s%s" % (ORIG_REPO_GITUSER + "_NOTEXISTS", TEST_ADDR, REPO_A)

    wrongaddr = copy.deepcopy( MAP_INFOS[0] )
    wrongaddr[1] = "%s%s" % (TESTER_SSHACCESS + ".1", REPO_A)

    wrongpath = copy.deepcopy( MAP_INFOS[0] )
    wrongpath[1] = "%s%s" % (TESTER_SSHACCESS, REPO_A + "PATHNOTEXISTS" )

    wrongbranch = copy.deepcopy( MAP_INFOS[0] )
    wrongbranch[2] = wrongbranch[2] + "_BRANHCNOTEXISTS"

    #wrongchk = copy.deepcopy( MAP_INFOS[0] )
    #wrongchk[4] = "CHKNOTEXISTING"

    wrongs = [ wrongaddr, wrongpath, wrongbranch ]

    for w in wrongs:

      #add a wring
      out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ w ] )
      self.assertNotEqual( errCode, 0, "MUST FAIL adding repo %s to project %s - \n%s\n" % \
                           ( w, self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )

      #general checks ( dir exists, map exists, .gitignore exists)
      out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj( checkmappresence = False )
      self.assertEqual( errCode, 0, "Project not craeted correctly %s - \n%s\n" % \
                        ( self.REPO_PROJ_ABC_ORIGIN_DIR, out ) )

      # just proj create => map must be empty, .git must not exist
      self.assertFalse( os.path.exists( self.REPO_PROJ_ABC_ORIGIN_MAP ), \
                       "MUST NOT EXIST project file %s - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_MAP, out) )



  def test_Proj_02_00_DelFirstEntry_withRMcommand( self ):
    self.util_createrepos_cloneproj_createBr_addentry_commit_push( [ MAP_INFOS[0] ] )

    #del that entry
    shutil.rmtree( self.REPO_PROJ_ABC_A_CLONE_DIR, True ) #ignore errors

    #check project is not damaged, every file is there
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj( checkmappresence = False )
    self.assertEqual( errCode, 0, "Project %s has been damage while re-adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )

    #
    # commit must fail
    #
    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA()
    self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )


  def test_Proj_02_01_DelFirstEntry( self ):
    self.util_createrepos_cloneproj_createBr_addentry_commit_push( [ MAP_INFOS[0] ] )

    #del that entry
    out, errCode = self.swgitUtil_ABC_CLO.proj_del( MAP_INFOS[0][0] )
    self.assertEqual( errCode, 0, "FAILED deleting repo %s from project %s - \n%s\n" % ( MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #check project is not damaged, every file is there
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj( checkmappresence = False )
    self.assertEqual( errCode, 0, "Project %s has been damage while re-adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )

    #check map returned empty
    self.assertEqual( os.stat( self.REPO_PROJ_ABC_CLONE_MAP )[6], 0, \
                      "FAILED - Map %s, MUST BE empty - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_MAP, out) )
    val, errCode = get_cfg( "submodule.%s.url" % MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR )
    self.assertNotEqual( errCode, 0, \
                         "MUST FAIL retrieving option %s into proj %s - \n%s\n" % ( "submodule.%s.url" % MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR, out) )

    self.assertEqual( self.swgitUtil_ABC_CLO.is_file_under_cc( MAP_INFOS[0][0] )[1], 1, \
        "MUST FAIL retrieving object type for obj: %s into proj %s - \n%s\n" % ( MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR, out) )

    #
    # commit shoild be done with --repo-list ... but no more repo configured ...
    #
    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = MAP_INFOS[0][0] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository", 
                                   "committing with repolist after deleting subrepo" )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA( msg = "deleted submodule" )
    self.util_check_SUCC_scenario( out, errCode, "", "committing without repolist after deleting subrepo" )

    # push
    out, errCode = self.swgitUtil_ABC_CLO.tag_dev( "modif - cappa inside DEVTDM" )
    self.util_check_SUCC_scenario( out, errCode, "", "tagging DEV to push" )
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )



  def test_Proj_02_02_Add_Del_Entries( self ):

    self.util_createrepos_cloneproj_createBr_addentry_commit_push( [ MAP_INFOS[0], MAP_INFOS[1] ] )

    #del first entry
    out, errCode = self.swgitUtil_ABC_CLO.proj_del( MAP_INFOS[0][0] )
    self.assertEqual( errCode, 0, "FAILED deleting repo %s from project %s - \n%s\n" % ( MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # check project is not damaged, every file is there
    #
    #general checks ( dir exists, map exists, .gitignore exists)
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj()
    self.assertEqual( errCode, 0, "Project %s has been damage while adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[0], out ) )
    #check map values, by unix (grep ... )
    #  B must be present
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_map_unix( MAP_INFOS[1] )
    self.assertEqual( errCode, 0, "FAILED Worng values into map entry %s, for proj: %s - \n%s\n" % \
                      ( MAP_INFOS[1], self.REPO_PROJ_ABC_CLONE_DIR, out ) )


    # A must be deleted
    #map must exists
    self.assertTrue( os.path.exists( self.REPO_PROJ_ABC_CLONE_MAP ), \
                      "FAILED - Map %s, MUST EXISTs - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_MAP, out) )

    # cfg must be cleaned
    val, errCode = get_cfg( "submodule.%s.url" % MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR )
    self.assertNotEqual( errCode, 0, \
                         "MUST FAIL retrieving option %s into proj %s - \n%s\n" % ( "submodule.%s.url" % MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR, out) )

    # directory A must be no more under CC
    self.assertEqual( self.swgitUtil_ABC_CLO.is_file_under_cc( MAP_INFOS[0][0] )[1], 1, \
        "MUST FAIL retrieving object type for obj: %s into proj %s - \n%s\n" % ( MAP_INFOS[0][0], self.REPO_PROJ_ABC_CLONE_DIR, out) )



    #
    # commit must be done with --repo-list ...
    #
    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev()
    #self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
    #                  ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )
    self.assertEqual( errCode, 0, "FAILED commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    # push
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #
    # now clean also B repo
    #
    out, errCode = self.swgitUtil_ABC_CLO.proj_del( MAP_INFOS[1][0] )
    self.assertEqual( errCode, 0, "FAILED deleting repo %s from project %s - \n%s\n" % ( MAP_INFOS[1][0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #check project is not damaged, every file is there
    out, errCode = self.swgitUtil_ABC_CLO.proj_check_dir_is_proj( checkmappresence = False )
    self.assertEqual( errCode, 0, "Project %s has been damage while re-adding section %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, MAP_INFOS[1], out ) )

    #check map returned empty
    self.assertEqual( os.stat( self.REPO_PROJ_ABC_CLONE_MAP )[6], 0, \
                      "FAILED - Map %s, MUST BE empty - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_MAP, out) )
    val, errCode = get_cfg( "submodule.%s.url" % MAP_INFOS[1][0], self.REPO_PROJ_ABC_CLONE_DIR )
    self.assertNotEqual( errCode, 0, \
                         "MUST FAIL retrieving option %s into proj %s - \n%s\n" % ( "submodule.%s.url" % MAP_INFOS[1][0], self.REPO_PROJ_ABC_CLONE_DIR, out) )

    self.assertEqual( self.swgitUtil_ABC_CLO.is_file_under_cc( MAP_INFOS[1][0] )[1], 1, \
        "MUST FAIL retrieving object type for obj: %s into proj %s - \n%s\n" % ( MAP_INFOS[1][0], self.REPO_PROJ_ABC_CLONE_DIR, out) )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev()
    #self.assertNotEqual( errCode, 0, "MUST FAIL commit without --repo-list, for proj: %s - \n%s\n" % \
    #                  ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )
    self.assertEqual( errCode, 0, "FAILED commit without --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    # push
    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )


  def test_Proj_03_00_Commit_morerepos_listed1by1( self ):

    self.util_createrepos_cloneproj_createBr_addentry_commit_push( [ MAP_INFOS[0], MAP_INFOS[1] ] )

    #modif A
    sha_A_before, errCode = self.swgitUtil_ABC_A_CLO.get_currsha()
    self.swgitUtil_ABC_A_CLO.modify_repo( filename = REPOS_INFOS[0][4], msg = "modify file into repo A" )
    sha_A_after, errCode = self.swgitUtil_ABC_A_CLO.get_currsha()

    #modif B
    sha_B_before, errCode = self.swgitUtil_ABC_B_CLO.get_currsha()
    self.swgitUtil_ABC_B_CLO.modify_repo( filename = REPOS_INFOS[1][4], msg = "modify file into repo B" )
    sha_B_after, errCode = self.swgitUtil_ABC_B_CLO.get_currsha()

    #into proj, go on int, commit both repos
    out, errCode = self.swgitUtil_ABC_CLO.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch to int" ) 

    sha_ABC_before, errCode = self.swgitUtil_ABC_CLO.get_currsha()
    repolist = "%s %s_notexists" % ( MAP_INFOS[0][0], MAP_INFOS[1][0] )
    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_repolist( msg="committing multiple repos", repolist = repolist  )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit with not existing repository on command line" ) 
    sha_ABC_after, errCode = self.swgitUtil_ABC_CLO.get_currsha()
    self.assertEqual( sha_ABC_before, sha_ABC_after, "MUST BE EQUAL sha before and after failed commit - \n%s\n%s\n" % (sha_ABC_before, sha_ABC_after) )

    repolist = "%s ./%s/" % ( MAP_INFOS[0][0], MAP_INFOS[1][0] )
    out, errCode = self.swgitUtil_ABC_CLO.commit_repolist( msg="committing multiple repos", repolist = repolist  )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED committing all" ) 
    sha_ABC_after, errCode = self.swgitUtil_ABC_CLO.get_currsha()

    #into proj, check shas
    self.assertNotEqual( sha_ABC_before, sha_ABC_after, "MUST BE DIFFERENT sha before and after successful commit - \n%s\n%s\n" % (sha_ABC_before, sha_ABC_after) )

    sha_repochk_A_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[0][0] )
    sha_repochk_B_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[1][0] )
    self.assertEqual( sha_A_after, sha_repochk_A_after, "MUST BE EQUAL sha repo A and references sha inside proj for A - \n%s\n%s\n" % (sha_A_after, sha_repochk_A_after) )
    self.assertEqual( sha_B_after, sha_repochk_B_after, "MUST BE EQUAL sha repo B and references sha inside proj for B - \n%s\n%s\n" % (sha_B_after, sha_repochk_B_after) )


  def test_Proj_03_01_Commit_morerepos_withminusA( self ):

    self.util_createrepos_cloneproj_createBr_addentry_commit_push( [ MAP_INFOS[0], MAP_INFOS[1] ] )

    #modif A
    sha_A_before, errCode = self.swgitUtil_ABC_A_CLO.get_currsha()
    self.swgitUtil_ABC_A_CLO.modify_repo( filename = REPOS_INFOS[0][4], msg = "modify file into repo A" )
    sha_A_after, errCode = self.swgitUtil_ABC_A_CLO.get_currsha()

    #modif B
    sha_B_before, errCode = self.swgitUtil_ABC_B_CLO.get_currsha()
    self.swgitUtil_ABC_B_CLO.modify_repo( filename = REPOS_INFOS[1][4], msg = "modify file into repo B" )
    sha_B_after, errCode = self.swgitUtil_ABC_B_CLO.get_currsha()

    #into proj, go on int, commit both repos
    out, errCode = self.swgitUtil_ABC_CLO.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch to int" ) 

    sha_ABC_before, errCode = self.swgitUtil_ABC_CLO.get_currsha()

    repolist = "-A"
    out, errCode = self.swgitUtil_ABC_CLO.commit_repolist( msg="committing multiple repos", repolist = repolist  )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED committing all" ) 
    sha_ABC_after, errCode = self.swgitUtil_ABC_CLO.get_currsha()

    #into proj, check shas
    self.assertNotEqual( sha_ABC_before, sha_ABC_after, "MUST BE DIFFERENT sha before and after successful commit - \n%s\n%s\n" % (sha_ABC_before, sha_ABC_after) )

    sha_repochk_A_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[0][0] )
    sha_repochk_B_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[1][0] )
    self.assertEqual( sha_A_after, sha_repochk_A_after, "MUST BE EQUAL sha repo A and references sha inside proj for A - \n%s\n%s\n" % (sha_A_after, sha_repochk_A_after) )
    self.assertEqual( sha_B_after, sha_repochk_B_after, "MUST BE EQUAL sha repo B and references sha inside proj for B - \n%s\n%s\n" % (sha_B_after, sha_repochk_B_after) )


  def test_Proj_03_02_Commit_morerepos_withminusA_withsnap( self ):

    self.util_createrepos_cloneproj_createBr_addentry_commit_push( [ MAP_INFOS[0], MAP_INFOS[1], MAP_INFOS[3] ] )

    #out, errCode = swgit__utils.create_default_proj_repos()
    #self.util_check_SUCC_scenario( out, errCode, "", "FAILED creating default repos" ) 
    #out, errCode = self.swgitUtil_ABC_A_CLO.proj_add_snapshot( [ SNAP_BI ] )
    #self.util_check_SUCC_scenario( out, errCode, "", "FAILED adding snap repo" ) 


    #modif A
    sha_A_before, errCode = self.swgitUtil_ABC_A_CLO.get_currsha()
    self.swgitUtil_ABC_A_CLO.modify_repo( filename = REPOS_INFOS[0][4], msg = "modify file into repo A" )
    sha_A_after, errCode = self.swgitUtil_ABC_A_CLO.get_currsha()

    #modif B
    sha_B_before, errCode = self.swgitUtil_ABC_B_CLO.get_currsha()
    self.swgitUtil_ABC_B_CLO.modify_repo( filename = REPOS_INFOS[1][4], msg = "modify file into repo B" )
    sha_B_after, errCode = self.swgitUtil_ABC_B_CLO.get_currsha()

    #do not modif S
    sha_S, errCode = self.swgitUtil_ABC_S_CLO.get_currsha()

    #into proj, go on int, commit both repos
    out, errCode = self.swgitUtil_ABC_CLO.branch_switch_to_int()
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED switch to int" ) 

    sha_ABC_before, errCode = self.swgitUtil_ABC_CLO.get_currsha()

    repolist = "-A"
    out, errCode = self.swgitUtil_ABC_CLO.commit_repolist( msg="committing multiple repos", repolist = repolist  )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED committing all" ) 
    sha_ABC_after, errCode = self.swgitUtil_ABC_CLO.get_currsha()

    #into proj, check shas
    self.assertNotEqual( sha_ABC_before, sha_ABC_after, "MUST BE DIFFERENT sha before and after successful commit - \n%s\n%s\n" % (sha_ABC_before, sha_ABC_after) )

    sha_repochk_A_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[0][0] )
    sha_repochk_B_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[1][0] )
    sha_repochk_S_after, errCode = self.swgitUtil_ABC_CLO.proj_getrepo_chk( MAP_INFOS[3][0] )
    self.assertEqual( sha_A_after, sha_repochk_A_after, "MUST BE EQUAL sha repo A and references sha inside proj for A - \n%s\n%s\n" % (sha_A_after, sha_repochk_A_after) )
    self.assertEqual( sha_B_after, sha_repochk_B_after, "MUST BE EQUAL sha repo B and references sha inside proj for B - \n%s\n%s\n" % (sha_B_after, sha_repochk_B_after) )
    self.assertEqual( sha_S, sha_repochk_S_after, "MUST BE EQUAL sha repo S and references sha inside proj for S - \n%s\n%s\n" % (sha_S, sha_repochk_S_after) )


  def test_Proj_03_03_Commit_nothingmod( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #############
    #nothing mod
    #############
    out, errCode = clo2_hm["TSS100"].commit( msg = "no mod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit no-changes" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "no mod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit no-changes with -a" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "no mod", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit no-changes with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "no mod", repolist = tss100_name2path( "DEVTDM" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit no-changes with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "no mod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit no-changes with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "no mod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit no-changes with -a and -A" )

  def test_Proj_03_04_Commit_submod_dirty( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #################
    #only submod mod
    #################
    out, errCode = clo2_hm["DEVTDM"].modify_file( tss100_name2file( "DEVTDM" ), msg = "modification" )

    out, errCode = clo2_hm["TSS100"].commit( msg = "only submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit dirty-submod" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "only submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit dirty-submod with -a" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "only submod", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit dirty-submod with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "only submod", repolist = tss100_name2path( "DEVTDM" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "but it is in a \"dirty\" state",
                                   "MUST FAIL commit dirty-submod with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "only submod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "but it is in a \"dirty\" state",
                                   "MUST FAIL commit dirty-submod with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "only submod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside local repository. Please remove -a option.",
                                   "MUST FAIL commit dirty-submod with -a and -A" )

  def test_Proj_03_05_Commit_submod_newcommits( self ):

    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #########################
    #only submod new-commits
    #########################
    out, errCode = clo2_hm["DEVTDM"].commit_minusA( msg = "new commits submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit directly on INTBR" )
    out, errCode = clo2_hm["DEVTDM"].modify_repo( tss100_name2file("DEVTDM"), msg = "new commits submod inside DEVTDM" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED git commit -a?" )


    out, errCode = clo2_hm["TSS100"].commit( msg = "new commits submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit new-commits-submod" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "new commits submod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit new-commits-submod with -a" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits submod", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-submod with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits submod", repolist = tss100_name2path( "DEVTDM" ) )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "FAILED commit new-commits-submod with reponame exisitng" )


    #another committed mod
    out, errCode = clo2_hm["DEVTDM"].modify_file( tss100_name2file( "DEVTDM" ), msg = "another modification" )
    out, errCode = clo2_hm["DEVTDM"].system_unix( "git commit -a -m \"new commits submod inside DEVTDM\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED git commit -a?" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits submod", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "FAILED commit new-commits-submod with -A" )

    #another committed mod
    out, errCode = clo2_hm["DEVTDM"].modify_file( tss100_name2file( "DEVTDM" ), msg = "another modification" )
    out, errCode = clo2_hm["DEVTDM"].system_unix( "git commit -a -m \"new commits submod inside DEVTDM\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED git commit -a?" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "new commits submod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside local repository. Please remove -a option.",
                                   "MUST FAIL commit new-commits-submod with -a and -A" )

    #and now commit to avoid dirty state in next tests
    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits submod", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "FAILED commit new-commits-submod with -A" )


  def test_Proj_03_06_Commit_sub_submod_newcommits( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )


    #####################
    #only sub-submod mod
    # modified content
    #####################
    out, errCode = clo2_hm["DEVFS"].modify_file( tss100_name2file( "DEVFS" ), msg = "modification inside sub sub repo" )
    out, errCode = clo2_hm["DEVFS"].commit_minusA( msg = "new commits sub sub repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot issue this command on integration branches",
                                   "MUST FAIL commit directly on INTBR" )
    out, errCode = clo2_hm["DEVFS"].system_unix( "git commit -a -m \"new commits sub sub repo inside DEVFS\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED git commit -a?" )



    out, errCode = clo2_hm["TSS100"].commit( msg = "new commits sub sub repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit new-commits-sub-sub-repo" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "new commits sub sub repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit new-commits-sub-sub-repo with -a" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits sub sub repo", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-sub-sub-repo with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits sub sub repo", repolist = tss100_name2path( "DEVPLAT" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "but it is in a \"dirty\" state.",
                                   "FAILED commit new-commits-sub-sub-repo with reponame exisitng" )


    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits sub sub repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "but it is in a \"dirty\" state.",
                                   "FAILED commit new-commits-sub-sub-repo with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "new commits sub sub repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please remove -a option.",
                                   "MUST FAIL commit new-commits-sub-sub-repo with -a and -A" )

    #and now commit PLAT and TSS100 to avoid dirty state in next tests
    out, errCode = clo2_hm["DEVPLAT"].commit_repolist( msg = "new commits sub sub repo", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "MUST FAIL commit new-commits-sub-sub-repo with -a and -A" )
    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commits sub sub repo", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "MUST FAIL commit new-commits-sub-sub-repo with -a and -A" )

  def test_Proj_03_07_Commit_onlyfile( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )


    ###############
    #only file mod
    ###############
    #create branch
    out, errCode = clo2_hm["TSS100"].branch_create( self.MOD_BRANCH )
    self.assertEqual( errCode, 0, "FAILED creating branch for adding repo to proj %s - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out) )

    out, errCode = clo2_hm["TSS100"].modify_file( tss100_name2file( "TSS100" ), msg = "modification" )


    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "no mod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please remove -A option.",
                                   "MUST FAIL commit no-changes with -a and -A" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "no mod", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit no-changes with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "no mod", repolist = "./" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository '.'",
                                   "MUST FAIL commit no-changes with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "no mod", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please remove -A option.",
                                   "MUST FAIL commit no-changes with -A" )

    out, errCode = clo2_hm["TSS100"].commit( msg = "no mod" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing added to the index. Try using -a option.",
                                   "MUST FAIL commit no-changes" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "no mod" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "MUST FAIL commit no-changes with -a" )


  def test_Proj_03_08_Commit_both_file_submod( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #
    #both mod and submod mod
    #
    out, errCode = clo2_hm["TSS100"].branch_create( self.MOD_BRANCH )
    out, errCode = clo2_hm["TSS100"].modify_file( tss100_name2file( "TSS100" ), msg = "modification" )
    out, errCode = clo2_hm["DEVPLAT"].modify_file( tss100_name2file( "DEVPLAT" ), msg = "modification" )
    out, errCode = clo2_hm["DEVPLAT"].system_unix( "git commit -a -m \"new commits submod inside DEVPLAT\"" )
    self.util_check_SUCC_scenario( out, errCode, "", "FAILED git commit -a?" )


    out, errCode = clo2_hm["TSS100"].commit( msg = "new commit and  mod file" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing added to the index. Try using -a option.",
                                   "MUST FAIL commit new-commits-and-mod-file" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commit and  mod file", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-and-mod-file with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commit and  mod file", repolist = tss100_name2path( "DEVPLAT" ) )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Without -a option these files will not commit:",
                              "FAILED commit new-commits-and-mod-file with reponame exisitng" )

    #make another modif
    out, errCode = clo2_hm["DEVPLAT"].modify_file( tss100_name2file( "DEVPLAT" ), msg = "modification" )
    out, errCode = clo2_hm["DEVPLAT"].system_unix( "git commit -a -m \"new commits submod inside DEVPLAT\"" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "new commit and  mod file", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Without -a option these files will not commit:",
                              "FAILED commit new-commits-and-mod-file with -A" )

    #make another modif
    out, errCode = clo2_hm["DEVPLAT"].modify_file( tss100_name2file( "DEVPLAT" ), msg = "modification" )
    out, errCode = clo2_hm["DEVPLAT"].system_unix( "git commit -a -m \"new commits submod inside DEVPLAT\"" )


    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "new commit and  mod file", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "MUST FAIL commit new-commits-and-mod-file with -a and -A" )

    #make another modif
    out, errCode = clo2_hm["DEVPLAT"].modify_file( tss100_name2file( "DEVPLAT" ), msg = "modification" )
    out, errCode = clo2_hm["DEVPLAT"].system_unix( "git commit -a -m \"new commits submod inside DEVPLAT\"" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "new commit and  mod file" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside local repository.",
                                   "MUST FAIL commit new-commits-and-mod-file with -a" )

    out, errCode = clo2_hm["TSS100"].modify_file( tss100_name2file( "TSS100" ), msg = "modification" )
    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "new commit and  mod file" )
    self.util_check_SUCC_scenario( out, errCode, 
                              "Committing your contributes",
                              "MUST FAIL commit new-commits-and-mod-file with -a" )


  def test_Proj_03_09_Commit_conflict_repo( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )


    ##########################
    #conflict present on repo
    ##########################

    #
    #both mod and submod mod
    #
    out, errCode = clo2_hm["TSS100"].branch_create( self.BR_CONFLICT_1 )
    fullbr_1, errCode = clo2_hm["TSS100"].current_branch()

    out, errCode = clo2_hm["TSS100"].branch_create_src( self.BR_CONFLICT_2, va_sha_map_clonetime["TSS100"] )

    out, errCode = clo2_hm["TSS100"].modify_file( tss100_name2file( "TSS100" ), msg = "2222222" )
    fullbr_2, errCode = clo2_hm["TSS100"].current_branch()
    out, errCode = clo2_hm["TSS100"].commit_minusA_dev( "commit 222" )

    out, errCode = clo2_hm["TSS100"].branch_switch_to_br( self.BR_CONFLICT_1 )
    out, errCode = clo2_hm["TSS100"].modify_file( tss100_name2file( "TSS100" ), msg = "1111111" )
    out, errCode = clo2_hm["TSS100"].commit_minusA_dev( "commit 111" )

    dev_1 = "%s/DEV/000" % fullbr_1
    dev_2 = "%s/DEV/000" % fullbr_2

    out, errCode = clo2_hm["TSS100"].merge_on_int( dev_1 )

    #this second merge will create the conflict
    out, errCode = clo2_hm["TSS100"].merge_on_int( dev_2 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You already are on your current integration branch,",
                                   "MUST FAIL second merge with conflict" )
    out, errCode = clo2_hm["TSS100"].merge( dev_2 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "CONFLICT (content):",
                                   "MUST FAIL second merge with conflict" )


    out, errCode = clo2_hm["TSS100"].commit( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on file",
                                   "MUST FAIL commit new-commits-and-mod-file" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-and-mod-file with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVPLAT" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed for submodule",
                                   "FAILED commit new-commits-and-mod-file with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside submodules.",
                                   "FAILED commit new-commits-and-mod-file with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside submodules.",
                                   "MUST FAIL commit new-commits-and-mod-file with -a and -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on file",
                                   "MUST FAIL commit new-commits-and-mod-file with -a" )




  def test_Proj_03_10_Commit_conflict_submod( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #############################
    #conflict present on submod
    #############################

    #
    #both mod and submod mod
    #
    #create br1
    out, errCode = clo2_hm["TSS100"].branch_create( self.BR_CONFLICT_1 )
    out, errCode = clo2_hm["DEVPLAT"].branch_create( self.BR_CONFLICT_1 )
    fulltssbr_1 , errCode = clo2_hm["TSS100"].current_branch()
    fullplatbr_1, errCode = clo2_hm["DEVPLAT"].current_branch()

    #create br2
    out, errCode = clo2_hm["TSS100"].branch_create_src( self.BR_CONFLICT_2, va_sha_map_clonetime["TSS100"] )
    out, errCode = clo2_hm["DEVPLAT"].branch_create_src( self.BR_CONFLICT_2, va_sha_map_clonetime["DEVPLAT"] )

    out, errCode = clo2_hm["DEVPLAT"].modify_file( tss100_name2file( "DEVPLAT" ), msg = "2222222" )
    out, errCode = clo2_hm["DEVPLAT"].commit_minusA( "plat 2222" )

    fulltssbr_2 , errCode = clo2_hm["TSS100"].current_branch()
    fullplatbr_2, errCode = clo2_hm["DEVPLAT"].current_branch()
    out, errCode = clo2_hm["TSS100"].commit_dev_repolist( msg = "commit 222", repolist = "-A" )

    #come back to br 1
    out, errCode = clo2_hm["TSS100"].branch_switch_to_br( self.BR_CONFLICT_1 )
    out, errCode = clo2_hm["DEVPLAT"].branch_switch_to_br( self.BR_CONFLICT_1 )

    out, errCode = clo2_hm["DEVPLAT"].modify_file( tss100_name2file( "DEVPLAT" ), msg = "1111111" )
    out, errCode = clo2_hm["DEVPLAT"].commit_minusA( "plat 111" )
    out, errCode = clo2_hm["TSS100"].commit_dev_repolist( msg = "commit 111", repolist = "-A" )

    dev_1 = "%s/DEV/000" % fulltssbr_1
    dev_2 = "%s/DEV/000" % fulltssbr_2

    out, errCode = clo2_hm["TSS100"].merge_on_int( dev_1 )

    #this second merge will create the conflict
    out, errCode = clo2_hm["TSS100"].merge_on_int( dev_2 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "You already are on your current integration branch, please remote -I option",
                                   "MUST FAIL second merge with conflict" )
    out, errCode = clo2_hm["TSS100"].merge( dev_2 )
    self.util_check_DENY_scenario( out, errCode, 
                                   "CONFLICT (submodule):",
                                   "MUST FAIL second merge with conflict" )


    out, errCode = clo2_hm["TSS100"].commit( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on repository(s):",
                                   "MUST FAIL commit new-commits-and-mod-file" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-and-mod-file with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVPLAT" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on repository",
                                   "FAILED commit new-commits-and-mod-file with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on repository",
                                   "FAILED commit new-commits-and-mod-file with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on repository(s):",
                                   "MUST FAIL commit new-commits-and-mod-file with -a and -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Conflicts found on repository(s):",
                                   "MUST FAIL commit new-commits-and-mod-file with -a" )

    # TO RESOLVE CONFLICTS YOU CAN:
    #
    # git submodule update --merge "DEVPLAT"
    # git commit "TSS100"
    #
    # in this way you merge br1 and br2
    # and after commit result merge
    #
    # or
    #
    # choose which solution you prefer (br1 or br2) inside submod
    # checkout it
    # git commit "TSS100"



  def test_Proj_03_11_Commit_rmfile( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #############################
    #conflict present on submod
    #############################

    #
    #both mod and submod mod
    #
    #create br1
    out, errCode = clo2_hm["TSS100"].branch_create( self.BR_CONFLICT_1 )
    out, errCode = clo2_hm["TSS100"].system_unix( "rm -f %s" % tss100_name2file( "TSS100" ) )


    out, errCode = clo2_hm["TSS100"].commit( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "MUST FAIL commit new-commits-and-mod-file" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-and-mod-file with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVPLAT" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "FAILED commit new-commits-and-mod-file with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside submodules.",
                                   "FAILED commit new-commits-and-mod-file with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside submodules.",
                                   "MUST FAIL commit new-commits-and-mod-file with -a and -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "MUST FAIL commit new-commits-and-mod-file with -a" )


  def test_Proj_03_12_Commit_rmfile_intosubmod( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #############################
    #conflict present on submod
    #############################

    out, errCode = clo2_hm["TSS100"].branch_create( self.BR_CONFLICT_1 )
    out, errCode = clo2_hm["TSS100"].system_unix( "rm -rf %s" % tss100_name2path( "DEVTDM" ) )


    out, errCode = clo2_hm["TSS100"].commit( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside local repository. But if you want to commit",
                                   "MUST FAIL commit new-commits-and-mod-file" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-and-mod-file with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVTDM" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted repository:",
                                   "FAILED commit new-commits-and-mod-file with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted repository:",
                                   "FAILED commit new-commits-and-mod-file with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside local repository",
                                   "MUST FAIL commit new-commits-and-mod-file with -a and -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed inside local repository.",
                                   "MUST FAIL commit new-commits-and-mod-file with -a" )


  def test_Proj_03_13_Commit_rmfile_local_and_intosubmod( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )

    clo2_hm   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    va_sha_map_clonetime = self.util_map2_currshas( clo2_hm )

    #############################
    #conflict present on submod
    #############################

    out, errCode = clo2_hm["TSS100"].branch_create( self.BR_CONFLICT_1 )
    out, errCode = clo2_hm["TSS100"].system_unix( "rm -f %s" % tss100_name2file( "TSS100" ) )
    out, errCode = clo2_hm["TSS100"].system_unix( "rm -rf %s" % tss100_name2path( "DEVTDM" ) )


    out, errCode = clo2_hm["TSS100"].commit( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "MUST FAIL commit new-commits-and-mod-file" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVFS" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository",
                                   "MUST FAIL commit new-commits-and-mod-file with reponame not existing" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = tss100_name2path( "DEVTDM" ) )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "FAILED commit new-commits-and-mod-file with reponame exisitng" )

    out, errCode = clo2_hm["TSS100"].commit_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "FAILED commit new-commits-and-mod-file with -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA_repolist( msg = "conflict into repo", repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "MUST FAIL commit new-commits-and-mod-file with -a and -A" )

    out, errCode = clo2_hm["TSS100"].commit_minusA( msg = "conflict into repo" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Found deleted file:",
                                   "MUST FAIL commit new-commits-and-mod-file with -a" )


  def test_Proj_04_01_Edit( self ):
    self.util_createrepos_cloneproj_createBr()

    Arepo_info_without_branch = copy.deepcopy( MAP_INFOS[0] )
    Arepo_info_without_branch[2] = ""

    #add without br
    out, errCode = self.swgitUtil_ABC_CLO.proj_add( [ Arepo_info_without_branch ] )
    self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % \
                      ( Arepo_info_without_branch[0], self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.system_unix( "cat %s/.swdir/cfg/default_int_branches.cfg" % self.swgitUtil_ABC_CLO.getDir() )
    self.assertEqual( len( out ), 0, "FAILED adding repo without branch" )

    #edit def int br
    out, errCode = self.swgitUtil_ABC_CLO.proj_edit( "NOT_EXIST_REPO", "NOT_EXISTING_BR" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Not existing repository", 
                                   "Editing def-int-br" )

    out, errCode = self.swgitUtil_ABC_CLO.system_unix( "cat %s/.swdir/cfg/default_int_branches.cfg" % self.swgitUtil_ABC_CLO.getDir() )
    self.assertEqual( len( out ), 0, "FAILED adding repo without branch" )

    #
    out, errCode = self.swgitUtil_ABC_CLO.proj_edit( MAP_INFOS[0][0], "NOT_EXISTING_BR" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Please specify a valid branch", 
                                   "Editing def-int-br" )

    out, errCode = self.swgitUtil_ABC_CLO.system_unix( "cat %s/.swdir/cfg/default_int_branches.cfg" % self.swgitUtil_ABC_CLO.getDir() )
    self.assertEqual( len( out ), 0, "FAILED adding repo without branch" )

    #
    out, errCode = self.swgitUtil_ABC_CLO.proj_edit( MAP_INFOS[0][0], MAP_INFOS[0][2] )
    self.util_check_SUCC_scenario( out, errCode, "", "Editing def-int-br" )

    out, errCode = self.swgitUtil_ABC_CLO.system_unix( "cat %s/.swdir/cfg/default_int_branches.cfg" % self.swgitUtil_ABC_CLO.getDir() )
    self.util_check_SUCC_scenario( out, errCode, 
                                   MAP_INFOS[0][2], 
                                   "Searching DEVTDM into defintbr" )

    out, errCode = self.swgitUtil_ABC_CLO.commit_minusA_dev_repolist( repolist = Arepo_info_without_branch[0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    out, errCode = self.swgitUtil_ABC_CLO.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PROJ_ABC_CLONE_DIR, out ) )

    #unset
    out, errCode = self.swgitUtil_ABC_CLO.proj_edit( MAP_INFOS[0][0], "" )
    self.util_check_SUCC_scenario( out, errCode, "", "Editing unset-int-br" )

    out, errCode = self.swgitUtil_ABC_CLO.system_unix( "cat %s/.swdir/cfg/default_int_branches.cfg" % self.swgitUtil_ABC_CLO.getDir() )
    self.assertEqual( len( out ), 0, "FAILED adding repo without branch" )





if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()


