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

import pwd,os,sys,string,logging,re
from optparse import *
from MyCmd import *


def indentOutput( output, tab = 0 ):
  str_tab = "%s" % ("\t"*tab)
    
  output = str_tab +  output
  output = output.replace("\n","\n"+str_tab)
  return output


def getOutputOpt(options):
  #print options
  output_opt =""
  if options.quiet == True:
    output_opt =  output_opt + " --quiet"
  if options.debug == True:
    output_opt =  output_opt + " --debug"
  if options.verbose == True:
    output_opt =  output_opt + " --verbose"
  #if hasattr(options, 'stat'):
  #  if options.stat == True:
  #    output_opt =  output_opt + " --stat"

  return output_opt

def add_slash( str ):
  if str == "":
    return "/"
  if str[-1] == "/":
    return str
  return str +"/"

def del_slash( str ):
  if str == "":
    return ""
  if str[-1] != "/":
    return str
  return str[:-1]


def check_allowed_options( checkopt, allowmap, alias_short2long ):

  str_print = checkopt

  #un-alias checkopt
  for (s,l) in alias_short2long.items():
    if checkopt == s or checkopt == l:
      str_print += "%s/%s" % (s,l)
      checkopt = l
      break

  #un-alias input
  input = sys.argv
  for (pos,val) in enumerate( input ):
    if val[0] != "-":
      continue
    if val in alias_short2long.keys():
      input[pos] = alias_short2long[val]

  #un-alias allowmap
  for (key,val) in allowmap.items():
    if val[0] != "-":
      continue
    if val in alias_short2long.keys():
      allowmap[key] = alias_short2long[val]

  #check compatibility
  if checkopt in allowmap.keys():
    for currinopt in input:
      if currinopt[0] != "-":
        continue
      if checkopt == currinopt:
        continue #do not process myseld
      if currinopt not in allowmap[checkopt]:
        return "Cannot specify option %s and %s toghether." % ( str_print, currinopt ), 1

  return "", 0


def check_allowed_options_p( checkopt, allowmap, parser ):

  alias_short2long = {}
  for s in parser._short_opt.keys():
    l = parser._short_opt[s]._long_opts[0] #take only first
    alias_short2long[s] = l

  return check_allowed_options( checkopt, allowmap, alias_short2long )


################################################
# options management

def load_command_options( parser, optionList ):
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


def check_input(option, opt_str, value, parser):
  if value[0] == "-":
    parser.error("Argument error on: "+ value)
  setattr(parser.values, option.dest, value)


################################################
# colors


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


errorMSG = "\n"+bcolors.FAIL + " ERROR:" + bcolors.ENDC + "\n "
waringMSG = "\n"+bcolors.WARNING + " WARNING:" + bcolors.ENDC + "\n "
OK = "\n"+bcolors.OKGREEN + " OK:" + bcolors.ENDC + "\n "
START = "\n"+bcolors.OKBLUE + " START:" + bcolors.ENDC + "\n "
DONE = bcolors.OKGREEN + " DONE " + bcolors.ENDC
FAIL = bcolors.FAIL + " FAIL " + bcolors.ENDC


################################################
# checks


################################################
# git obj management


def getFromSlash( ref, start, end=None ):
  jump = False
  if end == None: 
     end = ref.count("/") 
     jump = True
  if end <= start:
    return ""
  if ref.count("/") < end :
    return ""
  a = 0
  while a < start:
    ref = ref[ ref.find("/")+1 : ] 
    a = a + 1
  if jump == False:
    out = ""
    while a < end:
      out = out + "/" + ref[ : ref.find("/") ]
      ref = ref[ ref.find("/")+1 : ]
      a = a + 1
    return out[1:]
  return ref



def getSHAFromRef( ref, root = "." ):
  outerr, errCode = myCommand_fast( "cd %s; git rev-parse --quiet --verify %s^{}" % ( root, ref ) )
  if errCode != 0:
    return errCode, "Cannot get sha for reference: " + ref + "^{}"

  ret = outerr[:-1]
  return errCode, ret


def AisparentofB( a, b ):
  # A = git rev-parse --verify A 
  # B = git rev-parse --verify B
  # mb = git merge-base A B
  # mb = A => A parent B
  aErr, aSha = getSHAFromRef( a )
  if aErr != 0:
    return aErr, aSha

  bErr, bSha = getSHAFromRef( b )
  if bErr != 0:
    return bErr, bSha

  cmd = "git merge-base " + aSha + " " + bSha
  outerr, errCode = myCommand_fast( cmd )
  if errCode != 0:
    return errCode, "Error in command " + cmd
  mSha = outerr[:-1]
  if mSha == aSha:
    return 0, True

  return 0, False

