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

import os, sys, pwd, time, re
import subprocess
import shutil
import socket
import copy
from datetime import datetime
from pprint import pprint


############################
# BASE UTILS
############################

GITCFG_USERNAME_test    = "user.name"
SWCFG_USER_REGEXP_test  = '^[a-zA-Z_]+$'

def myCommand_fast( cmd ):

  command = subprocess.Popen( cmd,
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                            )
  out = ""
  retcode = command.poll()
  out += "".join( command.stdout.readlines() )
  while ( retcode == None ):
    time.sleep(0.001)
    retcode = command.poll()
    out += "".join( command.stdout.readlines() )
  if retcode != 0:
    retcode = 1
  return ( out[:-1], retcode )

#  command = popen2.Popen4( cmd );
#
#  # use poll instead of wait when long output can be genearetd. 
#  #  In those cases this happen:
#  #  1. command generates great output
#  #  2. no one consumes it
#  #  3. wait blocks untils command ends but it cannot because queue if full.
#  out = ""
#  retcode = command.poll()
#  out += "".join( command.fromchild.readlines() )
#  while ( retcode == -1 ):
#    time.sleep(0.001)
#    retcode = command.poll()
#    out += "".join( command.fromchild.readlines() )
#
#  if retcode != 0:
#    return ( out[:-1], 1 )
#  return ( out[:-1], 0 )


def get_cfg( key, dir = ".", fglobal = False ):
  if os.path.exists( dir ) == False:
    return "Invalid path %s" % dir, 1

  optglob = ""
  if fglobal == True:
    optglob = " --global "

  cmd = "cd %s && git config --get %s %s" % ( dir, optglob, key )
  return myCommand_fast( cmd )

def set_cfg( key, value, dir = "." ):
  if os.path.exists( dir ) == False:
    return "Invalid path %s" % dir, 1

  if value == SWCFG_TEST_UNSET:
    cmd = "cd %s && git config --get %s && git config --unset %s || exit 0" % ( dir, key, key )
  else:
    cmd = "cd %s && git config %s %s" % ( dir, key, value )
  return myCommand_fast( cmd )


def getCurrUser( ):
  genericUserName = re.compile( SWCFG_USER_REGEXP_test )

  #DO NOT LOOK at local user.name
  #  because when creating test repositories, 
  #  this local configuration will not be present no more.
  #  Only global one will be considered 
  #  (This is pointed out only when global and local 
  #  settings are different)
  #
  #str, errCode = get_cfg( GITCFG_USERNAME_test )
  #if errCode == 0:
  #  un = str
  #  if len( genericUserName.findall( un ) ) > 0:
  #    return un

  str, errCode = get_cfg( GITCFG_USERNAME_test, fglobal = True )
  if errCode == 0:
    un = str
    if len( genericUserName.findall( un ) ) > 0:
      return un

  return pwd.getpwuid( os.getuid() )[0]



############################
# DEFINES
############################

GIT_VERSION              = map( int, myCommand_fast( "git --version | cut -d ' ' -f 3" )[0].split('.') )
# I do not know, i testes against this one, as perceived the difference (against 1.7.4.1)
GIT_VERSION_SUBMODCHANGE = [1,7,5,4]
GIT_VERSION_MERGE_CHANGE = [1,7,8,0]

FIX_MERGE_EDIT = ""
if GIT_VERSION >= GIT_VERSION_MERGE_CHANGE:
  FIX_MERGE_EDIT = "--no-edit"


TEST_USER          = getCurrUser()
TEST_USER_SSH      = pwd.getpwuid( os.getuid() )[0]
TEST_ADDR          = socket.gethostbyname_ex(socket.gethostname())[2][0]

TESTDIR        = os.path.dirname( os.path.abspath( __file__ ) ) + "/"
REPOS_DIR      = TESTDIR + "REPOS/"
SANDBOX        = TESTDIR + "SANDBOX/"
SANDBOX_777    = TESTDIR + "SANDBOX_777/"
SWENV_TESTMODE = "SWENV_TESTMODE"
SWENV_NONE     = "SWENV_NONE"
SWENV_MOREREMOTES = "SWENV_MOREREMOTES"
SWENV_LOCALREPOS = "SWENV_LOCALREPOS"
LOGS_DIR       = TESTDIR + "LOGS/"
LOGS_FILE      = "swgit_tests.log"
DEBUG          = False

