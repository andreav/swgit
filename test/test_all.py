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


class Test_All( Test_ProjBase ):

  def setUp( self ):
    super( Test_All, self ).setUp()

  def tearDown( self ):
    super( Test_All, self ).tearDown()


  def test_All_01_00_Branch( self ):
    self.util_createAndCheck_TSS100_FULL_withbkp_andclonedefbr( self.REPO_TSS100__CLOVALLEA_DIR )

    ori_hm = self.util_get_TSS10FULL_helper_map_orig()
    clo_hm = self.util_get_TSS10FULL_helper_map_clone( self.REPO_TSS100__CLOVALLEA_DIR )

    out, errCode = clo_hm["TSS100"].local_branches( "--all" )
    self.util_check_SUCC_scenario( out, errCode, "", "get local br" )

    out, errCode = clo_hm["TSS100"].remote_branches( "--all" )
    self.util_check_SUCC_scenario( out, errCode, "", "get local br" )

    out, errCode = clo_hm["TSS100"].all_branches( "--all" )
    self.util_check_SUCC_scenario( out, errCode, "", "get local br" )


    out, errCode = clo_hm["TSS100"].local_branches_byuser( TEST_USER, "--all" )
    self.util_check_SUCC_scenario( out, errCode, "", "get local br" )


    #fails for CST repos
    out, errCode = clo_hm["TSS100"].int_branch_get( "--all" )
    self.util_check_DENY_scenario( out, errCode, "", "get int br" )
    #here it pass
    out, errCode = clo_hm["DEVPLAT"].int_branch_get( "--all" )
    self.util_check_SUCC_scenario( out, errCode, "", "get int br" )

    out, errCode = clo_hm["TSS100"].current_branch( "--all" )
    self.util_check_SUCC_scenario( out, errCode, "", "get curr br" )




if __name__ == '__main__':
  manage_debug_opt( sys.argv )
  unittest.main()





