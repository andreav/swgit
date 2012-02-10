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

from pprint import pprint
import ConfigParser

from Common import *
from ObjEnv import *


#
# factory methods
#
def create_swmap( startdir = ".", debug = False ):

  root = Env.getProjectRoot( startdir )
  if root == "":
    return SwMap_Null()

  m = SwMap( root, debug )

  if debug == True:
    m.dump()

  return m



#config = ConfigParser.RawConfigParser()
g_swProjMap = None

MAP_URL = "ORIGINAL_URL"
MAP_LOCALPATH = "LOCAL_PATH"
MAP_DEF_BRANCH = "DEF_BRANCH"
MAP_ACT_BRANCH = "ACT_BRANCH"
MAP_CHK = "CHECKOUT"
MAP_NAME = "NAME"
MAP_ABS_LOCALPATH = "ABS_LOCALPATH"
MAP_CURR_BRANCH = "CURR_BRANCH"

# Attention, this is valorized only during SwOperation process,
#  because depth is a dynamic info, depending on root  start point.
MAP_DEPTH = "DEPTH"


######################
#
# SwMap
#
######################
class SwMap( object ):
  def __init__( self, rootdir, debug = False ):

    if debug == True:
      print "SwMap - rootdir: %s" %  rootdir

    try:

      self._absfilename = ""
      self._sectionObjs_written = None
      self._sectionObjs_actual = None
      self._debug = debug
      self._isValid = False

      absfilename = os.path.abspath( rootdir + "/" + SWFILE_PROJMAP )
      if os.path.exists( absfilename ) == False:
        raise Exception( "swMap - [%s] is not a SwMap" % absfilename )

      self._absfilename = absfilename
      self._isValid = True

    except Exception, e:
      print e

  def dump( self ):
    print "MAP: [ %s ]" % self._absfilename
    for o in self.getSectionObjs():
      pprint( o )

  def isValid( self ):
    return self._isValid

  def getDir( self ):
    return os.path.dirname(  self._absfilename )

  def getAbsFileName( self ):
    return self._absfilename

  def getAllSubmod( self ):
    cmd_get_submod = "cd %s && git config -l | grep \"submodule.*.url=\"" % self.getDir()
    out,errCode = myCommand_fast( cmd_get_submod )
    submods = []
    for s in out.splitlines():
      submods.append( s[ s.find( "." ) +1 : s.find( ".url=" ) ] )
    return submods

  def getSubmod( self, sm ):
    objs = self.getSectionObjs()
    for o in objs:
      if o[MAP_NAME] == sm:
        return o
    return Null

  #
  # Read file / allocate objects methods
  ######################################
#  @staticmethod
#  def get_section_obj(  ):

  def getWrittenSectionObjs( self ):
    return self.getSectionObjs()

  def getSectionObjs( self ):
    if self._absfilename == "":
      return []
    if self._sectionObjs_written != None:
      return self._sectionObjs_written

    # only first time
    objs = []
    submods = self.getAllSubmod()

    for sm in submods:

      currobj = {}
      currobj[MAP_NAME] = sm
      currobj[MAP_LOCALPATH] = sm
      currobj[MAP_ABS_LOCALPATH] = os.path.abspath( self.getDir() + "/" + currobj[MAP_LOCALPATH] )

      url, errCode = get_repo_cfg( GITCFG_URL_ORIGIN, dir = currobj[MAP_ABS_LOCALPATH] )
      if errCode != 0:
        currobj[MAP_URL] = "origin"
      else:
        currobj[MAP_URL] = url[:-1]

      errCode, sha = getSHAFromRef( "HEAD", root = currobj[MAP_ABS_LOCALPATH] )
      currobj[MAP_CHK] = sha

      cmd_actIntBr = "grep -e \"^%s:\" %s/%s" % ( currobj[MAP_LOCALPATH], self.getDir(), SWFILE_DEFBR )
      out,errCode = myCommand_fast( cmd_actIntBr )
      if errCode != 0:
        currobj[MAP_DEF_BRANCH] = "@#@# ENTRY NOT FOUND INTO PROJ @#@#"
      else:
        currobj[MAP_DEF_BRANCH] = out[:-1].split( ":" )[1]

      cmd_intBr = "cd %s && git config --get %s" % ( currobj[MAP_ABS_LOCALPATH], SWCFG_INTBR )
      out,errCode = myCommand_fast( cmd_intBr )
      if errCode != 0:
        currobj[MAP_ACT_BRANCH] = "@#@# INT BR NOT SET @#@#"
      else:
        currobj[MAP_ACT_BRANCH] = out[:-1]

      cmd_currbranch = "cd %s && git symbolic-ref -q HEAD | cut -d '/' -f 3-" % currobj[MAP_ABS_LOCALPATH]
      currb,errCode = myCommand_fast( cmd_currbranch )
      if currb[:-1] == "":
        currobj[MAP_CURR_BRANCH] = "DETACHED-HEAD"
      else:
        currobj[MAP_CURR_BRANCH] = currb[:-1] 

      objs.append( currobj )

    #print objs
    self._sectionObjs_written = objs
    return self._sectionObjs_written

  def getSectionObjs_NOCHK( self ):
    objs = self.getSectionObjs()

    retobjs = []
    for o in objs:
      if o[MAP_CURR_BRANCH].find("/CHK/") == -1:
        retobjs.append( o )

    return retobjs


  def getSectionObjs_ONLYCHK( self ):
    objs = self.getSectionObjs()

    retobjs = []
    for o in objs:
      if o[MAP_CURR_BRANCH].find("/CHK/") != -1:
        retobjs.append( o )

    return retobjs

class SwMap_Null( SwMap ):
  def __init__( self ):
    self._absfilename = ""
    self._sectionObjs_written = []
    self._sectionObjs_actual = []
    self._debug = False
    self._isValid = False



def main():
  aMap = SwMap( sys.argv[1] )
  if aMap.isValid():
    aMap.dump()
  else:
    print ""
    print "sys.argv[1] HAS no a map"
    print ""
    upperMap = create_swmap( debug = True)
    upperMap.dump()

  def dump( self ):
    print "MAP: [ NULL MAP ]"


if __name__ == "__main__":
  main()
