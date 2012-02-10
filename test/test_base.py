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

from _utils import *
from _git__utils import *
from _swgit__utils import *


class Test_Base( unittest.TestCase ):

  sw_origrepo_h = swgit__utils( TEST_ORIG_REPO )
  sw_aremoterepo_h = swgit__utils( TEST_ORIG_REPO_AREMOTE )

  DDTS            = "Issue12345"

  def setUp( self ):
    if hasattr( self, '_TestCase__testMethodName' ): #older python
      initlogs( self._TestCase__testMethodName + ".log" )
    elif hasattr( self, '_testMethodName' ): #newer python
      initlogs( self._testMethodName + ".log" )
    #else write on global file (swgit_tests.log)

  def tearDown( self ):
    pass


  def util_check_SUCC_scenario( self, cmd_out, cmd_res, cmd_attended_out, test_out ):
    self.assertEqual( cmd_res, 0, "\n\n<<FAILED>> - %s\n\n%s\n" % (test_out, cmd_out) )
    if cmd_attended_out != "":
      self.assertTrue ( cmd_attended_out in cmd_out, "\n%s,\nNOT FOUND\n'%s'\n\n - inside output - \n\n%s\n" % (test_out,cmd_attended_out,cmd_out) )


  def util_check_DENY_scenario( self, cmd_out, cmd_res, cmd_attended_out, test_out ):
    self.assertEqual( cmd_res, 1, "\n\n<<MUST FAIL>> - %s\n\n%s\n" % (test_out, cmd_out) )
    if cmd_attended_out != "":
      self.assertTrue ( cmd_attended_out in cmd_out, "\n%s,\nNOT FOUND\n'%s'\n\n - inside output - \n\n%s\n" % (test_out,cmd_attended_out,cmd_out) )

