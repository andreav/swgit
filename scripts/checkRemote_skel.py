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

from string import Template
import sys

check_remote_script = Template("""\

import sys, os
from pwd import getpwuid
from os import stat

path = "${PLACEHOLDER_PATH}"
path = os.path.abspath( path )
user = "${PLACEHOLDER_USER}"
branch = "${PLACEHOLDER_BRANCH}"
chk = "${PLACEHOLDER_CHK}"


# [ [ -a %s/.git ] || [ -a %s/swProjMap ] ] && exit 0 || exit 1
if os.path.exists( path + "/.git" ) != True:
  print "ERROR: \\n Repository %s seems not to be a git repository (no .git root directory)" % path
  sys.exit( 1 )

#[ $$( stat -c %%U %s ) == %s ] && exit 0 || exit 1" % ( path, ssh_user )
if  getpwuid(stat(path).st_uid).pw_name != user:
  print "ERROR: \\n User '%s' is not the owner of repository %s " % ( user, path )
  sys.exit( 1 )

#
# if no branch passed, jump this check, clone HEAD
#
if branch != "": 
  branch_dot = branch.replace( '.', '\.' )
  cmd_branch = "/bin/bash -c 'cd %s && git branch | cut -c 3- | grep -w -e \\"^%s$$\\" &>/dev/null'" % ( path,branch_dot )
  ret = os.system( cmd_branch )
  if ret != 0:
    print "ERROR: \\n Branch '%s' not existing into repository '%s' " % ( branch, path )
    sys.exit( 1 )

if chk != "":
  cmd_checkout = "/bin/bash -c 'cd %s && git rev-parse --quiet --verify %s^{} &>/dev/null'" % ( path, chk )
  ret = os.system( cmd_checkout )
  if ret != 0:
    print "ERROR: \\n Reference '%s' not existing into repository '%s' " % ( chk, path )
    sys.exit( 1 )


sys.exit( 0 )

""" )

def main():
  global check_remote_script
  check_remote_script = check_remote_script.substitute(
      PLACEHOLDER_PATH = sys.argv[1],
      PLACEHOLDER_USER = sys.argv[2],
      PLACEHOLDER_BRANCH = sys.argv[3],
      PLACEHOLDER_CHK = sys.argv[4]
      )
  print check_remote_script


if __name__ == "__main__":
  main()