SWREPO_DIR          = ".swdir/"
SWTAG_FILE          = SWREPO_DIR + "cfg/custom_tags.cfg"
SWSTABILIZE_MAILCFG = SWREPO_DIR + "cfg/mail.cfg"
SWSTABILIZE_FILE    = SWREPO_DIR + "cfg/generic.cfg"
SWCFG_TEST_UNSET    = "SWCFG_TEST_UNSET"


# Scripts repo (owner is root => 2/0/0/0./root/INT/...)
ORIG_REPO_DIR   = SANDBOX
ORIG_REPO_NAME  = "PROTOREPO"
ORIG_REPO_NAME_SHARED  = "%s_SHARED" % ORIG_REPO_NAME
AREMOTE_PATH    = "_AREMOTE"
ORIG_REPO_NAME_AREMOTE  = "%s%s" % (ORIG_REPO_NAME, AREMOTE_PATH)
ORIG_REPO_SSHUSER  = TEST_USER_SSH
ORIG_REPO_GITUSER  = "swgittestuser"
ORIG_REPO_aFILE = "b.txt"
ORIG_REPO_REL = "2/0"
ORIG_REPO_SUBREL = "0/0"
ORIG_REPO_ADDR = TEST_ADDR

REPO_SSHACCESS = "ssh://%s@%s" % ( ORIG_REPO_SSHUSER, ORIG_REPO_ADDR )
TESTER_SSHACCESS = "ssh://%s@%s" % ( TEST_USER_SSH, TEST_ADDR )
if os.environ.get( SWENV_TESTMODE ) == SWENV_LOCALREPOS:
  REPO_SSHACCESS = ""
  TESTER_SSHACCESS = ""

ORIG_REPO_URL           = "%s%s%s" % ( REPO_SSHACCESS, ORIG_REPO_DIR, ORIG_REPO_NAME )
ORIG_REPO_SHARED_URL    = "%s%s%s" % ( REPO_SSHACCESS, ORIG_REPO_DIR, ORIG_REPO_NAME_SHARED )
ORIG_REPO_AREMOTE_URL   = "%s%s%s" % ( REPO_SSHACCESS, ORIG_REPO_DIR, ORIG_REPO_NAME_AREMOTE )
ORIG_REPO_AREMOTE_NAME  = "aRemote"
ORIG_REPO_DEVEL_BRANCH  = "2/0/0/0/%s/INT/develop" % ORIG_REPO_GITUSER
ORIG_REPO_STABLE_BRANCH = "2/0/0/0/%s/INT/stable" % ORIG_REPO_GITUSER
ORIG_REPO_SLAVE_BRANCH  = "0/0/0/0/%s/INT/slave" % ORIG_REPO_GITUSER
ORIG_REPO_aBRANCH_NAME  = "aBranch"
ORIG_REPO_aBRANCH       = "2/0/0/0/%s/FTR/%s" % ( ORIG_REPO_GITUSER, ORIG_REPO_aBRANCH_NAME )
ORIG_REPO_aBRANCH_DEV0  = "%s/DEV/000" % ( ORIG_REPO_aBRANCH)
ORIG_REPO_aBRANCH_DEV1  = "%s/DEV/001" % ( ORIG_REPO_aBRANCH)
ORIG_REPO_aFIX_NAME     = "Issue12345"
ORIG_REPO_aBRANCH_FIX   = "%s/FIX/%s" % ( ORIG_REPO_aBRANCH, ORIG_REPO_aFIX_NAME)
ORIG_REPO_aBRANCH_NEWBR = "%s/NEW/BRANCH" % ( ORIG_REPO_aBRANCH)
TEST_ORIG_REPO          = SANDBOX + ORIG_REPO_NAME #repo to work with
TEST_ORIG_REPO_SHARED   = SANDBOX + ORIG_REPO_NAME_SHARED #repo to work with (with init --shared)
TEST_ORIG_REPO_AREMOTE  = SANDBOX + ORIG_REPO_NAME_AREMOTE #repo to work with (with init --shared)
SWGIT = TESTDIR + "../swgit"
NO_BRANCH   = "(no branch)"
DETACH_HEAD = "(detached-head)"

