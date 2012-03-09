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
from Common import * 
from ObjLog import *
from ObjEnv import *
from ObjStatus import * 
from ObjBranch import *
from ObjTag import *
import Utils
import Utils_All

def creaBranch( branch, type, ref ):
 
  currUser = Env.getCurrUser()
  ret, currRel = evalCandidateRel( ref )

  brName = currRel + "/" + currUser + "/" + type + "/" + branch

  GLog.s( GLog.S, "Creating branch " + brName + " starting from " + ref + " ..." )
  
  #branch
  cmd="git checkout -b %s %s " % ( brName, ref )
  out,errCode = myCommand( cmd )
  GLog.logRet( errCode )

  brStartLbl = "%s/%s/%s" % ( brName, SWCFG_TAG_NEW, SWCFG_TAG_NEW_NAME )
  GLog.s( GLog.S, "Creating starting branch label: " + brStartLbl + " ..." )

  #label
  cmd="git tag %s -f %s -m \"Created branch\"" % ( brStartLbl, ref )
  out,errCode = myCommand(cmd)
  GLog.logRet( errCode )

  return errCode


def del_tag_of_br( tag ):
  GLog.s( GLog.S, "Deleting tag %s locally ..." % tag )

  out,errCode = myCommand( "git tag -d %s" %  (tag) )
  if errCode != 0:
    strerr  = "FAILED deleting tag %s\n" % (tag)
    strerr += indentOutput( out[:-1], 1 )
    GLog.f( GLog.E, strerr )
    return 1
  GLog.logRet( 0 )
  return 0

def delete_br( options ):

  brObj, f_delete, f_erase, f_alsotags, f_islocal, f_isremote = options_to_delbr_info( options )

  #eval before deleting
  br_repo, br_repo_errcode = brObj.branch_to_remote()
  br_shortRef = brObj.getShortRef()
  br_newbr    = brObj.getNewBrRef()
  
  # with 2 remotes 
  # remote/abranch is present twice but NEW/BRANCH only once 
  #  manage it manually
  labels = []
  if f_alsotags:
    err, labels = Tag.list_by_branch( [ br_shortRef ] )
    if br_newbr in labels:
      labels.remove( br_newbr )

  allret = 0

  #erase => delete only if local branch has same remote as remote branch been deleted
  f_jump = False
  if f_erase and f_islocal:
    # Here we re-evaluate locBr obj:
    # if you isseued branch -e/-E with short reference (no remote) this is unuseful
    # if you isseued branch -e/-E with long, remoted reference -> this may a local branch with different remote
    #  (only if more that 1 remote present)
    # see test_Branch_10_01_Create_Src_OnlyRemote (with mode = moreremotes)
    locBr = Branch( brObj.getShortRef() )
    loc_repo, loc_repo_err = locBr.branch_to_remote()

    if loc_repo != br_repo:
      f_jump = True


  #
  #1. local br
  #   delete or erase always delete locally
  #
  if f_jump:
    GLog.s( GLog.S, "Not deleting branch %s and tags locally because its remote is '%s' (rather than '%s')" % (br_shortRef,loc_repo,br_repo) )
    labels = []

  if f_islocal and not f_jump:

    GLog.s( GLog.S, "Deleting branch %s locally ..." % br_shortRef )

    out,errCode = myCommand( "git branch -D %s" % (br_shortRef) )
    if errCode != 0:
      GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
      GLog.logRet( 1 )
      return 1

    GLog.logRet( 0 )

  # always NEW BRANCH
  #  also if branch is only remote
  err, sha =  getSHAFromRef( br_newbr )
  if err == 0:
    ret = del_tag_of_br( br_newbr )
    if ret != 0:
      allret = 1


  #
  #2. local tags
  #
  for l in labels:
    ret = del_tag_of_br( l )
    if ret != 0:
      allret = 1


  #3. remote br and tags
  if f_erase:

    GLog.s( GLog.S, "Deleting references remotely ..." )

    #br
    cmd_push_del  = "git push %s :%s " % ( br_repo, br_shortRef )
    #newbr (manually)
    cmd_push_del += " :%s " % ( br_newbr )
    #tags
    for l in labels:
      cmd_push_del += " :refs/tags/%s " % l

    out,errCode = myCommand( cmd_push_del )
    GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    if errCode != 0:
      allret = 1
      GLog.logRet( 1 )
      return 1

    GLog.logRet( 0 )

  return allret


