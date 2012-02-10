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

import sys
import string
import logging
import datetime

from MyCmd import *
from optparse import *
from Common import *
from ObjEnv import *


# quiet   => no stdout
# verbose => anche stdout il lofFull
# debug   => abilita stampe a debug

f_initialized_ = False
o_initialized_ = False
g_nolog        = False

logF_ = None
logS_ = None
repo2logger = {}


###########
#
# GLog
#
###########
class GLog:
  NORMAL, VERBOSE, QUIET = range( 3 )
 
  logging.addLevelName(25, "SLIM")
   
  C = logging.CRITICAL
  E = logging.ERROR
  W = logging.WARNING
  S = 25;#logging.SLIM
  I = logging.INFO
  D = logging.DEBUG

  tab = 0

  def __init__( self ):
    pass
  def __str__( self ):
    return "Init = " + str( f_initialized_ ) + "/" + str( f_initialized_ )

  @staticmethod
  def logRet( errCode, indent="",reason = ""):
    
    if reason != "":
      reason = " - " + reason
    if errCode != 0:
      GLog.s( GLog.E, indent + "FAILED" + reason )
    else:
      GLog.s( GLog.S, indent + "DONE" )

  @staticmethod
  def initGitLogs( options ): # first param returned by parser.parse_args()
    GLog.initLogs( options )
    return


  @staticmethod
  def initLogs( options ): # first param returned by parser.parse_args()
    lvl = logging.INFO
    if options.debug == True:
      lvl = logging.DEBUG
  
    if options.verbose == True:
      type = GLog.VERBOSE
    elif options.quiet == True:
      type = GLog.QUIET
    else:
      type = GLog.NORMAL
  
    if  os.environ.get('SWINDENT') != None:
      GLog.tab = int(os.environ.get('SWINDENT'))
    else:
      GLog.tab = 0

    GLog.initF( lvl, type )
    GLog.initS( lvl, type )

    if os.environ.get('SWINDENT') == None:
      GLog.s( GLog.I, "--"*10 + " START "+"--"*10 )
 
    return


  @staticmethod
  def initF( e_layer, e_type ):
    global logF_
    global f_initialized_
    if f_initialized_ == True:
      return

    logF_ = logging.getLogger( "Full" )
    logF_.setLevel( e_layer )

    dirname = "%s/%s" % ( Env.getLocalRoot(), SWDIR_LOG )
    if not os.path.exists( dirname ):
      print "Init FULL log - directory " + dirname + " not existing"
      import traceback
      traceback.print_stack()
      return

    file_handler = logging.FileHandler( "%s/%s_full.log" % (dirname, Env.getCurrUser() ) )
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
    file_handler.setLevel( e_layer )
    file_handler.setFormatter( file_formatter )

    logF_.addHandler( file_handler )


    # verbose management, redirect all to stdout
    stdout_handler = logging.StreamHandler( sys.stdout )
    stdout_formatter = logging.Formatter("%(message)s")
    stdout_handler.setLevel( GLog.E )
    
    if e_type == GLog.VERBOSE:
      stdout_handler.setLevel( GLog.I )

    if e_type == GLog.QUIET:
      stdout_handler.setLevel( GLog.C )
        
    if e_layer == GLog.D:
      stdout_handler.setLevel( GLog.D )

    stdout_handler.setFormatter( stdout_formatter )

    logF_.addHandler( stdout_handler )

    f_initialized_ = True
    return


  @staticmethod
  def initS( e_layer, e_type ):
    global logS_
    global o_initialized_
    if o_initialized_ == True:
      return

    logS_ = logging.getLogger( "Slim" )
    logS_.setLevel( e_layer )

    dirname = "%s/%s" % ( Env.getLocalRoot(), SWDIR_LOG )
    if not os.path.exists( dirname ):
      print "Init Slim log - directory " + dirname + " not existing"
      import traceback
      traceback.print_stack()
      return

    file_handler = logging.FileHandler( "%s/%s_slim.log" % (dirname, Env.getCurrUser() ) )
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
    file_handler.setLevel( GLog.I )
    file_handler.setFormatter( file_formatter )

    logS_.addHandler( file_handler )

    # verbose management, redirect all to stdout
    if e_type == GLog.NORMAL and e_layer != GLog.D :
      stdout_handler = logging.StreamHandler( sys.stdout )
      stdout_formatter = logging.Formatter( "%(message)s" )
      stdout_handler.setLevel( GLog.S )
      stdout_handler.setFormatter( stdout_formatter )

      logS_.addHandler( stdout_handler )
    
    o_initialized_ = True
    return



  @staticmethod
  def _log( logger, lvl, msg ):
      msg = indentOutput(msg,GLog.tab)
      if lvl == logging.CRITICAL:
        logger.critical( msg )
      elif lvl == logging.ERROR:
        logger.error( msg )
      elif lvl == logging.WARNING:
        logger.warning( msg )
      elif lvl == 25: #logging.SLIM:
        logger.log(25, msg )
      elif lvl == logging.INFO:
        logger.info( msg )
      elif lvl == logging.DEBUG:
        logger.debug( msg )
      else:
        print "@@@@ NO LEVEL FOUND:" + msg

  @staticmethod
  def f( lvl, msg ):
    if f_initialized_ == False:
      #print "FULL LOGGER NOT INITIALIZED"
      #print msg
      return
    # local log
    GLog._log( logF_, lvl, msg )
        

  @staticmethod
  def s( lvl, msg ):
    if o_initialized_ == False:
      #print "SLIM LOGGER NOT INITIALIZED LOG"
      #print msg
      return

    # local log
    GLog._log( logS_, lvl, msg )
    GLog.f(GLog.S, msg ) # GLog.S print SLIM in full_file, maybe only difference



