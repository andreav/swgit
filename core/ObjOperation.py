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

from ObjProj import *
from ObjSnapshotRepo import *
#import Utils_Submod
from ObjStatus import *

#
# Utils
#
def get_all_sections( adir = ".", noCHK = False, depth = -1, alsoRootDir = False, debug = False ):

  proj = create_swproj( adir, debug )

  if noCHK == True:
    getproj_op = SwOp_GetAll_SectObjs_NOCHK( maxdepth = depth )
  else:
    getproj_op = SwOp_GetAll_SectObjs( maxdepth = depth, debug = debug )

  proj.accept( getproj_op )

  projects = getproj_op.get_sect_objs()

  if alsoRootDir == True:
    rootDummySection = {}
    rootDummySection[MAP_LOCALPATH] = "."
    rootDummySection[MAP_ABS_LOCALPATH] = os.path.abspath( Env.getProjectRoot( adir ) )
    rootDummySection[MAP_NAME] = "ROOT REPO"
    rootDummySection[MAP_DEPTH] = -1

    projects.insert( 0, rootDummySection )

  return projects


#
# Visitor pattern
#

######################################
# SwOperation - base class
######################################
class SwOperation( object ):
  def __init__( self, name, maxdepth = -1, debug = False ):
    self._name  = name
    self.debug_ = debug
    self._maxdepth = int(maxdepth)
    self._depth = 0
    self._abort = False

  def abort( self ):
    self._abort = True

  def dump( self ):
    return "(SwOp %s)" % self._name

  def log( self, any ):
    if self.debug_ == True:
      print "SwOperation - %s" % ( any )
    return

  def down( self, swComp ):
    self._depth += 1

  def up( self, swComp ):
    self._depth -= 1

  def descend( self ):
    #self.log( "<< descend max: [%s] curr: [%s] >>" % ( self._maxdepth, self._depth ) )
    if self._maxdepth == -1:
      #self.log( "GO-ON DESCEND (-1)" )
      return True

    if self._depth < self._maxdepth:
      #self.log( "GO-ON DESCEND" )
      return True

    self.log( "STOP DESCEND" )
    return False

  def visit( self, SwComponent ):
    if self._abort:
      return
    self.visit_int( SwComponent )



######################################
# SwOp_DumpProj
######################################
class SwOp_Dump( SwOperation ):
  def __init__( self, maxdepth = -1, debug = False ):
    super( SwOp_Dump, self ).__init__( "Dump", maxdepth = maxdepth, debug = debug )
    self.indent_ = 0

  def visit_int( self, swComp ):
    pprint( swComp.__dict__ )
    if swComp.isProj():
      pprint( swComp.getMapObj() )
    str_father_root = "  (Father: "
    if swComp.getFatherDir() != "":
      str_father_root += swComp.getFatherDir() + ")"
    else:
      str_father_root += "None)"

    str_children = "  (Children: "
    for c in swComp.getChildren():
      str_children += "<" + c.getRootDir() + "> "
    if len( swComp.getChildren() ) == 0:
      str_children += "None"
    str_children += " )"

    str_map = "  (Map:"
    if swComp.isProj():
      for o in swComp.getMapObj().getSectionObjs():
        #pprint( o )
        str_map += "  " + o[MAP_NAME]
    else:
      str_map += "None"
    str_map += ")"

    str_addinfo = str_father_root + str_children + str_map

    if swComp.isProj():
      print "\t" * self.indent_ + "PROJ: " + swComp.getRootDir() + str_addinfo
      self.indent_ += 1
    elif swComp.isRepo():
      print "\t" * self.indent_ + "REPO: " + swComp.getRootDir() + str_addinfo
    else:
      pass
      #print swComp.start_dir_


