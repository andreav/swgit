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

#from Utils import *
from MyCmd import *
from Common import *
from ObjEnv import *
from ObjRemote import *
from pprint import pprint
from Utils import *

def dir2reponame( dir ):
  ret = del_slash( dir )
  if ret.find( "./" ) == 0:
    ret = ret[2:]
  return ret

########################
# SRC PARAM MANAGEMENT #
########################

def src_reference_check_all_entries( src_str, batch = False ):

  projroot = Env.getProjectRoot()
  if projroot == "":
    return 1, "Not inside a Projects"

  not_listed_dirs = ""
  proj_abs_written = submod_list_repos( projroot, firstLev = True )

  for currentry in src_str.split( ',' ):
    dir, ref = currentry.split(':')

    #proj_abs_input = os.path.abspath( "%s/%s" % ( projroot, dir ) )
    proj_abs_input = os.path.abspath( "%s/%s" % ( os.getcwd(), dir ) )

    #print proj_abs_written
    #print proj_abs_input

    if proj_abs_input in proj_abs_written:
      proj_abs_written.remove( proj_abs_input )

  for d in proj_abs_written:
    #not_listed_dirs += "\t" + d.replace( projroot, "." ) + "\n"
    not_listed_dirs += "\t" + d.replace( os.getcwd(), "." ) + "\n"

  if not batch:
    if not_listed_dirs != "":
      ask = "Not all repositories are listed into src param. These will be skipped:\n" + \
          not_listed_dirs + \
          "Continue? [Y/n]"
      ans = raw_input( ask )
      if ans=="no" or ans=="n" or ans=="N" or ans == "NO" or ans == "No" or ans == "nO":
        GLog.s( GLog.S, "\taborted by user" )
        GLog.logRet(1)
        sys.exit(1)

  return 0, ""


def src_reference_check_strlist( src_str, batch = False ):

  regular_src_str = ",%s" % src_str #make all entries like this: <,PATH:REF>

  numcurrentry = 0
  for currentry in src_str.split( ',' ):
    numcurrentry += 1
    if currentry.count( ':' ) != 1:
      return 1, "%d (%s)" % ( numcurrentry, currentry )

    dir = currentry.split(':')[0]
    ref = currentry.split(':')[1]

    if os.path.exists( dir ) == False:
      return 1, "%d (%s) - invalid path." % ( numcurrentry, currentry )

    errCode, sha = getSHAFromRef( ref, dir )
    if errCode != 0:
      return 1, "%d (%s) - invalid reference." % ( numcurrentry, currentry )

    if regular_src_str.count( ",%s:" % dir ) != 1:
      return 1, "%d (%s) - listed more than once." % ( numcurrentry, currentry )

  # ask if some dir is forgotten
  src_reference_check_all_entries( src_str, batch ) #will exit if error

  return 0, src_str



def src_reference_check_parse_file( filename, batch = False ):

  retstr = ""
  srcfile = open( filename, "r" )
  lines = srcfile.read()
  lines = lines.splitlines()
  srcfile.close()
  numline = 0
  for origline in lines:
    numline += 1
    line = origline
    line = line.replace(' ', '')
    line = line.replace('\t', '')
    line = line.split('#')[0] #throw away comments
    if len( line ) == 0:
      continue

    if line.count( ':' ) != 1:
      return 1, "\tWrong formatted line %d (%s) into file %s" % ( numline, origline, filename )
    retstr += line + ','

  retstr = retstr[:-1]
  ret, errstr = src_reference_check_strlist( retstr, batch )
  if ret != 0:
    return 1, "\tWrong formatted file %s at entry: %s" % ( filename, errstr )

  return 0, retstr



# src reference can be:
# 1. any valid ref
# 2. a file of PATH:valid reference
# 2. a comma-separed list of PATH:valid reference
def src_reference_check( src, batch = False ):

  if os.path.exists( src ):
    return src_reference_check_parse_file( src, batch )

  if src.find( ":" ) != -1:
    ret, errstr = src_reference_check_strlist( src, batch )
    if ret != 0:
      return 1, "\tWrong formatted comma-separed list at position %s" % errstr
    return ret, errstr

  errCode, sha = getSHAFromRef( src )
  if errCode != 0:
    return 1, "\tPlease specify an existing file, a valid PATH:REFERENCE comma separed list or a single valid REFERENCE"

  return 0, src


#check only among initialized
def submod_check_hasrepo_initialized( reponame, dir = ".", firstLev = False, excludeRoot = False, localpaths = False ):

  reponame = del_slash( reponame )

  localrepos = submod_list_repos( dir, firstLev = True, excludeRoot = True, localpaths = True )
  if reponame not in localrepos:
    return "Repository '%s' inside project '%s' is not initialized. Cannot un-initialize it." % ( reponame, dir ), 1

  return "OK", 0

def submod_check_hasrepo_configured( reponame, dir = "." ):

  reponame = del_slash( reponame )

  localrepos = submod_list_all_default( dir )
  if reponame not in localrepos:
    return "ERROR: Not existing repository '%s' inside project %s" % ( reponame, dir ), 1

  return "OK", 0