# Repo created with swgit init (owner is vallea => 1/0/0/0./vallea/INT/...)
TEST_REPO = SANDBOX + "BaseRepo"
TEST_REPO_R   = "2/0"
TEST_REPO_S   = "0/0"
TEST_REPO_LIV = "Drop.A"

TEST_REPO_BR_DEV    = "%s/%s/%s/INT/develop" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER )
TEST_REPO_BR_STB    = "%s/%s/%s/INT/stable" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER )
TEST_REPO_BR_SLA    = "0/0/%s/%s/INT/slave" % ( TEST_REPO_S, ORIG_REPO_GITUSER )
TEST_REPO_CHK_LIV   = "%s/%s/%s/CHK/LIV_%s" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER, TEST_REPO_LIV )
TEST_REPO_STR_CLONE = "%s/STR/CLONE" % ( TEST_REPO_BR_DEV )

TEST_REPO_TAG_STB_DEV = "%s/%s/%s/INT/develop/STB/%s" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER, TEST_REPO_LIV )
TEST_REPO_TAG_STB_STB = "%s/%s/%s/INT/stable/STB/%s" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER, TEST_REPO_LIV )
TEST_REPO_TAG_LIV     = "%s/%s/%s/INT/stable/LIV/%s" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER, TEST_REPO_LIV )
TEST_REPO_TAG_DEV_NEWBR = "%s/%s/%s/INT/develop/NEW/BRANCH" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER )
TEST_REPO_TAG_STB_NEWBR = "%s/%s/%s/INT/stable/NEW/BRANCH" % ( TEST_REPO_R, TEST_REPO_S, ORIG_REPO_GITUSER )
TEST_REPO_FILE_A      = "a.txt"
TEST_REPO_FILE_B      = "b.txt"

#
# CUSTOM TAGS
#
CUSTTAG_NUM = {
    "tagtype"              : "CUSTTAG_NUM",
    "regexp"               : "",
    "regexp_1"             : "",
    "regexp_2"             : "",
    "push_on_origin"       : "true",
    "one_x_commit"         : "false",
    "only_on_integrator_repo"     : "false",
    "allowed_brtypes"      : "",
    "denied_brtypes"       : "",
    "tag_in_past"          : "FAlse",
    "hook_pretag_script"   : "",
    "hook_pretag_sshuser"  : "",
    "hook_pretag_sshaddr"  : "",
    "hook_posttag_script"  : "",
    "hook_posttag_sshuser" : "",
    }
CUSTTAG_NAME = {
    "tagtype"              : "CUSTTAG_NAME",
    "regexp"               : "^Drop[A-Z]{1,3}(_[0-9]{1,3})?$",
    "regexp_1"             : "^Issue[0-9]{5}$",
    "regexp_2"             : "^[0-9]{7}$",
    "push_on_origin"       : "true",
    "one_x_commit"         : "false",
    "only_on_integrator_repo"     : "false",
    "allowed_brtypes"      : "",
    "denied_brtypes"       : "",
    "tag_in_past"          : "FAlse",
    "hook_pretag_script"   : "",
    "hook_pretag_sshuser"  : "",
    "hook_pretag_sshaddr"  : "",
    "hook_posttag_script"  : "",
    "hook_posttag_sshuser" : "",
    }

#
# PROJECTS
#
PROJMAP = ".gitmodules"

REPO_A_DIRNAME = "TEST_PROJ_REPO_A"
REPO_B_DIRNAME = "TEST_PROJ_REPO_B"
REPO_C_DIRNAME = "TEST_PROJ_REPO_C"
REPO_S_DIRNAME = "SNAPSHOT"
REPO_A = SANDBOX + REPO_A_DIRNAME
REPO_B = SANDBOX + REPO_B_DIRNAME
REPO_C = SANDBOX + REPO_C_DIRNAME
REPO_S = SANDBOX + REPO_S_DIRNAME

