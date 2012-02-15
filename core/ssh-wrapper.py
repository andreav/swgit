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

import os, sys, subprocess
import Defines
import ObjCfg

objSsh = ObjCfg.ObjCfgSsh()
ssh_elem_list = objSsh.eval_git_ssh_envvar_list()

args = [ "dummy_argv0" ]
args += ssh_elem_list[1:]
args += sys.argv[1:]


#debug
#print >> sys.stderr, args

# v => variable list of argument
# p => uses $PATH
os.execvp( ssh_elem_list[0], args )