######################################
# SwOp_DumpProj
######################################
class SwOp_DumpProj( SwOperation ):
  def __init__( self, listall = False, maxdepth = -1, debug = False ):
    super( SwOp_DumpProj, self ).__init__( "DumpProj", maxdepth = maxdepth, debug = debug )
    self._depth_map = {}
    self._listall    = listall

  #
  # This maps project to infos:
  # projname <--> indent
  #               already dumped
  #               (children number)
  MAXCHL         = "CHILDREN_NUM"
  ALREADYDUMPED  = "ALREADYDUMPED"
  UNINIT_LIST    = "UNINIT_LIST"
  SNAPSH_LIST    = "SNAPSH_LIST"

  indent_empty_nopipe = "         "
  indent_empty_pipe   = "    |    "
  indent_dash         = "    |----"
  indent_dash_last    = "    '----"
  indent_majr         = "    |>>>>"

  def get_prefixes( self ):
    mydepth = self._depth

    #previous elems
    prefixindent = ""
    for i in range( 0, mydepth - 1 ):
      #print "ROUND: ", i
      if self._depth_map[i][self.ALREADYDUMPED] < self._depth_map[i][self.MAXCHL]:
        prefixindent += self.indent_empty_pipe
      else:
        prefixindent += self.indent_empty_nopipe

    #last elem for this row
    last_title_prefix = ""
    last_body_prefix = ""
    if self._depth_map[mydepth-1][self.ALREADYDUMPED] == ( self._depth_map[mydepth-1][self.MAXCHL] - 1 ):
      last_title_prefix = self.indent_dash_last
      last_body_prefix = self.indent_empty_nopipe
    else:
      last_title_prefix = self.indent_dash
      last_body_prefix = self.indent_empty_pipe

    return prefixindent, last_title_prefix, last_body_prefix


  def up( self, swComp ):

    if swComp.isProj():

      #before exiting from proj, dump uninited and snapshot
      mydepth = self._depth

      #print "\nUP\n"
      #pprint( swComp.__dict__ )
      #print "\nDEPTH\n"
      #print self._depth
      #print "\nMAP\n"
      #pprint( self._depth_map[mydepth-1] )


      for s in self._depth_map[ mydepth - 1 ][self.SNAPSH_LIST]:
        prefixindent, last_title_prefix, last_body_prefix = self.get_prefixes()

        ret =  prefixindent + self.indent_empty_pipe + "\n"
        ret += prefixindent + last_title_prefix + "[" + s + "]  (\"snapshot repo\")"

        origin = ""
        o = ObjSnapshotRepo( s )
        if o.isValid():
          origin = o.get_url()

        version = ""
        currver_file = "%s/%s/%s" % (swComp.getRootDir(), s, SWFILE_SNAPCFG_CURRVER)
        if os.path.exists( currver_file  ) == True:
          cmd_get_curr_sha = "cat %s" % currver_file
          out, errCode = myCommand_fast( cmd_get_curr_sha )
          if errCode == 0:
            version = out[:-1]

        ret += "\n%s%s  Origin         : %s" % ( prefixindent, last_body_prefix, origin )
        ret += "\n%s%s  Curr ver pulled: %s" % ( prefixindent, last_body_prefix, version )

        self._depth_map[mydepth-1][self.ALREADYDUMPED] += 1
        print ret


      for i in self._depth_map[ mydepth - 1 ][self.UNINIT_LIST]:
        prefixindent, last_title_prefix, last_body_prefix = self.get_prefixes()

        ret =  prefixindent + self.indent_empty_pipe + "\n"
        ret += prefixindent + last_title_prefix + "[" + i + "]  \"not initialized\""

        self._depth_map[mydepth-1][self.ALREADYDUMPED] += 1
        print ret

    super( SwOp_DumpProj, self ).up( swComp )


  def down( self, swComp ):
    super( SwOp_DumpProj, self ).down( swComp )



  # depth: 0  1  2
  #
  #        P
  #        |--R
  #        |--P
  #        |  |--R
  #        |  '--R
  #        '--R

  def visit_int( self, swComp ):

    #pprint( self.__dict__ )
    mydepth = self._depth

    if swComp.isProj():
      #self.log( "New Layer %s" % ( mydepth ) )

      snapsh_list = []
      snapsh_list = Utils_Submod.submod_list_snapshot( swComp.getRootDir() )

      uninit_list = []
      if self._listall  == True:
        uninit_list = Utils_Submod.submod_list_notinitialized_notsnapshot( swComp.getRootDir() )

      total_len = len( swComp.getChildren() ) + len( uninit_list ) + len( snapsh_list )

      self._depth_map[ mydepth ] = { self.MAXCHL        : total_len,  \
                                     self.ALREADYDUMPED : 0,
                                     self.UNINIT_LIST : uninit_list,
                                     self.SNAPSH_LIST : snapsh_list,
                                   }


    if mydepth == 0:

      #self.log( "Root Repo %s" % ( swComp.getRootDir() ) )
      ret = "\n" + swComp.getRootDir()

      ret += "\n  Local Path     : ."

      # show remote only on root, because:
      #  if you issue a proj --init, this remote decides behaviour
      #  children remotes do not matter here because:
      #    now they are configured and only that url matters
      #    when they were configured (at clone/init time) only their father remote did matter
      remotes = Remote.get_remote_list()
      if len( remotes ) == 0:
        #pass
        ret += "\n  Origin         : " + "origin"
      else:
        remote_name = Utils.eval_default_remote_name()
        #projRemote = create_remote_byname( remote_name )
        cmd_url = "cd %s && git config --get remote.%s.url" % (swComp.getRootDir(),remote_name)
        out, errCode = myCommand_fast( cmd_url )
        if errCode != 0:
          #pass
          ret += "\n  Curr remote    : " + "origin"
        else:
          ret += "\n  Curr remote    : " + "(%s) %s" % (remote_name, out[:-1])


      cmd_intbr = "cd %s && git config --get %s" % ( swComp.getRootDir(), SWCFG_INTBR )
      out, errCode = myCommand_fast( cmd_intbr )
      if errCode != 0:
        ret += "\n  Int Branch     : " + "@#@# INT BR NOT SET @#@#"
      else:
        ret += "\n  Int Branch     : " + out[:-1]

      errCode, currsha =  getSHAFromRef( "HEAD" )
      ret += "\n  Checkout       : " + currsha

      cmd_currbranch = "cd %s && git symbolic-ref -q HEAD | cut -d '/' -f 3-" % swComp.getRootDir()
      currb,errCode = myCommand_fast( cmd_currbranch )
      if currb[:-1] == "":
        ret += "\n  CurrBr         : " + "DETACHED-HEAD"
      else:
        ret += "\n  CurrBr         : " + currb[:-1]

      print ret

    else:

      self.log( "Repo [%s]" % ( swComp.getRootDir() ) )

      mysect = swComp.getMySectionObj()

      self.log( "MyDepth: %s" % ( mydepth ) )
      self.log( "_depth_map: %s" % ( self._depth_map ) )
      self.log( "mysect: %s" % ( mysect ) )

      #previous elems
      prefixindent, last_title_prefix, last_body_prefix = self.get_prefixes()

      ret =  prefixindent + self.indent_empty_pipe + "\n"
      ret += prefixindent + last_title_prefix + "[" + mysect[MAP_NAME] + "]"
      ret += "\n%s%s  Local Path     : %s" % ( prefixindent, last_body_prefix, mysect[MAP_LOCALPATH] )
      ret += "\n%s%s  Origin         : %s" % ( prefixindent, last_body_prefix, mysect[MAP_URL] )
      ret += "\n%s%s  Def int Branch : %s" % ( prefixindent, last_body_prefix, mysect[MAP_DEF_BRANCH] )
      ret += "\n%s%s  Act int Branch : %s" % ( prefixindent, last_body_prefix, mysect[MAP_ACT_BRANCH] )

      if mysect[MAP_CHK] != None:
        ret += "\n%s%s  Checkout       : %s" % ( prefixindent, last_body_prefix, mysect[MAP_CHK] )

      ret += "\n%s%s  CurrBr         : %s"   % ( prefixindent, last_body_prefix, mysect[MAP_CURR_BRANCH] )

      self._depth_map[mydepth-1][self.ALREADYDUMPED] += 1

      print ret