REPO_A_REL = "1/0"
REPO_B_REL = "2/0"
REPO_C_REL = "3/0"
REPO_S_REL = "4/4"
REPO_A_SREL = "0/0"
REPO_B_SREL = "0/0"
REPO_C_SREL = "1/0"
REPO_S_SREL = "4/4"

REPO_A_URL = "%s%s" % (TESTER_SSHACCESS, REPO_A)
REPO_B_URL = "%s%s" % (TESTER_SSHACCESS, REPO_B)
REPO_C_URL = "%s%s" % (TESTER_SSHACCESS, REPO_C)
REPO_S_URL = "%s%s" % (TESTER_SSHACCESS, REPO_S)
REPO_A_INTBR = "%s/%s/%s/INT/develop" % (REPO_A_REL, REPO_A_SREL, ORIG_REPO_GITUSER )
REPO_B_INTBR = "%s/%s/%s/INT/develop" % (REPO_B_REL, REPO_B_SREL, ORIG_REPO_GITUSER )
REPO_C_INTBR = "%s/%s/%s/INT/develop" % (REPO_C_REL, REPO_C_SREL, ORIG_REPO_GITUSER )
REPO_S_INTBR = "%s/%s/%s/INT/develop" % (REPO_S_REL, REPO_S_SREL, ORIG_REPO_GITUSER )

#
# Test on maps
#
REPOS_INFOS = (
    # name  | rel | subrel | liv |  file | user | cstbranch | src cstbranch
    (REPO_A, REPO_A_REL, REPO_A_SREL, "Drop.A", "a.txt", ORIG_REPO_GITUSER, None, None, REPO_A_URL, REPO_A_INTBR ),
    (REPO_B, REPO_B_REL, REPO_B_SREL, "Drop.B", "b.txt", ORIG_REPO_GITUSER, None, None, REPO_B_URL, REPO_B_INTBR ),
    (REPO_C, REPO_C_REL, REPO_C_SREL, "Drop.C", "c.txt", ORIG_REPO_GITUSER, None, None, REPO_C_URL, REPO_C_INTBR ),
    (REPO_S, REPO_S_REL, REPO_S_SREL, "Drop.S", "snap.txt", ORIG_REPO_GITUSER, None, None, REPO_S_URL, REPO_S_INTBR ),
    )
MAP_INFOS = [
    # name
    # url
    # branch
    [ REPO_A_DIRNAME,
      "%s%s" % (TESTER_SSHACCESS, REPO_A),
      "%s/%s/%s/INT/develop" % (REPOS_INFOS[0][1], REPOS_INFOS[0][2], ORIG_REPO_GITUSER ),
      False,
      ],
    [ REPO_B_DIRNAME + "_LOCAL",
      "%s%s" % (TESTER_SSHACCESS, REPO_B),
      "%s/%s/%s/INT/develop" % (REPOS_INFOS[1][1], REPOS_INFOS[1][2], ORIG_REPO_GITUSER ),
      False,
      ],
    [ "INDIRECT/" + REPO_C_DIRNAME + "_LOCAL",
      "%s%s" % (TESTER_SSHACCESS, REPO_C),
      "%s/%s/%s/INT/develop" % (REPOS_INFOS[2][1], REPOS_INFOS[2][2], ORIG_REPO_GITUSER ),
      False,
      ],
    [ "SNAPSHOT/" + REPO_S_DIRNAME,
      "%s%s" % (TESTER_SSHACCESS, REPO_S),
      "%s/%s/%s/INT/develop" % (REPOS_INFOS[3][1], REPOS_INFOS[3][2], ORIG_REPO_GITUSER ),
      True,
      ],
    ]

LABEL_CHK_A = "%s/%s/%s/CHK/LIV_%s" % ( REPOS_INFOS[0][1], REPOS_INFOS[0][2], ORIG_REPO_GITUSER,  REPOS_INFOS[0][3] )
LABEL_CHK_B = "%s/%s/%s/CHK/LIV_%s" % ( REPOS_INFOS[1][1], REPOS_INFOS[1][2], ORIG_REPO_GITUSER,  REPOS_INFOS[1][3] )
LABEL_CHK_C = "%s/%s/%s/CHK/LIV_%s" % ( REPOS_INFOS[2][1], REPOS_INFOS[2][2], ORIG_REPO_GITUSER,  REPOS_INFOS[2][3] )


