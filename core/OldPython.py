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
# IN THIS FILE WE PUT THING OLD PYTHONS HAS NOT
#

import os
import sys

# Creates os.path.relpath for Python 2.4

if not hasattr(os, 'relpath'):
    if os.path is sys.modules.get('ntpath'):
        def relpath(path, start=os.path.curdir):
            """Return a relative version of a path"""
        
            if not path:
                raise ValueError("no path specified")
            start_list = os.path.abspath(start).split(os.path.sep)
            path_list = os.path.abspath(path).split(os.path.sep)
            if start_list[0].lower() != path_list[0].lower():
                unc_path, rest = os.path.splitunc(path)
                unc_start, rest = os.path.splitunc(start)
                if bool(unc_path) ^ bool(unc_start):
                    raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)"
                                                                        % (path, start))
                else:
                    raise ValueError("path is on drive %s, start on drive %s"
                                                        % (path_list[0], start_list[0]))
            # Work out how much of the filepath is shared by start and path.
            for i in range(min(len(start_list), len(path_list))):
                if start_list[i].lower() != path_list[i].lower():
                    break
            else:
                i += 1
        
            rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
            if not rel_list:
                return os.path.curdir
            return os.path.join(*rel_list)
    
    else:
        # default to posixpath definition
        def relpath(path, start=os.path.curdir):
            """Return a relative version of a path"""
        
            if not path:
                raise ValueError("no path specified")
        
            start_list = os.path.abspath(start).split(os.path.sep)
            path_list = os.path.abspath(path).split(os.path.sep)
        
            # Work out how much of the filepath is shared by start and path.
            i = len(os.path.commonprefix([start_list, path_list]))
        
            rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
            if not rel_list:
                return os.path.curdir
            return os.path.join(*rel_list)
        
    os.path.relpath = relpath

