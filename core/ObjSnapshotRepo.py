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

from ObjCfg import *
from ObjLog import *
import Utils
import Utils_Submod
import shutil

class ObjSnapshotRepo( ObjCfgSnap ):
  DEFAULT_SNAPSHOT_CFG = """\
#
# Inside this file user can provide sensible defaults for every 
#   shanpshot repository
#
# Please run
#   swgit --tutorial-snapshot
# for more informations
#
#[A-SNAP-REPO]
#URL     =
#BRANCH  =
#AR-TYPE = (tar or zip)
#AR-TOOL = (tar or unzip)
#
"""

  def __init__( self, reponame ):
    reponame = del_slash( reponame )
    super(ObjSnapshotRepo, self ).__init__( reponame )

    self.existRepo_errCode_ = 1
    self.existRepo_errStr_  = ""

    self.existRepo_errStr_,  self.existRepo_errCode_ = Utils_Submod.submod_check_hasrepo_configured( reponame )
    if self.existRepo_errCode_ != 0:
       return

    if reponame not in Utils_Submod.submod_list_snapshot():
      self.existRepo_errStr_ = "Repository %s is not a snapshot repo" % reponame
      return

    self.load_cfg()


  def dump( self ):
    retstr = "\n"
    if self.isValid_ == False:
      retstr += "INVALID "
    retstr += "Snapshot repo %s\n" % self.section_

    if self.existRepo_errCode_ != 0:
      retstr += self.existRepo_errStr_
    else:
      retstr += super(ObjSnapshotRepo, self ).dump()

    return retstr


  def pull_reference( self, proot, pref, rname ):

    # includes: 
    #  * does not exist 
    #  * bad configured
    #  * not a snapshot repo
    if self.isValid_ == False:
      return self.dump(), 1

    repover, errCode = Utils_Submod.submod_getrepover_atref( proot, rname, pref )
    if errCode != 0:
      return repover, errCode

    abs_repo_dir = "%s/%s" % (proot, rname)

    abs_currver_file = "%s/%s/%s" % (proot, rname, SWFILE_SNAPCFG_CURRVER)
    if os.path.exists( abs_currver_file  ) == True:
      cmd_get_curr_sha = "cat %s" % abs_currver_file
      out, errCode = Utils.myCommand( cmd_get_curr_sha )
      if errCode != 0:
        GLog.s( GLog.S, indentOutput( out[:-1], 1) )
        GLog.s( GLog.S, "FAILED" )
        return out, 1

      if out[:-1] == repover:
        GLog.s( GLog.S, "No need to upgrade snapshot repository \"%s\", right version already present." % ( rname ) )
        GLog.s( GLog.S, "DONE" )
        return "OK", 0



    GLog.s( GLog.S, "Updating snapshot repository %s to reference %s ... " % ( rname, repover ) )
    GLog.s( GLog.S, "\tCleaning current repository content" )

    shutil.rmtree( abs_repo_dir, True ) #ignore errors
    os.mkdir( abs_repo_dir )

    GLog.s( GLog.S, "\tGetting remote content ... " )

    GOT_FILE_NAME = SWFILE_SNAPCFG_GOTFNAME
    if self.get_format() == "tar":
      GOT_FILE_NAME += ".tar"
    else: #zip
      GOT_FILE_NAME += ".zip"

    dest_file = "%s/%s" % (rname, GOT_FILE_NAME)
    cmd_archive_get = "cd %s && git archive --remote %s -o %s --format %s %s" % ( proot, self.get_url(), dest_file, self.get_format(), repover )
    #print cmd_archive_get
    out, errCode = Utils.myCommand( cmd_archive_get )
    if errCode != 0:
      GLog.s( GLog.S, indentOutput( out[:-1], 1) )
      GLog.s( GLog.S, "FAILED" )
      return out, 1

    GLog.s( GLog.S, "\tExpanding content locally ... " )

    cmd_unrar = "cd %s && %s -x " % ( abs_repo_dir, self.get_bintar() )
    if self.get_format() == "tar":
      cmd_unrar += "-f "
    cmd_unrar += "./%s" % GOT_FILE_NAME
    #print cmd_unrar
    out, errCode = Utils.myCommand( cmd_unrar )
    if errCode != 0:
      GLog.s( GLog.S, indentOutput( out[:-1], 1) )
      GLog.s( GLog.S, "FAILED" )
      return out, 1

    cmd_mark_ver = "echo %s > %s" % ( repover, abs_currver_file )
    out, errCode = Utils.myCommand( cmd_mark_ver )
    if errCode != 0:
      GLog.s( GLog.S, indentOutput( out[:-1], 1) )
      GLog.s( GLog.S, "FAILED" )
      return out, 1

    os.remove( dest_file )

    GLog.s( GLog.S, "DONE" )

    return "OK", 0



def main():
  if len( sys.argv ) != 2:
    print "Usage: %s <snapshot dir>" % sys.argv[0]
    sys.exit(1)

  o = ObjSnapshotRepo( sys.argv[1] )

  print o.show_config_options()
  print ""
  print o.dump()
  print ""

  out, err = o.pull_reference( Env.getProjectRoot(), "HEAD", sys.argv[1] )
  print out, err


if __name__ == "__main__":
    main()