def isMerged( toBeCheckedRef, mainRef ):
  return AisparentofB( toBeCheckedRef, mainRef )


def listToLog(lista):
  out=""
  for l in lista:
    out = out+l+"\n"

  return out

 
def is_integrator_repo( root = "." ):
  cmd_int_repo = "cd %s && git config --get --bool swgit.integrator" % ( root )  
  outerr, errCode = myCommand_fast( cmd_int_repo )
  if errCode == 0 and outerr[:-1] == "true":
    return True
  return False


def trunch_describe_output(ref):
  #if ref.find("-") != -1:
  #  ref = ref[:ref.find("-")]
  if ref.find("^") != -1:
    ref = ref[:ref.find("^")]
  if ref.find("~") != -1:
    ref = ref[:ref.find("~")]
  #ref = ref.replace( "%s/" % SWCFG_TAG_NAMESPACE_TBD, "" )
  #ref = ref.replace( "%s/" % SWCFG_TAG_NAMESPACE_PAST, "" )

  return ref

def findnth(allstr, ch, n):
    parts= allstr.split(ch, n)
    if len(parts)<=n:
        return -1
    return len(allstr)-len(parts[-1])-len(ch)

def rfindnth(allstr, ch, n):
  rev_allstr = allstr[::-1] #(reverse)
  rev_num = findnth( rev_allstr, ch, n )
  if rev_num == -1:
    return -1
  return len( allstr ) - rev_num -1

def check_release( rel ):
  genericRel = re.compile( SWCFG_REL_REGEXP )
  matches = genericRel.findall( rel )
  if len( matches ) > 0:
    retrel = rel.replace(".", "/")
    return retrel, 0

  return "ERROR: Please specify a valid release number: matching \"X.Y.Z.T\" (regexp '%s')" % SWCFG_REL_REGEXP, 1

def check_username( uname ):
  genericUserName = re.compile( SWCFG_USER_REGEXP )
  if len( genericUserName.findall( uname ) ) == 0:
    return "Invalid user name, must match this regexp: %s" % SWCFG_USER_REGEXP, 1
  return "", 0

def check_brname(val):

  generic_brname = re.compile( SWCFG_BR_NAME_REGEXP )
  matches = generic_brname.findall( val )
  if len( matches ) == 0:
    return "Please specify a branch name respecting this regexp: '%s'" % SWCFG_BR_NAME_REGEXP, 1

  if len( val ) == 0 or len( val ) > SWCFG_BR_NAME_MAXLEN:
    return "Please specify a valid branch name (less than %s characters)" % SWCFG_BR_NAME_MAXLEN, 1

  if val.find( "develop" ) != -1 or  val.find( "stable" ) != -1:
    return "Please specify a valid branch name (not containing 'develop' or 'stable' string)", 1

  return "", 0


def is_valid_swgit_tag( ref ):

  num = SWCFG_TAG_NUM_SLASHES
  if ref.find( "refs/" ) == 0:
    num = SWCFG_TAG_NUM_SLASHES_FULL

  if ref.count( "/" ) == num:
    return True
  return False

def is_valid_swgit_branch( ref ):

  num = -1
  if ref.find( "refs/" ) == 0:
    if ref.find( "refs/tags/" ) == 0:
      return False
    if ref.find( "refs/heads" ) == 0:
      num = SWCFG_BR_NUM_SLASHES_LOCAL_FULL
    else:
      num = SWCFG_BR_NUM_SLASHES_REMOTE_FULL
  else:
    num = SWCFG_BR_NUM_SLASHES_LOCAL

  if ref.count( "/" ) == num:
    return True

  #remains swgit remote branch case output
  if ref.count( "/" ) == SWCFG_BR_NUM_SLASHES_REMOTE:
    return True

  return False


def is_local_branch( ref, root = "." ):
  #must be a valid reference and have 6 "/"
  aErr, aSha = getSHAFromRef( ref, root )
  if aErr != 0:
    return False

  #refs/heads format
  if ref.find("refs/heads/") == 0:
    if ref.count("/") == SWCFG_BR_NUM_SLASHES_LOCAL_FULL:
      return True

  #without refs/heads format
  if ref.count("/") != SWCFG_BR_NUM_SLASHES_LOCAL:
    return False

  return True

def is_remote_branch( ref, root = "." ):
  #must be a valid reference and have 6 "/"
  aErr, aSha = getSHAFromRef( ref, root )
  if aErr != 0:
    return False

  # branches are in form:
  #  refs/remote/r/s/m/o/u/...
  # or
  #  r/s/m/o/u/...
  if ref.find("refs/heads/") == 0:
    return False

  if ref.find("refs/") == 0:
    if ref.count("/") == SWCFG_BR_NUM_SLASHES_REMOTE_FULL:
      return True

  #without refs/repo/ format swgit branch dumps with remote prepended
  if ref.count("/") != SWCFG_BR_NUM_SLASHES_REMOTE:
    return False

  return True