def move_tag_of_br( oldtag, newtag ):

  GLog.s( GLog.S, "Renaming tag %s into %s locally ..." % (oldtag,newtag) )

  cmd_getmsg = "git log -1 --format=%%B %s" % oldtag
  tag_body,errCode = myCommand( cmd_getmsg )
  if errCode != 0:
    tag_body="moved tag\n"
  #tag_body = tag_body.replace( "\n", "\\n" )

  out,errCode = myCommand( "git tag -m '%s' %s %s && git tag -d %s" %  ( tag_body[:-1], newtag, oldtag, oldtag) )
  if errCode != 0:
    strerr  = "FAILED renaming tag %s\n" % (oldtag)
    strerr += indentOutput( out[:-1], 1 )
    GLog.f( GLog.E, strerr )
    return 1

  GLog.logRet( 0 )
  return 0



def move_br( options ):

  newbr_shortref, f_deep, f_islocal, f_isremote = options_to_movebr_info( options )

  cb = Branch.getCurrBr()
  oldbr_shortref = cb.getShortRef()
  #eval before deleting
  br_repo, br_repo_errcode = cb.branch_to_remote()

  err, labels = Tag.list_by_branch( [ oldbr_shortref ] )

  allret = 0

  GLog.s( GLog.S, "Renaming branch %s into %s locally ..." % (oldbr_shortref, newbr_shortref) )

  out,errCode = myCommand( "git branch -m %s %s" % (oldbr_shortref,newbr_shortref) )
  if errCode != 0:
    GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    GLog.logRet( 1 )
    return 1

  GLog.logRet( 0 )

  for l in labels:
    newl = l.replace( oldbr_shortref, newbr_shortref )
    ret = move_tag_of_br( l, newl )
    if ret != 0:
      allret = 1


  #also on remote
  if f_deep:

    GLog.s( GLog.S, "Deleting references remotely ..." )


    cmd_push_del = "git push %s :%s %s" % ( br_repo, oldbr_shortref, newbr_shortref )
    for l in labels:
      cmd_push_del += " :refs/tags/%s " % l

      newl = l.replace( oldbr_shortref, newbr_shortref )
      cmd_push_del += " refs/tags/%s " % newl

    out,errCode = myCommand( cmd_push_del )
    GLog.f( GLog.E, indentOutput( out[:-1], 1 ) )
    if errCode != 0:
      allret = 1
      GLog.logRet( 1 )
      return 1

  return allret



def evalCandidateRel( ref ):

  br_sr, strerr = Utils.eval_curr_branch_shortref( ref )
  if br_sr == "":
    strerr  = "ERROR - " + strerr
    return 1, strerr
  return 0, br_sr[ 0: findnth( br_sr, "/", SWCFG_REL_SLASHES) ]


def switch_to( ref ):

  cb = Branch.getCurrBr()
  if cb.isValid():
    if cb.is_local_br():
      lastbr = cb.getShortRef()
    else:
      lastbr = cb.getRemoteRef()
  else:
    err, sha =  getSHAFromRef( "HEAD" )
    lastbr = sha

  GLog.s( GLog.S, "Switching to %s ..." % ref )

  cmd = "git checkout %s" % ref
  out,errCode = myCommand( cmd )
  if errCode != 0:
    GLog.f( GLog.E, indentOutput( out[:-1], 1) )

  GLog.logRet( errCode )

  #only if success
  filename = "%s/%s" % ( Env.getLocalRoot(), SWFILE_BRANCH_LAST )
  fin = open( filename, "w+" )
  fin.write( lastbr )
  fin.close()

  return errCode  


# If you specify a local  branch not tracked => will be tracked and set to int
# If you specify a local  branch tracked => will be only set new int
# If you specify a remote branch not local => will be tracked and set to int
# If you specify a remote branch also local =>  will be only set new int
# If you specify a local  branch not existing on origin => will be set as int and when pushed, will be tracked to.
def set_new_int_br( branch ):

  objBr = Branch( branch )

  #if a remote exists, track it now, otehrwise will be done at push time
  rem_br = objBr.branch_to_remote_obj()
  if rem_br.isValid():
    #
    # if it is not tracked, track it now
    #
    trackedInfo, tracked = rem_br.get_track_info()
    if not tracked or trackedInfo[Branch.TRACK_REMOTE] != rem_br.getRepo() :
      cmd_track = "SWINDENT=%s %s branch --track %s" % ( GLog.tab, SWGIT, rem_br.getRemoteRef() )
      errCode = os.system( cmd_track )
      if errCode != 0:
        return 1

  ib = Branch.getIntBr()
  if ib.getShortRef() == objBr.getShortRef():
    return 0

  #
  # set it as intbr
  #
  GLog.s( GLog.S, "Setting INTEGRATION branch to %s into repo %s ... " % (objBr.getShortRef(),Env.getLocalRoot()) )
  out, errCode = set_repo_cfg( SWCFG_INTBR, objBr.getShortRef() )
  GLog.logRet( errCode )

  return errCode  