CST_BRANCH_NAME = "cst_tss100"
CST_BRANCH_REL = "1/1/1/1"
CST_BRANCH_FULLNAME = "%s/%s/CST/%s" % ( CST_BRANCH_REL, ORIG_REPO_GITUSER, CST_BRANCH_NAME )

#
# TEST on projects
#
REPO_FS__NAME     = "TEST_PROJ_REPO_FS"
REPO_APP__NAME    = "TEST_PROJ_REPO_APP"
REPO_PLAT__NAME   = "TEST_PROJ_REPO_PLAT"
REPO_TSS100__NAME = "TEST_PROJ_REPO_TSS100"
REPO_TDM__NAME    = "TEST_PROJ_REPO_TDM"
REPO_CSTTDM__NAME = "CST-TEST_PROJ_REPO_TDM"
REPO_SNAP__NAME   = REPO_S_DIRNAME

REPO_FS__ORI_DIR     = SANDBOX + REPO_FS__NAME     
REPO_APP__ORI_DIR    = SANDBOX + REPO_APP__NAME    
REPO_PLAT__ORI_DIR   = SANDBOX + REPO_PLAT__NAME   
REPO_TSS100__ORI_DIR = SANDBOX + REPO_TSS100__NAME 
REPO_TDM__ORI_DIR    = SANDBOX + REPO_TDM__NAME    
REPO_CSTTDM__ORI_DIR = SANDBOX + REPO_CSTTDM__NAME    
REPO_SNAP__ORI_DIR   = SANDBOX + REPO_SNAP__NAME    

REPO_FS__ORI_URL     = "%s%s" % ( TESTER_SSHACCESS, REPO_FS__ORI_DIR )
REPO_APP__ORI_URL    = "%s%s" % ( TESTER_SSHACCESS, REPO_APP__ORI_DIR )
REPO_PLAT__ORI_URL   = "%s%s" % ( TESTER_SSHACCESS, REPO_PLAT__ORI_DIR )
REPO_TSS100__ORI_URL = "%s%s" % ( TESTER_SSHACCESS, REPO_TSS100__ORI_DIR )
REPO_TDM__ORI_URL    = "%s%s" % ( TESTER_SSHACCESS, REPO_TDM__ORI_DIR )
REPO_SNAP__ORI_URL   = "%s%s" % ( TESTER_SSHACCESS, REPO_SNAP__ORI_DIR )

REPO_FS__REL     = "7/0"
REPO_APP__REL    = "8/0"
REPO_PLAT__REL   = "2/0"
REPO_TSS100__REL = "1/0"
REPO_TDM__REL    = "5/0"
REPO_SNAP__REL   = "4/4"

REPO_FS__SREL     = "0/0"
REPO_APP__SREL    = "0/0"
REPO_PLAT__SREL   = "0/0"
REPO_TSS100__SREL = "0/0"
REPO_TDM__SREL    = "0/0"
REPO_SNAP__SREL   = "4/4"

REPO_FS__DEVBRANCH     = "%s/%s/%s/INT/develop" % (REPO_FS__REL, REPO_FS__SREL, ORIG_REPO_GITUSER )
REPO_APP__DEVBRANCH    = "%s/%s/%s/INT/develop" % (REPO_APP__REL, REPO_APP__SREL, ORIG_REPO_GITUSER )
REPO_PLAT__DEVBRANCH   = "%s/%s/%s/INT/develop" % (REPO_PLAT__REL, REPO_PLAT__SREL, ORIG_REPO_GITUSER )
REPO_TSS100__DEVBRANCH = "%s/%s/%s/INT/develop" % (REPO_TSS100__REL, REPO_TSS100__SREL, ORIG_REPO_GITUSER )
REPO_TDM__DEVBRANCH    = "%s/%s/%s/INT/develop" % (REPO_TDM__REL, REPO_TDM__SREL, ORIG_REPO_GITUSER )
REPO_SNAP__DEVBRANCH   = "%s/%s/%s/INT/develop" % (REPO_SNAP__REL, REPO_SNAP__SREL, ORIG_REPO_GITUSER )

