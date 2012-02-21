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
from pprint import pprint
from optparse import *

from _utils import *
from util_prepare_sandbox import *

# Test defined by ourselves
import test_clone
import test_branch
import test_checkout
import test_commit
import test_tag
import test_merge
import test_init
import test_pull
import test_push
import test_nointbr
import test_stabilize
import test_proj
import test_proj_clone
import test_proj_snapshot
import test_proj_update
import test_proj_merge
import test_proj_stabilize
import test_all
import test_workflow
import test_readonly

tests_map = (
    test_init,
    test_clone,
    test_branch,
    test_commit,
    test_checkout,
    test_tag,
    test_merge,
    test_pull,
    test_push,
    test_nointbr,
    test_stabilize,
    test_proj,
    test_proj_clone,
    test_proj_snapshot,
    test_proj_merge,
    test_proj_update,
    test_proj_stabilize,
    test_all,
    test_workflow,
    test_readonly,
    )

tests_modes = ( SWENV_NONE, SWENV_MOREREMOTES, SWENV_LOCALREPOS )

def usage():
  print "\nall_tests_runner.py [--debug]\t\t\tRunning all tests"
  print "all_tests_runner.py [aTestNum] [--debug]\tRunning a specific bunch of tests\n"
  for idx, val in enumerate( tests_map ):
    print '[%s] %s' % (idx, val)
  sys.exit( 1 )


################
# MAIN
################
def main():
  usagestr = """
  all_tests_runner.py [-d|-p|-m]
  all_tests_runner.py [aTestNum] [-d][-l][-m]

"""
  usagestr += "TESTS:\n"
  for idx, val in enumerate( tests_map ):
    usagestr += ("[%s]" % idx).ljust(4) + " %s\n" % val.__name__
  usagestr += "\nMODES:\n"
  for idx, val in enumerate( tests_modes ):
    usagestr += ("[%s]" % idx).ljust(4) + " %s\n" % val

  parser     = OptionParser( usage = usagestr, description='>>>>>>>>>>>>>> swgit - Test Management <<<<<<<<<<<<<<' )
  parser.add_option( debug_option[0][0], debug_option[0][1], **debug_option[0][2] )
  parser.add_option( debug_option[1][0], debug_option[1][1], **debug_option[1][2] )
  parser.add_option( debug_option[2][0], debug_option[2][1], **debug_option[2][2] )
  parser.add_option( list_option[0], list_option[1], **list_option[2] )

  (options, args)  = parser.parse_args()

  str_debug = ""
  if options.debug:
    debug()
    str_debug = "-d"

  if options.printdefs:
    print_defines()

  if len( args ) == 0:
    if options.list:
      parser.error( "" )
    else:
      pass
  elif len( args ) == 1:
    try:
      opnum = int( args[0] )
      if options.list:
        #
        # print all tests from one category
        #
        if options.test_mode != None:
          strenv = "%s=%s " % (SWENV_TESTMODE,tests_modes[options.test_mode])
        else:
          strenv = ""

        tests = unittest.TestLoader().loadTestsFromModule( tests_map[opnum] )
        for elem in tests._tests:
          for t in elem._tests:
            cname = t.__class__.__name__
            strr = "%s./%s.py -vc %s.%s --debug" % ( strenv, tests_map[opnum].__name__, cname, t._testMethodName )
            print strr

        sys.exit( 0 )

      else:
        #
        # run all tests from one category
        #
        if options.test_mode == SWENV_NONE or options.test_mode == SWENV_MOREREMOTES:
          ret = check_sshd()
          if ret != 0:
            print "Cannot execute mode %s because of NOT ssh access" % tests_modes[options.test_mode]
            sys.exit( 1 )

        if options.test_mode != None:
          os.environ[SWENV_TESTMODE] = tests_modes[options.test_mode]

        ret = os.system( "%s/_int_all_tests_runner.py %s %d" % ( TESTDIR, str_debug, opnum ) )

        sys.exit( ret )

    except ValueError:
      parser.error( "" )

  else:
    parser.error( "" )
  
  if options.test_mode == None:

    #
    # run all tests, all modes
    #
    for env_var in tests_modes:

      if env_var == SWENV_NONE or env_var == SWENV_MOREREMOTES:
        ret = check_sshd()
        if ret != 0:
          print "Cannot execute mode %s because of NOT ssh access" % env_var
          continue

      os.environ[SWENV_TESTMODE] = env_var
      os.system( "%s/_int_all_tests_runner.py %s" % ( TESTDIR, str_debug) )

  else:

      #
      # run all tests, 1 mode
      #
      if options.test_mode == SWENV_NONE or options.test_mode == SWENV_MOREREMOTES:
        ret = check_sshd()
        if ret != 0:
          print "Cannot execute mode %s because of NOT ssh access" % tests_modes[options.test_mode]
          sys.exit( 1 )

      os.environ[SWENV_TESTMODE] = tests_modes[options.test_mode]
      os.system( "%s/_int_all_tests_runner.py %s" % (TESTDIR, str_debug) )

  return 0



#############
# INPUT
#############
def check_sshd():
  print "testing ssh access on %s with user %s" % ( TEST_USER_SSH, TEST_ADDR )
  return os.system( "ssh %s@%s 'exit 0'" % ( TEST_USER_SSH, TEST_ADDR ) )

def check_testmode(option, opt_str, value, parser):
  if value < 0 or value >= len( tests_modes ):
    parser.error("Option -m must be between: %s and %s" % (0, len(tests_modes) -1) )
  setattr(parser.values, option.dest, value)


debug_option = [
    [
      "-d",
      "--debug",
      {
        "action"  : "store_true",
        "dest"    : "debug",
        "default" : False,
        "help"    : 'print executed commands to stdout'
        }
      ],
    [
      "-p",
      "--print",
      {
        "action"  : "store_true",
        "dest"    : "printdefs",
        "default" : False,
        "help"    : 'print defines used into these tests'
        }
      ],
    [
      "-m",
      "--mode",
      { 
        "nargs"   : 1,
        "type"    : "int",
        "action"  : "callback",
        "dest"    : "test_mode",
        "metavar" : "test_mode",
        "callback": check_testmode,
        "help"    : "Choose a test mode among '%s'" % "' '".join( tests_modes )
        }
      ],
    ]


list_option = [
    "-l",
    "--list",
    {
      "action"  : "store_true",
      "dest"    : "list",
      "default" : False,
      "help"    : 'print all tests to be runned 1 by 1'
      }
    ]


if __name__ == "__main__":
  main()