def unset_intbr():

  GLog.s( GLog.S, "UnSetting INTEGRATION branch into repo %s ... " % (Env.getLocalRoot()) )
  out, errCode = set_repo_cfg( SWCFG_INTBR, SWCFG_UNSET )
  GLog.logRet( errCode )
  return 0


def trackBranch( brObj ):

  trackedInfo, tracked = brObj.get_track_info()
  if tracked and trackedInfo[Branch.TRACK_REMOTE] == brObj.getRepo():
      return 0

  GLog.s( GLog.S, "Tracking branch %s into repo %s ... " % (brObj.getRemoteRef(), os.path.basename( os.getcwd() )) )
  
  cmd_track = "git branch --set-upstream %s %s" % ( brObj.getShortRef(), brObj.getRemoteRef() )
  out,errCode = myCommand( cmd_track )
  GLog.logRet( errCode )
  if errCode != 0:
    print out
    return 1 

  return errCode


def check_move( options ):

  newbr_name, f_deep, f_islocal, f_isremote = options_to_movebr_info( options )

  cb = Branch.getCurrBr()
  if not cb.isValid():
    GLog.f( GLog.E, "Branch rename can be done only on current branch (not in detahced head or on any non swgit-valid branch)" )
    return 1

  brObj = Branch( newbr_name )
  if brObj.isValid():
    GLog.f( GLog.E, "Already exists a branch named '%s'" % newbr_name )
    return 1

  if newbr_name.count("/") != SWCFG_BR_NUM_SLASHES_LOCAL:
    GLog.f( GLog.E, "Only local branch names allowed (%s slashes)" % SWCFG_BR_NUM_SLASHES_LOCAL )
    return 1

  rel    = newbr_name[ 0 : findnth( newbr_name, '/', SWCFG_REL_SLASHES ) ]
  user   = newbr_name[ findnth( newbr_name, '/', SWCFG_REL_SLASHES )     + 1 : findnth( newbr_name, '/', SWCFG_REL_SLASHES + 1) ]
  brtype = newbr_name[ findnth( newbr_name, '/', SWCFG_REL_SLASHES + 1 ) + 1 : findnth( newbr_name, '/', SWCFG_REL_SLASHES + 2) ]
  brname = newbr_name[ findnth( newbr_name, '/', SWCFG_REL_SLASHES + 2 ) + 1 : ]

  #print rel, user, brtype, brname

  rel, ret = check_release( rel )
  if ret != 0:
    GLog.f( GLog.E, rel )
    return 1

  user, ret = check_username( user )
  if ret != 0:
    GLog.f( GLog.E, user )
    return 1

  if brtype != cb.getType():
    GLog.f( GLog.E, "Cannot change branch type." )
    return 1

  strerr, err = check_brname( brname )
  if err != 0:
    GLog.f( GLog.E, strerr )
    return 1

  if f_deep and not f_isremote:
    GLog.f( GLog.E, "Not existing remote branch, try using -m option instead." )
    return 1

  return 0



def check_track( value ):
  toBeTrackedBr = Branch( value )
  if not toBeTrackedBr.isValid():
    if len( toBeTrackedBr.getMatches() ) > 0:
      GLog.f( GLog.E, toBeTrackedBr.getNotValidReason() )
      return 1

  if toBeTrackedBr.is_local_br():
    GLog.f( GLog.E, "Please specify a remote branch to be tracked (i.e. starting with \"origin\" or any valid remote name)" )
    return 1

  if not toBeTrackedBr.exist_remote():
    GLog.f( GLog.E, "Remote branch %s does not exists (maybe you can pull that remote?)" % value )
    return 1

  trackedInfo, tracked = toBeTrackedBr.get_track_info()
  if tracked and trackedInfo[Branch.TRACK_REMOTE] == toBeTrackedBr.getRepo():
    GLog.f( GLog.E, "Already tracked branch %s " % value )
    return 0

  return 0 

def evalBranchType( options ):
  type = SWCFG_BR_FTR
  cb = Branch.getCurrBr()
  if cb.isStable():
    type = SWCFG_BR_FIX
  return type


