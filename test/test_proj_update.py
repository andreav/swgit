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


class Test_ProjUpdate( Test_ProjBase ):

  #This method is executed before each test_*
  def setUp( self ):
    super( Test_ProjUpdate, self ).setUp()


  #This method is executed after each test_*
  def tearDown( self ):
    super( Test_ProjUpdate, self ).tearDown()

  def test_ProjUpdate_00_00_clone_reset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLO2
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    clo_helpmap = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )

    #reset HEAD
    clo_helpmap["TSS100"].proj_reset( "HEAD" )

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
    # all DEV repos are on same INT/develop TIP (no develop in any repo)
    #
    for clo2_h, orig_h in zip( [ clo_helpmap["DEVTDM"], clo_helpmap["DEVPLAT"], clo_helpmap["DEVFS"], clo_helpmap["DEVAPP"] ],
                               [ ori_helpmap["CSTTDM"], ori_helpmap["DEVPLAT"], ori_helpmap["DEVFS"], ori_helpmap["DEVAPP"] ] ):

      ib = clo2_h.int_branch_get()[0]

      sha_orig   = orig_h.get_currsha( ib )[0] #must retireve ib from clone, because not set on origin
      sha_cloned = clo2_h.get_currsha()[0]
      self.assertEqual( sha_orig,
                        sha_cloned,
                        "\nCloning and immedeately reset." + \
                        "\nNo develop on origin repos." + \
                        "\nCloned repos must stay on same sha of original repos" + \
                        "\nCloned repo: %s,\ncloned sha [%s],\norig repo: %s,\norig sha [%s]" % \
                        ( clo2_h.getDir(), sha_cloned, orig_h.getDir(), sha_orig ) )

    #
    # all first level CST repos are on CST-branch TIP
    #
    for clo2_h, orig_h in zip( [ clo_helpmap["CSTTDM"], clo_helpmap["CSTPLAT"] ],
                               [ ori_helpmap["CSTTDM"], ori_helpmap["CSTPLAT"] ] ):

      sha_orig   = orig_h.get_currsha( CST_BRANCH_FULLNAME )[0]
      sha_cloned = clo2_h.get_currsha()[0]
      self.assertEqual( sha_orig,
                        sha_cloned,
                        "\nCloning and immedeately reset." + \
                        "\nNo develop on origin repos." + \
                        "\nFirst level CST repos must stay on CST branch" + \
                        "\nCloned repo: [%s]\ncloned sha [%s]\norig repo: [%s]\norig sha [%s]" % \
                        ( clo2_h.getDir(), sha_cloned, orig_h.getDir(), sha_orig ) )

    #
    # all second level CST repos are on map value 
    #
    sha_proj   = clo_helpmap["CSTPLAT"].proj_getrepo_chk( PROJ_PLAT_DESCRIPTION[1][0][0] )[0]
    sha_cloned = clo_helpmap["CSTFS"].get_currsha()[0]
    self.assertEqual( sha_proj,
                      sha_cloned,
                      "\nCloning and immedeately reset." + \
                      "\nNo develop on origin repos." + \
                      "\nSecond level CST repos must stay on map commit" + \
                      "\ncloned repo: [%s]\nrepo sha [%s]\nproj sha [%s]" % \
                      ( clo_helpmap["CSTTDM"].getDir(), sha_cloned, sha_proj ) )

    sha_orig   = clo_helpmap["CSTPLAT"].proj_getrepo_chk( PROJ_PLAT_DESCRIPTION[1][1][0] )[0]
    sha_cloned = clo_helpmap["CSTAPP"].get_currsha()[0]
    self.assertEqual( sha_orig,
                      sha_cloned,
                      "\nCloning and immedeately reset." + \
                      "\nNo develop on origin repos." + \
                      "\nSecond level CST repos must stay on map commit" + \
                      "\ncloned repo: [%s]\nrepo sha [%s]\nproj sha [%s]" % \
                      ( clo_helpmap["CSTAPP"].getDir(), sha_cloned, sha_orig ) )


  def test_ProjUpdate_00_01_clone_reset_1by1( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLO2
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLO2_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    clo_helpmap = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )

    clo_sha_map_clonetime = self.util_map2_currshas( clo_helpmap )

    #
    # reset HEAD 1 by 1
    #
    clo_helpmap["TSS100"].proj_reset( "HEAD", tss100_name2path( "DEVTDM" ) )
    clo_helpmap["TSS100"].proj_reset( "HEAD", tss100_name2path( "DEVPLAT" ) )
    clo_helpmap["TSS100"].proj_reset( "HEAD", tss100_name2path( "CSTPLAT" ) )
    clo_helpmap["TSS100"].proj_reset( "HEAD", tss100_name2path( "CSTTDM" ) )


    clo_sha_map_afterreset_1by1 = self.util_map2_currshas( clo_helpmap )

    self.util_assert_EQ_UNEQ_maps( clo_sha_map_clonetime, 
                                   clo_sha_map_afterreset_1by1, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   "FAILED modify_repo inside %s" % clo_helpmap["TSS100"].getDir()
                                 )

  def test_ProjUpdate_00_02_CrossPull( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLO2_DIR )
    ori_helpmap = self.util_get_TSS10FULL_helper_map_orig()
    clo_helpmap = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLO2_DIR )
    clo_sha_map_clonetime = self.util_map2_currshas( clo_helpmap )
    #make a modif into repo A, exec a pull into repo B
    clo_helpmap["DEVTDM"].branch_create( self.MOD_DEVTDM_BR )
    clo_helpmap["DEVTDM"].modify_file( tss100_name2file("DEVTDM"), msg = "modified a side repository" )
    out, errCode = clo_helpmap["DEVPLAT"].pull()
    self.util_check_SUCC_scenario( out, errCode, "", "Should be possible pulling from another repo under same project" )

    out, errCode = clo_helpmap["TSS100"].proj_update()
    self.util_check_DENY_scenario( out, errCode, 
                                  "Locally modified file(s) detected.", 
                                  "Should NOT be possible updating whole proj" )

    out, errCode = clo_helpmap["DEVPLAT"].proj_update()
    self.util_check_SUCC_scenario( out, errCode, "", "Should be possible updating a contained proj" )



  # Test:
  #   va works into subrepo and committed
  #   ca works and push subrepo
  #   va issue a proj --update from side branch
  #
  # Result:
  #   YES subrepo develop upgrade
  #   YES side merge on subrepo on va branch
  def test_ProjUpdate_01_00_00_YESMERGE_DEVrepo_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["DEVTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_devtdm_ca = clo_cappa_hm["DEVTDM"].get_currsha()[0]
    clo_cappa_hm["DEVTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check DEVTDM moved
    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].tag_dev( "modif - valle inside DEVTDM" )

    va_sha_map_after_repo_push = self.util_map2_currshas( clo_valle_hm )


    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )

    sha_devtdm_va = clo_valle_hm["DEVTDM"].get_currsha( "HEAD^2^2" )[0] #first parent must be other contribute
    self.assertEqual( sha_devtdm_ca,
                      sha_devtdm_va,
                      "After proj --update no side merge done" )


  # Test:
  # like test_ProjUpdate_01_00_00 but proj_update instead of proj_update_yesmerge
  #
  # Result:
  #   YES subrepo develop upgrade
  #   NO side merge on subrepo on va branch
  def test_ProjUpdate_01_00_01_DEFAULT_DEVrepo_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["DEVTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_devtdm_ca = clo_cappa_hm["DEVTDM"].get_currsha()[0]
    clo_cappa_hm["DEVTDM"].push_with_merge()
    clo_cappa_hm["DEVTDM"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check DEVTDM moved
    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].tag_dev( "modif - valle inside DEVTDM" )

    va_sha_map_after_repo_push = self.util_map2_currshas( clo_valle_hm )


    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    va_sha_devtdm_intbr = clo_valle_hm["DEVTDM"].get_currsha( REPO_TDM__DEVBRANCH )[0] #first parent must be other contribute
    #va DEVTDM went on develop and pulled from ca
    self.assertEqual( va_sha_map_after_update["DEVTDM"],
                      va_sha_devtdm_intbr,
                      "After proj --update va not gone onto intbr" )


  # Test:
  # like test_ProjUpdate_01_00_00 but proj_update_nomerge instead of proj_update_yesmerge
  #
  # Result:
  #   NO subrepo develop upgrade (only remote branch moves)
  #   NO side merge on subrepo on va branch
  def test_ProjUpdate_01_00_02_NOMERGE_DEVrepo_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["DEVTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_devtdm_ca = clo_cappa_hm["DEVTDM"].get_currsha()[0]
    clo_cappa_hm["DEVTDM"].push_with_merge()
    clo_cappa_hm["DEVTDM"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check DEVTDM moved
    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].tag_dev( "modif - valle inside DEVTDM" )

    va_sha_map_after_repo_push = self.util_map2_currshas( clo_valle_hm )


    ####################################
    clo_valle_hm["TSS100"].proj_update_nomerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )

    #everithing came back (also DEVTDM)
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #but ca contributes have been pulled
    # i.e. try switching onto cappa branch
    out, errCode = clo_valle_hm["DEVTDM"].branch_switch_to_br( self.MOD_DEVTDM_BR + "_ca" )
    # No need to download other history, not downloaded branch_ca
    #self.util_check_SUCC_scenario( out, errCode, "", "switch back to new imported  br" )
    self.util_check_DENY_scenario( out, errCode, "", "switch back to new imported  br" )


  # Test:
  #   va works into subrepo but now is in detached
  #   ca works and push subrepo
  #   va issue a proj --update from detached
  #
  # Result:
  #   YES subrepo develop upgrade
  #   NO  side merge on subrepo because va was in detached
  def test_ProjUpdate_01_01_00_YESMERGE_DEVrepo_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["DEVTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_devtdm_ca = clo_cappa_hm["DEVTDM"].get_currsha()[0]
    clo_cappa_hm["DEVTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check DEVTDM moved
    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle 1 inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle 2 inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].branch_switch_to_br( "HEAD~1" )

    sha_devtdm_va_before_update = clo_valle_hm["DEVTDM"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    sha_devtdm_va_after_update = clo_valle_hm["DEVTDM"].get_currsha()[0]

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )

    self.assertNotEqual( sha_devtdm_va_before_update,
                         sha_devtdm_va_after_update,
                         "After proj --update HEAD must be changed" )

    self.assertNotEqual( ca_sha_map_after_repo_push["DEVTDM"],
                         sha_devtdm_va_after_update,
                         "After proj --update HEAD must be changed" )


  # Test:
  # like test_ProjUpdate_01_01_00 but proj_update instead of proj_update_yesmerge
  #
  # Result:
  #   YES subrepo develop upgrade
  #   NO  side merge on subrepo because va was in detached and because proj_update should never do merge
  def test_ProjUpdate_01_01_01_DEFAULT_DEVrepo_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["DEVTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_devtdm_ca = clo_cappa_hm["DEVTDM"].get_currsha()[0]
    clo_cappa_hm["DEVTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check DEVTDM moved
    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle 1 inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle 2 inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].branch_switch_to_br( "HEAD~1" )

    sha_devtdm_va_before_update = clo_valle_hm["DEVTDM"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    sha_devtdm_va_after_update = clo_valle_hm["DEVTDM"].get_currsha()[0]

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )

    self.assertNotEqual( sha_devtdm_va_before_update,
                         sha_devtdm_va_after_update,
                         "After proj --update HEAD must be changed" )

    self.assertNotEqual( ca_sha_map_after_repo_push["DEVTDM"],
                         sha_devtdm_va_after_update,
                         "After proj --update HEAD must be changed" )


  # Test:
  # like test_ProjUpdate_01_01_00 but proj_update_nomerge instead of proj_update_yesmerge
  #
  # Result:
  #   YES subrepo develop upgrade
  #   NO  side merge on subrepo because va was in detached and because proj_update_nomerge should never do merge
  def test_ProjUpdate_01_01_02_NOMERGE_DEVrepo_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["DEVTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_devtdm_ca = clo_cappa_hm["DEVTDM"].get_currsha()[0]
    clo_cappa_hm["DEVTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check DEVTDM moved
    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["DEVTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle 1 inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].modify_repo( msg = "modif - valle 2 inside DEVTDM", gotoint = False )
    clo_valle_hm["DEVTDM"].branch_switch_to_br( "HEAD~1" )

    sha_devtdm_va_before_update = clo_valle_hm["DEVTDM"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update_nomerge()
    ####################################

    sha_devtdm_va_after_update = clo_valle_hm["DEVTDM"].get_currsha()[0]

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVTDM" ],
                                   msg
                                 )

    self.assertNotEqual( sha_devtdm_va_before_update,
                         sha_devtdm_va_after_update,
                         "After proj --update HEAD must be changed" )

    self.assertNotEqual( ca_sha_map_after_repo_push["DEVTDM"],
                         sha_devtdm_va_after_update,
                         "After proj --update HEAD must be changed" )

  # Test:
  #   va works only into root project (DEVPLAT)
  #   ca works into root project and subrepo
  #   va issue a proj --update to refresh proj and subrepo
  #
  # Result:
  #   side merge on proj repo
  #   fast-forward on subrepo
  def test_ProjUpdate_01_02_00_YESMERGE_DEVproj_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVPLAT inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )

    sha_devplat_va = clo_valle_hm["DEVPLAT"].get_currsha( "HEAD^2^2" )[0] #first parent must be other contribute
    self.assertEqual( sha_devplat_ca,
                      sha_devplat_va,
                      "After proj --update no side merge on devplat done" )

    self.assertNotEqual( sha_devfs_va_before_update,
                         sha_devfs_va_after_update,
                         "After proj --update DEVFS must be changed" )

    self.assertEqual( sha_devfs_ca,
                      sha_devfs_va_after_update,
                      "After proj --update DEVFS must be same as cappa" )


  # Test:
  # like test_ProjUpdate_01_02_00 but proj_update instead of proj_update_yesmerge
  #
  # Result:
  #   NO side merge on proj repo
  #   fast-forward on subrepo
  def test_ProjUpdate_01_02_01_DEFAULT_DEVproj_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )
    clo_cappa_hm["DEVPLAT"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVPLAT inside %s" % clo_valle_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

  # Test:
  # like test_ProjUpdate_01_02_00 but proj_update_nomerge instead of proj_update_yesmerge
  #
  # Result:
  #   NO side merge on proj repo
  #   fast-forward on subrepo
  #
  # Note:
  #   unnecessary history is not downloaded (of DEVFS)
  #
  #
  # Test 2:
  #   va comes back onto sidebr and issues a proj --update
  #   va will download also new history, and mooves on
  def test_ProjUpdate_01_02_02_NOMERGE_DEVproj_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )
    clo_cappa_hm["DEVPLAT"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update_nomerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_valle_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )

    #everithing came back (also DEVPLAT)
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #and ca contributes inside subrepo are not pulled (because not necessary)
    # i.e. try switching onto cappa branch
    out, errCode = clo_valle_hm["DEVFS"].branch_switch_to_br( self.MOD_DEVFS_BR + "_ca" )
    self.util_check_DENY_scenario( out, errCode, "", "switch to br %s must fail because this history is not necessary" )


    #
    # Test 2
    #
    clo_valle_hm["DEVPLAT"].branch_switch_to_br( self.MOD_DEVPLAT_BR + "_va" )
    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_second_update = self.util_map2_currshas( clo_cappa_hm )

    msg = "FAILED modify/push of DEVPLAT inside %s" % clo_valle_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   va_sha_map_after_second_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #NOW ca contributes inside subrepo are pulled
    # i.e. try switching onto cappa branch
    out, errCode = clo_valle_hm["DEVFS"].branch_switch_to_br( self.MOD_DEVFS_BR + "_ca" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch to br %s must fail because this history is not necessary" )


  # Test:
  #   va works only into root project (DEVPLAT) and go detached
  #   ca works into root project and subrepo
  #   va issue a proj --update to refresh proj and subrepo
  #
  # Result:
  #   YES merge inside proj repo, on develop branch
  #   NO  side merge inside proj repo, onto local branch
  #   YES fast-forward on subrepo
  def test_ProjUpdate_01_03_00_YESMERGE_DEVproj_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].branch_switch_to_br( "HEAD~1" )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVPLAT inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )

    sha_va_devplat_intbr_minuone = clo_valle_hm["DEVPLAT"].get_currsha( REPO_PLAT__DEVBRANCH + "^2" )[0]
    self.assertEqual( sha_devplat_ca,
                      sha_va_devplat_intbr_minuone,
                      "After proj --update intbr must be merged from cappa" )

    self.assertEqual( sha_devfs_ca,
                      sha_devfs_va_after_update,
                      "After proj --update DEVFS must be same as cappa" )

  # Test:
  #   Like previous, but issue reset before update
  #
  # Result:
  #   Like previous because reset HEAD moves into detached in the same way and switching back manually
  def test_ProjUpdate_01_03_00_YESMERGE_DEVproj_fromCheckout_withReset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].branch_switch_to_br( "HEAD~1" )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_reset()
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVPLAT inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )

    sha_va_devplat_intbr_minuone = clo_valle_hm["DEVPLAT"].get_currsha( REPO_PLAT__DEVBRANCH + "^2" )[0]
    self.assertEqual( sha_devplat_ca,
                      sha_va_devplat_intbr_minuone,
                      "After proj --update intbr must be merged from cappa" )

    self.assertEqual( sha_devfs_ca,
                      sha_devfs_va_after_update,
                      "After proj --update DEVFS must be same as cappa" )


  # Test:
  # like test_ProjUpdate_01_03_00 but proj_update instead of proj_update_yesmerge
  #
  # Result:
  #   YES merge inside proj repo, on develop branch
  #   NO  side merge inside proj repo, onto local branch
  #   YES fast-forward on subrepo
  def test_ProjUpdate_01_03_01_DEFAULT_DEVproj_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].branch_switch_to_br( "HEAD~1" )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVPLAT inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )

    sha_va_devplat_intbr_minuone = clo_valle_hm["DEVPLAT"].get_currsha( REPO_PLAT__DEVBRANCH + "^2" )[0]
    self.assertEqual( sha_devplat_ca,
                      sha_va_devplat_intbr_minuone,
                      "After proj --update intbr must be merged from cappa" )

    self.assertEqual( sha_devfs_ca,
                      sha_devfs_va_after_update,
                      "After proj --update DEVFS must be same as cappa" )

  # Test:
  # like test_ProjUpdate_01_03_00 but proj_update_nomerge instead of proj_update_yesmerge
  #
  # Result:
  #   NO merge inside proj repo
  #   NO  side merge inside proj repo, onto local branch
  #   nO fast-forward on subrepo because unuseful
  def test_ProjUpdate_01_03_02_NOMERGE_DEVproj_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_devfs = "modif - cappa inside DEVFS"
    msg_devplat = "modif - cappa inside DEVPLAT"
    clo_cappa_hm["DEVFS"].branch_create( self.MOD_DEVFS_BR + "_ca" )
    clo_cappa_hm["DEVFS"].modify_repo( msg = msg_devfs, gotoint = False )
    clo_cappa_hm["DEVFS"].tag_dev( msg_devfs )
    clo_cappa_hm["DEVFS"].push_with_merge()
    clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_ca" )
    clo_cappa_hm["DEVPLAT"].modify_file( tss100_name2file("DEVPLAT"), msg = msg_devplat )
    clo_cappa_hm["DEVPLAT"].commit_minusA_dev_repolist( msg = msg_devplat, repolist = "-A" )
    clo_cappa_hm["DEVPLAT"].tag_dev( msg_devplat )
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_devfs_ca = ca_sha_map_after_repo_push["DEVFS"]
    sha_devplat_ca = ca_sha_map_after_repo_push["DEVPLAT"]

    #check DEVPLAT moved
    msg = "FAILED modify/push of DEVPLAT DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_devplat = "modif - valle inside DEVPLAT"
    clo_valle_hm["DEVPLAT"].branch_create( self.MOD_DEVPLAT_BR + "_va" )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].modify_repo( msg = msg_devplat, gotoint = False )
    clo_valle_hm["DEVPLAT"].branch_switch_to_br( "HEAD~1" )

    sha_devfs_va_before_update = clo_valle_hm["DEVFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update_nomerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_devfs_va_after_update = va_sha_map_after_update["DEVFS"]

    msg = "FAILED modify/push of DEVTDM inside %s" % clo_valle_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVPLAT", "DEVFS" ],
                                   msg
                                 )

    #everithing came back (also DEVPLAT)
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #and ca contributes inside subrepo are not pulled (because not necessary)
    # i.e. try switching onto cappa branch
    out, errCode = clo_valle_hm["DEVFS"].branch_switch_to_br( self.MOD_DEVFS_BR + "_ca" )
    self.util_check_DENY_scenario( out, errCode, "", "switch to br %s must fail because this history is not necessary" )



  # Test:
  #   va works into subrepo and committed
  #   ca works and push subrepo
  #   va issue a proj --update from side branch
  #
  # Result:
  #   YES CST subrepo upgrade
  #   NO  side merge on CST subrepo on va branch
  #   YES come back to clone point inside va CST repo (git submodule update does so)
  #
  # Test2:
  #   va comes back onto side branch
  #   ca freezes CST advancement into TSS100
  #   va issue a proj --update from side branch
  #
  # Result2:
  #   NO  side merge on CST subrepo on va branch
  #   YES move to new CST position into CST va
  def test_ProjUpdate_01_04_00_YESMERGE_CSTrepo_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["CSTTDM"].branch_switch_to_int()
    clo_cappa_hm["CSTTDM"].branch_create( self.MOD_CSTTDM_BR + "_ca" )
    clo_cappa_hm["CSTTDM"].modify_repo( msg = "modif - cappa inside CSTTDM", gotoint = False )
    clo_cappa_hm["CSTTDM"].tag_dev( "modif - cappa inside CSTTDM" )
    clo_cappa_hm["CSTTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_csttdm_ca = ca_sha_map_after_repo_push["CSTTDM"]

    #check CSTTDM moved
    msg = "FAILED modify/push of CSTTDM inside %s" % clo_cappa_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTTDM" ],
                                   msg
                                 )



    clo_valle_hm["CSTTDM"].branch_switch_to_int()
    clo_valle_hm["CSTTDM"].branch_create( self.MOD_CSTTDM_BR + "_va" )
    clo_valle_hm["CSTTDM"].modify_repo( msg = "modif - valle inside CSTTDM", gotoint = False )
    clo_valle_hm["CSTTDM"].tag_dev( "modif - valle inside CSTTDM" )

    va_sha_map_after_repo_push = self.util_map2_currshas( clo_valle_hm )


    #
    #update, CSTTDM has developed
    #
    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_valle_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #
    # Test 2 
    #
    msg_tss100 = "modif - cappa inside TSS100 freeze CSTTDM"
    clo_cappa_hm["TSS100"].branch_switch_to_int()
    clo_cappa_hm["TSS100"].branch_create( self.MOD_CSTTDM_BR + "_ca" )
    clo_cappa_hm["TSS100"].commit_dev_repolist( msg = msg_tss100, repolist = "-A" )
    clo_cappa_hm["TSS100"].tag_dev( msg_tss100 )
    clo_cappa_hm["TSS100"].push_with_merge( remote )
    clo_cappa_hm["TSS100"].branch_switch_to_int()

    ca_sha_map_after_second_push = self.util_map2_currshas( clo_cappa_hm )

    #va comes back to side branch
    out, errCode = clo_valle_hm["CSTTDM"].branch_switch_to_br( self.MOD_CSTTDM_BR + "_va" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch back to br" )

    #
    #update, CSTPLAT has developed
    #
    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################
    va_sha_map_after_second_update = self.util_map2_currshas( clo_cappa_hm )

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_valle_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_second_update, 
                                   [], # all other must be eq
                                   [ "TSS100", "CSTTDM" ],
                                   msg
                                 )

    #sha_csttdm_va = clo_valle_hm["CSTTDM"].get_currsha( "HEAD^2^2" )[0] #first parent must be other contribute
    sha_csttdm_va = va_sha_map_after_second_update["CSTTDM"]
    self.assertEqual( sha_csttdm_ca,
                      sha_csttdm_va,
                      "After proj --update no side merge done" )


  # Test:
  #  like test_ProjUpdate_01_04_00 but proj_update instead of proj_update_yesmerge
  #
  # Result:
  #  Must be the same as test_ProjUpdate_01_04_00 because 
  #    no difference among --update -I and --update for CST repos
  #
  def test_ProjUpdate_01_04_01_DEFAULT_CSTrepo_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["CSTTDM"].branch_switch_to_int()
    clo_cappa_hm["CSTTDM"].branch_create( self.MOD_CSTTDM_BR + "_ca" )
    clo_cappa_hm["CSTTDM"].modify_repo( msg = "modif - cappa inside CSTTDM", gotoint = False )
    clo_cappa_hm["CSTTDM"].tag_dev( "modif - cappa inside CSTTDM" )
    clo_cappa_hm["CSTTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_csttdm_ca = ca_sha_map_after_repo_push["CSTTDM"]

    #check CSTTDM moved
    msg = "FAILED modify/push of CSTTDM inside %s" % clo_cappa_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTTDM" ],
                                   msg
                                 )



    clo_valle_hm["CSTTDM"].branch_switch_to_int()
    clo_valle_hm["CSTTDM"].branch_create( self.MOD_CSTTDM_BR + "_va" )
    clo_valle_hm["CSTTDM"].modify_repo( msg = "modif - valle inside CSTTDM", gotoint = False )
    clo_valle_hm["CSTTDM"].tag_dev( "modif - valle inside CSTTDM" )

    va_sha_map_after_repo_push = self.util_map2_currshas( clo_valle_hm )


    #
    #update, CSTTDM has developed
    #
    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_valle_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #
    # Test 2 
    #
    msg_tss100 = "modif - cappa inside TSS100 freeze CSTTDM"
    clo_cappa_hm["TSS100"].branch_switch_to_int()
    clo_cappa_hm["TSS100"].branch_create( self.MOD_CSTTDM_BR + "_ca" )
    clo_cappa_hm["TSS100"].commit_dev_repolist( msg = msg_tss100, repolist = "-A" )
    clo_cappa_hm["TSS100"].tag_dev( msg_tss100 )
    clo_cappa_hm["TSS100"].push_with_merge( remote )
    clo_cappa_hm["TSS100"].branch_switch_to_int()

    ca_sha_map_after_second_push = self.util_map2_currshas( clo_cappa_hm )

    #va comes back to side branch
    out, errCode = clo_valle_hm["CSTTDM"].branch_switch_to_br( self.MOD_CSTTDM_BR + "_va" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch back to br" )

    #
    #update, CSTPLAT has developed
    #
    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################
    va_sha_map_after_second_update = self.util_map2_currshas( clo_cappa_hm )

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_valle_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_second_update, 
                                   [], # all other must be eq
                                   [ "TSS100", "CSTTDM" ],
                                   msg
                                 )

    #sha_csttdm_va = clo_valle_hm["CSTTDM"].get_currsha( "HEAD^2^2" )[0] #first parent must be other contribute
    sha_csttdm_va = va_sha_map_after_second_update["CSTTDM"]
    self.assertEqual( sha_csttdm_ca,
                      sha_csttdm_va,
                      "After proj --update no side merge done" )


  # Test:
  #  like test_ProjUpdate_01_04_00 but proj_update_nomerge instead of proj_update_yesmerge
  #
  # Result:
  #  Must be the same as test_ProjUpdate_01_04_00 because 
  #    no difference among --update -I and --update for CST repos
  #
  def test_ProjUpdate_01_04_02_NOMERGE_CSTrepo_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["CSTTDM"].branch_switch_to_int()
    clo_cappa_hm["CSTTDM"].branch_create( self.MOD_CSTTDM_BR + "_ca" )
    clo_cappa_hm["CSTTDM"].modify_repo( msg = "modif - cappa inside CSTTDM", gotoint = False )
    clo_cappa_hm["CSTTDM"].tag_dev( "modif - cappa inside CSTTDM" )
    clo_cappa_hm["CSTTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_csttdm_ca = ca_sha_map_after_repo_push["CSTTDM"]

    #check CSTTDM moved
    msg = "FAILED modify/push of CSTTDM inside %s" % clo_cappa_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTTDM" ],
                                   msg
                                 )



    clo_valle_hm["CSTTDM"].branch_switch_to_int()
    clo_valle_hm["CSTTDM"].branch_create( self.MOD_CSTTDM_BR + "_va" )
    clo_valle_hm["CSTTDM"].modify_repo( msg = "modif - valle inside CSTTDM", gotoint = False )
    clo_valle_hm["CSTTDM"].tag_dev( "modif - valle inside CSTTDM" )

    va_sha_map_after_repo_push = self.util_map2_currshas( clo_valle_hm )


    #
    #update, CSTTDM has developed
    #
    ####################################
    clo_valle_hm["TSS100"].proj_update_nomerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_valle_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )

    #
    # Test 2 
    #
    msg_tss100 = "modif - cappa inside TSS100 freeze CSTTDM"
    clo_cappa_hm["TSS100"].branch_switch_to_int()
    clo_cappa_hm["TSS100"].branch_create( self.MOD_CSTTDM_BR + "_ca" )
    clo_cappa_hm["TSS100"].commit_dev_repolist( msg = msg_tss100, repolist = "-A" )
    clo_cappa_hm["TSS100"].tag_dev( msg_tss100 )
    clo_cappa_hm["TSS100"].push_with_merge( remote )
    clo_cappa_hm["TSS100"].branch_switch_to_int()

    ca_sha_map_after_second_push = self.util_map2_currshas( clo_cappa_hm )

    #va comes back to side branch
    out, errCode = clo_valle_hm["CSTTDM"].branch_switch_to_br( self.MOD_CSTTDM_BR + "_va" )
    self.util_check_SUCC_scenario( out, errCode, "", "switch back to br" )

    #
    #update, CSTPLAT has developed
    #
    ####################################
    clo_valle_hm["TSS100"].proj_update_nomerge()
    ####################################
    va_sha_map_after_second_update = self.util_map2_currshas( clo_cappa_hm )

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_valle_hm["CSTTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_second_update, 
                                   [], # all other must be eq
                                   [ "TSS100", "CSTTDM" ],
                                   msg
                                 )

    #sha_csttdm_va = clo_valle_hm["CSTTDM"].get_currsha( "HEAD^2^2" )[0] #first parent must be other contribute
    sha_csttdm_va = va_sha_map_after_second_update["CSTTDM"]
    self.assertEqual( sha_csttdm_ca,
                      sha_csttdm_va,
                      "After proj --update no side merge done" )


  # Test:
  #   va works into subrepo but now is in detached
  #   ca works and push subrepo
  #   va issue a proj --update from detached
  #
  # Result:
  #   YES subrepo develop upgrade
  #   NO  side merge on subrepo because va was in detached
  def test_ProjUpdate_01_05_00_YESMERGE_CSTrepo_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["CSTTDM"].branch_switch_to_int()
    clo_cappa_hm["CSTTDM"].branch_create( self.MOD_DEVTDM_BR + "_ca" )
    clo_cappa_hm["CSTTDM"].modify_repo( msg = "modif - cappa inside DEVTDM", gotoint = False )
    clo_cappa_hm["CSTTDM"].tag_dev( "modif - cappa inside DEVTDM" )
    sha_csttdm_ca = clo_cappa_hm["CSTTDM"].get_currsha()[0]
    clo_cappa_hm["CSTTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check CSTTDM moved
    msg = "FAILED modify/push of CSTTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTTDM" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["CSTTDM"].branch_switch_to_int()
    clo_valle_hm["CSTTDM"].branch_create( self.MOD_DEVTDM_BR + "_va" )
    clo_valle_hm["CSTTDM"].modify_repo( msg = "modif - valle 1 inside DEVTDM", gotoint = False )
    clo_valle_hm["CSTTDM"].modify_repo( msg = "modif - valle 2 inside DEVTDM", gotoint = False )
    clo_valle_hm["CSTTDM"].branch_switch_to_br( "HEAD~1" )

    sha_csttdm_va_before_update = clo_valle_hm["CSTTDM"].get_currsha()[0]

    #update, CSTTDM has developed
    clo_valle_hm["TSS100"].proj_update_yesmerge()

    sha_csttdm_va_after_update = clo_valle_hm["CSTTDM"].get_currsha()[0]

    msg = "FAILED modify/push of CSTTDM inside %s" % clo_cappa_hm["DEVTDM"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTTDM" ],
                                   msg
                                 )

    self.assertNotEqual( sha_csttdm_va_before_update,
                         sha_csttdm_va_after_update,
                         "After proj --update HEAD must be changed" )

    self.assertNotEqual( ca_sha_map_after_repo_push["CSTTDM"],
                         sha_csttdm_va_after_update,
                         "After proj --update HEAD must be changed" )


  # Test:
  #   va works only into root project (CSTPLAT)
  #   ca works into root project and subrepo
  #   va issue a proj --update to refresh proj and subrepo
  #
  # Result:
  #   CST are only updated (not merged) => NO side merge
  #   Idem for subrepo CSTFS
  #   NO commit changes because TSS100 did not registered CSTPLAT changes
  #
  # Test 2:
  #   ca freeze into tss100 CSTPLAT progress and pushes
  #   va issue another proj --update to refresh proj and subrepo
  #
  # Result:
  #   TSS100 is updated
  #   CST are updated newly (no contribute) but move their commits onto new shas
  #

  def test_ProjUpdate_01_06_00_YESMERGE_CSTproj_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_cstfs = "modif - cappa inside CSTFS"
    msg_cstplat = "modif - cappa inside CSTPLAT"
    clo_cappa_hm["CSTFS"].int_branch_set( REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].branch_create_src( self.MOD_CSTFS_BR + "_ca", REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].modify_repo( msg = msg_cstfs, gotoint = False )
    clo_cappa_hm["CSTFS"].tag_dev( msg_cstfs )
    clo_cappa_hm["CSTFS"].push_with_merge()
    clo_cappa_hm["CSTFS"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].branch_create( self.MOD_CSTPLAT_BR + "_ca" )
    clo_cappa_hm["CSTPLAT"].modify_file( tss100_name2file("CSTPLAT"), msg = msg_cstplat )
    clo_cappa_hm["CSTPLAT"].commit_minusA_dev_repolist( msg = msg_cstplat, repolist = "-A" )
    clo_cappa_hm["CSTPLAT"].tag_dev( msg_cstplat )
    clo_cappa_hm["CSTPLAT"].push_with_merge( remote )
    clo_cappa_hm["CSTPLAT"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_cstfs_ca = ca_sha_map_after_repo_push["CSTFS"]
    sha_cstplat_ca = ca_sha_map_after_repo_push["CSTPLAT"]

    #check CSTPLAT moved
    msg = "FAILED modify/push of CSTPLAT CSTFS inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTPLAT", "CSTFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_cstplat = "modif - valle inside CSTPLAT"
    clo_valle_hm["CSTPLAT"].branch_switch_to_int()
    clo_valle_hm["CSTPLAT"].branch_create( self.MOD_CSTPLAT_BR + "_va" )
    clo_valle_hm["CSTPLAT"].modify_repo( msg = msg_cstplat, gotoint = False )

    sha_cstfs_va_before_update = clo_valle_hm["CSTFS"].get_currsha()[0]

    #update, CSTPLAT has developed
    clo_valle_hm["TSS100"].proj_update_yesmerge()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_cstfs_va_after_update = va_sha_map_after_update["CSTFS"]

    msg = "FAILED modify/push of CSTPLAT inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVFS" ], #DEVFS only because DEV and CST have same origin
                                   msg
                                 )


    #
    # Test 2, now freeze CSTPLAT into TSS100
    #
    msg_tss100 = "modif - cappa inside TSS100 freeze CSTPLAT"
    clo_cappa_hm["TSS100"].branch_create( self.MOD_TSS100_BR + "_ca" )
    clo_cappa_hm["TSS100"].commit_dev_repolist( msg = msg_tss100, repolist = "-A" )
    clo_cappa_hm["TSS100"].tag_dev( msg_tss100 )
    clo_cappa_hm["TSS100"].push_with_merge( remote )
    clo_cappa_hm["TSS100"].branch_switch_to_int()

    ca_sha_map_after_second_push = self.util_map2_currshas( clo_cappa_hm )


    #update, CSTPLAT has developed
    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    va_sha_map_after_update_2 = self.util_map2_currshas( clo_valle_hm )
    sha_cstfs_va_after_update_2 = va_sha_map_after_update_2["CSTFS"]

    msg = "FAILED modify/push of TSS100 inside %s" % clo_valle_hm["TSS100"].getDir()
    #self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_second_push, 
                                   va_sha_map_after_update_2, 
                                   [], # all other must be eq
                                   [ "DEVFS" ], #DEVFS only because DEV and CST have same origin
                                   msg
                                 )

    sha_va_cstplat = clo_valle_hm["CSTPLAT"].get_currsha()[0]
    self.assertEqual( sha_cstplat_ca,
                      sha_va_cstplat,
                      "After proj --update intbr must be merged from cappa" )

    self.assertEqual( sha_cstfs_ca,
                      sha_cstfs_va_after_update_2,
                      "After proj --update CSTFS must be same as cappa" )


    #
    # Test 3, now reset HEAD, must be the same of cappa (DEVFS come back)
    #
    clo_valle_hm["TSS100"].proj_reset()
    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of TSS100 inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_second_push, 
                                   va_sha_map_after_reset, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )


  # Test:
  # like test_ProjUpdate_01_06_00 but proj_update_default instead of proj_update_yesmerge
  #
  # Result:
  #  Must be the same as test_ProjUpdate_01_04_00 because 
  #    no difference among --update -I and --update for CST repos
  def test_ProjUpdate_01_06_01_DEFAULT_CSTproj_fromSide( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_cstfs = "modif - cappa inside CSTFS"
    msg_cstplat = "modif - cappa inside CSTPLAT"
    clo_cappa_hm["CSTFS"].int_branch_set( REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].branch_create_src( self.MOD_CSTFS_BR + "_ca", REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].modify_repo( msg = msg_cstfs, gotoint = False )
    clo_cappa_hm["CSTFS"].tag_dev( msg_cstfs )
    clo_cappa_hm["CSTFS"].push_with_merge()
    clo_cappa_hm["CSTFS"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].branch_create( self.MOD_CSTPLAT_BR + "_ca" )
    clo_cappa_hm["CSTPLAT"].modify_file( tss100_name2file("CSTPLAT"), msg = msg_cstplat )
    clo_cappa_hm["CSTPLAT"].commit_minusA_dev_repolist( msg = msg_cstplat, repolist = "-A" )
    clo_cappa_hm["CSTPLAT"].tag_dev( msg_cstplat )
    clo_cappa_hm["CSTPLAT"].push_with_merge( remote )
    clo_cappa_hm["CSTPLAT"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_cstfs_ca = ca_sha_map_after_repo_push["CSTFS"]
    sha_cstplat_ca = ca_sha_map_after_repo_push["CSTPLAT"]

    #check CSTPLAT moved
    msg = "FAILED modify/push of CSTPLAT CSTFS inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTPLAT", "CSTFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_cstplat = "modif - valle inside CSTPLAT"
    clo_valle_hm["CSTPLAT"].branch_switch_to_int()
    clo_valle_hm["CSTPLAT"].branch_create( self.MOD_CSTPLAT_BR + "_va" )
    clo_valle_hm["CSTPLAT"].modify_repo( msg = msg_cstplat, gotoint = False )

    sha_cstfs_va_before_update = clo_valle_hm["CSTFS"].get_currsha()[0]

    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_cstfs_va_after_update = va_sha_map_after_update["CSTFS"]

    msg = "FAILED modify/push of CSTPLAT inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVFS" ], #DEVFS only because DEV and CST have same origin
                                   msg
                                 )


    #
    # Test 2, now freeze CSTPLAT into TSS100
    #
    msg_tss100 = "modif - cappa inside TSS100 freeze CSTPLAT"
    clo_cappa_hm["TSS100"].branch_create( self.MOD_TSS100_BR + "_ca" )
    clo_cappa_hm["TSS100"].commit_dev_repolist( msg = msg_tss100, repolist = "-A" )
    clo_cappa_hm["TSS100"].tag_dev( msg_tss100 )
    clo_cappa_hm["TSS100"].push_with_merge( remote )
    clo_cappa_hm["TSS100"].branch_switch_to_int()

    ca_sha_map_after_second_push = self.util_map2_currshas( clo_cappa_hm )


    ####################################
    clo_valle_hm["TSS100"].proj_update()
    ####################################

    va_sha_map_after_update_2 = self.util_map2_currshas( clo_valle_hm )
    sha_cstfs_va_after_update_2 = va_sha_map_after_update_2["CSTFS"]

    msg = "FAILED modify/push of TSS100 inside %s" % clo_valle_hm["TSS100"].getDir()
    #self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_second_push, 
                                   va_sha_map_after_update_2, 
                                   [], # all other must be eq
                                   [ "DEVFS" ], #DEVFS only because DEV and CST have same origin
                                   msg
                                 )

    sha_va_cstplat = clo_valle_hm["CSTPLAT"].get_currsha()[0]
    self.assertEqual( sha_cstplat_ca,
                      sha_va_cstplat,
                      "After proj --update intbr must be merged from cappa" )

    self.assertEqual( sha_cstfs_ca,
                      sha_cstfs_va_after_update_2,
                      "After proj --update CSTFS must be same as cappa" )


    #
    # Test 3, now reset HEAD, must be the same of cappa (DEVFS come back)
    #
    clo_valle_hm["TSS100"].proj_reset()
    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    msg = "FAILED modify/push of TSS100 inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_second_push, 
                                   va_sha_map_after_reset, 
                                   [], # all other must be eq
                                   None,
                                   msg
                                 )


  def test_ProjUpdate_01_07_00_YESMERGE_CSTproj_fromCheckout( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    remote = ""
    if modetest_morerepos():
      remote   = "origin"

    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    msg_cstfs = "modif - cappa inside CSTFS"
    msg_cstplat = "modif - cappa inside CSTPLAT"
    clo_cappa_hm["CSTFS"].int_branch_set( REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].branch_create_src( self.MOD_CSTFS_BR + "_ca", REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].modify_repo( msg = msg_cstfs, gotoint = False )
    clo_cappa_hm["CSTFS"].tag_dev( msg_cstfs )
    clo_cappa_hm["CSTFS"].push_with_merge()
    clo_cappa_hm["CSTFS"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].branch_create( self.MOD_CSTPLAT_BR + "_ca" )
    clo_cappa_hm["CSTPLAT"].modify_file( tss100_name2file("CSTPLAT"), msg = msg_cstplat )
    clo_cappa_hm["CSTPLAT"].commit_minusA_dev_repolist( msg = msg_cstplat, repolist = "-A" )
    clo_cappa_hm["CSTPLAT"].tag_dev( msg_cstplat )
    clo_cappa_hm["CSTPLAT"].push_with_merge( remote )
    clo_cappa_hm["CSTPLAT"].branch_switch_to_int()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )
    sha_cstfs_ca = ca_sha_map_after_repo_push["CSTFS"]
    sha_cstplat_ca = ca_sha_map_after_repo_push["CSTPLAT"]

    #check CSTPLAT moved
    msg = "FAILED modify/push of CSTPLAT CSTFS inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTPLAT", "CSTFS" ],
                                   msg
                                 )


    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    msg_cstplat = "modif - valle inside CSTPLAT"
    clo_valle_hm["CSTPLAT"].branch_switch_to_int()
    clo_valle_hm["CSTPLAT"].branch_create( self.MOD_CSTPLAT_BR + "_va" )
    clo_valle_hm["CSTPLAT"].modify_repo( msg = msg_cstplat, gotoint = False )
    clo_valle_hm["CSTPLAT"].modify_repo( msg = msg_cstplat, gotoint = False )
    clo_valle_hm["CSTPLAT"].branch_switch_to_br( "HEAD~1" )

    sha_cstfs_va_before_update = clo_valle_hm["CSTFS"].get_currsha()[0]

    #update, CSTPLAT has developed
    ####################################
    clo_valle_hm["TSS100"].proj_update_yesmerge()
    ####################################

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )
    sha_cstfs_va_after_update = va_sha_map_after_update["CSTFS"]

    msg = "FAILED modify/push of CSTPLAT inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVFS" ], #DEVFS only because DEV and CST have same origin
                                   msg
                                 )


  # Modify DEVTDM
  def test_ProjUpdate_02_00_DEVrepo_update_reset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    #
    #modify CAPPA DEV repo
    #
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside tdm" ) #make a simple empty commit.
    clo_cappa_hm["DEVTDM"].push_with_merge()

    ca_sha_map_after_push = self.util_map2_currshas( clo_cappa_hm )

    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_push, 
                                   [], # empty => all
                                   [ "DEVTDM" ],
                                   "FAILED modify_repo inside %s" % clo_cappa_hm["DEVTDM"].getDir()
                                 )

    #
    #proj VALLEA update
    #
    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    #check DEVTDM repo upgraded
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # empty => all
                                   [ "DEVTDM" ],
                                   "FAILED proj update inside %s" % clo_valle_hm["DEVTDM"].getDir()
                                 )


    #check BOTH PROJECTS commits are identicval now
    msg = "FAILED proj update inside %s: MUST have same commits inside ALL repos with project %s" % \
          ( clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir() )
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
                                   ca_sha_map_after_push, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )

    #
    # all other unchanged
    #
    #check DEV PLAT PROJ, so also all its subsubrepos
    self.util_check_DEV_clonedPROJ_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["DEVPLAT"],
                                                 ori_hm["TSS100"], ori_hm["DEVPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][1],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 

    #check CST PLAT PROJ, so also all its subsubrepos
    self.util_check_CST_clonedPROJ_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["CSTPLAT"],
                                                 ori_hm["TSS100"], ori_hm["CSTPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][2],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

    #check CST TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["CSTTDM"],
                                                      ori_hm["TSS100"], ori_hm["CSTTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][3] )


    #reset HEAD
    # this time will move back DEVTDM REPO
    clo_valle_hm["TSS100"].proj_reset()

    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    #check all repos commits came back
    msg = "FAILED proj reset inside %s: MUST come back commit inside project after reset" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_reset, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )


  def test_ProjUpdate_02_01_DEVrepo_update_reset_1by1( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLOVALLEA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ##clone proj into CLOCAPPA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )

    #
    #modify CAPPA DEV repo
    #
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVTDM"].modify_repo( msg = "modif - cappa inside tdm" ) #make a simple empty commit.
    clo_cappa_hm["DEVTDM"].push_with_merge()

    ca_sha_map_after_push = self.util_map2_currshas( clo_cappa_hm )

    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_push, 
                                   [], # empty => all
                                   [ "DEVTDM" ],
                                   "FAILED modify_repo inside %s" % clo_cappa_hm["DEVTDM"].getDir()
                                 )

    #
    #proj VALLEA update
    #
    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    #check DEVTDM repo upgraded
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # empty => all
                                   [ "DEVTDM" ],
                                   "FAILED proj update inside %s" % clo_valle_hm["DEVTDM"].getDir()
                                 )

    #reset HEAD
    # this time will move back DEVTDM REPO
    clo_valle_hm["TSS100"].proj_reset( "HEAD", tss100_name2path( "DEVTDM" ) )

    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    #check all repos commits came back
    msg = "FAILED proj reset inside %s: MUST come back commit inside project after reset" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_reset, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )


  # Modify DEVFS
  def test_ProjUpdate_03_00_DEVsubrepo_update_reset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLOVALLEA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ##clone proj into CLOCAPPA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )


    #
    #modify CAPPA DEVFS repo
    #
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["DEVFS"].modify_repo( msg = "modif - cappa inside fs" ) #make a simple empty commit.
    clo_cappa_hm["DEVFS"].push_with_merge()

    ca_sha_map_after_push = self.util_map2_currshas( clo_cappa_hm )

    #check only DEVFS moved
    msg = "FAILED push inside %s: MUST change commit inside DEV repo after push" % clo_cappa_hm["DEVFS"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_push, 
                                   [], # all other must be eq
                                   [ "DEVFS" ],
                                   msg
                                 )

    #
    #proj VALLEA update
    #
    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    #check only DEVFS upgraded
    msg = "FAILED proj update inside %s" % clo_valle_hm["DEVFS"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVFS" ],
                                   msg
                                 )

    #
    #proj VALLEA reset HEAD
    #
    clo_valle_hm["TSS100"].proj_reset()

    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    #check all repos commits came back
    msg = "FAILED proj reset inside %s: MUST come back commit inside project after reset" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_reset, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )

  # Modify DEVFS and DEVPLAT
  def test_ProjUpdate_04_00_DEVproj_update_reset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLOVALLEA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ##clone proj into CLOCAPPA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )


    #
    #modify CAPPA DEVFS repo, commit it inside DEVPLAT
    #
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    #clo_cappa_hm["DEVFS"].branch_switch_to_int()
    clo_cappa_hm["DEVFS"].modify_repo( msg = "modif - cappa inside fs" ) #make a simple empty commit.
    
    remote = ""
    if modetest_morerepos():
      #remote   = ORIG_REPO_AREMOTE_NAME
      remote   = "origin"
    clo_cappa_hm["DEVFS"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #clo_cappa_hm["DEVPLAT"].branch_switch_to_int()
    clo_cappa_hm["DEVPLAT"].modify_repo( msg = "modif proj - strore FS advanced" ) #freeze fs upgrade
    clo_cappa_hm["DEVPLAT"].push_with_merge( remote )

    ca_sha_map_after_proj_push = self.util_map2_currshas( clo_cappa_hm )

    #check only DEVPLAT moved inthis last push
    msg = "FAILED modify/push of DEVFS inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all other must be eq
                                   [ "DEVPLAT" ],
                                   msg
                                 )

    #check both DEVFS, DEVPLAT moved from the beginning
    msg = "FAILED modify/push of DEVFS and DEVPLAT inside %s" % clo_cappa_hm["DEVPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all other must be eq
                                   [ "DEVFS", "DEVPLAT" ],
                                   msg
                                 )

    #
    #proj VALLEA update
    #
    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    #check nothing but DEVFS, DEVPLAT have upgraded
    msg = "FAILED proj update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   [ "DEVFS", "DEVPLAT" ],
                                   msg
                                 )

    #check everithing same between vallea and cappa
    msg = "FAILED proj update inside %s, should be same as: %s" % (clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir())
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all equals
                                   None,
                                   msg
                                 )

    #
    #proj VALLEA reset HEAD
    #
    clo_valle_hm["TSS100"].proj_reset()

    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    #check all repos commits came back
    msg = "FAILED proj reset inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_reset, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )

    #
    #proj VALLEA update after reset
    #
    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_reset_and_update = self.util_map2_currshas( clo_valle_hm )

    #check all repos commits came back
    msg = "FAILED proj update after reset and update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
                                   va_sha_map_after_reset_and_update, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )
    #check everithing same between vallea and cappa after reset and update
    msg = "FAILED proj update after reset and update inside %s, should be same as: %s" % \
          (clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir())
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_reset_and_update, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all equals
                                   None,
                                   msg
                                 )

    #
    #comit TSS100 (with DEVPLAT upgrade) inside CAPPA
    #
    #clo_cappa_hm["TSS100"].branch_switch_to_int()
    clo_cappa_hm["TSS100"].modify_repo( msg = "modif proj - strore DEVPLAT upgrade inside TSS100" ) #freeze TSS100 upgrade
    clo_cappa_hm["TSS100"].push_with_merge( remote )

    ca_sha_map_after_projtss100_push = self.util_map2_currshas( clo_cappa_hm )

    #check only TSS100 moved during this last push
    msg = "FAILED modify/push of TSS100 inside %s" % clo_cappa_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_proj_push, 
                                   ca_sha_map_after_projtss100_push, 
                                   [], # all other must be eq
                                   [ "TSS100" ],
                                   msg
                                 )

    #
    #proj VALLEA update
    #
    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_tss100update = self.util_map2_currshas( clo_valle_hm )

    #check tss100 upgrade
    msg = "FAILED proj update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_tss100update, 
                                   [], # all other must be eq
                                   [ "DEVFS", "DEVPLAT", "TSS100" ],
                                   msg
                                 )

    #check only TSS100 moved during this last update
    msg = "FAILED proj update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_reset_and_update, 
                                   va_sha_map_after_tss100update, 
                                   [], # all other must be eq
                                   [ "TSS100" ],
                                   msg
                                 )

    #check everithing same between vallea and cappa
    msg = "FAILED proj update inside %s, should be same as: %s" % (clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir())
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_tss100update, 
                                   ca_sha_map_after_projtss100_push, 
                                   [], # all equals
                                   None,
                                   msg
                                 )


  # Modify DEVFS and DEVPLAT
  def test_ProjUpdate_05_00_CSTrepo_update_reset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLOVALLEA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ##clone proj into CLOCAPPA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )


    #
    #modify CAPPA DEVFS repo, commit it inside DEVPLAT
    #
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    clo_cappa_hm["CSTTDM"].modify_repo( msg = "modif - cappa inside cst tdm" ) #make a simple empty commit.
    clo_cappa_hm["CSTTDM"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # empty => all
                                   [ "CSTTDM" ],
                                   "FAILED modify_repo inside %s" % clo_cappa_hm["CSTTDM"].getDir()
                                 )

    #
    #proj VALLEA update
    #
    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    #check no repo upgraded
    #CST are upgraded only after proj freeze, now it stays on last 
    #freezed commit inside project TSS100
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # empty => all
                                   None,
                                   "FAILED proj update inside %s" % clo_valle_hm["CSTTDM"].getDir()
                                 )


    #check CSTTDM is different between va and ca
    msg = "FAILED proj update inside %s, other is %s." % \
          ( clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir() )
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
                                   ca_sha_map_after_repo_push, 
                                   [], # empty => all
                                   [ "CSTTDM" ],
                                   msg
                                 )
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
                                   ca_sha_map_clonetime, 
                                   [ "CSTTDM" ],
                                   None
                                 )

    #
    # all unchanged
    #
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["DEVTDM"],
                                                      ori_hm["TSS100"], ori_hm["DEVTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][0] )

    #check DEV PLAT PROJ, so also all its subsubrepos
    self.util_check_DEV_clonedPROJ_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["DEVPLAT"],
                                                 ori_hm["TSS100"], ori_hm["DEVPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][1],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 

    #check CST PLAT PROJ, so also all its subsubrepos
    self.util_check_CST_clonedPROJ_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["CSTPLAT"],
                                                 ori_hm["TSS100"], ori_hm["CSTPLAT"],
                                                 PROJ_TSS100_DESCRIPTION[1][2],
                                                 PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

    #check CST TDM
    self.util_check_DEVorCST_clonedREPO_consinstency( clo_valle_hm["TSS100"], clo_valle_hm["CSTTDM"],
                                                      ori_hm["TSS100"], ori_hm["CSTTDM"],
                                                      PROJ_TSS100_DESCRIPTION[1][3] )


    #reset HEAD
    # this time will move back CSTTDM REPO
    clo_valle_hm["TSS100"].proj_reset()

    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    #check all repos commits came back
    msg = "FAILED proj reset inside %s: MUST come back commit inside project after reset" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_reset, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg
                                 )

  #-----------------+---------------------+------------------------------------------------------------------------------
  #    CAPPA        |     VALLEA          |  COMMENT
  #-----------------+---------------------+------------------------------------------------------------------------------
  #   mod CSTFS     |                     |
  #   mod CSTPLAT   |                     |
  #                 |                     |
  #                 |    Proj Update      |  CSTPLAT -> do not change.
  #                 |                     |             Not even fetched new commits because nothing changed inside TSS100 =>
  #                 |                     |             CSTPLAT is fetched only when TSS100 change its reference
  #                 |                     |  DEVPLAT -> changes only because it is same origin as CSTPLAT.
  #                 |                     |             But DEVPLAT stays on develop HEAD, it is not changed
  #                 |                     |
  #                 |    Proj Reset HEAD  |  Should do nothing.
  #                 |                     |
  #   mod TSS100    |                     |  Register CSTPLAT upgrade
  #                 |                     |
  #                 |    Proj Update      |  CSTPLAT -> NOW CHANGES because TSS100 say: "CSTPLAT has new commit" => 
  #                 |                     |             git submodule update --recursive should fetch new commits.
  #                 |    Proj Reset HEAD  |
  #                 |                     |
  #-----------------+---------------------+------------------------------------------------------------------------------

  # Modify CSTFS and CSTPLAT
  def test_ProjUpdate_06_00_CSTproj_update_reset( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOCAPPA_DIR )
    #self.util_createAndCheck_TSS100_FULL_withbkp()

    ##clone proj into CLOVALLEA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ##clone proj into CLOCAPPA
    #out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH )
    #self.assertEqual( errCode, 0, "clone_repo_url( %s, %s, %s ) FAILED - \n%s\n" % \
    #                  ( REPO_TSS100__ORI_URL, self.REPO_TSS100__CLOCAPPA_DIR, REPO_TSS100__DEVBRANCH, out) )

    ori_hm       = self.util_get_TSS10FULL_helper_map_orig()
    clo_valle_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )
    clo_cappa_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOCAPPA_DIR )


    #
    #modify CAPPA CSTFS repo, commit it inside CSTPLAT
    #
    ca_sha_map_clonetime = self.util_map2_currshas( clo_cappa_hm )

    #this should not be the real case scenario.
    # i should just move on a new commit and freeze proj over me.
    # here, simulate it by creating a new commit
    #
    clo_cappa_hm["CSTFS"].int_branch_set( REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].branch_switch_to_br( REPO_FS__DEVBRANCH )
    clo_cappa_hm["CSTFS"].branch_create( self.MOD_CSTFS_INTBR_BR )
    clo_cappa_hm["CSTFS"].int_branch_set(  self.MOD_CSTFS_INTBR_BR ) #just in order to push this branch and do not modify develop
    clo_cappa_hm["CSTFS"].branch_create( self.MOD_CSTFS_BR )
    clo_cappa_hm["CSTFS"].modify_repo( msg = "modif - cappa inside CSTFS", gotoint = False )
    clo_cappa_hm["CSTFS"].tag_dev( "modif - cappa inside CSTFS" )
    clo_cappa_hm["CSTFS"].push_with_merge()

    ca_sha_map_after_repo_push = self.util_map2_currshas( clo_cappa_hm )

    #check CSTFS moved
    msg = "FAILED modify/push of CSTFS inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_repo_push, 
                                   [], # all other must be eq
                                   [ "CSTFS" ],
                                   msg
                                 )

    #clo_cappa_hm["CSTPLAT"].branch_switch_to_int()
    clo_cappa_hm["CSTPLAT"].modify_repo( msg = "modif proj - strore CSTFS advanced" ) #freeze fs upgrade
    clo_cappa_hm["CSTPLAT"].push_with_merge()

    ca_sha_map_after_proj_push = self.util_map2_currshas( clo_cappa_hm )

    #check only CSTPLAT moved inthis last push
    msg = "FAILED modify/push of CSTFS inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_repo_push, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all other must be eq
                                   [ "CSTPLAT" ],
                                   msg
                                 )

    #check both CSTFS, CSTPLAT moved from the beginning
    msg = "FAILED modify/push of CSTFS and CSTPLAT inside %s" % clo_cappa_hm["CSTPLAT"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_clonetime, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all other must be eq
                                   [ "CSTFS", "CSTPLAT" ],
                                   msg
                                 )

    #
    #proj VALLEA update
    # --------------------------------------------------------------------
    # NOTE: TSS100 map has not moved for CSTPLAT commit => nothing changes
    # --------------------------------------------------------------------
    #
    va_sha_map_clonetime = self.util_map2_currshas( clo_valle_hm )

    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_update = self.util_map2_currshas( clo_valle_hm )

    #check nothing but CSTFS, CSTPLAT have upgraded
    msg = "FAILED proj update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_update, 
                                   [], # all other must be eq
                                   #[ "CSTFS", "CSTPLAT" ],
                                   None, #None => consider only eq fields
                                   msg
                                 )

    #check differences between vallea and cappa for CSTPLAT
    msg = "FAILED proj update inside %s, should be different from: %s" % (clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir())
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
                                   ca_sha_map_after_proj_push, 
                                   [], # all equals
                                   [ "CSTFS", "CSTPLAT" ],
                                   msg
                                 )

    #
    #proj VALLEA reset HEAD
    #
    clo_valle_hm["TSS100"].proj_reset()

    va_sha_map_after_reset = self.util_map2_currshas( clo_valle_hm )

    #check nothing changed also after reset HEAD
    msg = "FAILED proj reset inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_reset, 
                                   [], # empty => all
                                   #[ "CSTFS", "CSTPLAT" ],
                                   None, #None => consider only eq fields
                                   msg )
    #self.util_assert_EQ_UNEQ_maps( va_sha_map_after_update, 
    #                               va_sha_map_after_reset, 
    #                               [ "CSTFS", "CSTPLAT" ],
    #                               None, #None => consider only eq fields
    #                               msg + "\n CSTFS and CSTPLAT should not come back" )

    remote = ""
    if modetest_morerepos():
      #remote   = ORIG_REPO_AREMOTE_NAME
      remote   = "origin"

    #
    #comit TSS100 (with CSTPLAT upgrade) inside CAPPA
    #
    #clo_cappa_hm["TSS100"].branch_switch_to_int()
    clo_cappa_hm["TSS100"].modify_repo( msg = "modif proj - strore CSTPLAT upgrade inside TSS100" ) #freeze TSS100 upgrade
    clo_cappa_hm["TSS100"].push_with_merge( remote )

    ca_sha_map_after_projtss100_push = self.util_map2_currshas( clo_cappa_hm )

    #check only TSS100 moved during this last push
    msg = "FAILED modify/push of TSS100 inside %s" % clo_cappa_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( ca_sha_map_after_proj_push, 
                                   ca_sha_map_after_projtss100_push, 
                                   [], # all other must be eq
                                   [ "TSS100" ],
                                   msg
                                 )

    #
    #proj VALLEA update
    # -------------------------------------------------------------------------
    # NOTE: TSS100 map has moved for CSTPLAT commit => now also repos must move
    # -------------------------------------------------------------------------
    #
    clo_valle_hm["TSS100"].proj_update()

    va_sha_map_after_tss100update = self.util_map2_currshas( clo_valle_hm )

    #check tss100 upgrade
    msg = "FAILED proj update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_clonetime, 
                                   va_sha_map_after_tss100update, 
                                   [], # all other must be eq
                                   [ "CSTFS", "CSTPLAT", "TSS100" ],
                                   msg
                                 )

    #check which repos moved during this last update
    msg = "FAILED proj update inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_reset, 
                                   va_sha_map_after_tss100update, 
                                   [], # all other must be eq
                                   [ "CSTFS", "CSTPLAT", "TSS100" ],
                                   msg
                                 )

    #check everithing same between vallea and cappa
    msg = "FAILED proj update inside %s, should be same as: %s" % (clo_valle_hm["TSS100"].getDir(), clo_cappa_hm["TSS100"].getDir())
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_tss100update, 
                                   ca_sha_map_after_projtss100_push, 
                                   [], # all equals
                                   None,
                                   msg
                                 )

    #
    #proj VALLEA second reset HEAD
    #
    clo_valle_hm["TSS100"].proj_reset()

    va_sha_map_after_secondreset = self.util_map2_currshas( clo_valle_hm )

    #check nothing changed also after reset HEAD
    msg = "FAILED proj reset inside %s" % clo_valle_hm["TSS100"].getDir()
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_tss100update, 
                                   va_sha_map_after_secondreset, 
                                   [], # empty => all
                                   None, #None => consider only eq fields
                                   msg )
    #check these commitdid not change after reset (they are now freezed inside map)
    self.util_assert_EQ_UNEQ_maps( va_sha_map_after_tss100update, 
                                   va_sha_map_after_secondreset, 
                                   [ "CSTFS", "CSTPLAT" ],
                                   None, #None => consider only eq fields
                                   msg + "\n CSTFS and CSTPLAT should not come back" )

if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()