REPO_FS__STBBRANCH     = "%s/%s/%s/INT/stable" % (REPO_FS__REL, REPO_FS__SREL, ORIG_REPO_GITUSER )
REPO_APP__STBBRANCH    = "%s/%s/%s/INT/stable" % (REPO_APP__REL, REPO_APP__SREL, ORIG_REPO_GITUSER )
REPO_PLAT__STBBRANCH   = "%s/%s/%s/INT/stable" % (REPO_PLAT__REL, REPO_PLAT__SREL, ORIG_REPO_GITUSER )
REPO_TSS100__STBBRANCH = "%s/%s/%s/INT/stable" % (REPO_TSS100__REL, REPO_TSS100__SREL, ORIG_REPO_GITUSER )
REPO_TDM__STBBRANCH    = "%s/%s/%s/INT/stable" % (REPO_TDM__REL, REPO_TDM__SREL, ORIG_REPO_GITUSER )
REPO_SNAP__STBBRANCH   = "%s/%s/%s/INT/stable" % (REPO_SNAP__REL, REPO_SNAP__SREL, ORIG_REPO_GITUSER )

REPO_FS__LBL_NAME     = "Drop.FS"
#REPO_APP__LBL_NAME    = "Drop.AP"
REPO_APP__LBL_NAME    = "" #no label , in order to add a repo with HEAD on same added branch (add submodule twice)
REPO_PLAT__LBL_NAME   = "Drop.PL"
REPO_TSS100__LBL_NAME = "Drop.TS"
REPO_TDM__LBL_NAME    = "Drop.TD"
REPO_SNAP__LBL_NAME   = "Drop.SN"

REPO_FS__LBL     = REPO_FS__STBBRANCH     + "/LIV/" + REPO_FS__LBL_NAME    
REPO_APP__LBL    = REPO_APP__STBBRANCH    + "/LIV/" + REPO_APP__LBL_NAME   
REPO_PLAT__LBL   = REPO_PLAT__STBBRANCH   + "/LIV/" + REPO_PLAT__LBL_NAME  
REPO_TSS100__LBL = REPO_TSS100__STBBRANCH + "/LIV/" + REPO_TSS100__LBL_NAME
REPO_TDM__LBL    = REPO_TDM__STBBRANCH    + "/LIV/" + REPO_TDM__LBL_NAME   
REPO_SNAP__LBL   = REPO_SNAP__STBBRANCH   + "/LIV/" + REPO_SNAP__LBL_NAME   

# INFOS:
#
# common infos
#   [0] name  
#   [1] rel
#   [2] subrel
#   [3] liv
#   [4] file
#   [5] user
# cst infos
#   [6] cstbranch # if must be created a cst branch, its full name
#   [7] src       # src param for cst branch
#   [8] url       # url of this repo (usefull only when cloning repo to create cst)
#   [9] repo      # -b option to clone (usefull only when cloning repo to create cst or clone for remote adding)
#
REPO_FS__INFOS     = ( REPO_FS__ORI_DIR     ,
                       REPO_FS__REL    ,
                       REPO_FS__SREL    ,
                       REPO_FS__LBL_NAME    ,
                       "fs.txt",
                       ORIG_REPO_GITUSER, 
                       None,
                       None,
                       REPO_FS__ORI_URL,
                       REPO_FS__DEVBRANCH
                       )

REPO_APP__INFOS    = ( REPO_APP__ORI_DIR    ,
                       REPO_APP__REL   ,
                       REPO_APP__SREL   ,
                       REPO_APP__LBL_NAME   ,
                       "app.txt",
                       ORIG_REPO_GITUSER,
                       None,
                       None,
                       REPO_APP__ORI_URL,
                       REPO_APP__DEVBRANCH,
                       )