# With only 1 remote (origin) everithing is ok to return getShortRef()
# With remotes > 1 we need to return also remote 
#    (otherwise error: pathspec '...' did not match any file(s) known to git )
# but
# when checkout with origin name, branch will not be tracked automatically
# =>
# evaluate result as getShortRef(), if it is shorter than input => return input, otehrwise result
def validate_ref( ref ):

  br = Branch( ref )
  tag = Tag( ref )

  if br.isValid():
    result = br.getShortRef()
    if ref.count("/") > result.count("/"):
      return ref, 0
    else:
      return result, 0

  if tag.isValid():
    result = tag.getTagShortRef()
    if ref.count("/") > result.count("/"):
      return ref, 0
    else:
      return result, 0

  err, sha = getSHAFromRef( ref )
  if err == 0:
    return sha, 0

  if len( br.getMatches() ) > 0:
    return br.getNotValidReason(), 1

  return "Please specify a valid reference", 1



def check_create( options ):

  strerr, err = check_brname( options.newB)
  if err != 0:
    GLog.f( GLog.E, strerr )
    return 1


  if options.src_ref == None:
    ib = Branch.getIntBr() #may be any kind of branch
    sb = Branch.getStableBr()
    cb = Branch.getCurrBr()
    if ib.isValid() == False:
      GLog.f( GLog.E, "ERROR: Without integration branch set, plese specify --source while creating branch." )
      return 1
    if cb.isValid() == False:
      GLog.f( GLog.E, "ERROR: In 'detached head', plese specify --source while creating branch." )
      return 1
    if ib.getShortRef() != cb.getShortRef() and not cb.isStable():
      GLog.f( GLog.E, "ERROR: Outside integration or stable branch, --source is mandatory." )
      return 1

  #src
  ref = "HEAD"
  if options.src_ref != None:
    valid, err = validate_ref( options.src_ref )
    if err != 0:
      GLog.f( GLog.E, valid )
      return 1
    ref = valid
  

  #rel
  cb = Branch.getCurrBr()
  if cb.isValid() == True:
    currRel = cb.getRel()
  else:
    ret, currRel = evalCandidateRel( ref )
    if ret != 0:
      GLog.f( GLog.E, currRel )
      return 1

  type = evalBranchType( options )
  currUser = Env.getCurrUser()
  
  brName = currRel + "/" + currUser + "/" + type + "/" + options.newB
  br = Branch( brName ) #this retrieves also branches with same name but different user
  if br.isValid() == True:
    GLog.f( GLog.E, "ERROR: This branch already exists (%s)" % br.getShortRef() )
    return 1
  
  return 0


def options_to_delbr_info( options ):

  br = ""
  f_delete   = False
  f_erase    = False
  f_alsotags = False

  if options.del_br != None:
    br = options.del_br
    f_delete = True
  if options.del_br_all != None:
    br = options.del_br_all
    f_delete = True
    f_alsotags = True
  if options.erase != None:
    br = options.erase
    f_erase = True
  if options.erase_all != None:
    br = options.erase_all
    f_erase = True
    f_alsotags = True

  brObj = Branch( br )

  err, any_rem_br = Branch.list_remote_br( "*", brObj.getRel(), brObj.getUser(), brObj.getType(), brObj.getName() )
  err, any_loc_br = Branch.list_local_br ( brObj.getRel(), brObj.getUser(), brObj.getType(), brObj.getName() )

  f_isremote = False
  if len( any_rem_br ) > 0:
    f_isremote = True

  f_islocal  = False
  if len( any_loc_br ) > 0:
    f_islocal = True


  #print  brObj, f_delete, f_erase, f_alsotags, f_islocal, f_isremote
  return brObj, f_delete, f_erase, f_alsotags, f_islocal, f_isremote


def options_to_movebr_info( options ):

  br = ""
  f_deep = False

  if options.move_br != None:
    br = options.move_br
  if options.move_br_deep != None:
    br = options.move_br_deep
    f_deep = True

  cb = Branch.getCurrBr()

  err, any_rem_br = Branch.list_remote_br( "*", cb.getRel(), cb.getUser(), cb.getType(), cb.getName() )
  err, any_loc_br = Branch.list_local_br ( cb.getRel(), cb.getUser(), cb.getType(), cb.getName() )

  #print  any_rem_br
  #print  any_loc_br

  f_isremote = False
  if len( any_rem_br ) > 0:
    f_isremote = True

  f_islocal  = False
  if len( any_loc_br ) > 0:
    f_islocal = True

  #print  br, f_deep, f_islocal, f_isremote
  return br, f_deep, f_islocal, f_isremote


def check_delete( options ):

  brObj, f_delete, f_erase, f_alsotags, f_islocal, f_isremote = options_to_delbr_info( options )

  if not brObj.isValid():
    GLog.f( GLog.E, brObj.getNotValidReason() )
    return 1

  cb = Branch.getCurrBr()
  if cb.isValid() and cb.getShortRef() == brObj.getShortRef():
    GLog.f( GLog.E, "Cannot delete a branch on which you are" )
    return 1

  if f_islocal and f_isremote:
    pass
  elif f_islocal:
    if f_erase:
      GLog.f( GLog.E, "Not existing remote branch, try using -d/-D option instead" )
      return 1
  elif f_isremote:
    if f_delete:
      GLog.f( GLog.E, "Not existing local branch, try using -e/-E option instead" )
      return 1

  return 0


