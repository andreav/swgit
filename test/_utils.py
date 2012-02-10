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

from defines import *
from util_prepare_sandbox import *
import os,sys,pwd

def url_parse( url ):
  # user
  # address
  # root
  if url.find("@") == -1:
    return { "USER" : "",
             "ADDR" : "",
             "ROOT" : url
             }

  return { "USER" : url[6:url.find("@")],
           "ADDR" : url[url.find("@")+1:url.find("/",6)],
           "ROOT" : url[url.find("/",6):]
           }

def plat_name2path( name ):
  if name == "DEVFS":  return "TEST_PROJ_REPO_FS"
  if name == "DEVAPP": return "TEST_PROJ_REPO_APP"
  if name == "SNAP":   return "SNAPSHOT"
  return "NOTFOUND"

def tss100_name2path( name ):
  if name == "DEVTDM":  return "TEST_PROJ_REPO_TDM"
  if name == "DEVPLAT": return "DEV/TEST_PROJ_REPO_PLAT"
  if name == "CSTPLAT": return "CST/TEST_PROJ_REPO_PLAT"
  if name == "CSTTDM":  return "CST-TEST_PROJ_REPO_TDM"
  if name == "DEVFS":   return "DEV/TEST_PROJ_REPO_PLAT/TEST_PROJ_REPO_FS"
  if name == "DEVAPP":  return "DEV/TEST_PROJ_REPO_PLAT/TEST_PROJ_REPO_APP"
  if name == "CSTFS":   return "CST/TEST_PROJ_REPO_PLAT/TEST_PROJ_REPO_FS"
  if name == "CSTAPP":  return "CST/TEST_PROJ_REPO_PLAT/TEST_PROJ_REPO_APP"
  return "NOTFOUND"

def tss100_name2file( name ):
  if name == "TSS100":  return "tss100.txt"
  if name == "DEVTDM":  return "tdm.txt"
  if name == "DEVPLAT": return "plat.txt"
  if name == "CSTPLAT": return "plat.txt"
  if name == "CSTTDM":  return "tdm.txt"
  if name == "DEVFS":   return "fs.txt"
  if name == "DEVAPP":  return "app.txt"
  if name == "CSTFS":   return "fs.txt"
  if name == "CSTAPP":  return "app.txt"
  return "NOTFOUND"



#
# TEST dir layout:
# 
#   test/all_tests_runner.py
#   test/test_*.py
#   test/SANDBOX/
#   test/SANDBOX/TEST_ORIG_REPO         # is the repo from with to clone for every test
#   test/SANDBOX/TEST_A_CLONE
#