def is_ref_pushed_on_origin( ref ):
  cmd_check = "git branch  -r --contains %s" % ref
  outerr, errCode = myCommand_fast( cmd_check )
  if errCode != 0:
    return False
  if outerr[:-1] == "":
    return False
  return True


def input_eliminate_option( optionList, optionWithParam = False ):
  input = ""
  jump = False
  for arg in sys.argv:

    if jump == True: #jump param of option
      jump = False
      continue

    if arg.find(" ") != -1:
      input = input + " \"" + arg + "\" "
      continue

    if arg in optionList:
      if optionWithParam == True:
        jump = True
      continue

    input = input + " " + arg   

  input=input.replace("*", "\*")
  return input 

def getAllIntBranches_local():
  cmd_list_int = "git for-each-ref --format='%(refname:short)' \"refs/heads/*/*/*/*/*/INT/*\""
  out, errCode = myCommand_fast( cmd_list_int )
  if errCode != 0: #no...
    return []
  return out[:-1].splitlines()

def getAllIntBranches_remotes():
  cmd_list_int = "git for-each-ref --format='%(refname:short)' \"refs/remotes/*/*/*/*/*/*/INT/*\""
  out, errCode = myCommand_fast( cmd_list_int )
  if errCode != 0: #no...
    return []
  return out[:-1].splitlines()

def get_commit_subject( commit, dir = "." ):
  cmd = "cd %s && git log -1 --pretty=format:%%s %s" % (dir, commit )
  return myCommand_fast( cmd )


def br_2_rel ( r ):
  if not is_valid_swgit_branch( r ):
    return ""
  stratpos = 0
  relslash = rfindnth( r, '/', 7 ) + 1
  if relslash != 0:
    startpoint = relslash
  return r[ relslash : rfindnth( r, '/', 3 ) ]

def br_2_user( r ):
  if not is_valid_swgit_branch( r ):
    return ""
  return r[ rfindnth( r, '/', 3 ) + 1 : rfindnth( r, '/', 2 ) ]

def br_2_type( r ):
  if not is_valid_swgit_branch( r ):
    return ""
  return r[ rfindnth( r, '/', 2 )  + 1: rfindnth( r, '/', 1 ) ]

def br_2_name( r ):
  if not is_valid_swgit_branch( r ):
    return ""
  return r[ rfindnth( r, '/', 1 ) + 1 : ]


def tag_2_rel ( r ):
  if not is_valid_swgit_tag( r ):
    return ""
  stratpos = 0
  relslash = rfindnth( r, '/', 9 ) + 1
  if relslash != 0:
    startpoint = relslash
  return r[ relslash : rfindnth( r, '/', 5 ) ]

def tag_2_user( r ):
  if not is_valid_swgit_tag( r ):
    return ""
  return r[ rfindnth( r, '/', 5 ) + 1: rfindnth( r, '/', 4 ) ]

def tag_2_brtype( r ):
  if not is_valid_swgit_tag( r ):
    return ""
  return r[ rfindnth( r, '/', 4 ) + 1: rfindnth( r, '/', 3 ) ]

def tag_2_brname( r ):
  if not is_valid_swgit_tag( r ):
    return ""
  return r[ rfindnth( r, '/', 3 ) + 1: rfindnth( r, '/', 2 ) ]

def tag_2_tagtype( r ):
  if not is_valid_swgit_tag( r ):
    return ""
  return r[ rfindnth( r, '/', 2 ) + 1: rfindnth( r, '/', 1 ) ]

def tag_2_tagname( r ):
  if not is_valid_swgit_tag( r ):
    return ""
  return r[ rfindnth( r, '/', 1 ) + 1  : ]

def usage():
  print "%s <reference>" % sys.argv[0]
  sys.exit( 1 )

def main():

  if len( sys.argv ) != 2:
    usage()

  ref = sys.argv[1]
  print ref

  for m in ( is_valid_swgit_tag, 
      is_valid_swgit_branch, 
      br_2_rel ,
      br_2_user,
      br_2_type,
      br_2_name,
      tag_2_rel ,
      tag_2_user,
      tag_2_brtype,
      tag_2_brname,
      tag_2_tagtype,
      tag_2_tagname ):

    print ("%s" % m.__name__).ljust(25) + str( m( ref ))



if __name__ == "__main__":
  main()
  
 