######################################
# SwOp_GetAll_SectObjs_Base
######################################
class SwOp_GetAll_SectObjs_Base( SwOperation ):
  def __init__( self, name, maxdepth = -1, debug = False ):
    super( SwOp_GetAll_SectObjs_Base, self ).__init__( name, maxdepth = maxdepth, debug = debug )

    self._sect_objs = []

  def get_sect_objs( self ):
    return self._sect_objs

  def visit_int( self, swComp ):
    pass


######################################
# SwOp_GetAll_SectObjs
######################################
class SwOp_GetAll_SectObjs( SwOp_GetAll_SectObjs_Base ):
  def __init__( self, maxdepth = -1, debug = False ):
    super( SwOp_GetAll_SectObjs, self ).__init__( "GetAll_SectObjs", maxdepth = maxdepth, debug = debug )

  def visit_int( self, swComp ):

    #self.log( "depth %s" % ( self._depth ) )
    if self._depth == 0:
      self.log( "Add also zero-level section" )


    if swComp.isProj():
      self.log( "proj %s" % ( swComp.getRootDir() ) )

      currLevelSections = swComp.getMapObj().getSectionObjs()
      for s in currLevelSections:
        s[MAP_DEPTH] = self._depth

      self._sect_objs.extend( currLevelSections )

    else:
      self.log( "repo %s, noop" % ( swComp.getRootDir() ) )


