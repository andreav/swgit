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


class Test_ProjSnapshot( Test_ProjBase ):
  BRANCH = "test_snap_br"

  #This method is executed before each test_*
  def setUp( self ):
    super( Test_ProjSnapshot, self ).setUp()


  #This method is executed after each test_*
  def tearDown( self ):
    super( Test_ProjSnapshot, self ).tearDown()


  def test_ProjSnapshot_00_00_1SNAP_default( self ):
    self.util_createrepos_clonePLATproj_createBr_addSNAP_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, out) )

    clo2_h = self.swu_PLAT_CLO2
    snap_h = swgit__utils( "%s/%s" % (clo2_h.getDir(), SNAP_BI[0]) )

    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s " % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s " % snap_h.getDir() )

    # must be empty
    snapfile = "%s/snap.txt" % ( snap_h.getDir() )
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )

    #####
    # proj update must do not touch it
    #####
    out, errCode = clo2_h.proj_update()
    self.assertEqual( errCode, 0, "FAILED proj update for snap repo %s" % snap_h.getDir() )


    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be empty
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )

    #####
    # proj reset must do not touch it
    #####
    out, errCode = clo2_h.proj_reset()
    self.assertEqual( errCode, 0, "FAILED proj reset for snap repo %s" % snap_h.getDir() )


    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be empty
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )


    #####
    # proj init must do not touch it
    #####
    out, errCode = clo2_h.proj_init()
    self.assertEqual( errCode, 0, "FAILED proj init for snap repo %s" % snap_h.getDir() )


    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be empty
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )


    #####
    # proj update --repo must download file
    #####
    out, errCode = clo2_h.proj_update( SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED update --repo for snap repo %s" % snap_h.getDir() )

    # NEVER INITIALIZE IT (except if you  issue proj --init --repo it)
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be with default content
    # but without .git (is not a repo!!!)
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "FAILED CREATING snap repo content %s" % snapfile )


    #####
    # proj reset HEAD --repo must download same version file
    #####
    out, errCode = clo2_h.proj_reset( "HEAD", SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED reset HEAD --repo for snap repo %s" % snap_h.getDir() )
    # must be with default content
    # but without .git (is not a repo!!!)
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "FAILED CREATING snap repo content %s" % snapfile )

    #####
    # proj reset HEAD~1 must fail
    #####
    out, errCode = clo2_h.proj_reset( "HEAD~1", SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST FAIL reset HEAD~1 --repo for snap repo %s (was not existing)" % snap_h.getDir() )

    #####
    # proj init --repo must download all history
    #####
    out, errCode = clo2_h.proj_init( SNAP_BI[0] )
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "FAILED CREATING snap repo content %s" % snapfile )

    repo_bi = SNAP_BI
    snap_ori_h   = swgit__utils( REPO_SNAP__ORI_DIR )
    snap_clone_h = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, snap_clone_h,
                                                      self.swu_PLAT_ORI, snap_ori_h,
                                                      repo_bi )



  #
  # NOREC => nothing downloaded.
  # all options without --repo does not affect
  # all option with --repo act on snapshot repos (differently from normal repos) 
  #  that are not initialized
  #
  def test_ProjSnapshot_01_00_1SNAP_cloneNOREC( self ):
    self.util_createrepos_clonePLATproj_createBr_addSNAP_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url_norec( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url_norec( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, out) )


    clo2_h = self.swu_PLAT_CLO2
    snap_h = swgit__utils( "%s/%s" % (clo2_h.getDir(), SNAP_BI[0]) )

    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s " % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s " % snap_h.getDir() )

    # must be empty
    snapfile = "%s/snap.txt" % ( snap_h.getDir() )
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )


    #####
    # proj update must do not touch it
    #####
    out, errCode = clo2_h.proj_update()
    self.assertEqual( errCode, 0, "FAILED proj update for snap repo %s" % snap_h.getDir() )


    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be empty
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )

    #####
    # proj reset must do not touch it
    #####
    out, errCode = clo2_h.proj_reset()
    self.assertEqual( errCode, 0, "FAILED proj reset for snap repo %s" % snap_h.getDir() )


    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be empty
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )


    #####
    # proj init must do not touch it
    #####
    out, errCode = clo2_h.proj_init()
    self.assertEqual( errCode, 0, "FAILED proj init for snap repo %s" % snap_h.getDir() )


    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be empty
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )


    #####
    # proj update --repo must download file
    #####
    out, errCode = clo2_h.proj_update( SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED update --repo for snap repo %s" % snap_h.getDir() )

    # NEVER INITIALIZE IT (except if you  issue proj --init --repo it)
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s" % snap_h.getDir() )

    # must be with default content
    # but without .git (is not a repo!!!)
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "FAILED CREATING snap repo content %s" % snapfile )


    #####
    # proj reset HEAD --repo must download same version file
    #####
    out, errCode = clo2_h.proj_reset( "HEAD", SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED reset HEAD --repo for snap repo %s" % snap_h.getDir() )
    # must be with default content
    # but without .git (is not a repo!!!)
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "FAILED CREATING snap repo content %s" % snapfile )

    #####
    # proj reset HEAD~1 must fail
    #####
    out, errCode = clo2_h.proj_reset( "HEAD~1", SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST FAIL reset HEAD~1 --repo for snap repo %s (was not existing)" % snap_h.getDir() )

    #####
    # proj init --repo must download all history
    #####
    clo2_h.proj_init( SNAP_BI[0] )
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "FAILED CREATING snap repo content %s" % snapfile )

    repo_bi = SNAP_BI
    snap_ori_h   = swgit__utils( REPO_SNAP__ORI_DIR )
    snap_clone_h = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, snap_clone_h,
                                                      self.swu_PLAT_ORI, snap_ori_h,
                                                      repo_bi )

  #
  # clone --snapshot => also proj --update --snapshot
  #
  def test_ProjSnapshot_01_01_1SNAP_cloneSNAPSHOT( self ):
    self.util_createrepos_clonePLATproj_createBr_addSNAP_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url_norec( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, " --snapshot " )
    self.assertEqual( errCode, 0, "clone_repo_url_norec( %s, %s, %s ) FAILED SNAPSHOT CLONE - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, out) )


    clo2_h = self.swu_PLAT_CLO2
    snap_h = swgit__utils( "%s/%s" % (clo2_h.getDir(), SNAP_BI[0]) )

    # must not be initialized
    val, errCode = clo2_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s " % clo2_h.getDir() )

    val, errCode = snap_h.get_cfg( "submodule.%s.url" % SNAP_BI[0] )
    self.assertEqual( errCode, 1, "MUST  FAIL retrieving initialization for snap repo %s " % snap_h.getDir() )

    # must NOT be empty
    snapfile = "%s/snap.txt" % ( snap_h.getDir() )
    self.assertTrue ( os.path.exists( snap_h.getDir() ), "FAILED creating snap repo dir %s" % snap_h.getDir() )
    self.assertFalse( os.path.exists( snap_h.getDir() + "/.git" ), "MUST NOT create snap repo dir %s/.git" % snap_h.getDir() )
    self.assertTrue ( os.path.exists( snapfile ), "MUST be created snap repo content %s" % snapfile )



  def test_ProjSnapshot_02_00_1SNAP_commit( self ):
    self.util_createrepos_clonePLATproj_createBr_addSNAP_commit_push()

    #clone proj into CLOVALLEA
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__DEVBRANCH, out) )

    clo_valle_plat_hm = swgit__utils( self.REPO_PLAT__CLOVALLEA_DIR )
    clo_valle_snap_hm = swgit__utils( self.REPO_PLAT__CLOVALLEA_DIR + "/" + SNAP_BI[0] )

    clone_sha = clo_valle_plat_hm.get_currsha()[0]

    out, errCode = clo_valle_plat_hm.commit_minusA_repolist( repolist = SNAP_BI[0] )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Cannot commit snapshot repository",
                                   "MUST FAIL commit with SNAP repo not initialized" ) 

    out, errCode = clo_valle_plat_hm.commit_minusA_repolist( repolist = "-A" )
    self.util_check_DENY_scenario( out, errCode, 
                                   "Nothing to be committed",
                                   "MUST FAIL commit with SNAP repo not initialized" ) 


    out, errCode = clo_valle_plat_hm.proj_init( opt = "--snapshot" )
    self.util_check_SUCC_scenario( out, errCode, "emtpying it before converting to \"standard\" repo",
                                   "init --snapshot" ) 




  def test_ProjSnapshot_02_01_1SNAP_pushpull( self ):
    self.util_createrepos_clonePLATproj_createBr_addSNAP_commit_push()

    #clone proj into CLOVALLEA
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__DEVBRANCH, out) )

    #clone proj into CLOCAPPA
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOCAPPA_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOCAPPA_DIR, REPO_PLAT__DEVBRANCH, out) )

    clo_valle_plat_hm = swgit__utils( self.REPO_PLAT__CLOVALLEA_DIR )
    clo_valle_snap_hm = swgit__utils( self.REPO_PLAT__CLOVALLEA_DIR + "/" + SNAP_BI[0] )
    clo_cappa_plat_hm = swgit__utils( self.REPO_PLAT__CLOCAPPA_DIR )
    clo_cappa_snap_hm = swgit__utils( self.REPO_PLAT__CLOCAPPA_DIR + "/" + SNAP_BI[0] )

    #
    #modify CAPPA SNAP repo
    # transform into git repo, modify, commit, push
    #
    CONTENT = "DACAPPA"
    clo_cappa_plat_hm.proj_init( SNAP_BI[0] )
    clo_cappa_snap_hm.modify_repo( filename = "snap.txt", msg = CONTENT )
    clo_cappa_snap_hm.push()
    clo_cappa_plat_hm.commit_repolist( repolist = SNAP_BI[0] )
    clo_cappa_plat_hm.push()


    #
    #proj VALLEA update
    #
    clo_valle_plat_hm.proj_update()

    snapfile = "%s/snap.txt" % ( clo_valle_snap_hm.getDir() )

    self.assertFalse( os.path.exists( snapfile ), "MUST NOT be created snap repo content %s" % snapfile )
    out, errCode = clo_valle_snap_hm.system_unix( "grep -e \"%s\" %s" % ( CONTENT, snapfile ) )
    self.assertEqual( errCode, 1, "MUST not be present file at all - \n%s\n" % out )

    clone_sha = clo_valle_plat_hm.get_currsha()[0]

    #
    #proj VALLEA update --repo
    #
    out, errCode = clo_valle_plat_hm.proj_update( SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED update --repo for snap repo %s" % clo_valle_plat_hm.getDir() )

    self.assertTrue( os.path.exists( snapfile ), "MUST be created snap repo content %s" % snapfile )

    out, errCode = clo_valle_snap_hm.system_unix( "grep -e \"%s\" %s" % ( CONTENT, snapfile ) )
    self.assertEqual( errCode, 0, "MUST be present content %s into file %s pulled from other repo - \n%s\n" % ( CONTENT, snapfile, out ) )


    #
    #proj VALLEA reset --repo
    #
    out, errCode = clo_valle_plat_hm.proj_reset( "HEAD~1", SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED reset --repo for snap repo %s" % clo_valle_plat_hm.getDir() )

    self.assertTrue( os.path.exists( snapfile ), "MUST be created snap repo content %s" % snapfile )

    out, errCode = clo_valle_snap_hm.system_unix( "grep -e \"%s\" %s" % ( CONTENT, snapfile ) )
    self.assertEqual( errCode, 1, "MUST be present content %s into file %s pulled from other repo - \n%s\n" % ( CONTENT, snapfile, out ) )

    #
    #proj VALLEA update --repo
    # restore last version
    #
    out, errCode = clo_valle_plat_hm.proj_update( SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED update --repo for snap repo %s" % clo_valle_plat_hm.getDir() )

    self.assertTrue( os.path.exists( snapfile ), "MUST be created snap repo content %s" % snapfile )

    out, errCode = clo_valle_snap_hm.system_unix( "grep -e \"%s\" %s" % ( CONTENT, snapfile ) )
    self.assertEqual( errCode, 0, "MUST be present content %s into file %s pulled from other repo - \n%s\n" % ( CONTENT, snapfile, out ) )

    #
    #proj VALLEA reset --repo (come back again)
    # proj update (withou --repo) must not change snapshot repo
    #
    out, errCode = clo_valle_plat_hm.proj_reset( "HEAD~1", SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED reset --repo for snap repo %s" % clo_valle_plat_hm.getDir() )
    out, errCode = clo_valle_plat_hm.proj_update()
    self.assertEqual( errCode, 0, "FAILED update --repo for snap repo %s" % clo_valle_plat_hm.getDir() )

    self.assertTrue( os.path.exists( snapfile ), "MUST be created snap repo content %s" % snapfile )

    out, errCode = clo_valle_snap_hm.system_unix( "grep -e \"%s\" %s" % ( CONTENT, snapfile ) )
    self.assertEqual( errCode, 1, "MUST NOT be present content %s into file %s pulled from other repo without --repo - \n%s\n" % ( CONTENT, snapfile, out ) )



  def test_ProjSnapshot_03_00_1SNAP_1DEV( self ):
    self.util_createrepos_clonePLATproj_createBr_addFS_addAPP_addSNAP_commit_push()

    #clone proj into CLOVALLEA
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__DEVBRANCH, out) )

    ori_va_hm = self.util_get_PLATFULL_helper_map_orig( snap = True )
    clo_va_hm = self.util_get_PLATFULL_helper_map_clone( self.REPO_PLAT__CLOVALLEA_DIR, snap = True )

    va_sha_map_clonetime = self.util_map2_currshas( clo_va_hm )

    #
    #modify VALLEA DEV repo
    #
    CONTENT = "DAVALLEA"
    clo_va_hm["DEVFS"].modify_repo( filename = REPO_FS__INFOS[4], msg = CONTENT )
    clo_va_hm["PLAT"].commit_repolist( msg = "commit with command line args", repolist = plat_name2path("DEVFS") )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED commit DEVFS" ) 

    va_sha_map_after1commit = self.util_map2_currshas( clo_va_hm )
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after1commit, 
                                   [ "DEVAPP" ], # empty => all
                                   [ "PLAT", "DEVFS" ],
                                   "FAILED modify_repo inside %s" % clo_va_hm["PLAT"].getDir()
                                 )

    #
    #modify VALLEA DEV repo again
    #
    CONTENT = "DAVALLEA 2"
    clo_va_hm["DEVFS"].modify_repo( filename = REPO_FS__INFOS[4], msg = CONTENT )
    clo_va_hm["PLAT"].commit_repolist( msg = "commit with -A", repolist = "-A" )
    self.util_check_SUCC_scenario( out, errCode, "",
                              "FAILED commit DEVFS with -A" ) 

    va_sha_map_after2commit = self.util_map2_currshas( clo_va_hm )

    self.util_assert_EQ_UNEQ_maps( va_sha_map_after1commit, 
                                   va_sha_map_after2commit, 
                                   [ "DEVAPP" ], # empty => all
                                   [ "PLAT", "DEVFS" ],
                                   "FAILED modify_repo inside %s" % clo_va_hm["PLAT"].getDir()
                                 )



if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()




