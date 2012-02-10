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

#import warnings
#warnings.filterwarnings("ignore", message="The popen2 module is deprecated.")
#import popen2
import subprocess
import os,time,sys,pwd,socket,re

from Defines import *
import OldPython

#general purpose command.
def myCommand_fast( cmd, shell = True ):

  # use poll instead of wait when long output can be genearetd. 
  #  In those cases this happen:
  #  1. command generates great output
  #  2. no one consumes it
  #  3. wait blocks untils command ends but it cannot because queue if full.
  
  command = subprocess.Popen( cmd,
                              shell=shell,
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

  return ( out, retcode )

#  command = subprocess.Popen( cmd,
#                              shell=shell,
#                              stdin=subprocess.PIPE,
#                              stdout=subprocess.PIPE,
#                              stderr=subprocess.STDOUT,
#                            )
#  out = ""
#  retcode = command.wait()
#  out = "".join( command.stdout.readlines() )
#
#  if retcode != 0:
#    retcode = 1
#
#  return ( out, retcode )



#returns list of rows.
def myCommand_fast_nojoin( cmd, shell = True ):

  command = subprocess.Popen( cmd,
                              shell=shell,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                            )
  out = []
  retcode = command.poll()
  out += command.stdout.readlines()
  while ( retcode == None ):
    time.sleep(0.001)
    retcode = command.poll()
    out += command.stdout.readlines()

  if retcode != 0:
    retcode = 1

  return ( out, retcode )


#polls to avoid deadlocks.
def myCommand_fast_longoutput( cmd, shell = True ):
  # use poll instead of wait when long output can be genearetd. 
  #  In those cases this happen:
  #  1. command generates great output
  #  2. no one consumes it
  #  3. wait blocks untils command ends but it cannot because queue if full.
  
  command = subprocess.Popen( cmd,
                              shell=shell,
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

  return ( out, retcode )



def mySSHCommand_fast( cmd, user, address ):
  # HOME DIRECOTRY => use ~
  #   because 
  #     $HOME depends only on UID
  #   but
  #     when UID != EUID => ~ looks on the right direcotry (that of EUID)
  euid_home = "~%s" % pwd.getpwuid( os.geteuid() )[0]
  euid_home = os.path.expanduser( euid_home )
  ssh_key = "%s/.ssh/swgit_sshKey" % euid_home
  cmd = "ssh -i %s %s@%s ' %s '" % ( ssh_key, user, address, cmd )
  out, errCode = myCommand_fast( cmd )
  return (out, errCode)
  

def sw():
  return os.path.abspath( os.path.dirname( os.path.abspath( __file__ ) ) + "/../swgit" )

def get_repo_cfg_bool( key, dir = ".", fglobal = False ):
  outerr, errCode = get_repo_cfg( key, dir, fglobal, "--bool" )
  if errCode != 0:
    return False
  if outerr[:-1] == "true":
    return True
  return False

def get_repo_cfg_regexp( key, dir = ".", fglobal = False, type = "" ):
  if os.path.exists( dir ) == False:
    return "Invalid path %s" % dir, 1

  optglob = ""
  if fglobal == True:
    optglob = " --global "

  cmd = "cd %s && git config --get-regexp %s %s %s" % ( dir, optglob, type, key )
  return myCommand_fast( cmd )


def get_repo_cfg( key, dir = ".", fglobal = False, type = "" ):
  if os.path.exists( dir ) == False:
    return "Invalid path %s" % dir, 1

  optglob = " --local "
  if fglobal == True:
    optglob = " --global "

  cmd = "cd %s && git config --get %s %s %s" % ( dir, optglob, type, key )
  return myCommand_fast( cmd )


def set_repo_cfg( key, value, dir = ".", type = "" ):
  if os.path.exists( dir ) == False:
    return "Invalid path %s" % dir, 1

  if value == SWCFG_UNSET:
    cmd = "cd %s && git config --get %s && git config --unset %s || exit 0" % ( dir, key, key )
  else:
    cmd = "cd %s && git config %s %s %s" % ( dir, type, key, value )
  return myCommand_fast( cmd )