#####################
# SUBMOD RETRIEVING #
#####################
#given proj and its ref => return version stored for rname at that reference
#pref = None => current position
def submod_getrepover_atref( proot, rname, pref ):
  rname = del_slash( rname )

  if pref != None:

    cmd_get_commit = "cd %s && git ls-tree %s %s | cut -f 1 | cut -d ' ' -f 3" % ( proot, pref, rname )

  else:

    cmd_get_commit = "cd %s && git submodule %s | cut -c 2- | cut -d ' ' -f 1" % ( proot, rname )

  #print cmd_get_commit
  c, e = myCommand( cmd_get_commit )
  #print c, e
  c = c[:-1]
  if c == "":
    return "Not found valid version for subrepo %s at project commit %s" % ( rname, pref ), 1
  return c, e


def submod_list_all_default( dir = "." ):
  proot = Env.getProjectRoot( dir )
  if proot == "":
    # not inside repo
    return []

  cmd_submod_list = "cd %s && git submodule  | cut -c 2-| cut -d ' ' -f 2" % proot
  out, errCode = myCommand_fast( cmd_submod_list )
  if errCode != 0:
    return []

  return out[:-1].splitlines()

def submod_list_snapshot( dir = "." ):
  ret_list = []
  inits = submod_list_initialized( dir )

  #CONFIGURED by FILE
  config = ConfigParser.RawConfigParser()
  try:
    config.read( "%s/%s" % (Env.getLocalRoot( dir ), SWFILE_SNAPCFG) )
  except Exception, e:
    return ret_list

  for snap in config.sections():
    if not snap in inits: #initialized repos not returned here
      ret_list.append( snap )

  return ret_list


def submod_list_initialized( dir = "." ):
  cmd_get_submod = "cd %s && git config -l | grep \"submodule.*.url=\"" % dir
  out,errCode = myCommand_fast( cmd_get_submod )
  submods = []
  for s in out.splitlines():
    submods.append( s[ s.find( "." ) +1 : s.find( ".url=" ) ] )
  return submods


def submod_list_not_initialized( dir = "." ):
  all    = submod_list_all_default( dir )
  inited = submod_list_initialized( dir )
  notinited = []
  for a in all:
    if a not in inited:
      notinited.append( a )
  return notinited

def submod_list_notinitialized_notsnapshot( dir = "." ):
  all    = submod_list_all_default( dir )
  inited = submod_list_initialized( dir )
  snap   = submod_list_snapshot( dir )
  notinited = []
  for a in all:
    if a not in inited and a not in snap:
      notinited.append( a )
  return notinited

def submod_list_initialized_notsnapshot( dir = "." ):
  inited = submod_list_initialized( dir )
  snap   = submod_list_snapshot( dir )
  inited_notsnap = []
  for a in inited:
    if a not in snap:
      inited_notsnap.append( a )
  return inited_notsnap



#return downloaded repos
def submod_list_repos( dir = ".", firstLev = False, excludeRoot = False, localpaths = False ):
  proot = Env.getProjectRoot( dir )
  if proot == "":
    # not inside repo
    if not excludeRoot:
      absroot = os.path.abspath( dir )
      if localpaths:
        return absroot
      else:
        return os.path.relpath( absroot, dir )
    return []

  if firstLev == True:
    cmd_submod_list = "cd %s && git submodule foreach --quiet 'echo $PWD'" % proot
  else:
    cmd_submod_list = "cd %s && git submodule foreach --recursive --quiet 'echo $PWD'" % proot

  out, errCode = myCommand_fast( cmd_submod_list )
  if errCode != 0:
    print out
    return []
  out = out[:-1]
  allrepos = out.splitlines()

  if excludeRoot == False:
    allrepos.insert( 0, os.path.abspath( dir ) )

  if localpaths == True:
    retlist = []
    for r in allrepos:
      retlist.append( os.path.relpath( r, dir ) )
    return retlist

  return allrepos


def submod_list_projs( dir = ".", firstLev = False, excludeRoot = False ):
  allrepos = submod_list_repos( dir, firstLev, excludeRoot )
  retlist = []
  for d in allrepos:
    if os.path.exists( d + "/" + SWFILE_PROJMAP ) == True:
      retlist.append( d )
  return retlist


def submod_get_defbr( abs_projdir, abs_repodir ):

  #not efficent ... 
  filename = "%s/%s" % ( abs_projdir, SWFILE_DEFBR )
  if os.path.exists( filename ) == False:
    print "Not foud file %s" % filename
    return ""

  swdefbr_file = open( filename , 'r' )
  lines = swdefbr_file.read()
  swdefbr_file.close()

  rel_repodir = abs_repodir.replace( abs_projdir, "" )
  rel_repodir = rel_repodir[ 1 :] #remove starting "/"

  for line in lines.splitlines():
    if line.find( "%s:" % rel_repodir ) == 0:
      return line[ line.find(':')+1 : ]
  return ""


def getRepoType( dir ):
  val, errCode = get_repo_cfg( SWCFG_INTBR, dir )
  if errCode != 0:
    #print "qui: ", val
    return ""

  br = val[:-1]
  br_type = br[ findnth( br,"/",5 ) + 1 : findnth( br,"/",6 ) ]
  return br_type

