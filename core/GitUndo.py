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

from Utils import *
from ObjLog import *
from optparse import *


def uncoFiles( *files ):
  cmd = "git checkout -- " +" ".join( files[0] )
  out, errCode = myCommand( cmd )
  if errCode != 0:
    GLog.f(GLog.E, "Error when undo changes on these files: \n\t" + "\n\t".join( files[0] ) )
    return 1, "" 
  return 0, ""
 
   
def main():
  usagestr =  """\
Usage: swgit undo <file>... """

  parser = OptionParser( usage = usagestr, 
                         description='>>>>>>>>>>>>>> swgit - Status <<<<<<<<<<<<<<' )

  output_group = OptionGroup( parser, "Output options" )
  load_command_options( output_group, arr_output_options )
  parser.add_option_group( output_group )

  (options, args)  = parser.parse_args()
  args = parser.largs
  
  help_mac( parser )

  GLog.initGitLogs( options )
 
  if len(args) == 0:
    parser.error("Please specify file(s) to undo changes")

  GLog.s( GLog.I, " ".join( sys.argv ) )

  GLog.s( GLog.S, "Undo changes on file(s)" )
  errCode, out= uncoFiles( args ) 
  if errCode != 0:
    GLog.logRet(1)
    sys.exit(1)
  
  GLog.logRet(0)
  sys.exit(0)



if __name__ == "__main__":
    main()


