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

import copy
import glob

from test_base import *


class Test_ProjBase( Test_Base ):
  # CLO is USED TO ADD REPOS
  REPO_FS__CLO_DIR     = REPO_FS__ORI_DIR + "_CLONE"
  REPO_APP__CLO_DIR    = REPO_APP__ORI_DIR + "_CLONE"
  REPO_PLAT__CLO_DIR   = REPO_PLAT__ORI_DIR + "_CLONE"
  REPO_TSS100__CLO_DIR = REPO_TSS100__ORI_DIR + "_CLONE"
  REPO_TSS100__CLO_URL = "%s%s" % ( TESTER_SSHACCESS, REPO_TSS100__CLO_DIR )
  REPO_TDM__CLO_DIR    = REPO_TDM__ORI_DIR + "_CLONE"
  REPO_CSTTDM__CLO_DIR = REPO_CSTTDM__ORI_DIR + "_CLONE"

  # CLO2 is USED like fresh new cloned repo over which to check clone operation
  REPO_FS__CLO2_DIR     = REPO_FS__ORI_DIR + "_CLONE2"
  REPO_APP__CLO2_DIR    = REPO_APP__ORI_DIR + "_CLONE2"
  REPO_PLAT__CLO2_DIR   = REPO_PLAT__ORI_DIR + "_CLONE2"
  REPO_TSS100__CLO2_DIR = REPO_TSS100__ORI_DIR + "_CLONE2"
  REPO_TSS100__CLO2_URL = "%s%s" % ( TESTER_SSHACCESS, REPO_TSS100__CLO2_DIR )
  REPO_TDM__CLO2_DIR    = REPO_TDM__ORI_DIR + "_CLONE2"
  REPO_CSTTDM__CLO2_DIR = REPO_CSTTDM__ORI_DIR + "_CLONE2"

  REPO_TSS100__CLOVALLEA_DIR = REPO_TSS100__ORI_DIR + "_CLONEVALLEA"
  REPO_TSS100__CLOVALLEA_URL = "%s%s" % ( TESTER_SSHACCESS, REPO_TSS100__CLOVALLEA_DIR )
  REPO_TSS100__CLOCAPPA_DIR  = REPO_TSS100__ORI_DIR + "_CLONECAPPA"
  REPO_TSS100__CLOCAPPA_URL  = "%s%s" % ( TESTER_SSHACCESS, REPO_TSS100__CLOCAPPA_DIR )

  REPO_PLAT__CLOVALLEA_DIR = REPO_PLAT__ORI_DIR + "_CLONEVALLEA"
  REPO_PLAT__CLOVALLEA_URL = "%s%s" % ( TESTER_SSHACCESS, REPO_PLAT__CLOVALLEA_DIR )
  REPO_PLAT__CLOCAPPA_DIR  = REPO_PLAT__ORI_DIR + "_CLONECAPPA"
  REPO_PLAT__CLOCAPPA_URL  = "%s%s" % ( TESTER_SSHACCESS, REPO_PLAT__CLOCAPPA_DIR )

  # CLOCLO is USED to check clone of clone operation
  REPO_FS__CLOCLO_DIR     = REPO_FS__ORI_DIR + "CLOCLO"
  REPO_APP__CLOCLO_DIR    = REPO_APP__ORI_DIR + "CLOCLO"
  REPO_PLAT__CLOCLO_DIR   = REPO_PLAT__ORI_DIR + "CLOCLO"
  REPO_TSS100__CLOCLO_DIR = REPO_TSS100__ORI_DIR + "CLOCLO"
  REPO_TDM__CLOCLO_DIR    = REPO_TDM__ORI_DIR + "CLOCLO"
  REPO_CSTTDM__CLOCLO_DIR = REPO_CSTTDM__ORI_DIR + "CLOCLO"



  ALL_REPOS = ( REPO_FS__ORI_DIR, REPO_APP__ORI_DIR, REPO_PLAT__ORI_DIR,
                REPO_TSS100__ORI_DIR, REPO_TDM__ORI_DIR, REPO_CSTTDM__ORI_DIR,
                REPO_FS__CLO_DIR, REPO_APP__CLO_DIR, REPO_PLAT__CLO_DIR,
                REPO_TSS100__CLO_DIR, REPO_TDM__CLO_DIR, REPO_CSTTDM__CLO_DIR,
                REPO_FS__CLO2_DIR, REPO_APP__CLO2_DIR, REPO_PLAT__CLO2_DIR,
                REPO_TSS100__CLO2_DIR, REPO_TDM__CLO2_DIR, REPO_CSTTDM__CLO2_DIR,
                REPO_FS__CLOCLO_DIR, REPO_APP__CLOCLO_DIR, REPO_PLAT__CLOCLO_DIR,
                REPO_TSS100__CLOCLO_DIR, REPO_TDM__CLOCLO_DIR, REPO_CSTTDM__CLOCLO_DIR,
                REPO_TSS100__CLOVALLEA_DIR, REPO_TSS100__CLOCAPPA_DIR,
                REPO_PLAT__CLOVALLEA_DIR, REPO_PLAT__CLOCAPPA_DIR
                )


  MOD_PLAT_BR = "MOD_PLAT"
  MOD_TSS100_BR = "MOD_TSS100"
  MOD_DEVTDM_BR = "MOD_DEVTDM"
  MOD_DEVPLAT_BR = "MOD_DEVPLAT"
  MOD_DEVFS_BR   = "MOD_DEVFS"
  MOD_CSTTDM_BR   = "MOD_CSTTDM"
  MOD_CSTPLAT_BR   = "MOD_CSTPLAT"
  MOD_CSTFS_INTBR_BR = "MOD_CSTFS_BASE"
  MOD_CSTFS_BR = "MOD_CSTFS"

  def setUp( self ):
    super( Test_ProjBase, self ).setUp()

    for r in self.ALL_REPOS:
      shutil.rmtree( r, True ) #ignore errors

    self.swu_FS_ORI  = swgit__utils( REPO_FS__ORI_DIR )
    self.gu_FS_ORI  = git__utils( REPO_FS__ORI_DIR )
    self.swu_APP_ORI  = swgit__utils( REPO_APP__ORI_DIR )
    self.gu_APP_ORI  = git__utils( REPO_APP__ORI_DIR )
    self.swu_PLAT_ORI  = swgit__utils( REPO_PLAT__ORI_DIR )
    self.gu_PLAT_ORI  = git__utils( REPO_PLAT__ORI_DIR )
    self.swu_TSS100_ORI  = swgit__utils( REPO_TSS100__ORI_DIR )
    self.gu_TSS100_ORI  = git__utils( REPO_TSS100__ORI_DIR )
    self.swu_TDM_ORI  = swgit__utils( REPO_TDM__ORI_DIR )
    self.gu_TDM_ORI  = git__utils( REPO_TDM__ORI_DIR )
    self.swu_CSTTDM_ORI  = swgit__utils( REPO_CSTTDM__ORI_DIR )
    self.gu_CSTTDM_ORI  = git__utils( REPO_CSTTDM__ORI_DIR )

    self.swu_FS_CLO  = swgit__utils( self.REPO_FS__CLO_DIR )
    self.gu_FS_CLO  = git__utils( self.REPO_FS__CLO_DIR )
    self.swu_APP_CLO  = swgit__utils( self.REPO_APP__CLO_DIR )
    self.gu_APP_CLO  = git__utils( self.REPO_APP__CLO_DIR )
    self.swu_PLAT_CLO  = swgit__utils( self.REPO_PLAT__CLO_DIR )
    self.gu_PLAT_CLO  = git__utils( self.REPO_PLAT__CLO_DIR )
    self.swu_TSS100_CLO  = swgit__utils( self.REPO_TSS100__CLO_DIR )
    self.gu_TSS100_CLO  = git__utils( self.REPO_TSS100__CLO_DIR )
    self.swu_TDM_CLO  = swgit__utils( self.REPO_TDM__CLO_DIR )
    self.gu_TDM_CLO  = git__utils( self.REPO_TDM__CLO_DIR )
    self.swu_CSTTDM_CLO  = swgit__utils( self.REPO_CSTTDM__CLO_DIR )
    self.gu_CSTTDM_CLO  = git__utils( self.REPO_CSTTDM__CLO_DIR )

    self.swu_FS_CLO2  = swgit__utils( self.REPO_FS__CLO2_DIR )
    self.gu_FS_CLO2  = git__utils( self.REPO_FS__CLO2_DIR )
    self.swu_APP_CLO2  = swgit__utils( self.REPO_APP__CLO2_DIR )
    self.gu_APP_CLO2  = git__utils( self.REPO_APP__CLO2_DIR )
    self.swu_PLAT_CLO2  = swgit__utils( self.REPO_PLAT__CLO2_DIR )
    self.gu_PLAT_CLO2  = git__utils( self.REPO_PLAT__CLO2_DIR )
    self.swu_TSS100_CLO2  = swgit__utils( self.REPO_TSS100__CLO2_DIR )
    self.gu_TSS100_CLO2  = git__utils( self.REPO_TSS100__CLO2_DIR )
    self.swu_TDM_CLO2  = swgit__utils( self.REPO_TDM__CLO2_DIR )
    self.gu_TDM_CLO2  = git__utils( self.REPO_TDM__CLO2_DIR )
    self.swu_CSTTDM_CLO2  = swgit__utils( self.REPO_CSTTDM__CLO2_DIR )
    self.gu_CSTTDM_CLO2  = git__utils( self.REPO_CSTTDM__CLO2_DIR )

    self.swu_FS_CLOCLO  = swgit__utils( self.REPO_FS__CLOCLO_DIR )
    self.gu_FS_CLOCLO  = git__utils( self.REPO_FS__CLOCLO_DIR )
    self.swu_APP_CLOCLO  = swgit__utils( self.REPO_APP__CLOCLO_DIR )
    self.gu_APP_CLOCLO  = git__utils( self.REPO_APP__CLOCLO_DIR )
    self.swu_PLAT_CLOCLO  = swgit__utils( self.REPO_PLAT__CLOCLO_DIR )
    self.gu_PLAT_CLOCLO  = git__utils( self.REPO_PLAT__CLOCLO_DIR )
    self.swu_TSS100_CLOCLO  = swgit__utils( self.REPO_TSS100__CLOCLO_DIR )
    self.gu_TSS100_CLOCLO  = git__utils( self.REPO_TSS100__CLOCLO_DIR )
    self.swu_TDM_CLOCLO  = swgit__utils( self.REPO_TDM__CLOCLO_DIR )
    self.gu_TDM_CLOCLO  = git__utils( self.REPO_TDM__CLOCLO_DIR )
    self.swu_CSTTDM_CLOCLO  = swgit__utils( self.REPO_CSTTDM__CLOCLO_DIR )
    self.gu_CSTTDM_CLOCLO  = git__utils( self.REPO_CSTTDM__CLOCLO_DIR )


    self.HELPERS_REPOS_ORI = ( self.swu_FS_ORI, self.gu_FS_ORI,
                               self.swu_APP_ORI, self.gu_APP_ORI,
                               self.swu_PLAT_ORI, self.gu_PLAT_ORI,
                               self.swu_TSS100_ORI, self.gu_TSS100_ORI,
                               self.swu_TDM_ORI, self.gu_TDM_ORI,
                               self.swu_CSTTDM_ORI, self.gu_CSTTDM_ORI )
        
    self.HELPERS_REPOS_CLO = ( self.swu_FS_CLO, self.gu_FS_CLO,
                               self.swu_APP_CLO, self.gu_APP_CLO,
                               self.swu_PLAT_CLO, self.gu_PLAT_CLO,
                               self.swu_TSS100_CLO, self.gu_TSS100_CLO,
                               self.swu_TDM_CLO, self.gu_TDM_CLO,
                               self.swu_CSTTDM_CLO, self.gu_CSTTDM_CLO,
                               self.swu_FS_CLO2, self.gu_FS_CLO2,
                               self.swu_APP_CLO2, self.gu_APP_CLO2,
                               self.swu_PLAT_CLO2, self.gu_PLAT_CLO2,
                               self.swu_TSS100_CLO2, self.gu_TSS100_CLO2,
                               self.swu_TDM_CLO2, self.gu_TDM_CLO2,
                               self.swu_CSTTDM_CLO2, self.gu_CSTTDM_CLO2,
                               self.swu_FS_CLOCLO, self.gu_FS_CLOCLO,
                               self.swu_APP_CLOCLO, self.gu_APP_CLOCLO,
                               self.swu_PLAT_CLOCLO, self.gu_PLAT_CLOCLO,
                               self.swu_TSS100_CLOCLO, self.gu_TSS100_CLOCLO,
                               self.swu_TDM_CLOCLO, self.gu_TDM_CLOCLO,
                               self.swu_CSTTDM_CLOCLO, self.gu_CSTTDM_CLOCLO )

    #pprint( self.__dict__ )

  def tearDown( self ):
    super( Test_ProjBase, self ).tearDown()
    pass

  #
  # Asserts 2 helper maps.
  #
  #  +---------+---------+----------------------------------------------------+
  #  |  eqs    |  uneqs  |  meaning                                           |
  #  +---------+---------+----------------------------------------------------+
  #  |  any    |  None   |  ONLY assert equals                                |
  #  |  None   |  any    |  ONLY assert unequals                              |
  #  |  []     |  None   |  assert ALL equals                                 |
  #  |  None   |  []     |  assert ALL unequals                               |
  #  |  someE  |  someU  |  assert someE are equals, someU are unequals       |
  #  |  []     |  someU  |  assert someU are unequals, ALL others are equals  |
  #  |  someE  |  []     |  assert someE are equals, ALL others are unequals  |
  #  +---------+---------+----------------------------------------------------+
  #
  def util_assert_EQ_UNEQ_maps( self, helpermap1, helpermap2, eqs, uneqs, msg = "" ):
    keys1 = set( helpermap1.keys() )
    keys2 = set( helpermap2.keys() )
    self.assertEqual( len( keys2 - keys2 ), 0,
                      "DIFFERENT KEYS between %s and %s" % (helpermap1.keys(), helpermap2.keys()) )

    alleqs = False
    if eqs == None:
      EQkeys = set()
    elif len( eqs ) == 0:
      alleqs = True
      EQkeys = keys1
    else:
      EQkeys = set( eqs )

    self.assertEqual( len( EQkeys - keys1 ), 0,
                      "KEYS in EQ not inside HLP1\n%s\n%s" % (EQkeys, helpermap1.keys()) )
    self.assertEqual( len( EQkeys - keys2 ), 0,
                      "KEYS in EQ not inside HLP2\n%s\n%s" % (EQkeys, helpermap2.keys()) )

    alluneqs = False
    if uneqs == None:
      UNeqkeys = set()
    elif len( uneqs ) == 0:
      alluneqs = True
      UNeqkeys = keys1
    else:
      UNeqkeys = set( uneqs )

    self.assertEqual( len( UNeqkeys - keys1 ), 0,
                      "KEYS in UNEQ not inside HLP1\n%s\n%s" % (UNeqkeys, helpermap1.keys()) )
    self.assertEqual( len( UNeqkeys - keys2 ), 0,
                      "KEYS in UNEQ not inside HLP2\n%s\n%s" % (UNeqkeys, helpermap2.keys()) )

    self.assertNotEqual( len( EQkeys - UNeqkeys ), 0, "SPECIFY AT LEAST 1 EQ or UNEQ KEY" )

    #manage "ALL" value field:
    if alleqs == True:
      EQkeys = EQkeys - UNeqkeys
    if alluneqs == True:
      UNeqkeys = UNeqkeys - EQkeys

    mess = ""
    if msg != "":
      mess = "\n%s\n" % msg
    mess += "MUST BE EQUAL:\n[%s]\n[%s]\n[%s]"

    for k in EQkeys:
      self.assertTrue( k in helpermap1.keys(), "Not found key %s inside helper %s" % (k,helpermap1) )
      self.assertTrue( k in helpermap2.keys(), "Not found key %s inside helper %s" % (k,helpermap2) )

      self.assertEqual( helpermap1[k], helpermap2[k], mess % (k,helpermap1[k],helpermap2[k]) )

    mess = ""
    if msg != "":
      mess = "\n%s\n" % msg
    mess += "MUST BE NOT EQUAL:\n[%s]\n[%s]\n[%s]"

    for k in UNeqkeys:
      self.assertTrue( k in helpermap1.keys(), "Not found key %s inside helper %s" % (k,helpermap1) )
      self.assertTrue( k in helpermap2.keys(), "Not found key %s inside helper %s" % (k,helpermap2) )

      self.assertNotEqual( helpermap1[k], helpermap2[k], mess % (k,helpermap1[k],helpermap2[k]) )

    return


  def util_assert_EQ_maps( self, helpermap1, helpermap2, comparethem = [], jumpthem = [], msg = "" ):

    keys1 = set( helpermap1.keys() )
    keys2 = set( helpermap2.keys() )
    keys = keys1 & keys2

    compkeys = set( comparethem )
    keys = keys & compkeys

    diffkeys = keys1 - keys2
    self.assertEqual( len(diffkeys), 0,
                      "DIFFERENT KEYS between %s and %s" % (helpermap1.keys(), helpermap2.keys()) )

    jumpkeys = set( jumpthem )
    keys = keys - jumpkeys

    mess = ""
    if msg != "":
      mess = "\n%s\n" % msg
    mess += "MUST BE EQUAL:\n[%s]\n[%s]"

    for k in keys:
      self.assertTrue( k in helpermap1.keys(), "Not found key %s inside helper %s" % (k,helpermap1) )
      self.assertTrue( k in helpermap2.keys(), "Not found key %s inside helper %s" % (k,helpermap2) )

      self.assertEqual( helpermap1[k], helpermap2[k], mess % (helpermap1[k], helpermap2[k]) )

    return

  def util_assert_UNEQ_maps( self, helpermap1, helpermap2, comparethem = [], jumpthem = [], msg = "" ):

    keys1 = set( helpermap1.keys() )
    keys2 = set( helpermap2.keys() )
    keys = keys1 & keys2

    diffkeys = keys1 - keys2
    self.assertEqual( len(diffkeys), 0,
                      "DIFFERENT KEYS between %s and %s" % (helpermap1.keys(), helpermap2.keys()) )

    compkeys = set( comparethem )
    keys = keys & compkeys

    jumpkeys = set( jumpthem )
    keys = keys - jumpkeys

    mess = ""
    if msg != "":
      mess = "\n%s\n" % msg
    mess += "MUST BE NOT EQUAL:\n[%s]\n[%s]"

    for k in keys:
      self.assertTrue( k in helpermap1.keys(), "Not found key %s inside helper %s" % (k,helpermap1) )
      self.assertTrue( k in helpermap2.keys(), "Not found key %s inside helper %s" % (k,helpermap2) )

      self.assertNotEqual( helpermap1[k], helpermap2[k], mess % (helpermap1[k], helpermap2[k]) )

    return

  # Given helper map (directories)
  #  returns shamap:
  #    same keys
  #    currsha as value
  def util_map2_currshas( self, helpermap ):
    retshas = {}
    for name, helper in helpermap.items():
      sha, errCode = helper.get_currsha()
      self.assertEqual( errCode, 0, "Error retrieving sha inside repo %s - \n%s\n" %
                        ( helper.getDir(), sha ) )

      retshas[ name ] = sha

    return retshas


  ##################
  # FACTORY HELPER #
  ##################
  def util_get_PLATFULL_helper_map_orig( self, snap = False ):

    p = url_parse( PROJ_PLAT_DESCRIPTION[0][1] )
    plat_orig_helper = swgit__utils( p["ROOT"] )

    p = url_parse( PROJ_PLAT_DESCRIPTION[1][0][1] )
    dev_fs_orig_helper  = swgit__utils( p["ROOT"] )
    p = url_parse( PROJ_PLAT_DESCRIPTION[1][1][1] )
    dev_app_orig_helper = swgit__utils( p["ROOT"] )

    retmap = {}
    retmap["PLAT"]   = plat_orig_helper
    retmap["DEVFS"]  = dev_fs_orig_helper
    retmap["DEVAPP"] = dev_app_orig_helper

    if snap == True:
      snap_app_orig_helper = swgit__utils( REPO_S )
      retmap["SNAP"] = snap_app_orig_helper


    return retmap


  def util_get_PLATFULL_helper_map_clone( self, startdir, snap = False ):

    plat_clone_helper = swgit__utils( startdir )

    repo_bi = PROJ_PLAT_DESCRIPTION[1][0]
    fs_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )
    repo_bi = PROJ_PLAT_DESCRIPTION[1][1]
    app_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )

    retmap = {}
    retmap["PLAT"]   = plat_clone_helper
    retmap["DEVFS"]  = fs_clone_helper
    retmap["DEVAPP"] = app_clone_helper
    if snap == True:
      repo_bi = SNAP_BI
      snap_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )
      retmap["SNAP"] = snap_clone_helper

    return retmap


  def util_get_TSS10FULL_helper_map_orig( self ):

    dev, cst = self.util_get_TSS10FULL_ALL_orig_helpers_int( incroot = True )

    retmap = {}
    retmap["TSS100"]  = dev[0]
    retmap["DEVTDM"]  = dev[1]
    retmap["DEVPLAT"] = dev[2]
    retmap["CSTPLAT"] = cst[0]
    retmap["CSTTDM"]  = cst[1]
    retmap["DEVFS"]   = dev[3]
    retmap["DEVAPP"]  = dev[4]
    retmap["CSTFS"]   = cst[2]
    retmap["CSTAPP"]  = cst[3]
    return retmap

  def util_get_TSS10FULL_helper_map_clone( self, startdir ):

    dev, cst = self.util_get_TSS10FULL_ALL_helpers_int( startdir, incroot = True )

    retmap = {}
    retmap["TSS100"]  = dev[0]
    retmap["DEVTDM"]  = dev[1]
    retmap["DEVPLAT"] = dev[2]
    retmap["CSTPLAT"] = cst[0]
    retmap["CSTTDM"]  = cst[1]
    retmap["DEVFS"]   = dev[3]
    retmap["DEVAPP"]  = dev[4]
    retmap["CSTFS"]   = cst[2]
    retmap["CSTAPP"]  = cst[3]
    return retmap


  def util_get_TSS10FULL_ALL_orig_helpers_int( self, incroot = False, lev = "A" ):
    dev_list = []
    cst_list = []

    self.assertTrue( lev in [ "A", "N", "F", "S" ], "util_get_TSS10FULL_ALL_orig_helpers_int lev param not valid %s" % lev )

    if incroot == True:
      p = url_parse( PROJ_TSS100_DESCRIPTION[0][1] )
      tss100_orig_helper = swgit__utils( p["ROOT"] )
      dev_list.append( tss100_orig_helper )

    if lev == "F" or lev == "A":

      p = url_parse( PROJ_TSS100_DESCRIPTION[1][0][1] )
      tdm_orig_helper = swgit__utils( p["ROOT"] )
      dev_list.append( tdm_orig_helper )

      p = url_parse( PROJ_TSS100_DESCRIPTION[1][1][1] )
      devplat_orig_helper = swgit__utils( p["ROOT"] )
      dev_list.append( devplat_orig_helper )

      p = url_parse( PROJ_TSS100_DESCRIPTION[1][2][1] )
      cstplat_orig_helper = swgit__utils( p["ROOT"] )
      cst_list.append( cstplat_orig_helper )

      p = url_parse( PROJ_TSS100_DESCRIPTION[1][3][1] )
      csttdm_orig_helper = swgit__utils( p["ROOT"] )
      cst_list.append( csttdm_orig_helper )

    if lev == "S" or lev == "A":

      p = url_parse( PROJ_PLAT_DESCRIPTION[1][0][1] )
      dev_fs_orig_helper  = swgit__utils( p["ROOT"] )
      dev_list.append( dev_fs_orig_helper )
      p = url_parse( PROJ_PLAT_DESCRIPTION[1][1][1] )
      dev_app_orig_helper = swgit__utils( p["ROOT"] )
      dev_list.append( dev_app_orig_helper )

      cst_fs_orig_helper  = dev_fs_orig_helper
      cst_app_orig_helper = dev_app_orig_helper
      cst_list.append( cst_fs_orig_helper )
      cst_list.append( cst_app_orig_helper )

    return [ dev_list, cst_list ]

  #clone helpers are all under root
  def util_get_TSS10FULL_ALL_helpers_int( self, startdir, incroot = False, lev = "A" ):
    dev_list = []
    cst_list = []

    self.assertTrue( lev in [ "A", "N", "F", "S" ], "util_get_TSS10FULL_ALL_orig_helpers_int lev param not valid %s" % lev )

    if incroot == True:
      tss100_clone_helper = swgit__utils( startdir )
      dev_list.append( tss100_clone_helper )

    if lev == "F" or lev == "A":

      repo_bi = PROJ_TSS100_DESCRIPTION[1][0]
      tdm_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )
      dev_list.append( tdm_clone_helper )

      repo_bi = PROJ_TSS100_DESCRIPTION[1][1]
      devplat_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )
      dev_list.append( devplat_clone_helper )

      repo_bi = PROJ_TSS100_DESCRIPTION[1][2]
      cstplat_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )
      cst_list.append( cstplat_clone_helper )

      repo_bi = PROJ_TSS100_DESCRIPTION[1][3]
      csttdm_clone_helper = swgit__utils( startdir + "/" + repo_bi[0] )
      cst_list.append( csttdm_clone_helper )

    if lev == "S" or lev == "A":

      dev_plat_bi = PROJ_TSS100_DESCRIPTION[1][1]
      cst_plat_bi = PROJ_TSS100_DESCRIPTION[1][2]
      plat_bi = PROJ_PLAT_DESCRIPTION[1]

      dev_fs_clone_helper  = swgit__utils( startdir + "/" + dev_plat_bi[0] + "/" + plat_bi[0][0] )
      dev_app_clone_helper = swgit__utils( startdir + "/" + dev_plat_bi[0] + "/" + plat_bi[1][0] )
      dev_list.append( dev_fs_clone_helper )
      dev_list.append( dev_app_clone_helper )

      cst_fs_clone_helper  = swgit__utils( startdir + "/" + cst_plat_bi[0] + "/" + plat_bi[0][0] )
      cst_app_clone_helper = swgit__utils( startdir + "/" + cst_plat_bi[0] + "/" + plat_bi[1][0] )
      cst_list.append( cst_fs_clone_helper )
      cst_list.append( cst_app_clone_helper )

    return [ dev_list, cst_list ]

 

  ################
  # Simple utils #
  ################
  def util_clonePLAT_createBr( self ):
    #clone the empty origin proj
    dest   = self.REPO_PLAT__CLO_DIR
    url    = PROJ_PLAT_DESCRIPTION[0][1]
    branch = PROJ_PLAT_DESCRIPTION[0][2]
    out, errCode = swgit__utils.clone_repo_url( url, dest, branch )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s ) FAILED - \n%s\n" % ( url, dest, out) )

    # direcotries
    self.assertTrue( os.path.exists( self.REPO_PLAT__CLO_DIR ), "not created directory %s" % self.REPO_PLAT__CLO_DIR )

    #
    # test mode MOREREPOS => add remote to orig
    #
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      #print "\n%s\nMOREREMOTES for repo %s\n%s\n" % ( "="*20, dest, "="*20 )
      helper = swgit__utils( dest )
      AREMOTE_PLAT = PROJ_PLAT_DESCRIPTION[0][0] + AREMOTE_PATH
      AREPO_AREMOTE_URL = "%s%s" % ( TESTER_SSHACCESS, AREMOTE_PLAT )
      out, errCode = helper.remote_add( ORIG_REPO_AREMOTE_NAME, AREPO_AREMOTE_URL )
      out, errCode = helper.pull()

    #create branch
    clo_h = self.swu_PLAT_CLO
    out, errCode = clo_h.branch_create( self.MOD_PLAT_BR )
    self.assertEqual( errCode, 0, "FAILED creating branch for adding repo to proj %s - \n%s\n" % ( self.REPO_PLAT__CLO_DIR, out) )

  def util_cloneTSS100_createBr( self ):
    #clone the empty origin proj
    out, errCode = swgit__utils.clone_repo_url( PROJ_TSS100_DESCRIPTION[0][1], self.REPO_TSS100__CLO_DIR, PROJ_TSS100_DESCRIPTION[0][2] )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s ) FAILED - \n%s\n" % \
                      ( PROJ_TSS100_DESCRIPTION[0][1], self.REPO_TSS100__CLO_DIR, out) )

    # direcotries
    self.assertTrue( os.path.exists( self.REPO_TSS100__CLO_DIR ), "not created directory %s" % self.REPO_TSS100__CLO_DIR )

    #
    # test mode MOREREPOS => add remote to orig
    #
    dest   = self.REPO_TSS100__CLO_DIR
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      #print "\n%s\nMOREREMOTES for repo %s\n%s\n" % ( "="*20, dest, "="*20 )
      helper = swgit__utils( dest )
      AREMOTE_PLAT = PROJ_TSS100_DESCRIPTION[0][0] + AREMOTE_PATH
      AREPO_AREMOTE_URL = "%s%s" % ( TESTER_SSHACCESS, AREMOTE_PLAT )
      out, errCode = helper.remote_add( ORIG_REPO_AREMOTE_NAME, AREPO_AREMOTE_URL )
      out, errCode = helper.pull()

    #create branch
    out, errCode = self.swu_TSS100_CLO.branch_create( self.MOD_TSS100_BR )
    self.assertEqual( errCode, 0, "FAILED creating branch for adding repo to proj %s - \n%s\n" % ( self.REPO_TSS100__CLO_DIR, out) )

  def util_addrepo_2proj( self, helper, repolist ):
    #add projs, DEV and CST
    for e in repolist:

      out, errCode = helper.proj_add( [ e ] )
      self.assertEqual( errCode, 0, "FAILED adding repo %s to project %s - \n%s\n" % \
                        ( e, helper.getDir(), out ) )

      out, errCode = helper.commit_minusA_dev_repolist( repolist = e[0] )
      self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                        ( helper.getDir(), out ) )

  # helper, src, shortBrName, rel
  def util_createCST( self, helper, REPO_PLAT__DEVBRANCH, CST_BRANCH_NAME, CST_BRANCH_REL ):
    #init CST
    out, errCode = helper.init_cst( REPO_PLAT__DEVBRANCH, CST_BRANCH_NAME, CST_BRANCH_REL )
    self.assertEqual( errCode, 0, "FAILED creating CST branch %s starting from %s into proj %s - \n%s\n" % \
                      ( CST_BRANCH_NAME,  REPO_PLAT__DEVBRANCH, self.REPO_PLAT__CLO_DIR, out) )

    remote = ""
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      remote = "origin"

    out, errCode = helper.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_TSS100__CLO_DIR, out ) )


  
  #################
  # Prepare repos #
  #################
  def util_createrepos_clonePLATproj_createBr_addFS_addAPP_commit_push( self ):
    #create ORIG repos
    out, errCode = swgit__utils.create_default_proj_repos()
    self.assertEqual( errCode, 0, "FAILED create default proj repos - \n%s\n" % (out) )

    self.util_clonePLAT_createBr()

    self.util_addrepo_2proj( self.swu_PLAT_CLO, PROJ_PLAT_DESCRIPTION[1] )

    remote = ""
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      remote = "origin"

    #push
    out, errCode = self.swu_PLAT_CLO.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PLAT__CLO_DIR, out ) )


  def util_createrepos_cloneTSS100proj_createBr_addDEVTDM_addCSTTDM_commit_push( self ):
    #create ORIG repos
    out, errCode = swgit__utils.create_default_proj_repos()
    self.assertEqual( errCode, 0, "FAILED create default proj repos - \n%s\n" % (out) )

    self.util_cloneTSS100_createBr()

    self.util_addrepo_2proj( self.swu_TSS100_CLO, [ PROJ_TSS100_DESCRIPTION[1][0], PROJ_TSS100_DESCRIPTION[1][3] ] )

    remote = ""
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      remote = "origin"

    #push
    out, errCode = self.swu_TSS100_CLO.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_TSS100__CLO_DIR, out ) )


  def util_createrepos_cloneTSS100proj_createBr_addDEVPLAT_commit_push( self ):
    self.util_createrepos_clonePLATproj_createBr_addFS_addAPP_commit_push()

    self.util_cloneTSS100_createBr()

    self.util_addrepo_2proj( self.swu_TSS100_CLO, [ PROJ_TSS100_DESCRIPTION[1][1] ] )

    remote = ""
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      remote = "origin"
    #push
    out, errCode = self.swu_TSS100_CLO.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_TSS100__CLO_DIR, out ) )


  def util_createrepos_cloneTSS100proj_createBr_addCSTPLAT_commit_push( self ):
    self.util_createrepos_clonePLATproj_createBr_addFS_addAPP_commit_push()

    self.util_createCST( self.swu_PLAT_CLO, REPO_PLAT__DEVBRANCH, CST_BRANCH_NAME, CST_BRANCH_REL )

    self.util_cloneTSS100_createBr()

    self.util_addrepo_2proj( self.swu_TSS100_CLO, [ PROJ_TSS100_DESCRIPTION[1][2] ] )

    remote = ""
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      remote = "origin"
    #push
    out, errCode = self.swu_TSS100_CLO.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_TSS100__CLO_DIR, out ) )


  def util_createrepos_cloneTSS100proj_createBr_addDEVPLAT_addCSTPLAT_addDEVTDM_addCSTTDM_commit_push( self ):
    self.util_createrepos_clonePLATproj_createBr_addFS_addAPP_commit_push()

    self.util_createCST( self.swu_PLAT_CLO, REPO_PLAT__DEVBRANCH, CST_BRANCH_NAME, CST_BRANCH_REL )

    self.util_cloneTSS100_createBr()

    self.util_addrepo_2proj( self.swu_TSS100_CLO, PROJ_TSS100_DESCRIPTION[1] )

    remote = ""
    if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
      remote = "origin"
    #push
    out, errCode = self.swu_TSS100_CLO.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_TSS100__CLO_DIR, out ) )


  def util_createAndCheck_PLAT_FULL_withbkp( self ):

    orig_projdir = PROJ_PLAT_DESCRIPTION[0][0]
    bkp_projdir  = orig_projdir + ".PLAT.FULL.BKP"
    shutil.rmtree( orig_projdir, True ) #ignore errors

    for bi in PROJ_PLAT_DESCRIPTION[1]:
      orig_dir = url_parse( bi[1] )["ROOT"]
      shutil.rmtree( orig_dir, True ) #ignore errors

    if os.path.exists( bkp_projdir ):

      shutil.copytree( bkp_projdir, orig_projdir )
      for bi in PROJ_PLAT_DESCRIPTION[1]:
        orig_dir = url_parse( bi[1] )["ROOT"]
        bkp_dir  = orig_dir + ".PLAT.FULL.BKP"
        shutil.copytree( bkp_dir, orig_dir )

    else:
      #first time create and also run tests on a clone like in:
      #  Test_ProjClone.test_ProjClone_00_00_Clone_1PROJ_2DEVrepo
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
      app_orig_helper = swgit__utils( REPO_PLAT__ORI_DIR + "/" + PROJ_PLAT_DESCRIPTION[1][1][0] )
      self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_PLAT_CLO2, app_clone_helper,
                                                        self.swu_PLAT_ORI, self.swu_APP_ORI,
                                                        repo_bi )

      shutil.copytree( orig_projdir, bkp_projdir )
      for bi in PROJ_PLAT_DESCRIPTION[1]:
        orig_dir = url_parse( bi[1] )["ROOT"]
        bkp_dir  = orig_dir + ".PLAT.FULL.BKP"
        shutil.copytree( orig_dir, bkp_dir )

      # clean CLO2 in case some test want to use it for a fresh new clone
      shutil.rmtree( self.REPO_PLAT__CLO2_DIR, True ) #ignore errors

    return 


  def util_createAndCheck_TSS100_FULL_withbkp( self ):

    orig_projdir = PROJ_TSS100_DESCRIPTION[0][0]
    bkp_projdir  = orig_projdir + ".TSS100.FULL.BKP"
    shutil.rmtree( orig_projdir, True ) #ignore errors

    for bi in PROJ_TSS100_DESCRIPTION[1]:
      orig_dir = url_parse( bi[1] )["ROOT"]
      shutil.rmtree( orig_dir, True ) #ignore errors
    for bi in PROJ_PLAT_DESCRIPTION[1]:
      orig_dir = url_parse( bi[1] )["ROOT"]
      shutil.rmtree( orig_dir, True ) #ignore errors

    if os.path.exists( bkp_projdir ):

      #restore first level repos
      shutil.copytree( bkp_projdir, orig_projdir )
      for bi in PROJ_TSS100_DESCRIPTION[1]:
        orig_dir = url_parse( bi[1] )["ROOT"]
        bkp_dir  = orig_dir + ".TSS100.FULL.BKP"
        #inside this proj, TDM and PLAT are listed twice, but are the same repo
        # second copy shoud fail, avoid it
        if os.path.exists( orig_dir ) == False:
          shutil.copytree( bkp_dir, orig_dir )

      #restore second level repos
      for bi in PROJ_PLAT_DESCRIPTION[1]:
        orig_dir = url_parse( bi[1] )["ROOT"]
        bkp_dir  = orig_dir + ".TSS100.FULL.BKP"
        #print "cp %s %s" % ( bkp_dir, orig_dir )
        shutil.copytree( bkp_dir, orig_dir )

    else:
      #first time create and also run tests on a clone like in:
      #  Test_ProjClone.test_ProjClone_04_00_Clone_1PROJ_1DEVproj_1CSTproj_1DEVrepo_1CSTrepo

      self.util_createrepos_cloneTSS100proj_createBr_addDEVPLAT_addCSTPLAT_addDEVTDM_addCSTTDM_commit_push()

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

      #check DEV PLAT PROJ, so also all its subsubrepos
      repo_bi = PROJ_TSS100_DESCRIPTION[1][1]
      devplat_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
      self.util_check_DEV_clonedPROJ_consinstency( self.swu_TSS100_CLO2, devplat_clone_helper,
                                                   self.swu_TSS100_ORI, self.swu_PLAT_ORI,
                                                   repo_bi,
                                                   PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj 

      #check CST PLAT PROJ, so also all its subsubrepos
      repo_bi = PROJ_TSS100_DESCRIPTION[1][2]
      cstplat_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
      self.util_check_CST_clonedPROJ_consinstency( self.swu_TSS100_CLO2, cstplat_clone_helper,
                                                   self.swu_TSS100_ORI, self.swu_PLAT_ORI,
                                                   repo_bi,
                                                   PROJ_PLAT_DESCRIPTION[1] ) # binfos for PLAT proj

      #check CST TDM
      repo_bi = PROJ_TSS100_DESCRIPTION[1][3]
      csttdm_clone_helper = swgit__utils( self.REPO_TSS100__CLO2_DIR + "/" + repo_bi[0] )
      self.util_check_DEVorCST_clonedREPO_consinstency( self.swu_TSS100_CLO2, csttdm_clone_helper,
                                                        self.swu_TSS100_ORI, self.swu_CSTTDM_ORI,
                                                        repo_bi )

      #backup first level repos
      shutil.copytree( orig_projdir, bkp_projdir )
      for bi in PROJ_TSS100_DESCRIPTION[1]:
        orig_dir = url_parse( bi[1] )["ROOT"]
        bkp_dir  = orig_dir + ".TSS100.FULL.BKP"
        #inside this proj, TDM and PLAT are listed twice, but are the same repo
        # second copy shoud fail, avoid it
        if os.path.exists( bkp_dir ) == False:
          shutil.copytree( orig_dir, bkp_dir )

      #backup second level repos
      for bi in PROJ_PLAT_DESCRIPTION[1]:
        orig_dir = url_parse( bi[1] )["ROOT"]
        bkp_dir  = orig_dir + ".TSS100.FULL.BKP"
        #print "cp %s %s" % ( orig_dir, bkp_dir )
        shutil.copytree( orig_dir, bkp_dir )


      # clean CLO2 in case some test want to use it for a fresh new clone
      shutil.rmtree( self.REPO_TSS100__CLO2_DIR, True ) #ignore errors

    return


  def util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self, dst, f_integrator = False ):
    self.util_createAndCheck_TSS100_FULL_withbkp()

    orig_projdir = dst
    if f_integrator:
      bkp_projdir  = orig_projdir + ".TSS100.FULL.CLONE.INTEGRATOR.BKP"
    else:
      bkp_projdir  = orig_projdir + ".TSS100.FULL.CLONE.BKP"
    shutil.rmtree( orig_projdir, True ) #ignore errors

    if os.path.exists( bkp_projdir ) == True:
      shutil.copytree( bkp_projdir, orig_projdir )
    else:
      if f_integrator:
        out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, orig_projdir, REPO_TSS100__DEVBRANCH, opt = " --integrator " )
        self.util_check_SUCC_scenario( out, errCode, "", "FAILED clone integrator into %s" % orig_projdir )
      else:
        out, errCode = swgit__utils.clone_repo_url( REPO_TSS100__ORI_URL, orig_projdir, REPO_TSS100__DEVBRANCH )
        self.util_check_SUCC_scenario( out, errCode, "", "FAILED clone defbr into %s" % orig_projdir )

      if os.environ.get( SWENV_TESTMODE ) == SWENV_MOREREMOTES:
        dest = orig_projdir
        #print "\n%s\nMOREREMOTES for repo %s\n%s\n" % ( "="*20, dest, "="*20 )
        helper = swgit__utils( dest )
        AREMOTE_REPO = PROJ_TSS100_DESCRIPTION[0][0] + AREMOTE_PATH
        AREPO_AREMOTE_URL = "%s%s" % ( TESTER_SSHACCESS, AREMOTE_REPO )
        out, errCode = helper.remote_add( ORIG_REPO_AREMOTE_NAME, AREPO_AREMOTE_URL )
        out, errCode = helper.pull()

        dest = helper.getDir() + "/" + tss100_name2path( "DEVPLAT" )
        #print "\n%s\nMOREREMOTES for repo %s\n%s\n" % ( "="*20, dest, "="*20 )
        helper = swgit__utils( dest )
        AREMOTE_REPO = PROJ_PLAT_DESCRIPTION[0][0] + AREMOTE_PATH
        AREPO_AREMOTE_URL = "%s%s" % ( TESTER_SSHACCESS, AREMOTE_REPO )
        out, errCode = helper.remote_add( ORIG_REPO_AREMOTE_NAME, AREPO_AREMOTE_URL )
        out, errCode = helper.pull()

      shutil.copytree( orig_projdir, bkp_projdir )

    return


  def util_createrepos_clonePLATproj_createBr_addSNAP_commit_push( self ):
    #create ORIG repos
    out, errCode = swgit__utils.create_default_proj_repos()
    self.assertEqual( errCode, 0, "FAILED create default proj repos - \n%s\n" % (out) )

    #clone to add snapshot repo
    dest   = self.REPO_PLAT__CLO_DIR
    url    = PROJ_PLAT_DESCRIPTION[0][1]
    branch = PROJ_PLAT_DESCRIPTION[0][2]
    out, errCode = swgit__utils.clone_repo_url( url, dest, branch )
    self.assertEqual( errCode, 0, "clone_repo_url( %s, %s ) FAILED - \n%s\n" % ( url, dest, out) )

    clo_h = self.swu_PLAT_CLO
    out, errCode = clo_h.branch_create( self.MOD_PLAT_BR )
    self.assertEqual( errCode, 0, "FAILED creating branch for adding repo to proj %s - \n%s\n" % ( dest, out) )


    out, errCode = clo_h.proj_add_snapshot( [ SNAP_BI ] )
    self.assertEqual( errCode, 0, "FAILED adding snapshot repo %s to project %s - \n%s\n" % \
                      ( SNAP_BI, clo_h.getDir(), out ) )

    out, errCode = clo_h.commit_minusA_dev_repolist( repolist = SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( clo_h.getDir(), out ) )

    out, errCode = clo_h.push_with_merge()
    self.assertEqual( errCode, 0, "FAILED push from %s to origin - \n%s\n" % ( dest, out ) )



  def util_createrepos_clonePLATproj_createBr_addFS_addAPP_addSNAP_commit_push( self ):
    #create ORIG repos
    out, errCode = swgit__utils.create_default_proj_repos()
    self.assertEqual( errCode, 0, "FAILED create default proj repos - \n%s\n" % (out) )

    self.util_clonePLAT_createBr()

    #FS and APP
    self.util_addrepo_2proj( self.swu_PLAT_CLO, PROJ_PLAT_DESCRIPTION[1] )

    #SNAP
    out, errCode = self.swu_PLAT_CLO.proj_add_snapshot( [ SNAP_BI ] )
    self.assertEqual( errCode, 0, "FAILED adding snapshot repo %s to project %s - \n%s\n" % \
                      ( SNAP_BI, self.swu_PLAT_CLO.getDir(), out ) )

    out, errCode = self.swu_PLAT_CLO.commit_minusA_dev_repolist( repolist = SNAP_BI[0] )
    self.assertEqual( errCode, 0, "FAILED commit with --repo-list, for proj: %s - \n%s\n" % \
                      ( self.swu_PLAT_CLO.getDir(), out ) )

    remote = ""
    if modetest_morerepos():
      #remote   = ORIG_REPO_AREMOTE_NAME
      remote   = "origin"

    #push
    out, errCode = self.swu_PLAT_CLO.push_with_merge( remote )
    self.assertEqual( errCode, 0, "FAILED push from %s to origin- swgit__utils.push - \n%s\n" % ( self.REPO_PLAT__CLO_DIR, out ) )





  ##########
  # CHECKS #
  ##########
  def util_check_DEVorCST_clonedREPO_consinstency( self, cloned_SUPERproj_helper, cloned_SUBrepo_helper, \
                                                         orig_SUPERproj_helper, orit_SUBrepo_helper, \
                                                         SUBrepo_baseinfo ):

    intrepo = True
    if SUBrepo_baseinfo[2].find( "/CST/" ) != -1:
      intrepo = False

    # dir exists
    self.assertTrue( os.path.exists( cloned_SUBrepo_helper.getDir() ), "not created directory %s" % cloned_SUBrepo_helper.getDir() )

    #dir is extracted (at least .git exists)
    repodotgit = cloned_SUBrepo_helper.getDir() + "/.git"
    self.assertTrue( os.path.exists( repodotgit ), "not created directory %s" % repodotgit )

    #map contents
    out, errCode = cloned_SUPERproj_helper.proj_check_map_unix( SUBrepo_baseinfo )
    self.assertEqual( errCode, 0, "after cloning proj %s, its map is KO for repo %s - \n%s\n" % \
                      ( cloned_SUPERproj_helper.getDir(), SUBrepo_baseinfo[0], out) )

    #origin url
    val, errCode = get_cfg( "remote.origin.url", cloned_SUBrepo_helper.getDir() )
    self.assertEqual( errCode, 0, \
                      "FAILED retrieving option %s into proj %s" % ( "remote.origin.url", cloned_SUBrepo_helper.getDir()) )
    self.assertEqual( val, SUBrepo_baseinfo[1], \
                      "FAILED cloning repo %s, wrong origin url %s, instead of %s" % \
                      ( cloned_SUBrepo_helper.getDir(), val, SUBrepo_baseinfo[1]) )

    #Def int Branch
    val, errCode = get_cfg( "swgit.intbranch", cloned_SUBrepo_helper.getDir() )
    self.assertEqual( errCode, 0, \
                      "FAILED retrieving option %s into proj %s" % ( "swgit.intbranch", cloned_SUBrepo_helper.getDir()) )
    self.assertEqual( val, SUBrepo_baseinfo[2], \
                      "FAILED cloning repo %s, wrong DEFAULT integration branch %s, instead of %s" % \
                      ( cloned_SUBrepo_helper.getDir(), val, SUBrepo_baseinfo[2]) )

    #Act int Branch
    # Also on CST repos, repo has int br (in order to move project commit)
    #   only subrepos inside CST proj have no int branch set!
    out, errCode = cloned_SUBrepo_helper.int_branch_get()
    self.assertEqual( out, SUBrepo_baseinfo[2], \
                      "Cloned, but wrong ACTUAL integration branch:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, SUBrepo_baseinfo[2], cloned_SUBrepo_helper.getDir()) )

    #Checkout
    out, errCode = cloned_SUBrepo_helper.get_currsha()
    self.assertEqual( errCode, 0, \
                      "Error retrieving currchk inside %s - \n%s\n" % \
                      ( cloned_SUBrepo_helper.getDir(), out ) )
    if intrepo == True:
      #DEV repos always on cloned-branch HEAD
      outorig, errCodeorig = orit_SUBrepo_helper.get_currsha( SUBrepo_baseinfo[2] )
      self.assertEqual( errCodeorig, 0, \
                        "Error retrieving currsha inside %s - \n%s\n" % \
                        ( orit_SUBrepo_helper.getDir(), out ) )
    else:
      #CST repos always on project stored sha
      outorig, errCodeorig = cloned_SUPERproj_helper.proj_getrepo_chk( SUBrepo_baseinfo[0] )
      self.assertEqual( errCodeorig, 0, \
                        "Error retrieving submodule sha inside %s - \n%s\n" % \
                        ( orig_SUPERproj_helper.getDir(), out ) )

    self.assertEqual( out, outorig, \
                      "Cloned, but wrong CHK:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, outorig, cloned_SUBrepo_helper.getDir()) )


    #current branch
    # CST => DETACHED-HEAD
    out, errCode = cloned_SUBrepo_helper.current_branch()
    if intrepo == True:
      self.assertEqual( out, SUBrepo_baseinfo[2], \
                        "Cloned, but wrong current branch for INT repo:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, SUBrepo_baseinfo[2], cloned_SUBrepo_helper.getDir()) )
    else:
      self.assertEqual( out, "(detached-head)", \
                        "Cloned, but wrong current branch for CST repo:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, "(detached-head)", cloned_SUBrepo_helper.getDir()) )


  def util_check_CST_clonedREPO_insideCSTproj_consinstency( self, cloned_SUPERproj_helper, cloned_SUBrepo_helper, \
                                                                  orig_SUPERproj_helper, orit_SUBrepo_helper, \
                                                                  SUBrepo_baseinfo ):

    # dir exists
    self.assertTrue( os.path.exists( cloned_SUBrepo_helper.getDir() ), "not created directory %s" % cloned_SUBrepo_helper.getDir() )

    #dir is extracted (at least .git exists)
    repodotgit = cloned_SUBrepo_helper.getDir() + "/.git"
    self.assertTrue( os.path.exists( repodotgit ), "not created directory %s" % repodotgit )

    #map contents
    CSTrepo_under_CSTproj_binfo = copy.deepcopy( SUBrepo_baseinfo )
    CSTrepo_under_CSTproj_binfo[2] = "" #NO INT BR SET inside CST repos under CST project

    out, errCode = cloned_SUPERproj_helper.proj_check_map_unix( CSTrepo_under_CSTproj_binfo )
    self.assertEqual( errCode, 0, "after cloning proj %s, its map is KO for repo %s - \n%s\n" % \
                      ( cloned_SUPERproj_helper.getDir(), SUBrepo_baseinfo[0], out) )

    #origin url
    val, errCode = get_cfg( "remote.origin.url", cloned_SUBrepo_helper.getDir() )
    self.assertEqual( errCode, 0, \
                      "FAILED retrieving option %s into proj %s" % ( "remote.origin.url", cloned_SUBrepo_helper.getDir()) )
    self.assertEqual( val, SUBrepo_baseinfo[1], \
                      "FAILED cloning repo %s, wrong origin url %s, instead of %s" % \
                      ( cloned_SUBrepo_helper.getDir(), val, SUBrepo_baseinfo[1]) )

    #Def int Branch NOT SET
    val, errCode = get_cfg( "swgit.intbranch", cloned_SUBrepo_helper.getDir() )
    self.assertNotEqual( errCode, 0, \
                         "FAILED retrieving option %s into proj %s" % ( "swgit.intbranch", cloned_SUBrepo_helper.getDir()) )

    #Act int Branch
    # Also on CST repos, repo has int br (in order to move project commit)
    # BUT
    # here we have subrepos inside CST proj : they have NO int branch set!
    out, errCode = cloned_SUBrepo_helper.int_branch_get()
    self.assertNotEqual( errCode, 0,
                        "Cloned, but wrong ACTUAL integration branch:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                        ( out, "SHOUL FAIL THIS GET", cloned_SUBrepo_helper.getDir()) )

    #Checkout
    out, errCode = cloned_SUBrepo_helper.get_currsha()
    self.assertEqual( errCode, 0, \
                      "Error retrieving currchk inside %s - \n%s\n" % \
                      ( cloned_SUBrepo_helper.getDir(), out ) )
    #CST repos always on project stored sha
    outorig, errCodeorig = cloned_SUPERproj_helper.proj_getrepo_chk( SUBrepo_baseinfo[0] )
    self.assertEqual( errCodeorig, 0, \
                      "Error retrieving submodule sha inside %s - \n%s\n" % \
                      ( orig_SUPERproj_helper.getDir(), out ) )

    self.assertEqual( out, outorig, \
                      "Cloned, but wrong CHK:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, outorig, cloned_SUBrepo_helper.getDir()) )


    #current branch NOT SET: DETACHED-HEAD
    out, errCode = cloned_SUBrepo_helper.current_branch()
    self.assertEqual( errCode, 0, \
                      "Cloned, but wrong current branch:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, "(detached-head)", cloned_SUBrepo_helper.getDir()) )
    self.assertEqual( out, "(detached-head)", \
                      "Cloned, but wrong current branch:\ncurrent:[%s]\nright:[%s]\ninside repo %s" % \
                      ( out, "(detached-head)", cloned_SUBrepo_helper.getDir()) )


  def util_check_DEV_clonedPROJ_consinstency( self, cloned_SUPERproj_helper, cloned_SUBproj_helper, \
                                                    orig_SUPERproj_helper, orig_SUBproj_helper, \
                                                    SUBproj_baseinfo, SUBproj_binfos ):

    #1. check SUBproj as a normal repo inside SUPERproj
    self.util_check_DEVorCST_clonedREPO_consinstency( cloned_SUPERproj_helper, cloned_SUBproj_helper, \
                                                      orig_SUPERproj_helper, orig_SUBproj_helper, \
                                                      SUBproj_baseinfo )

    #2. check SUBproj subrepos
    #    reuse util_check_DEVorCST_clonedREPO_consinstency by scaling everithing 1 level down
    for subsubrepo_bi in SUBproj_binfos:

      cloned_SUBSUBrepo_helper = swgit__utils( cloned_SUBproj_helper.getDir() + "/" + subsubrepo_bi[0] )

      # This doe not owrk because origin project usually has no repos under it.
      # From project DSC eval REAL origin for that subrepo
      #orig_SUBSUBrepo_helper   = swgit__utils( orig_SUBproj_helper.getDir() + "/"   + subsubrepo_bi[0] )
      orig_SUBSUBrepo_helper   = swgit__utils( url_parse( subsubrepo_bi[1] )["ROOT"] )

      self.util_check_DEVorCST_clonedREPO_consinstency( cloned_SUBproj_helper, cloned_SUBSUBrepo_helper, \
                                                        orig_SUBproj_helper, orig_SUBSUBrepo_helper, \
                                                        subsubrepo_bi )

  def util_check_CST_clonedPROJ_consinstency( self, cloned_SUPERproj_helper, cloned_SUBproj_helper, \
                                                    orig_SUPERproj_helper, orig_SUBproj_helper, \
                                                    SUBproj_baseinfo, SUBproj_binfos ):

    #1. check SUBproj as a normal repo inside SUPERproj
    self.util_check_DEVorCST_clonedREPO_consinstency( cloned_SUPERproj_helper, cloned_SUBproj_helper, \
                                                      orig_SUPERproj_helper, orig_SUBproj_helper, \
                                                      SUBproj_baseinfo )

    for subsubrepo_bi in SUBproj_binfos:

      cloned_SUBSUBrepo_helper = swgit__utils( cloned_SUBproj_helper.getDir() + "/" + subsubrepo_bi[0] )

      # This doe not owrk because origin project usually has no repos under it.
      # From project DSC eval REAL origin for that subrepo
      #orig_SUBSUBrepo_helper   = swgit__utils( orig_SUBproj_helper.getDir() + "/"   + subsubrepo_bi[0] )
      orig_SUBSUBrepo_helper   = swgit__utils( url_parse( subsubrepo_bi[1] )["ROOT"] )

      self.util_check_CST_clonedREPO_insideCSTproj_consinstency( cloned_SUBproj_helper, cloned_SUBSUBrepo_helper, \
                                                                 orig_SUBproj_helper, orig_SUBSUBrepo_helper, \
                                                                 subsubrepo_bi )


  ###################
  # INTEGRATOR REPO #
  ###################
  def util_check_repo_integrator( self, repoh ):
    #1. cfg must be set
    val, errCode = repoh.get_cfg( "swgit.integrator" )
    self.assertEqual( errCode, 0,
                      "FAILED INTEGRATOR - error while retrieving swgit.integrator inside repo: %s. - \n%s\n" %
                      ( repoh.getDir(), val ) )
    self.assertEqual( val, "TRUE",
                      "FAILED INTEGRATOR - error in swgit.integrator value inside repo: %s. - \n%s\n" %
                      ( repoh.getDir(), val ) )

    #2. develop and stable must be local
    ib, errCode = repoh.int_branch_get()
    sb = ib.replace( "develop", "stable" )

    localB, errCode = repoh.local_branches()
    localB = localB.splitlines()
    self.assertTrue( ib in localB,
                     "FAILED TARCKALL - inside repo %s, intbr %s should be among %s" %
                     ( repoh.getDir(), ib, localB ) )
    self.assertTrue( sb in localB,
                     "FAILED TARCKALL - inside repo %s, stbbr %s should be among %s" %
                     ( repoh.getDir(), sb, localB ) )


  def util_check_repo_NOT_integrator( self, repoh ):
    #1. cfg must NOT be set
    val, errCode = repoh.get_cfg( "swgit.integrator" )
    self.assertNotEqual( errCode, 0,
                      "FAILED INTEGRATOR - MUST NOT BE SET swgit.integrator inside repo: %s. - \n%s\n" %
                      ( repoh.getDir(), val ) )

    #if CST int br => must not exist INT BRANCHES
    ib, errCode = repoh.int_branch_get()

    localB, errCode = repoh.local_branches()
    localB = localB.splitlines()

    if ib.find( "/CST/" ) != -1:
      sb = ib.replace( "develop", "stable" )

      self.assertTrue( ib in localB,
                       "FAILED TARCKALL - inside repo %s, intbr %s should be among local branches %s" %
                       ( repoh.getDir(), ib, localB ) )
      self.assertTrue( sb in localB,
                       "FAILED TARCKALL - inside repo %s, stbbr %s should be among local branches %s" %
                       ( repoh.getDir(), sb, localB ) )
    elif ib.find( "develop" ):
      #if INT integration branch => must not exists stable
      sb = ib.replace( "develop", "stable" )

      self.assertTrue( sb not in localB,
                       "FAILED TARCKALL - inside repo %s, stbbr %s should NOT be among local branches %s" %
                       ( repoh.getDir(), sb, localB ) )
    else:
      #if FTR integration branch => must not exists INT branches
      for b in localB:
        self.assertEqual( b.find( "/INT/" ), -1, 
                         "FAILED TARCKALL - inside repo %s, INT branch %s should NOT be among local branches %s" %
                         ( repoh.getDir(), b, localB ) )