def check_branch( value ):
  br = Branch( value )
  if br.isValid() == False:
    GLog.f( GLog.E, "Please specify an existing/valid branch reference" )
    return 1
  return 0
  

def check_br_ref( value ):
  err, sha = getSHAFromRef( value )
  if err != 0:
    GLog.f( GLog.E, "Please specify a valid reference" )
    return 1
  return 0


def check_branch_opt( option ):
  out, err = check_allowed_options( option, branch_allowmap, branch_opt_aliases )
  if err != 0:
    GLog.f( GLog.E, out[:-1] )
    return 1
  return 0


def check( options ):

  #params consistency
  if len( sys.argv ) == 1:
    return 0
  if options.list == True:
    return check_branch_opt( "--list" )
  if options.list_tracked == True:
    return check_branch_opt( "--list-tracked" )
  if options.list_local_remote == True:
    return check_branch_opt( "--local-remote" )
  if options.list_remote == True:
    return check_branch_opt( "--remote-branches" )
  if options.all_releases == True:
    return check_branch_opt( "--all-releases" )
  if options.rel != None:
    return check_branch_opt( "--release-selector" )
  if options.user != None:
    return check_branch_opt( "--user-selector" )
  if options.typeB != None:
    return check_branch_opt( "--branch-type-selector" )
  if options.nameB != None:
    return check_branch_opt( "--branch-name-selector" )
    
  if options.newB != None:
    err = check_branch_opt( "--create" )
    if err != 0:
      return 1
  if options.del_br != None:
    err = check_branch_opt( "--delete" )
    if err != 0:
      return 1
  if options.del_br_all != None:
    err = check_branch_opt( "--delete-all" )
    if err != 0:
      return 1
  if options.erase != None:
    err = check_branch_opt( "--erase" )
    if err != 0:
      return 1
  if options.erase_all != None:
    err = check_branch_opt( "--erase-all" )
    if err != 0:
      return 1
  if options.move_br != None:
    err = check_branch_opt( "--move" )
    if err != 0:
      return 1
  if options.move_br_deep != None:
    err = check_branch_opt( "--move-deep" )
    if err != 0:
      return 1
  if options.switch_to != None:
    err = check_branch_opt( "--switch" )
    if err != 0:
      return 1
  if options.switch_back == True:
   err = check_branch_opt( "--switch-back" )
   if err != 0:
     return 1
  if options.track_br != None:
    err = check_branch_opt( "--track-remote" )
    if err != 0:
      return 1
  if options.switch_to_int == True:
    err = check_branch_opt( "--to-integration" )
    if err != 0:
      return 1
  if options.set_new_int != None:
    err = check_branch_opt( "--set-integration-br" )
    if err != 0:
      return 1
  if options.unset_intbr:
    err = check_branch_opt( "--unset-integration-br" )
    if err != 0:
      return 1
  if options.get_int_br == True:
    err = check_branch_opt( "--get-integration-br" )
    if err != 0:
      return 1
  if options.show_cb == True:
    err = check_branch_opt( "--current-branch" )
    if err != 0:
      return 1

  #check local status
  if options.switch_to != None or options.switch_back == True or \
      options.newB != None or options.switch_to_int == True:
    err, errstr = Status.checkLocalStatus_rec( ignoreSubmod = True )
    if err != 0:
      GLog.f( GLog.E, errstr )
      return 1

  if options.switch_to != None:
    valid, err = validate_ref( options.switch_to )
    if err != 0:
      GLog.f( GLog.E, valid )
      return 1
    return 0

  if options.newB != None:
    return check_create( options )

  if options.del_br != None or options.del_br_all != None or options.erase != None or options.erase_all != None:
    return check_delete( options )

  if options.move_br != None or options.move_br_deep != None:
    return check_move( options )

  if options.track_br != None:
    return check_track( options.track_br )

  if options.get_int_br == True or options.switch_to_int == True:
    ib = Branch.getIntBr()
    if not ib.isValid():
      GLog.f( GLog.E, "No int branch set for this repo. Use swgit branch --set-integration-br" )
      return 1

  if options.set_new_int != None:
    newInt = Branch( options.set_new_int )
    if not newInt.isValid():
      GLog.f( GLog.E, newInt.getNotValidReason() )
      return 1

    # If you specify a local  branch not tracked => will be tracked and set to int
    # If you specify a local  branch tracked => will be only set new int
    # If you specify a remote branch not local => will be tracked and set to int
    # If you specify a remote branch also local =>  will be only set new int
    # If you specify a local  branch not existing on origin => will be set as int and when pushed, will be tracked to.

  return 0


