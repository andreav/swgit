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
from ObjBranch import *
from ObjTag import *
from ObjProj import *


# useful in detached head to eval on which branch we are
# and retrieve infos like rel or user or others
def eval_curr_branch_shortref( ref ):
  if ref == "HEAD":
    cb = Branch.getCurrBr()
    if cb.isValid() == True:
      return cb.getShortRef(), ""

  br = Branch( ref )
  if br.isValid() == True:
    return br.getShortRef(), ""

  tag = Tag( ref )
  if tag.isValid() == True:
    return tag.getBrStr(), ""

  currRel = "0/0/0/0"
  # must create a valid ref because
  #  0/0/0/0 creates probelms during getCurrBr() everywhere in the scripts
  cmd_describe = "git describe --contains --all %s " % ( ref ) 
  out,errCode = myCommand( cmd_describe )
  if errCode != 0:
    strerr  = "Not found any reference containing '%s'\n" % ref
    strerr += "Maybe you have to create an INT branch with swgit init"
    return "", strerr

  downstream_ref = trunch_describe_output( out[:-1] )
  if downstream_ref.find( SWCFG_TAG_NAMESPACE_PAST ) == 0:
    downstream_ref = downstream_ref[ len( SWCFG_TAG_NAMESPACE_PAST ) + 1 : ]

  dw_br = Branch( downstream_ref )
  dw_tag = Tag( downstream_ref )
  if dw_br.isValid():
    return dw_br.getShortRef(), ""
  elif dw_tag.isValid():
    return dw_tag.getBrStr(), ""
  else:
    return "", "Found a reference containing '%s', but not a valid swgit reference (%s)." % (ref, downstream_ref)

  return "",  "Cannot process reference '%s'" % ref


def find_describe_label( pattern, startpoint="HEAD", nolog=False):
    cmd = "git describe %s --tags --long --match %s" % (startpoint, pattern)

    if nolog:
      out,errCode = myCommand_fast( cmd )
    else:
      out,errCode = myCommand( cmd )
    
    if errCode != 0 :
      return errCode, "", ""

    dev = out.splitlines()[0] # take first result
    dev = dev[ 0 : dev.rfind('-') ]
    num = dev[ dev.rfind('-')+1 : ] # take distance of HEAD, must be 0
    dev = dev[ 0 : dev.rfind('-') ]
    return 0, dev, num


def describeCurrentSha():
  header = ""
  out, errCode = myCommand_fast( "git rev-parse --short HEAD; git rev-parse --abbrev-ref HEAD" )
  
  out = out.splitlines()

  header += "currSha:(%s) " % out[0]
  header += "currBra:(%s) " % out[1]
  return header


def myCommand( cmd, lvl=GLog.I):

  beforeInfo = describeCurrentSha()

  out, retcode = myCommand_fast( cmd )

  afterInfo = describeCurrentSha()

  GLog.f( lvl, "\n\nbefore: %s\n\ncommand: %s\n\noutput:\n%s\n\nAfter: %s\n\n%s\n" % ( beforeInfo, cmd, out, afterInfo, "#"*50 ) )
  return ( out, retcode )


def mySSHCommand( cmd, user, address, lvl=GLog.I):
  beforeInfo = describeCurrentSha()

  out, retcode = mySSHCommand_fast( cmd, user, address )

  afterInfo = describeCurrentSha()

  GLog.f( lvl, "\n\nbefore: %s\n\ncommand: %s\n\noutput:\n%s\n\nAfter: %s\n\n%s\n" % ( beforeInfo, cmd, out, afterInfo, "#"*50 ) )
  return ( out, retcode )


def dumpRepoName( default="" ):

  repo = create_swrepo()
  mysectObj = repo.getMySectionObj()

  if mysectObj != None:
    return mysectObj[MAP_LOCALPATH] 

  return os.path.basename( Env.getLocalRoot() )
  #return default



def info_eval_anylog( upstreamRef, downstreamRef, rel, typeTag ):
  cmd_grep_myrel = "grep -e \"^%s/\"" % rel
  cmd_grepaway_tagtype = "grep -e \"^[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/%s/[^/]\+$\"" % typeTag
  cmd_grepaway_rembranches = "grep -v -e \"^[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+$\""
  cmd_grepaway_localbranches = "grep -v -e \"^[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+/[^/]\+$\""
  cmd_sed = "sed -e 's/tag://g' -e 's/ //g' -e 's/(//g' -e 's/)//g' -e '/^$/d' -e 's/,/\\n/g'"
  cmd_find_devs_one_per_line = "git log --format='%%d' %s --not %s | %s | %s | %s | %s | %s" % \
      ( downstreamRef, upstreamRef, cmd_sed, cmd_grepaway_localbranches, cmd_grepaway_rembranches, cmd_grepaway_tagtype, cmd_grep_myrel )

  out, errCode = myCommand( cmd_find_devs_one_per_line )
  if errCode != 0 and len( out ) == 0:
    return 0, "" #no match
  if errCode != 0:
    return errCode, out
  return 0, out

def eval_default_remote_name():
  remotes = Remote.get_remote_list()
  remote_name = ""

  if len( remotes ) == 0:
    return remote_name
  elif len( remotes ) == 1:
    remote_name = remotes[0]
  else:
    cb = Branch.getCurrBr()
    br_repo, errCode = cb.branch_to_remote()
    if errCode == 0:
      remote_name = br_repo
    else: #maybe only local branch
      if SWNAME_ORIGIN_REMOTE in remotes: #more prio to origin
        remote_name = SWNAME_ORIGIN_REMOTE
      else: #else choose first
        remote_name = remotes[0]

  return remote_name


def main():
  print "\nTesting Utils\n"
  remotes = Remote.get_remote_list()
  print "remotes: [%s]\n" % "] [".join( remotes )
  def_remote_name = eval_default_remote_name()
  print "default remote: [%s]\n" % def_remote_name
  objRem = create_remote( def_remote_name )
  print objRem
  print "curr branch:\n"
  print eval_curr_branch_shortref( "HEAD" )

if __name__ == "__main__":
    main()
