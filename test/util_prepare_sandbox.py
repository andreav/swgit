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

from defines import *

def modetest_morerepos():
  env_var = os.environ.get(SWENV_TESTMODE)
  if env_var == SWENV_MOREREMOTES:
    return True
  return False


def recreate_sandbox():
  for d in ( SANDBOX, SANDBOX_777 ):
    recreate_dir( d )


  os.system( "chmod 777 %s 2>&1 1>/dev/null" % SANDBOX_777 )
  shutil.rmtree( TEST_ORIG_REPO, True )
  shutil.rmtree( LOGS_DIR, True )

  create_protorepo()

protorepos = (
    {
      "abspath" : TEST_ORIG_REPO,
      "name"    : ORIG_REPO_NAME,
      "initopt" : "",
      },
    {
      "abspath" : TEST_ORIG_REPO_SHARED,
      "name"    : ORIG_REPO_NAME_SHARED,
      "initopt" : "--shared group",
      },
    )


#used by other readonly tests
def recreate_protorepo():
  for p in protorepo:
    os.system( "rm -rf %s" % p["abspath"] )

def recreate_repos():
  import _swgit__utils
  _swgit__utils.swgit__utils.create_default_proj_repos()


def recreate_dir( dir ):
  #print "Cleaning %s " % dir
  shutil.rmtree( dir, True )
  os.mkdir( dir )

  env_var = os.environ.get(SWENV_TESTMODE)
  if env_var == "":
    env_var = SWENV_NONE

  cmd = "touch %s/%s" % ( dir, env_var )
  os.system( cmd )


def create_protorepo():

  env_var = os.environ.get(SWENV_TESTMODE)
  if env_var == None:
    env_var = SWENV_NONE

  if not os.path.exists( SANDBOX  ):
    recreate_dir( SANDBOX )
  if not os.path.exists( "%s/%s" % (SANDBOX, env_var) ):
    recreate_dir( SANDBOX )

  if not os.path.exists( SANDBOX_777 ):
    recreate_dir( SANDBOX_777 )
    os.system( "chmod 777 %s 2>&1 1>/dev/null" % SANDBOX_777 )
  if not os.path.exists( "%s/%s" % (SANDBOX_777, env_var) ):
    recreate_dir( SANDBOX_777 )
    os.system( "chmod 777 %s 2>&1 1>/dev/null" % SANDBOX_777 )

  if not os.path.exists( LOGS_DIR ):
    os.mkdir( LOGS_DIR )
    os.system( "chmod 777 %s 2>&1 1>/dev/null" % LOGS_DIR )


  for r in protorepos:

    # 2. every time scripts are runned, check for PROTOREPO existence
    ori_repo = r["abspath"]
    bkp_repo = "%s.ORI.BKP" % ori_repo

    if os.path.exists( ori_repo ):
      continue

    if os.path.exists( bkp_repo ):
      shutil.copytree( bkp_repo, ori_repo )
      continue

    cmd_create_10 = "cd %s && mkdir %s && cd %s && %s init -r 1.0.0.0 -l Drop.A --git-user %s %s" % \
        ( ORIG_REPO_DIR, r["name"], r["name"], SWGIT, ORIG_REPO_GITUSER, r["initopt"] )

    cmd_makecommit_10 = "cd %s && git checkout 1/0/0/0/%s/INT/develop && echo \"aa\" > a.txt && git add a.txt && git commit -m \"file 1.0\"" % \
        ( r["abspath"], ORIG_REPO_GITUSER )

    cmd_create_20 = "cd %s && %s init -r 2.0.0.0 -l Drop.A --source 1/0/0/0/%s/INT/develop --git-user %s %s" % \
        ( r["abspath"], SWGIT, ORIG_REPO_GITUSER, ORIG_REPO_GITUSER, r["initopt"] )

    cmd_makecommit_20 = "cd %s && git checkout 2/0/0/0/%s/INT/develop && echo \"bb\" > b.txt && git add b.txt && git commit -m \"file 2.0\"" % \
        ( r["abspath"], ORIG_REPO_GITUSER )

    cmd_makebranch_20 = "cd %s && %s branch -c %s --source %s && echo \"cc\" > c.txt && git add c.txt && git commit -m \"file from FTR branch\" && git tag -m \"test dev tag\" %s/DEV/000 &&  echo \"cc2\" >> c.txt && git add c.txt && git commit -m \"file from FTR branch second\" && git tag -m \"test fix tag\" %s/FIX/Issue12345 && echo \"cc3\" >> c.txt && git add c.txt && git commit -m \"file from FTR branch third\" && git tag -m \"test dev tag\" %s/DEV/001 && git checkout %s && git merge %s --no-ff %s/DEV/001" % \
        ( r["abspath"], SWGIT, ORIG_REPO_aBRANCH_NAME, ORIG_REPO_DEVEL_BRANCH, ORIG_REPO_aBRANCH, ORIG_REPO_aBRANCH, ORIG_REPO_aBRANCH, ORIG_REPO_DEVEL_BRANCH, FIX_MERGE_EDIT, ORIG_REPO_aBRANCH )

    o, e = myCommand_fast( cmd_create_10 )
    if e != 0:
      print "Error while issueing command: %s" % cmd_create_10
      return 0,e
    o, e = myCommand_fast( cmd_makecommit_10 )
    if e != 0:
      print "Error while issueing command: %s" % cmd_makecommit_10
      return 0,e
    o, e = myCommand_fast( cmd_create_20 )
    if e != 0:
      print "Error while issueing command: %s" % cmd_create_20
      return 0,e
    o, e = myCommand_fast( cmd_makecommit_20 )
    if e != 0:
      print "Error while issueing command: %s" % cmd_makecommit_20
      return 0,e

    o, e = myCommand_fast( cmd_makebranch_20 )
    if e != 0:
      print "Error while issueing command: %s" % cmd_makebranch_20
      return 0,e

    shutil.copytree( ori_repo, bkp_repo )
    continue




def main():
  usage = """
  usage: %s [-s|-p|-r]
            -s  recraete sandbox
            -p  recreate protorepo
            -r  recreate default repos
  """ % sys.argv[0]

  if len( sys.argv ) != 2 or sys.argv[1] == "-h":
    print usage
    sys.exit( 1 )

  if sys.argv[1] == "-p":
    recreate_protorepo()
  elif sys.argv[1] == "-s":
    recreate_sandbox()
  elif sys.argv[1] == "-r":
    recreate_repos()
  else:
    print usage
    sys.exit( 1 )




if __name__ == '__main__':
  main()