def execute( options ):
  #
  # -l list branch
  # 
  if len( sys.argv ) == 1:
    ret, total = Branch.list_local_br()
    if options.quiet == False:
      print "\n".join(total)
    return 0

  elif options.show_cb == True:
    cb = Branch.getCurrBr()
    if options.quiet == False:
      if cb.isValid() == True:
        print cb.getShortRef()
      else:
        print "(detached-head)"
    return 0

  elif options.list_tracked == True:
    err, local_branches = Branch.list_local_br ()
    for l in local_branches:
      objBr = Branch( l )
      trackedInfo, tracked = objBr.get_track_info()
      if tracked:
        print "local %s <--> %s %s" % (l, trackedInfo[Branch.TRACK_REMOTE], trackedInfo[Branch.TRACK_MERGE] )

  elif options.list == True or options.rel != None or options.user != None or \
       options.typeB != None or options.nameB != None or \
       options.all_releases == True or \
       options.list_remote == True or options.list_local_remote == True:


    rel   = "*/*/*/*"
    user  = "*"
    typeB = "*"
    nameB = "*"

    myb = Branch.getCurrBr()
    if myb.isValid():
      myb_sr, myb_strerr = Utils.eval_curr_branch_shortref( "HEAD" )
      myb = Branch( myb_sr )

    if options.list == True:
      user = Env.getCurrUser()
      if myb.isValid(): #-l and on br
        rel   = myb.getRel()

    if options.rel != None:
      rel, ret = check_release( options.rel )
      if ret != 0:
        print rel
        return 1

    if options.all_releases:
      rel   = "*/*/*/*"

    if options.user != None: 
      user = options.user
    if options.typeB != None: 
      typeB = options.typeB
    if options.nameB != None: 
      nameB = options.nameB

    repo = "heads"
    if options.list_local_remote == True:
      repo = "*"

    #print "repo: ", repo
    #print "rel : ", rel
    #print "user: ", user
    #print "type: ", typeB
    #print "name: ", nameB
    #print ""
    if options.list_remote:
      ret, total = Branch.list_remote_br( "*", rel, user, typeB, nameB )
    else:
      ret, total = Branch.list( repo, rel, user, typeB, nameB )

    if options.quiet == False:
      if len(total) == 0:
        print "No branches found for ref:  %s/%s/%s/%s"  % ( rel, user, typeB, nameB )
      else:
        print "\n".join(total)
    return ret

  ##########
  # CREATE #
  ##########
  elif options.newB:

    type = evalBranchType( options )

    ref = "HEAD"
    if options.src_ref != None:
      ref, err = validate_ref( options.src_ref )
  
    return creaBranch( options.newB, type, ref )

  elif options.del_br != None or options.del_br_all != None or options.erase != None or options.erase_all != None:

    return delete_br( options )

  elif options.move_br != None or options.move_br_deep != None:

    return move_br( options )

  elif options.switch_to_int == True:

    ib = Branch.getIntBr()
    return switch_to( ib.getShortRef() )

  elif options.switch_back == True:

    #load last br visited
    filename = "%s/%s" % ( Env.getLocalRoot(), SWFILE_BRANCH_LAST )

    if os.path.exists( filename ) == False:
      GLog.s( GLog.S, "No found any 'last branch' information. Cannot switch" )
      return 1
    fin = open( filename, "r" )
    lastbr = fin.readline()
    fin.close()

    return switch_to( lastbr )

  elif options.set_new_int != None:

    return set_new_int_br( options.set_new_int )

  elif options.unset_intbr:

    return unset_intbr()

  elif options.get_int_br == True:

    ib = Branch.getIntBr()
    if options.quiet == False:
      print ib.getFullRef()
    return 0

  elif options.switch_to != None:

    valid, err = validate_ref( options.switch_to )
    return switch_to( valid )

  elif options.track_br:

    br = Branch( options.track_br )
    return trackBranch( br )

  return 0




