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

from MyCmd import *
from ObjLog import *
from ObjLock import *
from ObjOperation import *
from ObjBranch import *
from ObjTag import *

import Utils_Submod


def regenInput( options ):
  #output_opt = getOutputOpt(options)
  input = ""
  for arg in sys.argv:
    if arg.find(" ") != -1:
      input = input + " \"" + arg + "\" "
      continue
    if arg in ["--all"]:
      continue
    input = input + " " + arg   

  input=input.replace("*", "\*")
  return input 


def All( options, noCHK=True, lockType="", bottomup = False, exportVar = "" ):
  #
  # input
  input = regenInput( options )
  GLog.f( GLog.I, "Apply '%s' into all contained repositories" % input )

  #
  # GET PROJECTS
  projetcs = get_all_sections( noCHK = noCHK, alsoRootDir = True )

  if bottomup == True:
    projetcs.reverse()
  
  #
  # CHECK
  GLog.s( GLog.S, "CHECK ALL" )

  err    = 0
  reason = ""
  for proj in projetcs:
    cmd = "cd %s && %s SWCHECK=\"ONLY\" SWINDENT=%d %s"  % \
           ( proj[MAP_ABS_LOCALPATH], exportVar, GLog.tab + proj[MAP_DEPTH] + 1, input )
    errCode = os.system( cmd )
    if errCode != 0 :
      err = 1
      reason = reason + " " + proj[MAP_ABS_LOCALPATH]
      continue
  
  if err != 0:
    GLog.logRet( 1, reason = reason )
    return 1
  GLog.logRet( 0 )

  
  #
  # LOCK
  guards = [] #keep scope of guards outside the 'for' scope
  if lockType != "":

    for proj in projetcs:

      path = proj[MAP_ABS_LOCALPATH]

      objRem = create_remote( path )
      if not objRem.isValid():
        GLog.f( GLog.E, str(objRem) )
        sys.exit(1)

      lock = createLockStartegy( objRem.getUrl() )

      guard = Guard( lock ) # When out of scope it automatically releases lock
      guards.append( guard )
      errCode, errstr = guard.acquire( lockType )
      if errCode != 0:
        GLog.f( GLog.E, "%s is temporary locked. Please retry later." % (url) )
        return 1 

  
  #
  # EXEC
  GLog.s( GLog.S, "EXECUTE ALL" )

  err = 0
  reason = ""
  for proj in projetcs:
    cmd = "cd %s && %s SWCHECK=\"NO\" SWINDENT=%d %s"  % \
           ( proj[MAP_ABS_LOCALPATH], exportVar, GLog.tab + proj[MAP_DEPTH] + 1, input )
    errCode = os.system( cmd )
    if errCode != 0 :
      err = 1
      reason = reason + " " + proj[MAP_ABS_LOCALPATH]
      continue
  
  if err != 0:
    GLog.logRet( 1, reason = reason )
    return 1
  GLog.logRet( 0 )
  return 0


