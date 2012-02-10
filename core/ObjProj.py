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

from Common import *
from ObjMap import *
import traceback

g_swobjects = {}

#
# factory methods
#

def create_swproj( startdir = ".", debug = False ):
  #print str( debug )
  #print startdir
  if debug == True:
    SwUtils._debug = True

  proot = Env.getProjectRoot( startdir )
  if proot == "":
    return None
  retobj = SwProj( proot )

  #SwUtils._debug = False
  return retobj

def create_swrepo( startdir = ".", debug = False ):
  if debug == True:
    SwUtils._debug = True

  rroot = Env.getLocalRoot( startdir )
  retobj = SwRepo( rroot )

  #SwUtils._debug = False
  return retobj




#
# Composite pattern
#

SWTAB = "\t"

class SwUtils:
  _debug = False
  #_debug = True

  @staticmethod
  def log( any ):
    if SwUtils._debug == True:
      print any
    return



######################
#
# SwRepo
#
######################
class SwRepo( object ):

  def __init__( self, rootdir, name = ""  ):

    SwUtils.log( "START - SwRepo::SwRepo( %s )" % rootdir )

    self._name = ""
    self._rootdir = ""
    self._fatherdir = "";
    self._my_section = None;
    self._isValid = False;

    try:

      if name == "":
        self._name = "SwRepo"
      else:
        self._name = name

      if os.path.exists( rootdir + "/.git" ) == False:
        raise Exception( "ROOT DIR [%s] is not a GIT REPO" % rootdir )
      self._rootdir = os.path.abspath( rootdir )

      if self._fatherdir == "":
        fdir = Env.getLocalRoot( self._rootdir + "/../", fexit = False )
        if fdir != "" and Env.is_aproj( fdir ) == True:
          self._fatherdir = fdir

    except Exception, e:
      SwUtils.log( e )
    else:
      self._isValid = True
      g_swobjects[ self._rootdir ] = self

    SwUtils.log( "END - SwRepo::SwRepo( %s )" % rootdir )


  def isRepo( self ):
    return self._name == "SwRepo"
  def isProj( self ):
    return self._name == "SwProj"

  def isValid( self ):
    return self._isValid
  def getRootDir( self ):
    return self._rootdir
  def getFatherDir( self ):
    return self._fatherdir

  def getFatherObj( self ):
    if self.getFatherDir() == "":
      SwUtils.log( "getFatherObj for (%s), father not existsing. " + self.getRootDir() )
      return None

    if self.getFatherDir() in g_swobjects:
      SwUtils.log( "getFatherObj for (%s), father already created, re-user it. " % self.getRootDir() )
      return g_swobjects[ self.getFatherDir() ]

    SwUtils.log( "getFatherObj for (%s), create it" % self.getRootDir() )
    newobj = SwProj( self.getFatherDir() )
    if newobj.isValid():
      return newobj
    return None


  def getChildren( self ):
    return []

  def dump( self, num_indent = 0 ):
    SwUtils.log( "SwRepo::dump %s - %s" % (num_indent,self.getRootDir()) )
    ret_str = "\n" + SWTAB * num_indent + "REPO - [%s]" % ( self.getRootDir() )
    return ret_str

  def accept( self, op ):
    SwUtils.log( "  SwRepo::accept %s on %s " % (op.dump(),self.getRootDir()) )
    return op.visit( self )

  def getMySectionObj( self ):
    SwUtils.log( "getMySectionObj - " + self.getRootDir() )

    # check father existence
    fobj = self.getFatherObj()
    if fobj == None:
      SwUtils.log( "getMySectionObj - On top of project, no section available" )
      return None

    # check already evaluated field
    if self._my_section != None: #eval once
      return self._my_section

    for o in fobj.getMapObj().getSectionObjs():
      path_in_map = o[MAP_ABS_LOCALPATH]
      my_path = os.path.abspath( self.getRootDir() )
      #print path_in_map
      #print my_path
      if path_in_map == my_path:
        self._my_section = o
        return o
    SwUtils.log( "NOT found my repo (%s) inside father map??" % self.getRootDir() )
    return None



######################
#
# SwProj
#
######################
class SwProj( SwRepo ):
  def __init__( self, rdir ):

    SwUtils.log( "START - SwProj::SwProj( %s )" % rdir )

    self._mapObj = None
    self._children = None #se e' none => devi ancora valutarli

    try:
      if os.path.exists( rdir + "/" + SWFILE_PROJMAP ) == False:
        traceback.print_stack()
        raise Exception( "ROOT DIR [%s] is not a SWPROJ REPO" % rdir )

      # INIT SwRepo
      super( SwProj, self ).__init__( name = "SwProj", rootdir = rdir )

      # INIT SwProj
      self._mapObj = SwMap( os.path.abspath( self._rootdir ) )

    except Exception, e:
      print e
      SwUtils.log( e )
      self._isValid = False

    SwUtils.log( "END - SwProj::SwProj( %s )" % rdir )

  def getChildren( self ):
    if self._children == None:
      self._eval_projects()
    return self._children

  def getMap_file( self ):
    return self._mapObj.getAbsFileName()
  def getMapObj( self ):
    return self._mapObj

  def dump( self, num_indent = 0 ):
    SwUtils.log( "SwProj::dump %s " % num_indent )
    ret_str = "\n" + SWTAB * num_indent + "PROJ - [%s]" % ( self.getRootDir() )
    for r in self.getChildren():
      ret_str += r.dump( num_indent + 1 )

    return ret_str

  def accept( self, op ):
    SwUtils.log( "  SwProj::accept %s on %s " % (op.dump(),self.getRootDir()) )

    op.visit( self )

    if op.descend() == False:
      SwUtils.log( "  SwProj::accept %s on %s - stop descending " % (op.dump(),self.getRootDir()) )
      return

    op.down( self )
    for r in self.getChildren():
      r.accept( op )
    op.up( self )

  #
  # Private methods
  # 
  def _eval_projects( self  ):
    SwUtils.log( "SwProj - %s - _eval_projects" % self.getRootDir() )

    self._children = []
    for r in self.getMapObj().getSectionObjs():

      aChild = None

      child_repo_dir = os.path.abspath( self.getRootDir() + "/" + r[MAP_LOCALPATH] )
      child_repo_map = os.path.abspath( child_repo_dir + "/" + SWFILE_PROJMAP )
      SwUtils.log( " check map: '%s'" % child_repo_map )
      if os.path.exists( child_repo_map ) == True:
        aChild = SwProj( child_repo_dir )
      else:
        aChild = SwRepo( child_repo_dir )

      self._children.append( aChild )

    return


  
def main():
  print "\nTesting ObjProj class with startpoint: %s" % sys.argv[1]

  print "%s\ncreate_swrepo\n%s" % ( "#"*20, "#"*20 )
  repo = create_swrepo( sys.argv[1] )
  print repo.dump()
  print ""

  print "%s\ncreate_swrepo\n%s" % ( "#"*20, "#"*20 )
  proj = create_swproj( sys.argv[1] )
  if proj != None:
    print proj.dump()
  else:
    print "None"
  print ""



if __name__ == "__main__":
  _debug = True
  main()