######################################
# SwOp_GetAll_SectObjs_NOCHK
######################################
class SwOp_GetAll_SectObjs_NOCHK( SwOp_GetAll_SectObjs_Base ):
  def __init__( self, maxdepth = -1, debug = False ):
    super( SwOp_GetAll_SectObjs_NOCHK, self ).__init__( "GetAll_SectObjs_NOCHK", maxdepth = maxdepth, debug = debug )

  def visit_int( self, swComp ):

    if swComp.isProj():
      self.log( "proj %s" % ( swComp.getRootDir() ) )

      currLevelSections = swComp.getMapObj().getSectionObjs_NOCHK()
      for s in currLevelSections:
        s[MAP_DEPTH] = self._depth

      self._sect_objs.extend( currLevelSections )

    else:
      self.log( "repo %s, noop" % ( swComp.getRootDir() ) )

######################################
# SwOp_GetAll_SectObjs_ONLYCHK
######################################
class SwOp_GetAll_SectObjs_ONLYCHK( SwOp_GetAll_SectObjs_Base ):
  def __init__( self, maxdepth = -1, debug = False ):
    super( SwOp_GetAll_SectObjs_ONLYCHK, self ).__init__( "GetAll_SectObjs_ONLYCHK", maxdepth = maxdepth, debug = debug )

  def visit_int( self, swComp ):

    if swComp.isProj():
      self.log( "proj %s" % ( swComp.getRootDir() ) )

      currLevelSections = swComp.getMapObj().getSectionObjs_ONLYCHK()
      for s in currLevelSections:
        s[MAP_DEPTH] = self._depth

      self._sect_objs.extend( currLevelSections )

    else:
      self.log( "repo %s, noop" % ( swComp.getRootDir() ) )



######################################
# SwOp_System_All
######################################
class SwOp_System_All( SwOperation ):
  def __init__( self, cmd, maxdepth = -1, debug = False ):
    super( SwOp_System_All, self ).__init__( "os.system( %s )" % cmd, maxdepth = maxdepth, debug = debug )
    self.cmd_ = cmd

  def visit_int( self, swComp ):

    self.log( "Executing system (%s) over repo: [%s]" % ( self.cmd_, swComp.getRootDir() ) )
    errCode = os.system( "cd %s; %s" % ( swComp.getRootDir(), self.cmd_ ) )
    if errCode != 0:
      return errCode, swComp

    return 0


######################################
# SwOp_ProjConfSpec
######################################
class SwOp_ProjConfSpec( SwOperation ):
  def __init__( self, ref, maxdepth = -1, debug = False ):
    super( SwOp_ProjConfSpec, self ).__init__( "ProjConfSpec", maxdepth = maxdepth, debug = debug )
    self.res_list_  = []
    self.base_dir_  = ""
    self.start_ref_ = ref
    self.ref_map_   = {}
    self.curr_init_ = []

  def getRetList( self ):
    return self.res_list_
  def getFormattedOutput( self ):
    paths = [ l.split(":")[0] for l in self.res_list_ ]
    #only on python > 2.5
    #maxlen = len( max( paths, key = len ) )
    maxlen = max( len(x) for x in paths )
    retval = []
    for r in self.res_list_:
      (path, ver) = r.split(':')
      retval.append( "%s : %s" % (path.ljust(maxlen), ver.strip()) )
    return retval

  def visit_int( self, swComp ):

    if self._depth == 0:
      self.base_dir_ = swComp.getRootDir()
      self.ref_map_[ swComp.getRootDir() ] = self.start_ref_

      prootref = "HEAD"
      if self.start_ref_ != None:
        prootref = self.start_ref_
      errCode, currsha =  getSHAFromRef( prootref )
      self.res_list_.append( "./ : %s" % ( currsha ) )

    father = swComp.getFatherDir()
    if father in self.ref_map_.keys(): #already processed father proj 

      rn = os.path.relpath( swComp.getRootDir(), father )
      repover, errCode = Utils_Submod.submod_getrepover_atref( father, rn, self.ref_map_[father] )
      if errCode != 0:
        self.res_list_.append( "%s : ERROR - %s" % (swComp.getRootDir(), repover) )
        return

      if swComp.isProj(): #set repover for children
        #if user specified at top None (current subrepo position)
        # must propagate it beneath
        pref = repover
        if self.start_ref_ == None:
          pref = None

        self.ref_map_[ swComp.getRootDir() ] = pref

      relpath2root = os.path.relpath( swComp.getRootDir(), self.base_dir_ )
      aline = "%s : %s" % (relpath2root, repover )

      labels = ( SWCFG_TAG_LIV, SWCFG_TAG_STB, SWCFG_TAG_NGT, SWCFG_TAG_FIX, SWCFG_TAG_DEV, SWCFG_TAG_RDY )

      for t in labels:
        cmd_describe_commit = "cd %s && git describe --tags --long --exact-match %s --match '*/*/*/*/*/*/*/%s/*'" % ( swComp.getRootDir(), repover, t )
        lbl, errCode = myCommand_fast( cmd_describe_commit )
        if errCode == 0:
          #lbl: label-0-g2bab7e0
          aline += " # %s" % lbl[:-1].split('-')[0]
          break

      self.res_list_.append( aline )

    return