def print_defines():
  print ""
  print "GIT_VERSION              " + GIT_VERSION
  print "GIT_VERSION_SUBMODCHANGE " + GIT_VERSION_SUBMODCHANGE
  print ""
  print "TESTDIR             " + TESTDIR
  print "REPOS_DIR           " + REPOS_DIR
  print "SANDBOX             " + SANDBOX
  print "LOGS_DIR            " + LOGS_DIR
  print "LOGS_FILE           " + LOGS_FILE
  print "DEBUG               " + str( DEBUG )
  print ""
  print "ORIG_REPO_DIR          " + ORIG_REPO_DIR
  print "ORIG_REPO_NAME         " + ORIG_REPO_NAME
  print "ORIG_REPO_NAME_SHARED  " + ORIG_REPO_NAME_SHARED
  print "ORIG_REPO_NAME_AREMOTE " + ORIG_REPO_NAME_AREMOTE
  print "ORIG_REPO_SSHUSER      " + ORIG_REPO_SSHUSER
  print "ORIG_REPO_GITUSER      " + ORIG_REPO_GITUSER
  print "ORIG_REPO_ADDR         " + ORIG_REPO_ADDR
  print "ORIG_REPO_aFILE        " + ORIG_REPO_aFILE
  print "ORIG_REPO_URL          " + ORIG_REPO_URL
  print ""
  print "ORIG_REPO_REL           " + ORIG_REPO_REL
  print "ORIG_REPO_SUBREL        " + ORIG_REPO_SUBREL
  print "ORIG_REPO_DEVEL_BRANCH  " + ORIG_REPO_DEVEL_BRANCH
  print "ORIG_REPO_STABLE_BRANCH " + ORIG_REPO_STABLE_BRANCH
  print "ORIG_REPO_SLAVE_BRANCH  " + ORIG_REPO_SLAVE_BRANCH
  print ""
  print "TEST_USER           " + TEST_USER
  print "TEST_USER_SSH       " + TEST_USER_SSH
  print "TEST_ADDR           " + TEST_ADDR
  print ""
  print "TEST_ORIG_REPO         " + TEST_ORIG_REPO
  print "TEST_REPO              " + TEST_REPO
  print "TEST_REPO_R            " + TEST_REPO_R  
  print "TEST_REPO_S            " + TEST_REPO_S  
  print "TEST_REPO_LIV          " + TEST_REPO_LIV
  print "TEST_REPO_BR_DEV       " + TEST_REPO_BR_DEV
  print "TEST_REPO_BR_STB       " + TEST_REPO_BR_STB
  print "TEST_REPO_BR_SLA       " + TEST_REPO_BR_SLA
  print "TEST_REPO_CHK_LIV      " + TEST_REPO_CHK_LIV
  print "TEST_REPO_TAG_STB_DEV  " + TEST_REPO_TAG_STB_DEV
  print "TEST_REPO_TAG_STB_STB  " + TEST_REPO_TAG_STB_STB
  print "TEST_REPO_TAG_LIV      " + TEST_REPO_TAG_LIV    
  print "TEST_REPO_FILE_A       " + TEST_REPO_FILE_A     
  print "TEST_REPO_FILE_B       " + TEST_REPO_FILE_B     
  
  print "\nCUSTOM TAG NUMERICAL:\n"
  pprint( CUSTTAG_NUM )
  print "\nCUSTOM TAG WITH USERDEF NAME:\n"
  pprint( CUSTTAG_NAME )
  
  
  print ""
  print "REPO_A_DIRNAME  "  + REPO_A_DIRNAME
  print "REPO_B_DIRNAME  "  + REPO_B_DIRNAME
  print "REPO_C_DIRNAME  "  + REPO_C_DIRNAME
  print "REPO_A          "  + REPO_A
  print "REPO_B          "  + REPO_B
  print "REPO_C          "  + REPO_C
  
  for i,v in enumerate( REPOS_INFOS ):
    print "REPOS_INFOS[%s]  %s" % ( i, v )
  str_mapinfos = ""
  for i,values in enumerate( MAP_INFOS ):
    str_mapinfos += "MAP_INFOS[%s]    " % i
    for pos, val in enumerate(values):
      if pos == 0:
        str_mapinfos += val + "\n"
      else:
        str_mapinfos += " "*16 + str(val) + "\n"
  print str_mapinfos
  
  print "LABEL_CHK_A     "      + LABEL_CHK_A
  print "LABEL_CHK_B     "      + LABEL_CHK_B
  print "LABEL_CHK_C     "      + LABEL_CHK_C
  print "CST_BRANCH_NAME "      + CST_BRANCH_NAME
  print "CST_BRANCH_REL "       + CST_BRANCH_REL
  print "CST_BRANCH_FULLNAME "  + CST_BRANCH_FULLNAME
  
  print ""
  
  print "REPO_FS__NAME     " + REPO_FS__NAME     
  print "REPO_APP__NAME    " + REPO_APP__NAME    
  print "REPO_PLAT__NAME   " + REPO_PLAT__NAME   
  print "REPO_TSS100__NAME " + REPO_TSS100__NAME 
  print "REPO_TDM__NAME    " + REPO_TDM__NAME    
  
  print "REPO_FS__ORI_DIR     " + REPO_FS__ORI_DIR     
  print "REPO_APP__ORI_DIR    " + REPO_APP__ORI_DIR    
  print "REPO_PLAT__ORI_DIR   " + REPO_PLAT__ORI_DIR   
  print "REPO_TSS100__ORI_DIR " + REPO_TSS100__ORI_DIR 
  print "REPO_TDM__ORI_DIR    " + REPO_TDM__ORI_DIR    
  
  print "REPO_FS__ORI_URL     " + REPO_FS__ORI_URL     
  print "REPO_APP__ORI_URL    " + REPO_APP__ORI_URL    
  print "REPO_PLAT__ORI_URL   " + REPO_PLAT__ORI_URL   
  print "REPO_TSS100__ORI_URL " + REPO_TSS100__ORI_URL 
  print "REPO_TDM__ORI_URL    " + REPO_TDM__ORI_URL    
  
  pprint( REPO_FS__INFOS )
  pprint(  REPO_APP__INFOS )
  pprint(  REPO_PLAT__INFOS )
  pprint(  REPO_TSS100__INFOS )
  pprint(  REPO_TDM__INFOS )
  
  print ""
  print "PROJ_PLAT_DESCRIPTION: "
  pprint( PROJ_PLAT_DESCRIPTION )
  print ""
  print "PROJ_TSS100_DESCRIPTION: "
  pprint( PROJ_TSS100_DESCRIPTION )
  
  
  
  print """
  
      PLAT --------.
       |  \         \      
    DEVFS  DEVAPP   (SNAP)
  
  
    TSS100---.---------------.---------------.                            
     |        \               \               \                             
    DEVTDM    DEVPLAT        CSTPLAT       CSTTDM                               
                |  \           |  \                             
             DEVFS DEVAPP   CSTFS CSTAPP                         
  
  """
  
  print "\n"


