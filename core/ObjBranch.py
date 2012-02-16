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

import sys,string

from MyCmd import *
from Common import *
from ObjEnv import *



class Branch:
  TRACK_REMOTE = "REMOTE"
  TRACK_MERGE = "MERGE"

  def __init__( self, br, root = "." ):
    self.br_             = br
    self.root_           = root
    self.fullRef_        = ""
    self.isValid_        = False
    self.matches_        = []
    self.local_matches_  = []
    self.remote_matches_ = []
    self.tokens_         = []

    cmd = "cd %s && git show-ref %s" % (self.root_, self.br_)
    outerr, errCode = myCommand_fast( cmd )
    if errCode != 0:
      return

    for line in outerr.splitlines():
      hash, ref = line.split( ' ' )
      if ref.find( 'refs/tags/' ) == 0:
        continue
      if ref.find( 'refs/heads/' ) == 0:
        if is_valid_swgit_branch( ref ):
          self.local_matches_.append( ref )
      if ref.find( 'refs/remotes/' ) == 0:
        if is_valid_swgit_branch( ref ):
          self.remote_matches_.append( ref )

    # 1. high priority to local branches
    if len( self.local_matches_ ) == 0 and len( self.remote_matches_ ) == 0:
      return

    if len( self.local_matches_ ) == 1:
      self.isValid_ = True
      self.fullRef_ = self.local_matches_[0]
      self.matches_ = self.local_matches_
      self.tokens_  = self.fullRef_.split("/")
      self.tokens_.insert( 1, "dummyremotes" )
      return 

    if len( self.local_matches_ ) > 1:
      self.matches_ = self.local_matches_
      return 

    # 2. lower priority to remotes branches
    if len( self.remote_matches_ ) == 1:
      self.isValid_ = True
      self.fullRef_ = self.remote_matches_[0]
      self.matches_ = self.remote_matches_
      self.tokens_  = self.fullRef_.split("/")
      return 

    if len( self.remote_matches_ ) > 1:
      self.matches_ = self.remote_matches_
      return 


  def __str__( self ):
    #return "val[%s] rem[%s] rel[%s] usr[%s] t[%s] n[%s]\nmatches   %s\nloc_match %s\nrem_match %s" % \
    #    (self.isValid(),self.getRepo(),self.getRel(), self.getUser(), self.getType(), self.getName(), 
    #        self.getMatches(), self.local_matches_, self.remote_matches_)
    return "isval[%s] rem[%s] rel[%s] usr[%s] t[%s] n[%s]" % \
        (self.isValid(),self.getRepo(),self.getRel(), self.getUser(), self.getType(), self.getName())
  
  def dump( self ):
    ret = ""
    ret += "  getFullRef:     [" + self.getFullRef() + "]\n"
    ret += "  isValid:        [" + str( self.isValid() ) + "]\n"
    if not self.isValid():
      ret += "  notValidReason: [" + self.getNotValidReason() + "]\n"
    ret += "  matches:        [" + "\n".join( self.getMatches() ) + "]\n"
    ret += "  L matches:      [" + "\n".join( self.getLocalMatches() ) + "]\n"
    ret += "  R matches:      [" + "\n".join( self.getRemoteMatches() ) + "]\n"
    ret += "  getRepo:        [" + self.getRepo() + "]\n"
    ret += "  getRel:         [" + self.getRel() + "]\n"
    ret += "  getUser:        [" + self.getUser() + "]\n"
    ret += "  getType:        [" + self.getType() + "]\n"
    ret += "  getName:        [" + self.getName() + "]\n"
    ret += "  getShortRef:    [" + self.getShortRef() + "]\n"
    ret += "  to_remote:      [" + self.branch_to_remote()[0] + "]\n"
    return ret

  def isValid( self ):
    return self.isValid_

  def getNotValidReason( self ):
    if len( self.getMatches() ) > 0:
      strerr  = "Multiple matches found, please specify one among:\n"
      for b in self.getMatches():
        strerr += "  %s\n" % b[ findnth( b, "/", 2 ) + 1 : ]
      return strerr
    else:
      return "Branch %s does not exists" % self.br_

  def getMatches( self ):
    return self.matches_

  def getLocalMatches( self ):
    return self.local_matches_
  def getRemoteMatches( self ):
    return self.remote_matches_

  def is_local_br( self ):
    if self.isValid() and self.getRepo() == "heads":
      return True
    return False

  def is_remote_br( self ):
    if self.isValid() and self.getRepo() != "heads":
      return True
    return False

  #not so useful, for symmetry
  def exist_local( self ):
    if not self.isValid():
      return False
    if self.is_local_br():
      return True
    return False

  def exist_remote( self ):
    if not self.isValid():
      return False
    if self.is_remote_br():
      return True
    
    err, rem_list = Branch.list_remote_br( "*", self.getRel(), self.getUser(), self.getType(), self.getName() )
    if len( rem_list ) > 0:
      return True
    return False

  def get_track_info( self ):

    retobj = { Branch.TRACK_MERGE : "Not valid branch", Branch.TRACK_REMOTE : "Not valid branch" }
    if not self.isValid():
      return retobj, False

    cmd_tracked = "git config --get branch.%s.merge && git config --get branch.%s.remote " % ( self.getShortRef(), self.getShortRef() )
    outerr, errCode = myCommand_fast( cmd_tracked )
    if errCode != 0:
      retobj[Branch.TRACK_MERGE] = outerr[:-1]
      retobj[Branch.TRACK_REMOTE] = outerr[:-1]
      return retobj, False

    retobj[Branch.TRACK_MERGE] = outerr.splitlines()[0]
    retobj[Branch.TRACK_REMOTE] = outerr.splitlines()[1]
    return retobj, True


  def branch_to_remote_obj( self ):
    br_repo, br_repo_errcode = self.branch_to_remote()
    if br_repo_errcode != 0:
      return NullBranch( br_repo )

    fullname = "%s/%s" % ( br_repo, self.getShortRef() ) 
    return Branch( fullname )


  def branch_to_remote( self ):
    if len( self.matches_ ) == 0:
      return "Not a valid branch %s" % self.br_, 1

    if self.is_remote_br():
      return self.getRepo(), 0

    #local br, look for remote
    if len( self.remote_matches_ ) == 1:
      r = self.remote_matches_[0]
      repo = r[ rfindnth( r, '/', 8 ) + 1 : rfindnth( r, '/', 7 ) ]
      return repo, 0

    #local => look for tracked
    repo, errCode = get_repo_cfg( GITCFG_BRANCH_REMOTE_TEMPLATE % self.getShortRef() )
    if errCode == 0:
      return repo[:-1], 0

    if len( self.local_matches_ ) > 1:
      return "More than one alternative for branch name '%s'" % self.br_, 1
    if len( self.remote_matches_ ) > 1:
      return "More than one alternative for branch name '%s'" % self.br_, 1

    if len( self.remote_matches_ ) == 0:
      return "No remote branch found for branch name '%s'" % self.br_, 1

    return "Not forseen case for branch '%s'" % self.br_, 1

  def getTokens( self ):
    return self.tokens_

  def getFullRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.fullRef_

  def getRepo( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[2]

  def getRel( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "/".join( self.tokens_[3:7] )

  def getUser( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[7]

  def getType( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[8]

  def getName( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[9]

  def getShortRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "/".join( self.tokens_[3:] )

  def getNewBrRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "%s/%s/%s" % (self.getShortRef(), SWCFG_TAG_NEW, SWCFG_TAG_NEW_NAME)

  def getRemoteRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "%s/%s" % (self.getRepo(), self.getShortRef() )

  def isDevelop( self ):
    if not self.isValid_:
      return False

    genericDevelop = re.compile('/INT/.*develop$')
    matches = genericDevelop.findall( self.getShortRef() )
    if len( matches ) > 0:
      return True

    return False

  def isStable( self ):
    if not self.isValid_:
      return False

    genericStable = re.compile('/INT/.*stable$')
    matches = genericStable.findall( self.getShortRef() )
    if len( matches ) > 0:
      return True
    return False

  @staticmethod
  def list( repo="*", rel="*/*/*/*", user="*", typeB="*", nameB="*" ):

    total=[]
    heads=[]

    if repo == "heads":
      return Branch.list_local_br( rel, user, typeB, nameB )

    if repo != "*":
      return Branch.list_remote_br( repo, rel, user, typeB, nameB )

    total  = Branch.list_local_br( rel, user, typeB, nameB )[1]
    total += Branch.list_remote_br( repo, rel, user, typeB, nameB )[1]

    return 0, total


  @staticmethod
  def list_local_br( rel="*/*/*/*", user="*", typeB="*", nameB="*" ):
    cmd="git for-each-ref --format='%%(refname:short)' refs/heads/%s/%s/%s/%s" % (rel,user,typeB,nameB)
    out, errCode = myCommand_fast( cmd )
    if errCode !=0:
      return errCode, []
    return 0, out.splitlines()

  @staticmethod
  def list_remote_br( repo = "*", rel="*/*/*/*", user="*", typeB="*", nameB="*" ):
    cmd="git for-each-ref --format='%%(refname:short)' refs/remotes/%s/%s/%s/%s/%s" % (repo,rel,user,typeB,nameB)
    out, errCode = myCommand_fast( cmd )
    if errCode !=0:
      return errCode, []
    return 0, out.splitlines()
    

  @staticmethod
  def getCurrBr( root = "."):
    outerr, errCode = myCommand_fast( "cd %s; git symbolic-ref -q HEAD" % root )
    if errCode != 0:
      #print "  Attention, you are in detached HEAD"
      return NullBranch( "You are in detached head" )
    ref = outerr[:-1]
    #format: refs/heads/... remove this
    ref = ref [ findnth( ref, "/", 2 ) + 1 : ]
    return Branch( ref, root )
    #return Branch( outerr[:-1], root )


  @staticmethod
  def getIntBr( dir = "." ):
    str, errCode = get_repo_cfg( SWCFG_INTBR, dir )
    if errCode == 0:
      return Branch(str[:-1], dir )
    else:
      return NullBranch( str )

  @staticmethod
  def getStableBr():
    ib = Branch.getIntBr()

    if not ib.isValid():
      return NullBranch( ib.getNotValidReason() )
    
    if not ib.isDevelop():
      return NullBranch( "Integration branch is not 'develop', no 'stable' exists." )

    devFullName = ib.getShortRef()
    sbBase = devFullName[ 0 : devFullName.rfind( "/" ) ]
    sbName = devFullName[ devFullName.rfind( "/" ) + 1 : ]

    sbName = sbName.replace( "develop", "stable" )
    sb = Branch( sbBase + "/" + sbName )
    return sb

       #startb.getType() == SWCFG_BR_INT or \
  @staticmethod
  def is_side_operation( startb, ib, sb ):
    #if startb.getShortRef() == ib.getShortRef() or \
    #   startb.getShortRef() == sb.getShortRef() or \
    #   startb.getType() == SWCFG_BR_CST:
    #     return False

    brtype = startb.getType()
    if brtype == SWCFG_BR_INT or brtype == SWCFG_BR_CST:
         return False

    if startb.getShortRef() == ib.getShortRef():
         return False

    return True



class NullBranch( Branch ):
  def __init__( self, errorReason = "" ):
    self.br_       = ""
    self.root_     = ""
    self.fullRef_  = ""
    self.errReason_ = ""
    self.isValid_  = False
    self.matches_  = []

  def __str__( self ):
    return "NullBranch"

  def getShortRef( self ):
    return ""

  def getNotValidReason( self ):
    return self.errReason_



def main():
  print "\nTesting Branch class with ref: " + sys.argv[1] + "\n"
  b = Branch( sys.argv[1] )
  print "  getTokens:          [" + " ".join( b.getTokens() ) + "]\n"
  print "  getFullRef:         [" + b.getFullRef() + "]\n"

  print "  isValid:            [" + str( b.isValid() ) + "]\n"
  if not b.isValid():
    print "  notvalidReason:     [" + b.getNotValidReason() + "]\n"
  print "  matches:            [" + " ".join( b.getMatches() ) + "]\n"
  print "  local  matches:     [" + " ".join( b.getLocalMatches() ) + "]\n"
  print "  remote matches:     [" + " ".join( b.getRemoteMatches() ) + "]\n"

  print "  getRepo:            [" + b.getRepo() + "]\n"
  print "  getRel:             [" + b.getRel() + "]\n"
  print "  getUser:            [" + b.getUser() + "]\n"
  print "  getType:            [" + b.getType() + "]\n"
  print "  getName:            [" + b.getName() + "]\n"
  print "  getShortRef:        [" + b.getShortRef() + "]\n"
  print "  getNewBrRef:        [" + b.getNewBrRef() + "]\n"
  print "  getRemoteRef:       [" + b.getRemoteRef() + "]\n"
  print "  getCurrBr fullref:  [" + Branch.getCurrBr().getFullRef() + "]\n"
  print "{",b,"}"
  print ""
  print "  int branch: {",Branch.getIntBr(),"}"
  print "  stb branch: {",Branch.getStableBr(),"}"
  print "  branch_to_remote --> ((",b.branch_to_remote()[0],"))"


if __name__ == "__main__":
    main()