######################################
# SwOp_ProjDiff
######################################
class SwOp_ProjDiff( SwOperation ):
  def __init__( self, pref1, pref2, smod_list, diff_args, maxdepth = -1, debug = False ):
    super( SwOp_ProjDiff, self ).__init__( "ProjDiff", maxdepth = maxdepth, debug = debug )
    self.base_dir_       = ""
    self.start_pref1_    = pref1
    self.start_pref2_    = pref2
    self.smod_list_      = smod_list
    self.str_diff_args_  = " ".join( diff_args )
    self.ref1_map_       = {}
    self.ref2_map_       = {}
    self.resout_         = ""

  def getResult( self ):
    return self.resout_

  def valid_ref( self, ref, swComp ):

    errCode, sha = getSHAFromRef( ref, swComp.getRootDir() )
    if errCode != 0:
      relpath2root = os.path.relpath( swComp.getRootDir(), self.base_dir_ )
      strerr  = "Reference %s not existing into repository %s.\n" % ( ref, relpath2root )
      strerr += "In order to download some new commit, you could issue:\n"
      strerr += "  cd %s && swgit submodule update\n" % ( swComp.getFatherDir() )
      strerr += "  or\n"
      strerr += "  cd %s && swgit proj --update" % ( swComp.getFatherDir() )
      strerr += "  or\n"
      strerr += "  cd %s && swgit pull" % ( swComp.getFatherDir() )
      return 1, strerr

    return 0, sha


  def visit_int( self, swComp ):

    self.log( "visit: %s" % swComp.getRootDir() )

    if self._depth == 0:
      self.base_dir_ = swComp.getRootDir()
      self.ref1_map_[ swComp.getRootDir() ] = self.start_pref1_
      self.ref2_map_[ swComp.getRootDir() ] = self.start_pref2_
      pref1 = self.start_pref1_
      pref2 = self.start_pref2_

    relpath2root = os.path.relpath( swComp.getRootDir(), self.base_dir_ )
    self.log( relpath2root )
    #under first level, enter everiwhere
    print self.smod_list_
    if self._depth == 0:
      if len( self.smod_list_ ) > 0 and relpath2root not in self.smod_list_:
        return

    str_tit1 = "REF1:    "
    str_tit2 = "REF2:    "
    str_cmd  = "CMD:     git diff $REF1 $REF2 %s" % self.str_diff_args_

    #
    # eval project references
    #
    #print swComp.getRootDir()

    father = swComp.getFatherDir()
    if father in self.ref1_map_.keys(): #already processed father proj 
      pref1 = self.ref1_map_[father]
      pref2 = self.ref2_map_[father]

    if Status.pendingMerge( swComp.getRootDir() ):
      self.resout_ += "Conflict is present, ignoring <ref1> and/or <ref2> arguments and showing merge differences."
      pref1    = "HEAD"
      pref2    = "MERGE_HEAD"
      str_tit1 = "HEAD:       "
      str_tit2 = "MERGE_HEAD: "
      str_cmd  = "CMD:        git diff HEAD MERGE_HEAD %s" % self.str_diff_args_

    #
    # eval diff references
    #
    if self._depth == 0:

      diffref1 = pref1
      diffref2 = pref2

    else:

      relpath2father = os.path.relpath( swComp.getRootDir(), father )

      #print father
      #print relpath2father
      #print pref1
      #print pref2
      diffref1, errCode = submod_getrepover_atref( father, relpath2father, pref1 )
      if errCode != 0:
        self.resout_ += indentOutput( diffref1, self._depth ) + "\n"
        self.abort()
        return

      diffref2 = "" #i.e. swgit proj -D HEAD
      if pref2 != "":
        diffref2, errCode = submod_getrepover_atref( father, relpath2father, pref2 )
        if errCode != 0:
          self.resout_ += indentOutput( diffref2, self._depth ) + "\n"
          self.abort()
          return

    #i.e. after pulling proj but not subrepos
    for dref in (diffref1, diffref2):
      if dref != "":
        errCode, sha = self.valid_ref( dref, swComp )
        if errCode != 0:
          self.resout_ += indentOutput( diffref2, self._depth ) + "\n"
          self.abort()
          return

    if swComp.isProj():
      self.ref1_map_[ swComp.getRootDir() ] = diffref1
      self.ref2_map_[ swComp.getRootDir() ] = diffref2


    #
    # Prepare title section
    #
    if swComp.isProj():
      if self._depth == 0:
        row0  = "proj:    %s" % self.base_dir_
      else:
        row0  = "proj:    %s" % relpath2root
    else:
      row0  = "repo:    %s" % relpath2root

    row1 = str_tit1 + diffref1
    row2 = str_tit2 + diffref2
    if diffref2 == "":
      row2 = str_tit2 + "working dir"
    #only on python > 2.5
    #maxlen = len( max( row0, row1, row2, str_cmd, key=len ) )
    maxlen = max( len(x) for x in [row0, row1, row2, str_cmd] )
    bound = "="*maxlen
    strout = "\n%s" % "\n".join( (bound,row0, row1, row2, str_cmd, bound) )

    self.resout_ += indentOutput( strout, self._depth )
    self.resout_ += "\n\n"

    cmd_proj_diff = "cd %s && git diff %s %s %s" % ( swComp.getRootDir(), diffref1, diffref2, self.str_diff_args_ )
    out, errCode = myCommand( cmd_proj_diff )

    self.resout_ += indentOutput( out, self._depth )
    self.resout_ += "\n"

    return


