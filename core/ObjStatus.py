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

from ObjEnv import * 
from Utils_Submod import * 

class Status:
  def __init__( self):
    pass

  def __str__( self ):
    out=""
    for type in self.getFile():
      if len(type) > 0:
        out=out + "\n"+"".join(type) 
    
    return out
    
  @staticmethod
  def getFile( root = ".", ignoreSubmod = False ):
    # use poll instead of wait when long output can be genearetd. 
    #  In those cases this happen:
    #  1. command generates great output
    #  2. no one consumes it
    #  3. wait blocks untils command ends but it cannot because queue if full.
    opt_smod = ""
    if ignoreSubmod == True:
      opt_smod = " --ignore-submodules "

    cmd = "cd %s && git status -s %s" % (root,opt_smod)
    outerr, errCode = myCommand_fast_nojoin( cmd )

    #outerr = out.splitlines()

    #when removing repo with rm, submod_list_repos does not list it
    #repolist =  submod_list_repos( firstLev = True, excludeRoot = True, localpaths = True )
    repolist =  submod_list_all_default( root )
    #print "curr subrepo %s" % repolist

    fileUU=[]
    fileBO=[]
    fileChanged=[]
    fileToCommit=[]
    fileRM=[]

    modUU=[]
    modBO=[]
    modChanged=[]
    modToCommit=[]
    modRM=[]

    for line in outerr:
      type = line[0:2]
      file = line[3:-1]

      mod = False
      if file in repolist:
        mod = True

      if type[1:] == "D" :
        if not mod:
          fileRM.append(file)
        else:
          modRM.append( file )
      # opzione a sinistra e destra vuoto ok
      if type in ("M ","A ","AM","R ","C ","D ") :
        if not mod:
          fileToCommit.append( file )
        else:
          modToCommit.append( file )
      elif type in ("DD","AA","UU","AU","UD","UA","DU") :
        if not mod:
          fileUU.append( file )
        else:
          modUU.append( file )
      elif type.count("M") > 0 or type.count("D") > 0:
        if not mod:
          fileChanged.append( file )
        else:
          modChanged.append( file )
      else :
        if not mod:
          fileBO.append( file )
        else:
          modBO.append( file )

    return fileUU,fileChanged,fileToCommit,fileBO,fileRM,\
           modUU,modChanged,modToCommit,modBO,modRM


  @staticmethod
  def getFileConflict():
    fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile()
    return fileUU

  @staticmethod
  def getFileToCommit( root = ".", ignoreSubmod = False ):
    fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile( root, ignoreSubmod )
    return fileToCommit

  @staticmethod
  def getFileChanged():
    fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile()
    return fileChanged

  @staticmethod
  def getFileUntracked():
    fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile()
    return fileBO

  @staticmethod
  def getFileRM():
    fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile()
    return fileRM


  @staticmethod
  def isDirtyWD( root = ".", ignoreSubmod = False ):
    fileUU,fileChanged,fileToCommit,fileBO,fileRM,\
        modUU,modChanged,modToCommit,modBO,modRM = \
          Status.getFile( root, ignoreSubmod )
    
    if len(fileUU) > 0:
      errstr = "Conflicted file(s) detected. Please procede in this way:\n\tResolve conflicts\n\tswgit add resolved files\n\tswgit commit\n\t\t"
      errstr = errstr + "\t\t".join( fileUU )
      return 1, errstr
      
    if len( fileChanged ) > 0:
      errstr  = "Locally modified file(s) detected. Please procede in this way:\n"
      errstr += "\tswgit stash\n"
      errstr += "\tor\n"
      errstr += "\tswgit commit -a\n\t\t"
      errstr = errstr + "\n\t\t".join( fileChanged )
      return 1, errstr

    if len( fileToCommit ) > 0:
      errstr = "New file(s) not commited detected. Please procede in this way:\n\tswgit Commit\n\t\t"
      errstr = errstr + "\n\t\t".join( fileToCommit )
      return 1, errstr

    if len(modUU) > 0:
      errstr = "Conflicted repository(ies) detected. Please procede in this way:\n\tResolve conflicts\n\tswgit add resolved repositories\n\tswgit commit\n\t\t"
      errstr = errstr + "\t\t".join( modUU )
      return 1, errstr
      
    if len( modChanged ) > 0:
      errstr = "Locally modified repository(ies) detected. Please procede in this way:\n\tswgit commit -a\n\t\t"
      errstr = errstr + "\n\t\t".join( modChanged )
      return 1, errstr

    if len( modToCommit ) > 0:
      errstr = "New repository(ies) not commited detected. Please procede in this way:\n\tswgit commit\n\t\t"
      errstr = errstr + "\n\t\t".join( modToCommit )
      return 1, errstr

    if Status.pendingMerge( root ):
      errstr = "Merge not yet finished. Please commit inside %s them to resolve pending merge." % root
      return 1, errstr

    return 0,""

  @staticmethod
  def pendingMerge( dir = "." ):
    myRepo = Env.getLocalRoot( dir )
    if os.path.exists("%s/%s" % (myRepo, SWFILE_MERGEHEAD)) == True:
      return True
    return False

  @staticmethod
  def pendingMerge_rec( root = "." ):
    #inside repo
    root = Env.getLocalRoot( root )

    for d in submod_list_repos( root ):
      if Status.pendingMerge( d ):
        return True, "Merge not finished inside repository %s" % ( d )

    return False, ""


  @staticmethod
  def checkLocalStatus( root = ".", ignoreSubmod = False ):
    #inside repo
    root = Env.getLocalRoot( root )

    #not in detached HEAD
    #outerr, errCode = myCommand_fast( "cd %s && git symbolic-ref -q HEAD" % root )
    #if errCode != 0:
    #  print "Attention, you are in detached HEAD. swgit tools do not support this state\n"
    #  sys.exit(1)

    #dirty Working Dir
    return Status.isDirtyWD( root, ignoreSubmod )


  @staticmethod
  def checkLocalStatus_rec( root = ".", ignoreSubmod = False ):
    #inside repo
    root = Env.getLocalRoot( root )

    for d in submod_list_repos( root ):
      ret, errstr = Status.checkLocalStatus( d, ignoreSubmod )
      if ret != 0:
        return ret, "Error inside repository %s\n%s" % ( d, errstr )

    return 0, ""

    
