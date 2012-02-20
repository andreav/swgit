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

from all_tests_runner import *

def run_all():

  env_var = os.environ.get(SWENV_TESTMODE)
  if env_var == None:
    env_var = ""

  print "\n>>>>>>>>>> CLEAN SANDBOX <<<<<<<<<<\n"

  setup_sandbox()
  
  print "\n>>>>>>>>>> mode='%s' INIT <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_init.Test_Init )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' CLONE <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_clone.Test_Clone )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' BRANCH <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_branch.Test_Branch )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' CHECKOUT <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_checkout.Test_Checkout )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' COMMIT <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_commit.Test_Commit )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' TAG <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_tag.Test_Tag )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' MERGE <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_merge.Test_Merge )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PULL <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_pull.Test_Pull )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PUSH <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_push.Test_Push )
  unittest.TextTestRunner( verbosity=2 ).run( suite )
  
  print "\n>>>>>>>>>> mode='%s' NO INTBR <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_nointbr.Test_NoIntBr )
  unittest.TextTestRunner( verbosity=2 ).run( suite )
  
  print "\n>>>>>>>>>> mode='%s' STABILIZE <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_stabilize.Test_Stabilize )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PROJ <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_proj.Test_Proj )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PROJ CLONE <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_proj_clone.Test_ProjClone )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PROJ SNAPSHOT <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_proj_snapshot.Test_ProjSnapshot )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PROJ MERGE <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_proj_merge.Test_ProjMerge )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' PROJ UPDATE <<<<<<<<<<\n" % env_var

  suite = unittest.TestLoader().loadTestsFromTestCase( test_proj_update.Test_ProjUpdate )
  unittest.TextTestRunner( verbosity=2 ).run( suite )

  print "\n>>>>>>>>>> mode='%s' WORKFLOW <<<<<<<<<<\n"

  suite = unittest.TestLoader().loadTestsFromTestCase( test_workflow.Test_Workflow )
  unittest.TextTestRunner( verbosity=2 ).run( suite )



def main():

  parser     = OptionParser( description='_int_all_test_runner.py' )
  parser.add_option( debug_option[0][0], debug_option[0][1], **debug_option[0][2] )
  (options, args)  = parser.parse_args()

  if options.debug:
    debug()

  if len( args ) > 1:

    parser.error( "" )

  elif len( args ) == 1:

    opnum = int( args[0] )

    create_protorepo()

    suite = unittest.TestLoader().loadTestsFromModule( tests_map[opnum] )
    ret = unittest.TextTestRunner( verbosity=2 ).run( suite )
    sys.exit( ret )

  else:

    run_all()

  return 0


if __name__ == "__main__":
  main()

