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

#
# This command is used for many many things
# try to distinguish between "sane" and "unsane"
#
# * "sane"   is: branch create, but force using swgit branch
#                checkout when work dir is clean
#                conflict resolution with binaries (--ours, --theirs ... )
#                file undo
#
# * "unsane" is: branch + reset (-B option)
#                set upstream information (use instead swgit branch --track)
#                create orphan branches (also if sometimes useful)
#                change branch and merge working dir with other branch: 
#                                        stash and stash pop is more sane
#
# only "sane" things are allowed
#   branch management is forwarded to swgit branch
#   rest is passed to git by system

import sys,os

from Common import *
from ObjStatus import * 

def main():
  help_mach()

  start_ref        = ""
  other_options    = False

  jump_next = False
  #print sys.argv
  for (i, o) in enumerate( sys.argv ):
    if i == 0:
      continue
    if jump_next: 
      jump_next = False
      continue

    if o in [ "--conflict", "--orphan", "--track", "-t", "-f", "--no-track", "-m", "--merge", "-p", "--patch" ]:
      print "Option %s not supported" % o
      sys.exit( 1 )

    #intercept checkout when it means create branch
    if o == "-b" or o == "-B":
      print "If you want to create a branch, please use swgit branch command"
      sys.exit( 1 )
  
    # --ours, --theirs, -l, -- <path>
    if o[0] == '-':
      continue

    #print "o: %s" % o
    err, sha = getSHAFromRef( o )
    #print err, sha
    if err == 0:
      start_ref = o
      continue

    #we found something not reference nor 'option' => path => stop parsing 
    #  pass to git
    other_options = True
    break


  #print "startref: %s" % start_ref
  #print "otheropt: %s" % other_options

  if start_ref != "" and other_options == False: #chekout to a new commit
    #check local status like in swgit branch -s
    err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
    if err != 0:
      print "Cannot change HEAD to %s because of dirty working directory. Please commit or stash and retry.\n%s" % (start_ref, errstr)
      sys.exit( 1 )

  #everithing else
  sys.argv[0] = "git checkout"
  cmd_res = " ".join( sys.argv )

  #print cmd_res
  
  ret = os.system( cmd_res )
  if ret != 0:
    sys.exit( 1 )
  sys.exit( 0 )


def help_mach():
  if os.environ.get('SWHELPMAC') != "PRINT": 
    return 0


if __name__ == "__main__":
  main()