REPO_PLAT__INFOS   = ( REPO_PLAT__ORI_DIR   ,
                       REPO_PLAT__REL  ,
                       REPO_PLAT__SREL  ,
                       REPO_PLAT__LBL_NAME  ,
                       "plat.txt",
                       ORIG_REPO_GITUSER,
                       None,
                       None,
                       #None,
                       #None
                       #CST_BRANCH_FULLNAME,
                       #REPO_PLAT__DEVBRANCH,
                       REPO_PLAT__ORI_URL,
                       REPO_PLAT__DEVBRANCH,
                       )

REPO_TSS100__INFOS = ( REPO_TSS100__ORI_DIR ,
                       REPO_TSS100__REL,
                       REPO_TSS100__SREL,
                       REPO_TSS100__LBL_NAME,
                       "tss100.txt",
                       ORIG_REPO_GITUSER,
                       None,
                       None,
                       REPO_TSS100__ORI_URL,
                       REPO_TSS100__DEVBRANCH,
                       )

REPO_TDM__INFOS    = ( REPO_TDM__ORI_DIR    ,
                       REPO_TDM__REL   ,
                       REPO_TDM__SREL   ,
                       REPO_TDM__LBL_NAME   ,
                       "tdm.txt",
                       ORIG_REPO_GITUSER,
                       CST_BRANCH_FULLNAME,
                       REPO_TDM__LBL,
                       REPO_TDM__ORI_URL,
                       REPO_TDM__DEVBRANCH,
                       )

REPO_SNAP__INFOS     = ( REPO_SNAP__ORI_DIR ,
                         REPO_SNAP__REL     ,
                         REPO_SNAP__SREL    ,
                         REPO_SNAP__LBL_NAME,
                         "snap.txt"           ,
                         ORIG_REPO_GITUSER  , 
                         None,
                         None,
                         REPO_SNAP__ORI_URL,
                         REPO_SNAP__DEVBRANCH
                         )



REPOS_PROJ__INFOS = ( REPO_FS__INFOS, REPO_APP__INFOS, REPO_PLAT__INFOS, REPO_TSS100__INFOS, REPO_TDM__INFOS, REPO_SNAP__INFOS )

# PROJ DESCRIPTION:
#
# [0]  root repo info
#
# [1]    sub repo  info LIST
#    [1]  baseinfo for adding each subrepo
#    [2]   ...
#    ...
# [/1]
#
# Every info is:
#   reponame
#   url
#   intbr

#
#  PLAT 
#   | \ 
#  FS  APP
#
PROJ_PLAT_DESCRIPTION = [
    # name
    # url
    # branch
    [ 
      REPO_PLAT__ORI_DIR,
      REPO_PLAT__ORI_URL,
      REPO_PLAT__DEVBRANCH,
      ],
    [
      [ REPO_FS__NAME,
        REPO_FS__ORI_URL,
        REPO_FS__DEVBRANCH,
        False,
        ],
      [ REPO_APP__NAME,
        REPO_APP__ORI_URL,
        REPO_APP__DEVBRANCH,
        False,
        ],
      ]
    ]


#
# TSS100---.---------------.-----------.
#  |        \               \           \ 
# DEVTDM    DEVPLAT        CSTPLAT   CSTTDM
#             |  \           |  \ 
#          DEVFS DEVAPP   CSTFS CSTAPP
#
PROJ_TSS100_DESCRIPTION = [
    [ 
      REPO_TSS100__ORI_DIR,
      REPO_TSS100__ORI_URL,
      REPO_TSS100__DEVBRANCH,
      ],
    [
      [ REPO_TDM__NAME,
        REPO_TDM__ORI_URL,
        REPO_TDM__DEVBRANCH,
        False,
        ],

      [ "DEV/" + REPO_PLAT__NAME,
        REPO_PLAT__ORI_URL,
        REPO_PLAT__DEVBRANCH,
        False,
        ],
      [ "CST/" + REPO_PLAT__NAME,
        REPO_PLAT__ORI_URL,
        CST_BRANCH_FULLNAME,
        False,
        ],
      [ "CST-" + REPO_TDM__NAME,
        REPO_TDM__ORI_URL,
        CST_BRANCH_FULLNAME,
        False,
        ],
      ]
    ]

SNAP_BI = [ REPO_SNAP__NAME,
            REPO_SNAP__ORI_URL,
            REPO_SNAP__DEVBRANCH,
            True,
            ]


