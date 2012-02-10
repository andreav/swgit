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


class Test_ProjMerge( Test_ProjBase ):

  #This method is executed before each test_*
  def setUp( self ):
    super( Test_ProjMerge, self ).setUp()
    
  #This method is executed after each test_*
  def tearDown( self ):
    super( Test_ProjMerge, self ).tearDown()

  #
  # Test:
  #   va develops into 2 submods in a NON conflict way and freezes into project both changes
  #   then merging project branches
  #
  # Result:
  #   a conflict will happen anyway ... 
  #   you can solve manually
  #   or
  #   by issueing a swgit submodule update --merge -- repo
  #   then adding repo to index
  #   finally committing with repolist
  #   
  # swgit proj -D will tell you which differences
  def test_ProjMerge_00_00_NOconflict__duringMerge_onlySubmod_resolveAUTO( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )

    clo_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    mod_file = "file_br111.txt"
    clo_valle_hm["TSS100"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].modify_file( mod_file, "from BR1111" )
    clo_valle_hm["DEVTDM"].system_swgit( "add %s" % mod_file )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR1" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br1", repolist = "-A" )

    cb1_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb1_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    mod_file = "file_br222.txt"
    clo_valle_hm["TSS100"].branch_create_src( "BR2", clo_sha_map_clonetime["TSS100"] )
    clo_valle_hm["DEVTDM"].branch_create_src( "BR2", clo_sha_map_clonetime["DEVTDM"] )
    clo_valle_hm["DEVTDM"].modify_file( mod_file, "from BR2222" )
    clo_valle_hm["DEVTDM"].system_swgit( "add %s" % mod_file )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR2" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br2", repolist = "-A" )

    cb2_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb2_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    out, errCode = clo_valle_hm["TSS100"].merge( cb1_tss100_full )
    self.util_check_DENY_scenario( out, errCode, "merge following commits not found", "merge tss100" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )

    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )

    ####################################
    # Resolve submod conflict automatically
    ####################################
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "submodule update --merge" )
    self.util_check_SUCC_scenario( out, errCode, "", "resolve merge automatically into tss100" )
    ####################################

    # git version GIT_VERSION_SUBMODCHANGE says:
    #  'Skipping unmerged submodule TEST_PROJ_REPO_TDM'
    # previous git versions makes merge
    if GIT_VERSION < GIT_VERSION_SUBMODCHANGE:

      va_sha_devtdm_head2 = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2" )[0]
      va_sha_devtdm_br1   = clo_valle_hm["DEVTDM"].get_currsha( cb1_devtdm_full )[0]
      self.assertEqual( va_sha_devtdm_head2,
                        va_sha_devtdm_br1,
                        "After merge resolution, no right merge" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % ( tss100_name2path("DEVTDM") ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding resolved repo" )

      out, errCode = clo_valle_hm["TSS100"].commit( "merge resolved" )
      self.util_check_DENY_scenario( out, errCode, "There is a submodule added to the index", "committing plain" )

      out, errCode = clo_valle_hm["TSS100"].commit_minusA_dev( "merge resolved" )
      self.util_check_DENY_scenario( out, errCode, "There is a submodule added to the index", "committing with -a" )

      out, errCode = clo_valle_hm["TSS100"].commit_minusA_dev_repolist( "merge resolved", repolist = tss100_name2path("DEVTDM") )
      self.util_check_SUCC_scenario( out, errCode, "", "committing with -a and -A" )

      va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD^2" )[0]
      va_sha_tss100_br1   = clo_valle_hm["TSS100"].get_currsha( cb1_tss100_full )[0]
      self.assertEqual( va_sha_tss100_head2,
                        va_sha_tss100_br1,
                        "After merge resolution, no right merge inside TSS100" )

    else: # GITVER > GIT_VERSION_SUBMODCHANGE : 'Skipping unmerged submodule TEST_PROJ_REPO_TDM'

      self.assertTrue( "Skipping unmerged submodule" in out, 
                       "GITVERSION > GIT_VERSION_SUBMODCHANGE skips unmerged when git submodule update)" )

      #NOTE: next test will resolve this scenario manually

  #
  # Test:
  #   like test_ProjMerge_00_00 but resolve merge manually
  def test_ProjMerge_00_01_NOconflict__duringMerge_onlySubmod_resolveMAN( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )

    clo_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    mod_file = "file_br111.txt"
    clo_valle_hm["TSS100"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].modify_file( mod_file, "from BR1111" )
    clo_valle_hm["DEVTDM"].system_swgit( "add %s" % mod_file )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR1" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br1", repolist = "-A" )

    cb1_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb1_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    mod_file = "file_br222.txt"
    clo_valle_hm["TSS100"].branch_create_src( "BR2", clo_sha_map_clonetime["TSS100"] )
    clo_valle_hm["DEVTDM"].branch_create_src( "BR2", clo_sha_map_clonetime["DEVTDM"] )
    clo_valle_hm["DEVTDM"].modify_file( mod_file, "from BR2222" )
    clo_valle_hm["DEVTDM"].system_swgit( "add %s" % mod_file )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR2" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br2", repolist = "-A" )

    cb2_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb2_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    out, errCode = clo_valle_hm["TSS100"].merge( cb1_tss100_full )
    self.util_check_DENY_scenario( out, errCode, "merge following commits not found", "merge tss100" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )


    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )


    ####################################
    # Resolve submod conflict manually
    ####################################
    out, errCode = clo_valle_hm["DEVTDM"].merge( cb1_devtdm_full )
    self.util_check_SUCC_scenario( out, errCode, "", "resolve merge manually into DEVTDM" )
    ####################################

    va_sha_devtdm_head2 = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2" )[0]
    va_sha_devtdm_br1   = clo_valle_hm["DEVTDM"].get_currsha( cb1_devtdm_full )[0]
    self.assertEqual( va_sha_devtdm_head2,
                      va_sha_devtdm_br1,
                      "After merge resolution, no right merge inside DEVTDM" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % ( tss100_name2path("DEVTDM") ) )
    self.util_check_SUCC_scenario( out, errCode, "", "adding resolved repo" )

    out, errCode = clo_valle_hm["TSS100"].commit( "merge resolved" )
    self.util_check_DENY_scenario( out, errCode, "There is a submodule added to the index", "committing plain" )

    out, errCode = clo_valle_hm["TSS100"].commit_minusA_dev( "merge resolved" )
    self.util_check_DENY_scenario( out, errCode, "There is a submodule added to the index", "committing with -a" )

    out, errCode = clo_valle_hm["TSS100"].commit_minusA_dev_repolist( "merge resolved", repolist = tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "committing with -a and -A" )

    va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD^2" )[0]
    va_sha_tss100_br1   = clo_valle_hm["TSS100"].get_currsha( cb1_tss100_full )[0]
    self.assertEqual( va_sha_tss100_head2,
                      va_sha_tss100_br1,
                      "After merge resolution, no right merge inside TSS100" )

  #
  # Test:
  #   va develops into 2 submods in a conflict way and freezes into project both changes
  #   when merging into project there is a conflict
  #   BUT     git status does not show it
  #   INSTEAD swgit proj -D does
  #
  #   In this test just add repo and commit. This works but is strange, is like not really resolving merge, 
  #      just current branch wins
  #
  # Result:
  #   Subrepo will have NO MERGE (merge there never began, it stopped at project level)
  #   This is no good, because maybe merge is needed also underneath
  #
  # Note:
  #   In next test will try resolving automatically and manually
  #
  def test_ProjMerge_01_00_YESconflict_duringMerge_onlySubmod( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )

    clo_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR1111" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR1" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br1", repolist = "-A" )

    cb1_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb1_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    clo_valle_hm["TSS100"].branch_create_src( "BR2", clo_sha_map_clonetime["TSS100"] )
    clo_valle_hm["DEVTDM"].branch_create_src( "BR2", clo_sha_map_clonetime["DEVTDM"] )
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR2222" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR2" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br2", repolist = "-A" )

    cb2_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb2_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    out, errCode = clo_valle_hm["TSS100"].merge( cb1_tss100_full )
    self.util_check_DENY_scenario( out, errCode, "merge following commits not found", "merge tss100" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )

    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )

    #add repo to index
    # attention, it does not appear into index ... why???
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
    self.util_check_SUCC_scenario( out, errCode, "", "adding DEVTDM" )

    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Nothing to be committed inside submodules. Please remove -A option.", "commit after resolving submod conflict" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Nothing added to the index. Try using -a option.", "commit with submod conflict" )

    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_SUCC_scenario( out, errCode, "", "commit with submod conflict" )

    #merge NOT done into DEVTDM
    va_sha_devtdm_head2, errCode  = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2" )
    self.assertEqual( errCode, 1, "must not exists ^2, no merge must be done in subrepo" )

    #merge done into tss100
    va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD^2" )[0]
    va_sha_tss100_br1   = clo_valle_hm["TSS100"].get_currsha( cb1_tss100_full )[0]
    self.assertEqual( va_sha_tss100_head2,
                      va_sha_tss100_br1,
                      "After merge resolution, no right merge inside TSS100" )


  #
  # Test:
  #  Like test_ProjMerge_01_00 but try AUTO merge  
  #   
  # Result:
  #  thanks to automerge, subrepo will be marked by git as conflicted, 
  #    and no more commit is possible until conflict resolution by hand
  #  This is good because we see the problem (conflict)
  #
  def test_ProjMerge_01_01_YESconflict_duringMerge_onlySubmod_tryAUTO( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )

    clo_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR1111" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR1" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br1", repolist = "-A" )

    cb1_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb1_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    clo_valle_hm["TSS100"].branch_create_src( "BR2", clo_sha_map_clonetime["TSS100"] )
    clo_valle_hm["DEVTDM"].branch_create_src( "BR2", clo_sha_map_clonetime["DEVTDM"] )
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR2222" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR2" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br2", repolist = "-A" )

    cb2_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb2_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    out, errCode = clo_valle_hm["TSS100"].merge( cb1_tss100_full )
    self.util_check_DENY_scenario( out, errCode, "merge following commits not found", "merge tss100" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )

    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )

    ####################################
    # Resolve submod conflict automatically WILL fail
    ####################################
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "submodule update --merge" )
    ####################################

    # git version GIT_VERSION_SUBMODCHANGE says:
    #  'Skipping unmerged submodule TEST_PROJ_REPO_TDM'
    # previous git versions makes merge
    if GIT_VERSION < GIT_VERSION_SUBMODCHANGE:

      self.util_check_DENY_scenario( out, errCode, "Automatic merge failed", "resolve merge automatically into tss100" )

      #add repo to index
      # there is a conflict not resolved, it will not be added! +1 to git!
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding DEVTDM" )

      out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Conflicted file(s) detected.", "commit after resolving submod conflict" )

      out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Nothing added to the index. Try using -a option.", "commit with submod conflict" )

      #this succeded, but does not commit repository
      out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit with submod conflict" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "modified content", "git status shows subrepo is not committed" )

      #add file conflicted to index
      out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "add %s" % tss100_name2file( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )

      out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "file(s) not commited detected.", "commit after resolving submod conflict" )

      #add repo to index
      # there is a something not committed into subrepo, it will not be added! +1 to git!
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "(modified content)", "git status shows subrepo is not committed" )


      # commit devtdm
      out, errCode = clo_valle_hm["DEVTDM"].commit_minusA( msg = "resolved merge" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit after resolving submod conflict" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "(new commits)", "git status shows subrepo is ready to be added" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )
      out, errCode = clo_valle_hm["TSS100"].commit_repolist( msg = "resolved merge", repolist = "-A" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit project after resolving submod conflict" )

      #merge done into devtdm
      va_sha_devtdm_head2 = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2" )[0]
      va_sha_devtdm_br1   = clo_valle_hm["DEVTDM"].get_currsha( cb1_devtdm_full )[0]
      self.assertEqual( va_sha_devtdm_head2,
                        va_sha_devtdm_br1,
                        "After merge resolution, no right merge inside DEVTDM" )

      #merge done into tss100
      va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD~1^2" )[0]
      va_sha_tss100_br1   = clo_valle_hm["TSS100"].get_currsha( cb1_tss100_full )[0]
      self.assertEqual( va_sha_tss100_head2,
                        va_sha_tss100_br1,
                        "After merge resolution, no right merge inside TSS100" )

    else: # GITVER > GIT_VERSION_SUBMODCHANGE : 'Skipping unmerged submodule TEST_PROJ_REPO_TDM'

      self.util_check_SUCC_scenario( out, errCode, 
                                     "Skipping unmerged submodule", 
                                     "GITVERSION > GIT_VERSION_SUBMODCHANGE skips unmerged when git submodule update" )

      #NOTE: next test will resolve this scenario manually

  #
  # Test:
  #  Like test_ProjMerge_01_00 but try MAN merge  
  #   
  # Result:
  #  thanks to automerge, subrepo will be marked by git as conflicted, 
  #    and no more commit is possible until conflict resolution by hand
  #  This is good because we see the problem (conflict)
  #
  def test_ProjMerge_01_01_YESconflict_duringMerge_onlySubmod_tryMAN( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )

    clo_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].branch_create( "BR1" )
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR1111" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR1" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br1", repolist = "-A" )

    cb1_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb1_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    clo_valle_hm["TSS100"].branch_create_src( "BR2", clo_sha_map_clonetime["TSS100"] )
    clo_valle_hm["DEVTDM"].branch_create_src( "BR2", clo_sha_map_clonetime["DEVTDM"] )
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR2222" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR2" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br2", repolist = "-A" )

    cb2_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    cb2_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()

    out, errCode = clo_valle_hm["TSS100"].merge( cb1_tss100_full )
    self.util_check_DENY_scenario( out, errCode, "merge following commits not found", "merge tss100" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )
    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit with submod conflict" )

    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
    self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )

    ####################################
    # Resolve submod conflict manually WILL FAIL too
    ####################################
    out, errCode = clo_valle_hm["DEVTDM"].merge( cb1_devtdm_full )
    self.util_check_DENY_scenario( out, errCode, "Automatic merge failed", "resolve merge manually into DEVTDM" )
    ####################################

    #add repo to index
    # there is a conflict not resolved, it will not be added! +1 to git!
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
    self.util_check_SUCC_scenario( out, errCode, "", "adding DEVTDM" )

    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Conflicted file(s) detected.", "commit after resolving submod conflict" )

    out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "Nothing added to the index. Try using -a option.", "commit with submod conflict" )

    #this succeded, but does not commit repository
    out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
    self.util_check_SUCC_scenario( out, errCode, "", "commit with submod conflict" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
    self.util_check_SUCC_scenario( out, errCode, "modified content", "git status shows subrepo is not committed" )

    #add file conflicted to index
    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "add %s" % tss100_name2file( "DEVTDM" ) )
    self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )

    out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
    self.util_check_DENY_scenario( out, errCode, "file(s) not commited detected.", "commit after resolving submod conflict" )

    #add repo to index
    # there is a something not committed into subrepo, it will not be added! +1 to git!
    out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
    self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
    self.util_check_SUCC_scenario( out, errCode, "(modified content)", "git status shows subrepo is not committed" )


    # commit devtdm
    out, errCode = clo_valle_hm["DEVTDM"].commit_minusA( msg = "resolved merge" )
    self.util_check_SUCC_scenario( out, errCode, "", "commit after resolving submod conflict" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
    self.util_check_SUCC_scenario( out, errCode, "(new commits)", "git status shows subrepo is ready to be added" )

    out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
    self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )
    out, errCode = clo_valle_hm["TSS100"].commit_repolist( msg = "resolved merge", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, "", "commit project after resolving submod conflict" )

    #merge done into devtdm
    va_sha_devtdm_head2 = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2" )[0]
    va_sha_devtdm_br1   = clo_valle_hm["DEVTDM"].get_currsha( cb1_devtdm_full )[0]
    self.assertEqual( va_sha_devtdm_head2,
                      va_sha_devtdm_br1,
                      "After merge resolution, no right merge inside DEVTDM" )

    #merge done into tss100
    va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD~1^2" )[0]
    va_sha_tss100_br1   = clo_valle_hm["TSS100"].get_currsha( cb1_tss100_full )[0]
    self.assertEqual( va_sha_tss100_head2,
                      va_sha_tss100_br1,
                      "After merge resolution, no right merge inside TSS100" )



  #
  # Test:
  #   ca develops into submods and pushes
  #   va develops into submods in a conflict way
  #   va proj --update
  #
  #   GIT_VERSION < GIT_VERSION_SUBMODCHANGE:
  #      there is a conflict into proj directory and no commits are downloaded from subrepo
  #      => swgit proj -D fails
  #         but with 
  #         swgit submodule update repairs it
  #   GIT_VERSION >= GIT_VERSION_SUBMODCHANGE:
  #      pull --all --tags at project level will fetch also submodule commits
  #      git does not shows no more conflict at proj level, but conflict exists (.git/MERGE_HEAD exists)
  #      git propose to make MERGE_HEAD win, but this is wrong in geneal (for me)
  #
  # Note:
  #   In next test will try resolving automatically and manually
  #
  # Result:
  #   Subrepo will have MERGE
  #   Proj will have MERGE too
  #
  def test_ProjMerge_01_01_YESconflict_duringProjUpdate_onlySubmod_tyrAUTO( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      #remote   = ORIG_REPO_AREMOTE_NAME
      remote   = "origin"

    #
    # modif from one repo
    clo_valle_hm["TSS100"].branch_create( "BR1" )
    cb1_tss100_full, err = clo_valle_hm["TSS100"].current_branch()
    clo_valle_hm["DEVTDM"].branch_create( "BR1" )
    cb1_devtdm_full, err = clo_valle_hm["DEVTDM"].current_branch()
    clo_valle_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR1111" )
    clo_valle_hm["DEVTDM"].commit_minusA_dev( "commit from BR1" )
    clo_valle_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br1", repolist = "-A" )
    clo_valle_hm["TSS100"].merge_on_int()

    va_sha_devtdm_brvalle = clo_valle_hm["DEVTDM"].get_currsha( cb1_devtdm_full )[0]
    va_sha_tss100_brvalle = clo_valle_hm["TSS100"].get_currsha( cb1_tss100_full )[0]

    #
    # modif from other repo
    clo_cappa_hm["TSS100"].branch_create( "BR_CAPPA" )
    clo_cappa_hm["DEVTDM"].branch_create( "BR_CAPPA" )
    clo_cappa_hm["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), "from BR_CAPPA" )
    clo_cappa_hm["DEVTDM"].commit_minusA_dev( "commit from BR_CAPPA" )
    clo_cappa_hm["TSS100"].commit_dev_repolist( msg = "tss100 commit for br_cappa", repolist = "-A" )
    clo_cappa_hm["DEVTDM"].push_with_merge( remote )
    clo_cappa_hm["TSS100"].push_with_merge( remote )

    cbcappa_tss100_full, err = clo_cappa_hm["TSS100"].current_branch()
    cbcappa_devtdm_full, err = clo_cappa_hm["DEVTDM"].current_branch()
    ca_sha_devtdm_brcappa = clo_cappa_hm["DEVTDM"].get_currsha( cbcappa_devtdm_full )[0]
    ca_sha_tss100_brcappa = clo_cappa_hm["TSS100"].get_currsha( cbcappa_tss100_full )[0]

    #
    # update repo
    out, errCode = clo_valle_hm["TSS100"].proj_update()
    self.util_check_DENY_scenario( out, errCode, "CONFLICT (submodule): Merge conflict in", "proj --update" )

    out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )

    # git version GIT_VERSION_SUBMODCHANGE says:
    #  'Skipping unmerged submodule TEST_PROJ_REPO_TDM'
    # previous git versions makes merge
    if GIT_VERSION < GIT_VERSION_SUBMODCHANGE:

      self.util_check_DENY_scenario( out, errCode, "In order to download any new commit,", "proj -D" )
      out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
      self.util_check_DENY_scenario( out, errCode, "In order to download any new commit,", "proj -D DEVTDM" )

      ####################################
      # Resolve submod conflict automatically WILL fail
      ####################################
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "submodule update --merge" )
      self.util_check_DENY_scenario( out, errCode, "Automatic merge failed", "resolve merge automatically into tss100" )
      ####################################

      out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D" )
      self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
      out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
      self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )

      #add repo to index
      # there is a conflict not resolved, it will not be added! +1 to git!
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding DEVTDM" )

      out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Conflicted file(s) detected.", "commit after resolving submod conflict" )

      out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Nothing added to the index. Try using -a option.", "commit with submod conflict" )

      #this succeded, but does not commit repository
      out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit with submod conflict" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "modified content", "git status shows subrepo is not committed" )

      #add file conflicted to index
      out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "add %s" % tss100_name2file( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )

      out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "file(s) not commited detected.", "commit after resolving submod conflict" )

      #add repo to index
      # there is a something not committed into subrepo, it will not be added! +1 to git!
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "(modified content)", "git status shows subrepo is not committed" )


      # commit devtdm
      out, errCode = clo_valle_hm["DEVTDM"].commit_minusA( msg = "resolved merge" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit after resolving submod conflict" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "(new commits)", "git status shows subrepo is ready to be added" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding %s" % tss100_name2file("DEVTDM") )
      out, errCode = clo_valle_hm["TSS100"].commit_repolist( msg = "resolved merge", repolist = "-A" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit project after resolving submod conflict" )

      #merge done into devtdm
      va_sha_devtdm_head2   = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2" )[0]
      self.assertEqual( va_sha_devtdm_head2,
                        ca_sha_devtdm_brcappa,
                        "After merge resolution, no right merge inside DEVTDM" )

      #merge done into tss100
      va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD~1^2^2" )[0]
      self.assertEqual( va_sha_tss100_head2,
                        ca_sha_tss100_brcappa,
                        "After merge resolution, no right merge inside TSS100" )

    else:
      #   GIT_VERSION >= GIT_VERSION_SUBMODCHANGE:
      #      pull --all --tags at project level will fetch also submodule commits
      #      git does not shows no more conflict at proj level, but conflict exists (.git/MERGE_HEAD exists)
      #      git propose to make MERGE_HEAD win, but this is wrong in geneal (for me)
      #      swgit proj -D now works
      self.util_check_SUCC_scenario( out, errCode, "", "proj -D" )
      out, errCode = clo_valle_hm["DEVTDM"].system_swgit( "proj -D %s" % tss100_name2path("DEVTDM") )
      self.util_check_SUCC_scenario( out, errCode, "", "proj -D DEVTDM" )

      ####################################
      # Resolve submod conflict automatically WILL NOT fail, but jumps conflicted repo
      ####################################
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "submodule update --merge" )
      self.util_check_SUCC_scenario( out, errCode, "Skipping unmerged submodule", "resolve merge automatically into tss100" )
      ####################################

      #add repo to index
      # OLD GIT: there is a conflict not resolved, it will not be added! +1 to git!
      # NEW GIT: it is added and choosed the suggestion into submodule (not right for me)
      #          and says 'both modified', this is better, is like any file
      #          but now if you add submod to the index, it will be resolved, like any file.
      #out, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      #self.util_check_SUCC_scenario( out, errCode, "", "adding DEVTDM" )

      out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit after pull conflict on submodule" )

      out, errCode = clo_valle_hm["TSS100"].commit( msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit after pull conflict on submodule" )

      #this succeded, but does not commit repository
      out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit after pull conflict on submodule" )

      #this succeded, but does not commit repository
      out, errCode = clo_valle_hm["TSS100"].commit_minusA_repolist( repolist = "-A", msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, "Conflicts found on repository", "commit after pull conflict on submodule" )

      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "both modified:", "git status shows subrepo is not resolved" )

      #
      # add file conflicted (in this case is a submod) to the  index
      #
      ut, errCode = clo_valle_hm["TSS100"].system_swgit( "add %s" % tss100_name2path( "DEVTDM" ) )
      self.util_check_SUCC_scenario( out, errCode, "", "adding DEVTDM" )

      out, errCode = clo_valle_hm["TSS100"].commit_repolist( "-A",  msg = "resolved merge" )
      self.util_check_DENY_scenario( out, errCode, 
                                     "Nothing to be committed inside submodules. Please remove -A option.", 
                                     "commit after resolving submod conflict" )

      #
      # Nooo! -1 to git!!
      #
      #  there is a pending merge, but nothing is shown on git status..
      # Instead, if you try making everthing else, swgit will prevent you 
      #           from doing because ther eis a merge
      out, errCode = clo_valle_hm["TSS100"].system_swgit( "status" )
      self.util_check_SUCC_scenario( out, errCode, "nothing to commit", "git status shows subrepo there is no more conflict" )

      # commit devtdm
      out, errCode = clo_valle_hm["TSS100"].commit_minusA( msg = "resolved merge" )
      self.util_check_SUCC_scenario( out, errCode, "", "commit after resolving submod conflict" )

      #just nothing done into subrepo
      va_sha_devtdm_head  = clo_valle_hm["DEVTDM"].get_currsha( "HEAD" )[0]
      self.assertEqual( va_sha_devtdm_head,
                        va_sha_devtdm_brvalle,
                        "After merge resolution, no right merge inside DEVTDM" )

      #merge done into tss100
      va_sha_tss100_head2 = clo_valle_hm["TSS100"].get_currsha( "HEAD~1^2" )[0]
      self.assertEqual( va_sha_tss100_head2,
                        va_sha_tss100_brvalle,
                        "After merge resolution, no right merge inside TSS100" )

      #merge done into tss100
      va_sha_tss100_head22 = clo_valle_hm["TSS100"].get_currsha( "HEAD^2^2" )[0]
      self.assertEqual( va_sha_tss100_head22,
                        ca_sha_tss100_brcappa,
                        "After merge resolution, no right merge inside TSS100" )


if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()