def submod_list_repos_byType( type, dir, firstLev = False, excludeRoot = False ):
  all = submod_list_repos( dir, firstLev, excludeRoot )

  retlist = []
  for d in all:
    if getRepoType( d ) == type:
      retlist.append( d )
  return retlist

def submod_is_initialized( dir, reponame ):
  if reponame in submod_list_initialized():
    return True
  return False


##################
# SUBMOD VISITOR #
##################
#
# func must be of type:
#   afunc( dir, depth )
#     dir = rootdir
#
def submod_apply_all( cdir, afunc, cdepth = 0 ):

  afunc( dir = cdir, depth = cdepth )

  if Env.is_aproj( cdir ) == False:
    return

  for r in submod_list_repos( cdir, excludeRoot = True, firstLev = True ):
    submod_apply_all( r, afunc, cdepth = cdepth + 1 )

  return 


def submod_get_repo_section( startdir ):

  rroot = Env.getLocalRoot( startdir )

  # common entries
  retobj = {}

  retobj[MAP_NAME] = os.path.basename( rroot )

  url, errCode = get_repo_cfg( GITCFG_URL_ORIGIN, dir = rroot )
  if errCode != 0:
    retobj[MAP_URL] = "origin"
  else:
    retobj[MAP_URL] = url[:-1]

  errCode, sha = getSHAFromRef( "HEAD", root = rroot )
  retobj[MAP_CHK] = sha

  retobj[MAP_ABS_LOCALPATH] = rroot
  retobj[MAP_LOCALPATH] = "."

  retobj[MAP_DEF_BRANCH] = "@#@# NO DEFAULT INT BRANCH FOUND @#@#"

  actbr, errCode = get_repo_cfg( SWCFG_INTBR, dir = rroot )
  if errCode != 0:
    retobj[MAP_ACT_BRANCH] = "@#@# INT BR NOT SET @#@#"
  else:
    retobj[MAP_ACT_BRANCH] = actbr[:-1]

  cmd_currbranch = "cd %s && git symbolic-ref -q HEAD | cut -d '/' -f 3-" % retobj[MAP_ABS_LOCALPATH]
  currb,errCode = myCommand_fast( cmd_currbranch )
  if currb[:-1] == "":
    retobj[MAP_CURR_BRANCH] = "DETACHED-HEAD"
  else:
    retobj[MAP_CURR_BRANCH] = currb[:-1] 

  proot = Env.getProjectRoot( rroot )
  if proot == "":
    return retobj

  #
  # inside project only values

  for lr in submod_list_repos( dir = proot, firstLev = True, localpaths = True ):

    bn = os.path.basename( rroot )
    pos = lr.find( bn )
    if pos != -1 and pos == len( lr ) - len( bn ): #ends with basename (only 1 exists)

      retobj[MAP_NAME] = lr #override standalone repo behaviour
      retobj[MAP_LOCALPATH] = lr

      cmd_actIntBr = "grep -e \"^%s:\" %s/%s" % ( retobj[MAP_LOCALPATH], proot, SWFILE_DEFBR )
      out,errCode = myCommand_fast( cmd_actIntBr )
      if errCode == 0:
        retobj[MAP_DEF_BRANCH] = out[:-1].split( ":" )[1]

      return retobj

  # here only when inside root dir of project 
  return retobj



def swop_dump( dir, depth ):
  #print "dir   : ", dir
  #print "depth : ", depth
  pprint( submod_get_repo_section( dir ) )




def main():
  if len( sys.argv ) != 2:
    print "usage: sys.argv[0] <aPATH>"
    sys.exit(1)

  from pprint import pprint
  print "ALL repos:"
  pprint( submod_list_repos( sys.argv[1] ) )
  print ""

  print "ALL LOCAL-PATH repos:"
  pprint( submod_list_repos( sys.argv[1], localpaths = True ) )
  print ""

  print "FIRST LEVEL repos:"
  pprint( submod_list_repos( sys.argv[1], firstLev = True ) )
  print ""

  print "FIRST LEVEL local repos:"
  pprint( submod_list_repos( sys.argv[1], firstLev = True, localpaths = True ) )
  print ""

  submod_apply_all( sys.argv[1], swop_dump )


  print "submod_list_all_default():"
  print submod_list_all_default()
  print "submod_list_snapshot():"
  print submod_list_snapshot()
  print "submod_list_initialized():"
  print submod_list_initialized()
  print "submod_list_not_initialized():"
  print submod_list_not_initialized()
  print "submod_list_notinitialized_notsnapshot():"
  print submod_list_notinitialized_notsnapshot()
  print "submod_list_initialized_notsnapshot():"
  print submod_list_initialized_notsnapshot()
  print "submod_list_repos():"
  print submod_list_repos()
  print "submod_list_projs():"
  print submod_list_projs()
  print "submod_list_repos_byType( INT ):"
  print submod_list_repos_byType( "INT", "." )
  print "submod_list_repos_byType( CST ):"
  print submod_list_repos_byType( "CST", "." )

if __name__ == "__main__":
  main()