def priv_load_command_options( parser, optionList ):
  for currOption in optionList:
    if len( currOption ) == 2:
      #parameters with just one option
      parser.add_option( currOption[0],
                         **currOption[1] )
    elif len( currOption ) == 3:
      #parameters with short and long options
      parser.add_option( currOption[0],
                         currOption[1],
                         **currOption[2] )


#
# Export options parameters 
#
def check_log_options(option, opt_str, value, parser):
  setattr(parser.values, option.dest, True)
  if parser.values.quiet == True and parser.values.verbose == True:
    parser.error( "Cannot specify --verbose and --quiet togheter" )


#from pprint import pprint
def help_mac( parser ):
  envvar = os.environ.get('SWHELPMAC')
  if envvar == None:
    return 0

  if envvar == "PRINT": 
    ret=""
    #pprint ( parser.__dict__ )
    for k, v in parser._long_opt.items():
      #pprint( v.__dict__ )
      if len( k ) > 5:
        if v.nargs == None or v.nargs == 0:
          ret += "%s:0:<>\n" %( k )
          continue
        ret += "%s:%s:%s\n" %( k, v.nargs, v.metavar.replace( " ", "_" ) )
    sys.stdout.write( ret )
    sys.exit( 0 )
  elif envvar.find( "S2L@" ) == 0:
    shortopt = envvar[4:]
    if shortopt in parser._short_opt and len( parser._short_opt[shortopt]._long_opts ) > 0:
      sys.stdout.write( "%s\n" % parser._short_opt[shortopt]._long_opts[0] )
      sys.exit( 0 )
    else:
      sys.exit( 1 )
  else:
    sys.exit( 0 )



arr_output_options = [
    [ 
      "--quiet",
      {
        "nargs"   : 0,
        "action"  : "callback",
        "callback": check_log_options,
        "dest"    : "quiet",
        "default" : False,
        "help"    : 'Enable quiet mode'
        }
      ],
    [ 
      "--verbose",
      {
        "nargs"   : 0,
        "action"  : "callback",
        "callback": check_log_options,
        "dest"    : "verbose",
        "default" : False,
        "help"    : 'Enable verbose mode, print everithing to stdout'
        }
      ],
    [ 
      "--debug",
      {
        "nargs"   : 0,
        "action"  : "callback",
        "callback": check_log_options,
        "dest"    : "debug",
        "default" : False,
        "help"    : 'Enable debug mode (does not imply verbose mode)'
        }
      ]
  ]
    

def main():
  print "\nTesting GLog class: "
  loggerNoinit = GLog()

  parser     = OptionParser( description='>>>>>>>>>>>>>> swgit - Log Management <<<<<<<<<<<<<<' )
  output_group = OptionGroup( parser, "Output options" )
  priv_load_command_options( output_group, arr_output_options )
  parser.add_option_group( output_group )
  (options, args)  = parser.parse_args()

  user = "utente"
  dir  = "/tmp/"

  #GLog.initLogs( dir + user, options )
  GLog.initGitLogs( options )

  GLog.f( GLog.C, "1 full logger, critical severity" )
  GLog.s( GLog.C, "2 out  logger, critical severity" )
  GLog.f( GLog.I, "3 full logger, info severity" )
  GLog.s( GLog.I, "4 out  logger, info severity" )
  GLog.f( GLog.D, "5 full logger, debug severity" )
  GLog.s( GLog.D, "6 out  logger, debug severity" )


if __name__ == "__main__":
    main()