test_opmap = (
    SwOp_Dump,
    SwOp_System_All,
    SwOp_DumpProj,
    SwOp_GetAll_SectObjs,
    SwOp_GetAll_SectObjs_NOCHK,
    SwOp_GetAll_SectObjs_ONLYCHK,
    SwOp_ProjConfSpec,
    SwOp_ProjDiff
    )


def usage():
  print "\nObjOperation [aDir] [aNumOp] [optional op args]\n"
  for idx, val in enumerate(test_opmap):
    print '[%s] %s' % (idx, val)
  sys.exit( 1 )


def main():
  if len( sys.argv ) == 1:
    usage()

  if len( sys.argv ) < 3:
    print "wrong arguments number"
    usage()

  startp = sys.argv[1]
  opnum = int( sys.argv[2] )
  depth = -1
  opargs = ""

  if opnum != 1 and opnum != 6:

    if len( sys.argv ) == 4:
      depth = sys.argv[3]
    elif len( sys.argv ) > 4:
      print "wrong arguments number"
      usage()

  else: # need arg param too

    if len( sys.argv ) == 4:
      opargs = sys.argv[3]
    elif len( sys.argv ) == 5:
      depth = sys.argv[4]
    else:
      print "wrong arguments number"
      usage()


  stroptargs = ""
  if opargs != "":
    stroptargs = "\n\twith arg: %s " % opargs

  #proj = create_swproj( startp )
  proj = create_swproj( startp, debug = True )
  if opargs == 1:
    op = test_opmap[opnum]( opargs, maxdepth = depth, debug = True )
  elif opnum == 6:
    op = test_opmap[opnum]( opargs, maxdepth = depth, debug = True )
  else:
    op = test_opmap[opnum]( maxdepth = depth, debug = True )

  print "%s\nTesting ObjOperation [%s]\n\tstartpoint: %s%s\n\tdepth: %s\n%s" % \
      ( "="*40, op.dump(), startp, stroptargs, depth, "="*40 )


  proj.accept( op )

  if isinstance( op, SwOp_GetAll_SectObjs ) or \
      isinstance( op, SwOp_GetAll_SectObjs_NOCHK ) or \
      isinstance( op, SwOp_GetAll_SectObjs_ONLYCHK ):
    pprint( op.get_sect_objs() )

  if isinstance( op, SwOp_ProjConfSpec ):
    print "\n".join( op.getFormattedOutput() )

  #projetcs = get_all_sections( alsoRootDir = True, debug = True )
  #pprint( projetcs )


if __name__ == "__main__":
  main()
