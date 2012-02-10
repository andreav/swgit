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


class Test_ProjClone( Test_ProjBase ):

  #This method is executed before each test_*
  def setUp( self ):
    super( Test_ProjClone, self ).setUp()


  #This method is executed after each test_*
  def tearDown( self ):
    super( Test_ProjClone, self ).tearDown()


  def test_ProjClone_00_00_Clone_1PROJ_2DEVrepo( self ):
    self.util_createrepos_clonePLATproj_createBr_addFS_addAPP_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, out) )

    #check DEV fs
    repo_bi = PROJ_PLAT_DESCRIPTION[1][0]
    fs_clone_helper = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, fs_clone_helper,
                                                      self.swu_PLAT_ORI, self.swu_FS_ORI,
                                                      repo_bi )

    #check DEV app
    repo_bi = PROJ_PLAT_DESCRIPTION[1][1]
    app_clone_helper = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, app_clone_helper,
                                                      self.swu_PLAT_ORI, self.swu_APP_ORI,
                                                      repo_bi )


  def test_ProjClone_01_00_Clone_1PROJ_1DEVrepo_1CSTrepo( self ):
    self.util_createrepos_cloneTSS100proj_createBr_addDEVTDM_addCSTTDM_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    #check DEV TDM
    repo_bi = PROJ_TSS100_DESCRIPTION[1][0]
    tdm_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_TSS100_CLO2, tdm_clone_helper,
                                                      self.swu_TSS100_ORI, self.swu_TDM_ORI,
                                                      repo_bi )
    #check CST TDM
    repo_bi = PROJ_TSS100_DESCRIPTION[1][3]
    csttdm_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_TSS100_CLO2, csttdm_clone_helper,
                                                      self.swu_TSS100_ORI, self.swu_CSTTDM_ORI,
                                                      repo_bi )


  def test_ProjClone_02_00_Clone_1PROJ_1DEVproj( self ):
    self.util_createrepos_cloneTSS100proj_createBr_addDEVPLAT_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    #check DEV PLAT PROJ, so also all its subsubrepos
    repo_bi = PROJ_TSS100_DESCRIPTION[1][1]
    devplat_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEV_clonedPROJ_consinstency( self.swu_TSS100_CLO2, devplat_clone_helper,
                                                 self.swu_TSS100_ORI, self.swu_PLAT_ORI,
                                                 repo_bi,
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 




  def test_ProjClone_03_00_Clone_1PROJ_1CSTproj( self ):
    self.util_createrepos_cloneTSS100proj_createBr_addCSTPLAT_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    #check CST PLAT PROJ, so also all its subsubrepos
    repo_bi = PROJ_TSS100_DESCRIPTION[1][2]
    cstplat_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_CST_clonedPROJ_consinstency( self.swu_TSS100_CLO2, cstplat_clone_helper,
                                                 self.swu_TSS100_ORI, self.swu_PLAT_ORI,
                                                 repo_bi,
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj




  def test_ProjClone_04_00_Clone_1PROJ_1DEVproj_1CSTproj_1DEVrepo_1CSTrepo( self ):
    self.util_createrepos_cloneTSS100proj_createBr_addDEVPLAT_addCSTPLAT_addDEVTDM_addCSTTDM_commit_push()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    clo_helpmap = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )

    #check DEV TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_helpmap["TSS100"], clo_helpmap["DEVTDM"],
                                                      ori_helpmap["TSS100"], ori_helpmap["DEVTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][0] )

    #check DEV PLAT PROJ, so also all its subsubrepos
    self.util_check_DEV_clonedPROJ_consinstency( clo_helpmap["TSS100"], clo_helpmap["DEVPLAT"],
                                                 ori_helpmap["TSS100"], ori_helpmap["DEVPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][1],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 

    #check CST PLAT PROJ, so also all its subsubrepos
    self.util_check_CST_clonedPROJ_consinstency( clo_helpmap["TSS100"], clo_helpmap["CSTPLAT"],
                                                 ori_helpmap["TSS100"], ori_helpmap["CSTPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][2],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

    #check CST TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_helpmap["TSS100"], clo_helpmap["CSTTDM"],
                                                      ori_helpmap["TSS100"], ori_helpmap["CSTTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][3] )



  def test_ProjClone_05_00_CloneIntegrator_1PROJ_2DEVrepo( self ):
    self.util_createAndCheck_PLAT_FULL_withbkp()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, opt = " --integrator " )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) INTEGRATOR FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, out) )

    ori_helpmap = self.util_get_PLATFULL_helper_map_orig()
    clo_helpmap = self.util_get_PLATFULL_helper_map_clone( self.REPO_PLAT__CLO2_DIR )

    #
    # check integrator does a normal clone
    #

    #check DEV fs
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_helpmap["PLAT"], clo_helpmap["DEVFS"],
                                                      ori_helpmap["PLAT"], ori_helpmap["DEVFS"],
                                                      PROJ_PLAT_DESCRIPTION[1][0] )

    #check DEV app
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_helpmap["PLAT"], clo_helpmap["DEVAPP"],
                                                      ori_helpmap["PLAT"], ori_helpmap["DEVAPP"],
                                                      PROJ_PLAT_DESCRIPTION[1][1] )

    #
    # check integrator just add all integrator repositories
    #

    for h in [ clo_helpmap["PLAT"], clo_helpmap["DEVFS"], clo_helpmap["DEVAPP"] ]:
      self.util_check_repo_integrator( h )




  def test_ProjClone_05_01_CloneIntegrator( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, opt = " --integrator " )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) INTEGRATOR FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )


    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    clo_helpmap = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )

    #check DEV TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_helpmap["TSS100"], clo_helpmap["DEVTDM"],
                                                      ori_helpmap["TSS100"], ori_helpmap["DEVTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][0] )

    #check DEV PLAT PROJ, so also all its subsubrepos
    self.util_check_DEV_clonedPROJ_consinstency( clo_helpmap["TSS100"], clo_helpmap["DEVPLAT"],
                                                 ori_helpmap["TSS100"], ori_helpmap["DEVPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][1],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 

    #check CST PLAT PROJ, so also all its subsubrepos
    self.util_check_CST_clonedPROJ_consinstency( clo_helpmap["TSS100"], clo_helpmap["CSTPLAT"],
                                                 ori_helpmap["TSS100"], ori_helpmap["CSTPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][2],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

    #check CST TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_helpmap["TSS100"], clo_helpmap["CSTTDM"],
                                                      ori_helpmap["TSS100"], ori_helpmap["CSTTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][3] )


    #
    # check integartor repo just add tracked all repositories
    #

    # DEV repos are all integrator repos
    for h in [ clo_helpmap["TSS100"], clo_helpmap["DEVTDM"], clo_helpmap["DEVPLAT"], clo_helpmap["DEVFS"], clo_helpmap["DEVAPP"] ]:
      self.util_check_repo_integrator( h )

    # CST repos are not integrator repos (you can make anyway a stabilize also if you are not integrator repos
    for h in [ clo_helpmap["CSTTDM"], clo_helpmap["CSTPLAT"], clo_helpmap["CSTFS"], clo_helpmap["CSTAPP"] ]:
      self.util_check_repo_NOT_integrator( h )



  def test_ProjClone_06_00_CLOofCLO( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    #clone proj into CLOCLO
    out, errCode = swgit__utils.clone_repo_url( self.REPO_TSS100__CLO2_URL, self.REPO_TSS100__CLOCLO_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( self.REPO_TSS100__CLO2_URL, self.REPO_TSS100__CLOCLO_DIR, REPO_TSS100__DEVBRANCH, out) )

    clo2_helpmap   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    cloclo_helpmap = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCLO_DIR  )

    #inside CLOCLO, check origin is on CLO2
    for clo2_h,cloclo_h in zip( clo2_helpmap.values(), cloclo_helpmap.values() ):
      cloclo_url, errCode = cloclo_h.get_cfg( "remote.origin.url" )
      self.assertEqual( errCode, 0, \
                        "FAILED retrieving option remote.origin.url into repo %s" % ( cloclo_h.getDir()) )
      clo2_url = "%s%s" % ( TESTER_SSHACCESS, clo2_h.getDir() )
      self.assertEqual( cloclo_url, clo2_url, \
                        "FAILED cloning repo %s, wrong origin url %s, instead of %s" % \
                        ( cloclo_h.getDir(), cloclo_url, clo2_url) )


  def test_ProjClone_06_01_CLO_remotized( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp()

    #
    # GO onto origin, move away from LIV to develop
    #   localize all repositories
    #
    TSS100_DEV_BR = PROJ_TSS100_DESCRIPTION[0][2]
    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    ori_helpmap["TSS100"].int_branch_set( TSS100_DEV_BR )
    ori_helpmap["TSS100"].branch_switch_to_int()
    ori_helpmap["TSS100"].proj_UNinit()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    clo2_helpmap   = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )

    #inside CLOCLO, check origin is on CLO2
    for ori_h, clo2_h in zip( ori_helpmap.values(), clo2_helpmap.values() ):
      clo2_url, errCode = clo2_h.get_cfg( "remote.origin.url" )
      self.assertEqual( errCode, 0, \
                        "FAILED retrieving option remote.origin.url into repo %s" % ( clo2_h.getDir()) )
      ori_url = "%s%s" % ( TESTER_SSHACCESS, ori_h.getDir() )
      self.assertEqual( clo2_url, ori_url, \
                        "FAILED cloning repo %s, wrong origin url %s, instead of %s" % \
                        ( clo2_h.getDir(), clo2_url, ori_url) )


  def test_ProjClone_06_02_CLO_localized( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp()

    #
    # GO onto origin, move away from LIV to develop
    #   localize all repositories
    #
    TSS100_DEV_BR = PROJ_TSS100_DESCRIPTION[0][2]
    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    ori_helpmap["TSS100"].int_branch_set( TSS100_DEV_BR )
    ori_helpmap["TSS100"].branch_switch_to_int()
    ori_helpmap["TSS100"].proj_init()

    #clone proj into CLO2
    out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    clo2_helpmap     = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    ORI_ROOT = url_parse( PROJ_TSS100_DESCRIPTION[0][1] )["ROOT"]
    ori_like_a_clone_helpmap = self.util_get_TSS10FULL_helper_map_clone( ORI_ROOT )

    #inside CLOCLO, check origin is on CLO2
    for ori_h, clo2_h in zip( ori_like_a_clone_helpmap.values(), clo2_helpmap.values() ):
      clo2_url, errCode = clo2_h.get_cfg( "remote.origin.url" )
      self.assertEqual( errCode, 0, \
                        "FAILED retrieving option remote.origin.url into repo %s" % ( clo2_h.getDir()) )
      ori_url = "%s%s" % ( TESTER_SSHACCESS, ori_h.getDir() )
      self.assertEqual( clo2_url, ori_url, \
                        "FAILED cloning repo %s, wrong origin url %s, instead of %s" % \
                        ( clo2_h.getDir(), clo2_url, ori_url) )



  def test_ProjClone_07_00_Clone_NOREC_1PROJ_2DEVrepo( self ):
    self.util_createAndCheck_PLAT_FULL_withbkp()

    PLAT_DEV_BR = PROJ_PLAT_DESCRIPTION[0][2]
    ori_hm  = self.util_get_PLATFULL_helper_map_orig()
    ori_hm["PLAT"].int_branch_set( PLAT_DEV_BR )
    ori_hm["PLAT"].branch_switch_to_int()
    ori_hm["PLAT"].proj_UNinit()

    #
    # clone proj into CLO2
    # with NOREC => only root is created
    #
    out, errCode = swgit__utils.clone_repo_url_norec( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url_norec( %s, %s, %s ) NOREC FAILED - \n%s\n" % \
                      ( REPO_PLAT__ORI_URL, self.REPO_PLAT__CLO2_DIR, REPO_PLAT__DEVBRANCH, out) )

    clo2_hm = self.util_get_PLATFULL_helper_map_clone( self.REPO_PLAT__CLO2_DIR )

    self.assertTrue( os.path.exists( clo2_hm["PLAT"].getDir() ), "FAILED CREATE directory %s" % clo2_hm["PLAT"].getDir() )

    for h in ( clo2_hm["DEVFS"], clo2_hm["DEVAPP"] ):
      self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT CREATE directory %s" % h.getDir() )


    #
    # INIT will clone everithing
    #
    clo2_hm["PLAT"].proj_init()

    #like in Test_ProjClone.test_ProjClone_00_00_Clone_1PROJ_2DEVrepo

    #check DEV fs
    repo_bi = PROJ_PLAT_DESCRIPTION[1][0]
    fs_clone_helper = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, fs_clone_helper,
                                                      self.swu_PLAT_ORI, self.swu_FS_ORI,
                                                      repo_bi )

    #check DEV app
    repo_bi = PROJ_PLAT_DESCRIPTION[1][1]
    app_clone_helper = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, app_clone_helper,
                                                      self.swu_PLAT_ORI, self.swu_APP_ORI,
                                                      repo_bi )

    #
    # UNINIT will delete everithing
    #
    clo2_hm["PLAT"].proj_UNinit()

    for h in ( clo2_hm["DEVFS"], clo2_hm["DEVAPP"] ):
      self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST BE DELETED directory %s" % h.getDir() )

    CONFIG_KEY = "submodule.%s.url"
    for n in ( "TEST_PROJ_REPO_FS", "TEST_PROJ_REPO_APP" ):
      CONFIG = CONFIG_KEY % n
      val, errCode = get_cfg( CONFIG )
      self.assertEqual( errCode, 1, "MUST BE UNSET %s" % CONFIG )

    #
    # INIT only TEST_PROJ_REPO_FS
    #
    clo2_hm["PLAT"].proj_init( "TEST_PROJ_REPO_FS" )
    h = clo2_hm["DEVAPP"]
    self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT BE CREATED directory %s" % h.getDir() )

    #check DEV fs
    repo_bi = PROJ_PLAT_DESCRIPTION[1][0]
    fs_clone_helper = swgit__utils( self.REPO_PLAT__CLO2_DIR + "/" + repo_bi[0] )
    self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, fs_clone_helper,
                                                      self.swu_PLAT_ORI, self.swu_FS_ORI,
                                                      repo_bi )



  def test_ProjClone_07_01_Clone_NOREC_1PROJ_1DEVproj_1CSTproj_1DEVrepo_1CSTrepo( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp()

    TSS100_DEV_BR = PROJ_TSS100_DESCRIPTION[0][2]
    ori_hm = self.util_get_TSS10FULL_helper_map_orig()
    ori_hm["TSS100"].int_branch_set( TSS100_DEV_BR )
    ori_hm["TSS100"].branch_switch_to_int()
    ori_hm["TSS100"].proj_UNinit()

    #
    # clone proj into CLO2
    # with NOREC => only root is created
    #
    out, errCode = swgit__utils.clone_repo_url_norec( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    self.assertEqual( errCode, 0, "clone_repo_url_norec( %s, %s, %s ) FAILED - \n%s\n" % \
                      ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    clo2_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )

    self.assertTrue( os.path.exists( clo2_hm["TSS100"].getDir() ), "FAILED CREATE directory %s" % clo2_hm["TSS100"].getDir() )

    for h in ( clo2_hm["DEVTDM"], clo2_hm["DEVPLAT"], clo2_hm["CSTPLAT"],
               clo2_hm["CSTTDM"], clo2_hm["DEVFS"], clo2_hm["DEVAPP"],
               clo2_hm["CSTFS"], clo2_hm["CSTAPP"] ):
      self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT CREATE directory %s" % h.getDir() )

    #
    # INIT will clone everithing
    #
    clo2_hm["TSS100"].proj_init()

    #like in Test_ProjClone.test_ProjClone_04_00_Clone_1PROJ_1DEVproj_1CSTproj_1DEVrepo_1CSTrepo

    #check DEV TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo2_hm["TSS100"], clo2_hm["DEVTDM"],
                                                      ori_hm["TSS100"], ori_hm["DEVTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][0] )

    #check DEV PLAT PROJ, so also all its subsubrepos
    self.util_check_DEV_clonedPROJ_consinstency( clo2_hm["TSS100"], clo2_hm["DEVPLAT"],
                                                 ori_hm["TSS100"], ori_hm["DEVPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][1],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 

    #check CST PLAT PROJ, so also all its subsubrepos
    self.util_check_CST_clonedPROJ_consinstency( clo2_hm["TSS100"], clo2_hm["CSTPLAT"],
                                                 ori_hm["TSS100"], ori_hm["CSTPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][2],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

    #check CST TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo2_hm["TSS100"], clo2_hm["CSTTDM"],
                                                      ori_hm["TSS100"], ori_hm["CSTTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][3] )

    #
    # UNINIT will delete everithing
    #
    clo2_hm["TSS100"].proj_UNinit()

    for h in ( clo2_hm["DEVTDM"], clo2_hm["DEVPLAT"], clo2_hm["CSTPLAT"],
               clo2_hm["CSTTDM"], clo2_hm["DEVFS"], clo2_hm["DEVAPP"],
               clo2_hm["CSTFS"], clo2_hm["CSTAPP"] ):
      self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT CREATE directory %s" % h.getDir() )

    CONFIG_KEY = "submodule.%s.url"
    for n in ( "TEST_PROJ_REPO_TDM", "DEV/TEST_PROJ_REPO_PLAT", "CST/TEST_PROJ_REPO_PLAT", 
               "CST-TEST_PROJ_REPO_TDM", "TEST_PROJ_REPO_APP", "TEST_PROJ_REPO_FS" ):
      CONFIG = CONFIG_KEY % n
      val, errCode = get_cfg( CONFIG )
      self.assertEqual( errCode, 1, "MUST BE UNSET %s" % CONFIG )


    #
    # INIT 1 by one
    #
    clo2_hm["TSS100"].proj_init( "TEST_PROJ_REPO_TDM" )
    for h in ( clo2_hm["DEVPLAT"], clo2_hm["CSTPLAT"],
               clo2_hm["CSTTDM"], clo2_hm["DEVFS"], clo2_hm["DEVAPP"],
               clo2_hm["CSTFS"], clo2_hm["CSTAPP"] ):
      self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT CREATE directory %s" % h.getDir() )

    #check DEV TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo2_hm["TSS100"], clo2_hm["DEVTDM"],
                                                      ori_hm["TSS100"], ori_hm["DEVTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][0] )

    clo2_hm["TSS100"].proj_init( "DEV/TEST_PROJ_REPO_PLAT" )
    for h in ( clo2_hm["CSTPLAT"], clo2_hm["CSTTDM"], 
               clo2_hm["CSTFS"], clo2_hm["CSTAPP"] ):
      self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT CREATE directory %s" % h.getDir() )

    #check DEV PLAT PROJ, so also all its subsubrepos
    self.util_check_DEV_clonedPROJ_consinstency( clo2_hm["TSS100"], clo2_hm["DEVPLAT"],
                                                 ori_hm["TSS100"], ori_hm["DEVPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][1],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 


    clo2_hm["TSS100"].proj_init( "CST/TEST_PROJ_REPO_PLAT" )
    h = clo2_hm["CSTTDM"]
    self.assertFalse( os.path.exists( h.getDir() + "/.git" ), "MUST NOT CREATE directory %s" % h.getDir() )

    #check CST PLAT PROJ, so also all its subsubrepos
    self.util_check_CST_clonedPROJ_consinstency( clo2_hm["TSS100"], clo2_hm["CSTPLAT"],
                                                 ori_hm["TSS100"], ori_hm["CSTPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][2],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

    clo2_hm["TSS100"].proj_init( "CST-TEST_PROJ_REPO_TDM" )

    #check CST TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo2_hm["TSS100"], clo2_hm["CSTTDM"],
                                                      ori_hm["TSS100"], ori_hm["CSTTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][3] )



if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()