def main():
  usagestr =  """\
Usage: swgit branch         (show all local branches)
   or: swgit branch -l      (show my  local branches)
   or: swgit branch [other list filters]
   or: swgit branch --create <brname> [--source <startpoint>]
   or: swgit branch --delete|--delete-all|--erase|--erase-all  <brname>
   or: swgit branch -m|-M  <newbrname>
   or: swgit branch --switch <brname>
   or: swgit branch --track <brname>
   or: swgit branch --to-integration
   or: swgit branch --set-integration-br <brname> """

  parser       = OptionParser( usage = usagestr, 
                               description='>>>>>>>>>>>>>> swgit - Branch Management <<<<<<<<<<<<<<' )
  mgt_group    = OptionGroup( parser, "Management options" )
  rtrv_group   = OptionGroup( parser, "Retrieve   options" )
  output_group = OptionGroup( parser, "Output options" )

  load_command_options( mgt_group, gitbranch_mgt_options )
  load_command_options( rtrv_group, gitbranch_rtrv_options )
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( mgt_group )
  parser.add_option_group( rtrv_group )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()
  args = parser.largs
  
  help_mac( parser )

  GLog.initGitLogs( options )
  

  if len(args) != 0:
    parser.error("Too many arguments")
 
  GLog.s( GLog.I, " ".join( sys.argv ) )

#  if options.all == True:
#    ret = Utils_All.All( options )
#    sys.exit( ret )

  if os.environ.get('SWCHECK') != "NO":
    if check(options) != 0:
      sys.exit(1)
  
  if os.environ.get('SWCHECK') == "ONLY":
    sys.exit(0)

  ret = execute(options)
  if ret != 0:
    sys.exit( 1 )
  sys.exit( 0 )



gitbranch_mgt_options = [
    [ 
      "-c",
      "--create",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "newB",
        "metavar" : "<branch_name_val>",
        "help"    : "Create branch specifying its name",
        }
      ],
    [ 
      "-S",
      "--source",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "src_ref",
        "metavar" : "<reference>",
        "help"    : "Create branch specifying a starting-from reference (commit, tag or branch)",
        }
      ],
    [ 
      "-d",
      "--delete",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "del_br",
        "metavar" : "<branch_name>",
        "help"    : 'Locally delete branch (also if not fully merged)',
        }
      ],
    [ 
      "-D",
      "--delete-all",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "del_br_all",
        "metavar" : "<branch_name>",
        "help"    : 'Locally delete branch and all its labels',
        }
      ],
    [ 
      "-e",
      "--erase",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "erase",
        "metavar" : "<branch_name>",
        "help"    : 'Locally and remotely delete branch',
        }
      ],
    [ 
      "-E",
      "--erase-all",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "erase_all",
        "metavar" : "<branch_name>",
        "help"    : 'Locally and remotely delete branch and all its labels',
        }
      ],
    [ 
      "-s",
      "--switch",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "switch_to",
        "metavar" : "<reference>",
        "help"    : 'Specify a reference to switch onto'
        }
      ],
    [ 
      "-b",
      "--switch-back",
      {
        "action"  : "store_true",
        "dest"    : "switch_back",
        "default" : False,
        "help"    : 'Shortcut to switch on last visited branch'
        }
     ],
    [
      "-i",
      "--to-integration",
      {
        "action"  : "store_true",
        "dest"    : "switch_to_int",
        "default" : False,
        "help"    : 'Shortcut to switch on integration branch'
        }
     ],
    [ 
      "--set-integration-br",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "set_new_int",
        "metavar" : "<branch_name>",
        "help"    : 'For this repository, set current integration branch to this new one'
        }
      ],
    [ 
      "--unset-integration-br",
      {
        "action"  : "store_true",
        "dest"    : "unset_intbr",
        "default" : False,
        "help"    : "Unset current integartion branch"
        }
      ],
    [ 
      "-t",
      "--track",
      { 
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "track_br",
        "metavar" : "<branch_name>",
        "help"    : 'Specify a remote branch to be tracked.'
        }
      ],
    [ 
      "-m",
      "--move",
      { 
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "move_br",
        "metavar" : "<new_branch_name>",
        "help"    : 'Change name to current branch and all its labels.'
        }
      ],
    [ 
      "-M",
      "--move-deep",
      { 
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "move_br_deep",
        "metavar" : "<new_branch_name>",
        "help"    : 'Change name to current branch and all its labels locally and remotely.'
        }
      ],
    ]