def myCommand( cmd ):
  log( cmd )

  out, errCode = myCommand_fast( cmd )

  log( out )

  return ( out, errCode )


def initlogs( fname ):
  global g_flog
  if not os.path.exists( LOGS_DIR ):
    os.mkdir( LOGS_DIR )
    os.system( "chmod 777 %s 2>&1 1>/dev/null" % LOGS_DIR )
  g_flog = open( "%s/%s" % ( LOGS_DIR, fname ),'w')


def manage_debug_opt ( script_argv ):
  for i,v in enumerate( script_argv ):
    if v == "--debug":
      debug()
      del sys.argv[i]

def debug ( val = True ):
  global DEBUG
  DEBUG = True


initonce = 0
def log ( msg ):
  global g_flog
  global initonce
  date = datetime.now()

  if initonce == 0:
    if not os.path.exists( LOGS_DIR ):
      os.mkdir( LOGS_DIR )
      os.system( "chmod 777 %s 2>&1 1>/dev/null" % LOGS_DIR )
    g_flog = open( "%s/%s" % ( LOGS_DIR, LOGS_FILE ),'w')
    os.system( "chmod 777 %s/%s 2>&1 1>/dev/null" % ( LOGS_DIR, LOGS_FILE ) )
    initonce = 1
    
  print >>g_flog, date, " - ", msg
  #g_flog.write( "%s\n%s" (date, msg) )

  if DEBUG == True:
    print msg



####################################################
# this is the place where to put initializations....
####################################################

def setup_sandbox():
  recreate_sandbox()


def create_dir_some_file( dir, file = TEST_REPO_FILE_A ):
  recreate_dir( dir )
  cmd  = "echo \"content of: %s\" >> %s/%s;" % ( file, dir, file )
  return myCommand( cmd )



def echo_on_file( file, msg="aaa" ):
  cmd = "echo \"%s\" >> %s" % ( msg, file )
  return myCommand( cmd )



def findnth(allstr, ch, n):
  parts= allstr.split(ch, n)
  if len(parts)<=n:
      return -1
  return len(allstr)-len(parts[-1])-len(ch)
