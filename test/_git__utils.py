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

import shutil

from _utils import *

#########################################################
#
# git tools
#
#########################################################
class git__utils:
  def __init__( self, repodir ):
    self.repodir_ = repodir

  def get_currsha( self, ref="HEAD" ):
    cmd = "cd %s; git rev-parse --quiet --verify %s^{}" % ( self.repodir_, ref )
    return myCommand( cmd )

  def status( self ):
    cmd = "cd %s; git status -s " % ( self.repodir_ )
    return myCommand( cmd )

  def checkout( self, ref ):
    cmd = "cd %s; git checkout %s" % ( self.repodir_, ref )
    return myCommand( cmd )

  def branch_create( self, name ):
    cmd = "cd %s; git checkout -b %s" % ( self.repodir_, name )
    return myCommand( cmd )

  def merge( self, ref ):
    cmd = "cd %s; git merge %s --no-ff %s" % ( self.repodir_, FIX_MERGE_EDIT, ref )
    return myCommand( cmd )

  # Here must switch before.
  #  this is because otherwise .gitignore of superior repo is used
  def commit_minusA( self ):
    cmd = "cd %s; git commit -a -m \"default msg\"" % ( self.repodir_ )
    return myCommand( cmd )

  def current_branch( self ):
    cmd = "cd %s; git branch | grep \* | cut -c 3-" % self.repodir_ 
    return myCommand( cmd )

  def all_branches( self ):
    cmd = "cd %s; git branch -a | cut -c 3- | grep -v -e \"\->\" " % self.repodir_
    return myCommand( cmd )

  def local_branches( self ):
    cmd = "cd %s; git branch | grep -v '%s' | cut -c 3-" % (self.repodir_, NO_BRANCH)
    return myCommand( cmd )

  def remote_branches( self ):
    cmd = "cd %s; git branch -r | cut -c 3- | grep -v -e \"\->\" | grep -e \"^origin\"" % self.repodir_
    return myCommand( cmd )

  def local_branches_byuser( self, user ):
    cmd = "cd %s; git branch | cut -c 3- | grep -e \"/%s/\"" % (self.repodir_, user )
    return myCommand( cmd )

  def branch_exists( self, brname ):
    cmd = "cd %s; git branch | grep %s" % ( self.repodir_, brname )
    return myCommand( cmd )

  def tag_get( self, type, ref="HEAD" ):
    cmd = "cd %s; git describe --exact-match --tags %s --match \"*/%s/*\"" % (self.repodir_, ref, type )
    return myCommand( cmd )

  def tag_list( self ):
    cmd = "cd %s; git tag" % (self.repodir_ )
    return myCommand( cmd )

  def tag_put( self, tag, msg = "default" ):
    cmd = "cd %s; git tag %s -m \"%s\"" % (self.repodir_, tag, msg )
    return myCommand( cmd )

  def tag_put_on_commit( self, tag, commit, msg = "default" ):
    cmd = "cd %s; git tag -m \"%s\" %s %s" % (self.repodir_, msg, tag, commit )
    return myCommand( cmd )

  def tag_get_subject( self, tag ):
    #cmd = "cd %s; git show --name-only %s" % (self.repodir_, tag )
    #cmd = "cd %s; git log -1 --pretty=format:%%s %s" % (self.repodir_, tag )
    cmd = "cd %s && git cat-file tag %s |  sed -n '6,$p'" % (self.repodir_, tag )
    return myCommand( cmd )
  def tag_get_body( self, tag ):
    cmd = "cd %s && git log -1 --format=%%B %s" % (self.repodir_, tag )
    return myCommand( cmd )

  def ref2sha( self, ref ):
    cmd = "cd %s; git rev-list -1 %s" % (self.repodir_, ref )
    return myCommand( cmd )