gitbranch_rtrv_options = [
    [ 
      "-H",
      "--current-branch",
      {
        "action"  : "store_true",
        "dest"    : "show_cb",
        "default" : False,
        "help"    : 'Show current branch (HEAD)'
        }
      ],
     [ 
      "-I",
      "--get-integration-br",
      {
        "action"  : "store_true",
        "dest"    : "get_int_br",
        "default" : False,
        "help"    : 'Show current integration branch'
        }
      ],
    [ 
      "-l",
      "--list",
      {
        "action"  : "store_true",
        "dest"    : "list",
        "default" : False,
        "help"    : 'List only current-user branches'
        }
      ],
    [ 
      "-T",
      "--list-tracked",
      {
        "action"  : "store_true",
        "dest"    : "list_tracked",
        "default" : False,
        "help"    : 'List only tracked branches'
        }
      ],
    [ 
      "-a",
      "--local-remote",
      {
        "action"  : "store_true",
        "dest"    : "list_local_remote",
        "default" : False,
        "help"    : 'List local and remote branches'
        }
      ],
    [ 
      "--remote",
      "--remote-branches",
      {
        "action"  : "store_true",
        "dest"    : "list_remote",
        "default" : False,
        "help"    : 'List only remote branches'
        }
      ],
    [ 
      "-A",
      "--all-releases",
      {
        "action"  : "store_true",
        "dest"    : "all_releases",
        "default" : False,
        "help"    : 'List all releases branches'
        }
      ],
    [ 
      "-R",
      "--release-selector",
      {
        "nargs"   : 1,
        "action"  : "store",
        "dest"    : "rel",
        "metavar" : "<release_val>",
        "help"    : 'List all branches given a specified release'
        }
      ],
    [
      "-U",
      "--user-selector",
      {
        "nargs"   : 1,
        "action"  : "store",
        "dest"    : "user",
        "metavar" : "<user_val>",
        "help"    : 'List all branches given a specific user'
        }
      ],
     [
       "-B",
       "--branch-type-selector",
       {
        "nargs"   : 1,
        "action"  : "store",
        "dest"    : "typeB",
        "metavar" : "<branch_type_val>",
         "help"    : 'List all branches given a specific branch type (i.e. FTR or FIX)'
         }
       ],
     [
       "-N",
       "--branch-name-selector",
       {
        "nargs"   : 1,
        "action"  : "store",
        "dest"    : "nameB",
        "metavar" : "<branch_name_val>",
        "help"    : 'List all branches given a specific branch name'
         }
       ]
    ]

branch_opt_aliases  = {
    "-c"        : "--create",
    "-S"        : "--source",
    "-d"        : "--delete",
    "-D"        : "--delete-all",
    "-e"        : "--erase",
    "-E"        : "--erase-all",
    "-m"        : "--move",
    "-M"        : "--move-deep",
    "-s"        : "--switch",
    "-b"        : "--switch-back",
    "-I"        : "--get-integration-br",
    "-i"        : "--to-integration",
    "-t"        : "--track",
    "-T"        : "--list-tracked",
    "-H"        : "--current-branch",
    "-l"        : "--list",
    "-a"        : "--local-remote",
    "-A"        : "--all-releases",
    "--remote"  : "--remote-branches",
    "-R"        : "--release-selector",
    "-U"        : "--user-selector",
    "-B"        : "--branch-type-selector",
    "-N"        : "--branch-name-selector",
    }

branch_opt_allowed  = [ "--quiet", "--verbose", "--debug" ]
branch_opt_list_all = [ "--list", "--all-releases", "--release-selector", "--user-selector", "--branch-type-selector", "--branch-name-selector", "--local-remote", "--remote-branches" ]
branch_allowmap = {
      "--create"               : branch_opt_allowed + [  "--source" ],
      "--delete"               : branch_opt_allowed,
      "--delete-all"           : branch_opt_allowed,
      "--erase"                : branch_opt_allowed,
      "--erase-all"            : branch_opt_allowed,
      "--move"                 : branch_opt_allowed,
      "--move-deep"            : branch_opt_allowed,
      "--switch"               : branch_opt_allowed,
      "--switch-back"          : branch_opt_allowed,
      "--track"                : branch_opt_allowed,
      "--to-integration"       : branch_opt_allowed,
      "--set-integration-br"   : branch_opt_allowed,
      "--unset-integration-br" : branch_opt_allowed,
      "--get-integration-br"   : branch_opt_allowed,
      "--current-branch"       : branch_opt_allowed,
      "--list"                 : branch_opt_allowed + branch_opt_list_all,
      "--list-tracked"         : branch_opt_allowed,
      "--all-releases"         : branch_opt_allowed + branch_opt_list_all,
      "--release-selector"     : branch_opt_allowed + branch_opt_list_all,
      "--user-selector"        : branch_opt_allowed + branch_opt_list_all,
      "--branch-type-selector" : branch_opt_allowed + branch_opt_list_all,
      "--branch-name-selector" : branch_opt_allowed + branch_opt_list_all,
      "--local-remote"         : branch_opt_allowed + branch_opt_list_all,
      "--remote"               : branch_opt_allowed + branch_opt_list_all,
      }

if __name__ == "__main__":
  main()
  
 
 