def main():

  for b in [ 1, 2 ]:
    if b == 1:
      print "%s\nIncluding submodules:\n%s" % (("#"*20),("#"*20))
      fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile( os.getcwd(), ignoreSubmod = False )
    else:
      print "%s\nIgnoring submodules:\n%s" % (("#"*20),("#"*20))
      fileUU,fileChanged,fileToCommit,fileBO,fileRM,modUU,modChanged,modToCommit,modBO,modRM = Status.getFile( os.getcwd(), ignoreSubmod = True )

    print "File with conflicts..."
    print "\t"+"\n\t".join( fileUU ) + "\n"
    
    print "File Changes to be committed..."
    print "\t"+"\n\t".join( fileToCommit ) + "\n"

    print "File Changed but not updated..."
    print "\t"+"\n\t".join( fileChanged ) + "\n"
    
    print "File Untracked files..."
    print "\t"+"\n\t".join( fileBO ) + "\n"

    print "File Removed files..."
    print "\t"+"\n\t".join( fileRM ) + "\n"

    print "Mod with conflicts..."
    print "\t"+"\n\t".join( modUU ) + "\n"
    
    print "Mod Changes to be committed..."
    print "\t"+"\n\t".join( modToCommit ) + "\n"

    print "Mod Changed but not updated..."
    print "\t"+"\n\t".join( modChanged ) + "\n"
    
    print "Mod Untracked mods..."
    print "\t"+"\n\t".join( modBO ) + "\n"

    print "Mod Removed mods..."
    print "\t"+"\n\t".join( modRM ) + "\n"


  print "%s\nStatus.checkLocalStatus_rec( ignoreSubmod = False )" % ("-"*50)
  ret, out = Status.checkLocalStatus_rec( Env.getLocalRoot(), ignoreSubmod = False )
  print ret
  print out
  print "%s\nStatus.checkLocalStatus_rec( ignoreSubmod = True )" % ("-"*50)
  ret, out = Status.checkLocalStatus_rec( Env.getLocalRoot(), ignoreSubmod = True )
  print ret
  print out

if __name__ == "__main__":
    main()

