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
from ObjLock import * 
from ObjLog import * 

from string import *

def main():
  usagestr =  """\
Usage: swgit lock [options] <remote-name>|<remote-url>"""
  parser       = OptionParser( usage = usagestr,
                               description='>>>>>>>>>>>>>> swgit - Lock Management <<<<<<<<<<<<<<' )
  mgt_group    = OptionGroup( parser, "Management options" )
  output_group = OptionGroup( parser, "Output options" )
  load_command_options( mgt_group, gitlock_mgt_options )
  load_command_options( output_group, arr_output_options )
  parser.add_option_group( mgt_group )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()

  help_mac( parser )

  GLog.initGitLogs( options )
  
  exclusive = [ parser.values.lock , parser.values.unlock ]
  num_true = 0
  for e in exclusive:
    if e == True:
      num_true = num_true + 1
  if num_true > 1 :
    parser.error( "Cannot specify -l or -u or --fl or --fu togheter" )

  
  GLog.s( GLog.I, " ".join( sys.argv ) )

  if len( args ) != 1:
    parser.error( "Please specify remote name (i.e. 'origin' ...) or remote url (i.e. ssh://...)" )

  objRem = create_remote( args[0] )
  if not objRem.isValid():
    GLog.f( GLog.E, str(objRem) )
    sys.exit(1)

  lock = createLockStartegy( objRem.getUrl() )

  errCode = 0

  type = ""
  if options.write == True and options.read == True:
    parser.error( "Cannot specify --write or --read togheter" )
  
  if options.write == False and options.read == False and options.status == False :
    parser.error( "Must specify one option of --write or --read " )

  if options.write or options.read:
    if not options.lock and not options.unlock:
      parser.error( "Please specify --lock or --unlock" )

  if options.write == True:
    type = "write"
  elif options.read == True:
    type = "read"
  


  if options.status == True:

    errCode, statusSTR = lock.status()
    if errCode != 0:
      GLog.f( GLog.E, "Git lock - %s" % ( statusSTR) )
      sys.exit(1)

    lines = statusSTR.splitlines()
    writeinfo = lines[0]
    locksinfo = lines[1:]

    retstr = "not locked\n"
    if len( locksinfo ) > 0:
      retstr = ""
      for s in locksinfo:
        tmp  = "\"" + s[ 0 : s.find('.') ] + "\""
        tmp += " lock by " +   s[ s.find('.') + 1 : ]
        retstr += "%s\n" % tmp

    GLog.s( GLog.S, "Repository \"%s\" is\n%s" % ( objRem.getUrl(), indentOutput( retstr[:-1],1 ) ) )
    GLog.s( GLog.S, writeinfo )

    sys.exit(0)

  if options.lock == True:

    GLog.s( GLog.S, "Manually locking repository \"%s\"" % ( objRem.getUrl() ) )
    errCode, errStr = lock.acquire( type, False )
    GLog.s( GLog.S, indentOutput( errStr, 1 ) )
    GLog.logRet( errCode )

  elif options.unlock == True:

    GLog.s( GLog.S, "Manually unlocking repository \"%s\"" % ( objRem.getUrl() ) )
    errCode, errStr = lock.release( type, False )
    GLog.s( GLog.S, indentOutput( errStr, 1 ) )
    GLog.logRet( errCode )

  if errCode != 0:
    sys.exit(1)
  sys.exit(0)



def check_lock(option, opt_str, value, parser):
  #if options.ml == False and options.mu == False:
  #  parser.error( "Please specify one option among --ml or --mu" )
#  parser.error( "Cannot specify -l or -u or --fl or --fu togheter" )
  setattr(parser.values, option.dest, True)


gitlock_mgt_options = [
    [ 
      "-s",
      "--status",
      {
        "action"  : "store_true",
        "dest"    : "status",
        "default" : False,
        "help"    : 'Check repository lock status'
        }
      ],
    [ 
      "-l",
      "--lock",
      {
        "nargs"   : 0,
        "action"  : "callback",
        "dest"    : "lock",
        "callback": check_lock,
        "default" : False,
        "help"    : 'Manually lock   repository'
        }
      ],
    [ 
      "-u",
      "--unlock",
      {
        "nargs"   : 0,
        "action"  : "callback",
        "dest"    : "unlock",
        "callback": check_lock,
        "default" : False,
        "help"    : 'Manually unlock repository'
        }
      ],
    [ 
      "--read",
      {
        "action"  : "store_true",
        "dest"    : "read",
        "default" : False,
        "help"    : "Read lock/unlock"
        }
      ],
    [ 
      "--write",
      {
        "action"  : "store_true",
        "dest"    : "write",
        "default" : False,
        "help"    : "Write lock/unlock"
        }
     ]
   ]

if __name__ == "__main__":
  main()
  
