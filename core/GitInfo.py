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

import sys,os,stat,string,pwd
from optparse import *
import os.path

from Common import * 
from Utils import * 
from ObjLog import *
from ObjBranch import *
from ObjTag import *

def find_new( ref ):
  ret, sha = getSHAFromRef( ref ) 
  cmd_describe = "git describe --contains --all %s" % ( sha )
  bornfrom, ret = myCommand_fast( cmd_describe )
  if ret != 0:
    return ""
  bornfrom=bornfrom[:-1]
  #print bornfrom
  #if bornfrom.count("/") == 6: # case normal branch
  #  bornfrom =  trunch(bornfrom)+"/NEW/BRANCH"
  if bornfrom.find("tags/") == 0:
    bornfrom = getFromSlash(bornfrom,1,8)
  if bornfrom.find("remotes/") == 0:
    bornfrom = getFromSlash(bornfrom,2)
  
  return trunch_describe_output(bornfrom) + "%s/%s" % ( SWCFG_TAG_NEW, SWCFG_TAG_NEW_NAME )


def info_describe_by_tagtype( ref, tagtype ):
  print "reference :\t%s" % ref

  cb = Branch.getCurrBr()
  rel = cb.getRel()

  cmd_describe = "git describe %s --tags --long  --match \"%s/*/*/*/%s/*\"" % ( ref, rel, tagtype )

  bornfrom, ret = myCommand_fast( cmd_describe )
  if ret != 0:
    bornfrom = "NO \"%s\" label found upstream" % tagtype
    print "upstream  :\t%s" % ( bornfrom )
  else:
    bornfrom = bornfrom[ 0 : bornfrom.rfind('-') ]
    num = bornfrom[ bornfrom.rfind('-')+1 : ] # take distance of HEAD, must be 0
    bornfrom = bornfrom[ 0 : bornfrom.rfind('-') ]
    print "upstream  :\t%s\t(%3s commits backwards )" % ( bornfrom, num )

  cmd_describe_contains = "git describe %s --contains --tags --long  --match \"%s/*/*/*/%s/*\"" % ( ref, rel, tagtype )

  mergedinto, ret = myCommand_fast( cmd_describe_contains )
  if ret != 0:
    mergedinto = "NOT yet merged into any \"%s\" label" % tagtype
    print "downstream:\t%s" % ( mergedinto )
  else:
    if mergedinto.find( '~' ) != -1:
      mergedinto = mergedinto[ 0 : mergedinto.find('~') ]
    if mergedinto.find( '^' ) != -1:
      mergedinto = mergedinto[ 0 : mergedinto.find('^') ]
    #git rev-list 1.0/0.0/vallea/FTR/test_sw/NEW/BRANCH..1.0/0.0/hudson/INT/stable/LIV/DROP.E | wc -l
    cmd_count_dist = "git rev-list %s..%s | wc -l" % ( ref, mergedinto )
    dist, ret = myCommand_fast( cmd_count_dist )
    if ret != 0:
      GLog.f( GLog.E, "Error retrieving distance between %s and %s" % ( ref, mergedinto ) )
      print "downstream:\t%s" % ( mergedinto )

    print "downstream:\t%s\t(%3s commits forwards  )" % ( mergedinto, dist[:-1] )
  

def info_describe_something( ref ):
  cmd_show_files = "git show --name-only %s" % ( ref )

  descr, ret = myCommand_fast( cmd_show_files )
  if ret != 0:
    GLog.f( GLog.E, "Error retrieving infos for reference %s" % ref )
    GLog.logRet(1)
    sys.exit(1)

  print descr[:-1]



def info_files( ref ):
  ret, sha = getSHAFromRef( ref )

  cmd_show_files = "git show --oneline --name-only %s" % ( sha )
  descr, ret = myCommand_fast( cmd_show_files )
  if ret != 0:
    GLog.f( GLog.E, "Error retrieving files modified by reference %s" % ref )
    GLog.logRet(1)
    sys.exit(1)

  print descr[:-1]


def info_is_pushed_on_origin( remote, ref ):
  ori_dev = "%s/%s" % (remote,Branch.getIntBr().getShortRef())

  ret, merged = AisparentofB( ref, ori_dev )
  if ret != 0:
    GLog.f( GLog.E, "Error checking if reference %s is merged on " % (ref, ori_dev) )
    GLog.logRet(1)
    sys.exit(1)

  if merged == True:
    print "%s\talready pushed on %s" % (ref, remote)
  else:
    print "%s\tNOT YET pushed on %s" % (ref, remote)



def info_eval_changelog( upstream, downstream, rel ):

  ret, out = info_eval_anylog( upstream, downstream, rel, SWCFG_TAG_DEV )
  if ret != 0:
    return out, 1

  cmd_show_commitmsg = " git for-each-ref \
  --format='From:    %(*authorname) %(*authoremail)\nDate:    %(*authordate)\nRef:     %(refname)\n\n    %(subject)\n\n'"

  result = "x"
  devs = out.splitlines()
  if len(devs) == 0:
    result = "NO DEVsx"
  else: 
    result, errCode = myCommand( "%s %s" % ( cmd_show_commitmsg, "refs/tags/"+" refs/tags/".join(devs) ) )
    if errCode != 0:
      return result, 1

  return result[:-1], 0


def info_eval_fixlog( upstream, downstream, rel ):

  ret, out = info_eval_anylog( upstream, downstream, rel, SWCFG_TAG_FIX )
  if ret != 0:
    return out, 1

  cmd_show_commitmsg = " git for-each-ref \
  --format='From:    %(*authorname) %(*authoremail)\nDate:    %(*authordate)\nRef:     %(refname)\n\n    %(subject)\n\n'"

  result = "x"
  fixes = out.splitlines()
  if len(fixes) == 0:
    result = "NO FIXesx"
  else: 
    result, errCode = myCommand( "%s %s" % ( cmd_show_commitmsg, "refs/tags/"+" refs/tags/".join(fixes) ) )
    if errCode != 0:
      return result, 1

  return result[:-1], 0


def info_eval_ticketlog( upstream, downstream, rel ):

  ret, out = info_eval_anylog( upstream, downstream, rel, SWCFG_TAG_FIX )
  if ret != 0:
    return out, 1

  tickets = []
  for f in out.splitlines():
    #example of lblfixes: tags/4.0/vallea/FTR/fixos/FIX/Issue11112
    tickets.append( f[ f.rfind("/")+1 : ] )

  if len( tickets ) == 0:
      return "", 0

  return "\n".join( tickets )


def info_eval_diff( upstreamRef, downstreamRef, stat = False, file = "", cbc = False , onlyme = False ):

  opt = ""
  if stat == True:
    opt = " --stat "
  if file != "":
    file = " -- %s " % file
  if onlyme == True:
    cbc = True

  commitsUP = []
  commitsDW = []
  jump = []
  if cbc == True:
    dw = downstreamRef
    if downstreamRef == "":
      dw = "HEAD"
    cmd = "git rev-list --reverse --parents --first-parent %s --not %s" % ( dw, upstreamRef ) # nodo padre ( merge )
    # print cmd
    refs, ret = myCommand_fast( cmd )
    # print refs
    diff = ""
    for r in refs.splitlines():
      sha = r.split(" ")
      if len(sha) == 3 and onlyme == True:
        jump.append( sha[0] )
      commitsUP.append( sha[1] )
      commitsDW.append( sha[0] )
    if downstreamRef == "":
      commitsUP.append( "HEAD" )
      commitsDW.append( "" )
  else:
    commitsUP.append( upstreamRef )
    commitsDW.append( downstreamRef )
  
  ret, sha = getSHAFromRef( upstreamRef )
  logUp, ret = myCommand_fast("git log --format='%%d' -1 %s" % upstreamRef )
  print "~"*100
  if logUp != "\n":
    print "Labels:   " + logUp[2:-2] 
  print "Commit:   " + sha
  logCmd, ret = myCommand_fast("git log --format='%%s' -1 %s" % sha )
  print "Subject: ",logCmd[:-1]
  print "~"*100

  for currpos in range( 0, len( commitsUP ) ):
    logDw, ret = myCommand_fast("git log --format='%%d' -1 %s" % commitsDW[currpos] ) 
    diffs = ""
    if commitsDW[currpos] not in jump:
      cmd_diff = "git diff %s %s %s %s" % ( opt,  commitsUP[currpos], commitsDW[currpos], file )
      diffs, ret = myCommand_fast( cmd_diff )
      if ret != 0:
        GLog.f( GLog.E, "Error retrieving differences between %s and %s" % (commitsUP[currpos], commitsDW[currpos] ) )
        GLog.logRet(1)
        sys.exit(1)
    if commitsDW[currpos] == "":
      commitsDW[currpos] = " WORKING DIRECTORY "
      logDw = "\n"
   
    if commitsDW[currpos] not in jump:
      #print "\nDiff between %s and %s" % (commitsUP[currpos], commitsDW[currpos] ) 
      print "\n"+diffs
    else:
      print " *** Jump merge commit %s *** " % commitsDW[currpos]

    print "~"*100
    if logDw != "\n" :
      print "Labels:   " + logDw[2:-2]
    if commitsDW[currpos] != " WORKING DIRECTORY ":
      print "Commit:   " + commitsDW[currpos]
      logCmd, ret = myCommand_fast("git log --format='%%s' -1 %s" % commitsDW[currpos] )
      print "Subject: ",logCmd[:-1]
    else:
      print commitsDW[currpos][1:]
    print "~"*100


def filter_all_tags( regexp, ignorecase=False, type="*", user="*" ):

  grepexp = " -e \"%s\" " % regexp
  if ignorecase == True:
    grepexp = " -i " + grepexp

  cmd_greptag = "git for-each-ref  --format='%%(refname)\t%%(subject)' 'refs/tags/*/*/*/*/%s/*/*/%s/*' | grep %s | cut -f 1" % ( user, type, grepexp )
  #print cmd_greptag

  out_grep, ret = myCommand_fast( cmd_greptag )
  #print out_grep
  out_list = out_grep.splitlines()
  return out_list



def main():

  parser       = OptionParser( description='>>>>>>>>>>>>>> swgit - Info retrieval <<<<<<<<<<<<<<' )

  gitinfo_ref_options_group = OptionGroup( parser, "* Range options" )
  gitinfo_filter_options_group = OptionGroup( parser, "* Filter options" )
  gitinfo_generic_options_group = OptionGroup( parser, "* Generic options" )
  gitinfo_log_options_group = OptionGroup( parser, "* Chg/Fix/tktlog options" )
  gitinfo_diff_options_group = OptionGroup( parser, "* Diff options" )
  output_group  = OptionGroup( parser, "* Output options" )

  load_command_options( gitinfo_ref_options_group, gitinfo_ref_options )
  load_command_options( gitinfo_filter_options_group, gitinfo_filter_options )
  load_command_options( gitinfo_generic_options_group, gitinfo_generic_options )
  load_command_options( gitinfo_log_options_group, gitinfo_log_options )
  load_command_options( gitinfo_diff_options_group, gitinfo_diff_options )
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( gitinfo_ref_options_group )
  parser.add_option_group( gitinfo_filter_options_group )
  parser.add_option_group( gitinfo_generic_options_group )
  parser.add_option_group( gitinfo_log_options_group )
  parser.add_option_group( gitinfo_diff_options_group )
  parser.add_option_group( output_group )

  (options, args)  = parser.parse_args()

  help_mac( parser )

  GLog.initGitLogs( options )
  GLog.s( GLog.I, " ".join( sys.argv ) )


  if len(args) > 1:
    parser.error("Too many arguments")


  rules_deny_single = set( [ "--upstream", "--downstreamRef", "--parent", "-d", "--diff", "--chg", "--change-log", "--fix", "--fix-log", "--tkt", "--ticket-log"] )
  rules_deny_range = set( [ "-r", "--reference", "-i", "--info-generic", "-f", "--show-files", "-t", "--show-by-tag", "-o", "--on-origin", "-p",  "--previous-diff", "-z", "--zero-diff", "--grep", "--igrep" ])
  
  rules =  [ 
      ( "-r", [], rules_deny_single ),
      ( "--reference", [], rules_deny_single.union( set( ["--grep", "--igrep" ] ) ) ),
      ( "--upstream", [], rules_deny_range ),
      ( "--downstreamRef", [], rules_deny_range ),
      ( "--all-dev", [], rules_deny_single ),
      ( "--all-fix", [], rules_deny_single ),
      ( "--all-tag", [], rules_deny_single )
      ]


  onlyotions = set([])
  for currop in sys.argv:
    if currop[0] == "-":
      onlyotions.add( currop )

  for opt in onlyotions:
    for r in rules:
      if r[0] == opt: #found a rule for this input
        allw = r[1] #allowed
        deny = r[2] #denies

        remain_opton = onlyotions - set( [opt] )
        intersect    = deny.intersection( remain_opton )
        if len( intersect ) > 0:
          print "Option %s is not compatible with %s" % ( opt, " ".join( intersect ) )
          sys.exit(1)


  cb = Branch.getCurrBr()
  rel = cb.getRel()
  user = "*"
  if options.user_filter != None:
    user = options.user_filter
  elif options.curruser == True:
    user = Env.getCurrUser()

  type = ""
  if options.allDev == True:
    type = SWCFG_TAG_DEV
  if options.allFix == True:
    type = SWCFG_TAG_FIX
  if options.allTag == True:
    type = "*"
  if type != "":
    jump = False 
    input = ""
    for arg in sys.argv[1:]:
      if jump == True:
        jump = False
        continue
      if arg.find(" ") != -1:
        input = input + " \"" + arg + "\" "
        continue
      if arg in ["--all-dev", "--all-fix", "--all-tag", "--cu", "--curruser"]:
        continue
      if arg in ["--upstream","--downstream","-r","--references", "--grep", "--igrep", "--user"]:
        jump=True
        continue
      input = input + " " + arg   

    err, total = Tag.list( "*/*/*/*", user, "*", "*", type, "*" )
    if len(total) != 0:
      total = [  "refs/tags/" + t for t in total  ]
    #print "ALL LABELS are:\n  %s\n\n%s\n" % ( "\n  ".join( total ), "="*100 )


    if options.regexp != None:
      total = filter_all_tags( options.regexp, False, type, user )
    if options.iregexp != None:
      total = filter_all_tags( options.iregexp, True, type, user )

    if len( input ) == 0: #no options => just dump labels
      if len( total ) == 0:
        sys.exit(0) #no result, avoid git for-each-ref

      cmd_show_ref_msg = "git for-each-ref --format='%(refname)@#@#%(subject)' "
      cmd_ref_msg = "%s %s | column -t -s '@#@#'" % ( cmd_show_ref_msg, " ".join(total) )
      #print cmd_ref_msg
      result, errCode = myCommand( cmd_ref_msg )
      if errCode != 0:
        GLog.f( GLog.E, "\tError executing command showing reference and its message" )
        GLog.logRet(errCode)
        sys.exit(1)
      print result
      sys.exit(0)

    for lbl in total:
      cmd = "%s info -r %s %s" % ( SWGIT, lbl, input )
      out, ret = myCommand_fast( cmd )
      print out
      print "-"*100+"\n"
    sys.exit(0)

  filename = ""
  if len(args) == 1:
    filename = args[0]
    if os.path.exists( filename ) == False:
        parser.error("%s is not a valid file name"%filename)

  genericRef = "HEAD"
  if options.reference != None:
      genericRef = options.reference
 
  dw = "HEAD"
  if options.downstream != None:
    dw = options.downstream

  
  #
  # generic infos
  #
  if options.files == True:
    info_files( genericRef )

  if options.show_by_tag != None:
    info_describe_by_tagtype( genericRef, options.show_by_tag )

  if options.infogen == True:
    info_describe_something( genericRef )

  if options.ispushed == True:
    remotes = Remote.get_remote_list()
    for r in remotes:
      info_is_pushed_on_origin( r, genericRef )

  if options.parent == True:
    errCode, res = AisparentofB( options.upstream, dw )
    if errCode != 0:
      print res 
    errCode2, res2 = AisparentofB( dw, options.upstream )
    if errCode2 != 0:
      print res 

    if res == True and res2 == True:
      print "%s and %s on same commit" % ( options.upstream, dw )
    elif res == True:
      print "%s is parent of %s " % ( options.upstream, dw )
    elif res2 == True:
      print "%s is parent of %s " % ( dw, options.upstream )
    else:
      cmd = "git merge-base " + options.upstream + " " + dw
      outerr, errCode = myCommand_fast( cmd )
      if errCode != 0:
        print "Error in command " + cmd
      print "%s and %s are both children of %s " % ( options.upstream, dw, outerr[:-1] )


  if options.regexp != None or options.iregexp != None:

    cmd_log = "git log --all --format='%H   %s' "

    if user != "*":
      cmd_log = cmd_log + " --author=\"%s\" " % user

    if options.regexp != None:
      cmd_log = cmd_log + " --grep=\"%s\" " % ( options.regexp )
    elif options.iregexp != None:
      cmd_log = cmd_log + " -i --grep=\"%s\"" % ( options.iregexp )

    #print cmd_log

    shas, ret = myCommand_fast( cmd_log )

    if options.infogen == False: #show only label names
      print shas
      sys.exit(0)

    for s in shas.splitlines():
      #print "[",s,"]"
      out, ret = myCommand_fast( "%s info -r %s -i" % ( SWGIT, s[:s.find(' ')] ) )
      print out
      print "-"*100+"\n"


  if options.upstream != None:
    errCode, res = AisparentofB( options.upstream, dw )
    if res != True:
      print "ERROR: %s is not parent of %s " % ( options.upstream, dw )
      sys.exit( 1 )
    
  #
  # log infos
  #
  if options.chg or options.fix or options.tkt:
    if options.chg == True:
      out, err = info_eval_changelog( options.upstream, dw, cb.getRel() )
    if options.fix == True:
      out, err = info_eval_fixlog( options.upstream, dw, cb.getRel() )
    if options.tkt == True:
      out, err = info_eval_ticketlog( options.upstream, dw, cb.getRel() )

    GLog.f( GLog.E, out )
    if err != 0:
      GLog.logRet(1)


  #
  # diff infos
  #
  if options.dif == True:
    if options.upstream == None:
      GLog.f( GLog.E, "-d/--diff need range options. Specify at least upstream (downstream default is HEAD)" )
    else:
      ref = "" #default is diff with working directory
      if options.downstream != None:
        ref = options.downstream

      info_eval_diff( options.upstream, ref, options.stat, file = filename, cbc = options.cbc, onlyme = options.my )


  if options.pdif == True:
    if options.reference == None: #diff agaist WorkingDir
      info_eval_diff( "HEAD", "", options.stat, file = filename )
    else: #diff agaist options.reference
      info_eval_diff( options.reference + "~1", options.reference, options.stat, file = filename )

  if options.zdif == True:
    cb = Branch.getCurrBr()
    ib = Branch.getIntBr()
    sb = Branch.getStableBr()

    newbr = cb.getNewBrRef()
    if options.reference != None:
      newbr = find_new ( options.reference )
    #print newbr
    ref = "" #default is diff with working directory
    if options.reference != None:
      ref = options.reference

    info_eval_diff( newbr, ref, options.stat, file = filename, cbc = options.cbc, onlyme = options.my )


def check_info_ref(option, opt_str, value, parser):
  check_input( option, opt_str, value, parser )

  ret, sha = getSHAFromRef( value )
  if ret != 0:
    parser.error( "Please specify a valid reference with %s option" % option )

  setattr(parser.values, option.dest, value)



gitinfo_ref_options = [
    [
      "-r",
      "--reference",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_info_ref,
        "dest"    : "reference",
        #"default" : "HEAD",
        "metavar" : "<reference>",
        "help"    : "Specify a reference for options needing just 1 param [-f][-t][-i][-o] (default is HEAD), [-p][-z] (default is Working Directory)"
        }
      ],
    [
      "--upstream",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_info_ref,
        "dest"    : "upstream",
        "metavar" : "<reference>",
        "help"    : "Specify upstream reference for options needing RANGE param [-d][--chg][--fix][--tkt][--parent]"
        }
      ],
    [
      "--downstream",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_info_ref,
        "dest"    : "downstream",
        #"default" : "HEAD",
        "metavar" : "<reference>",
        "help"    : "Specify downstream reference for options needing RANGE param [-d][--chg][--fix][--tkt][--parent] (Default is Working Directory) "
        }
      ],
    ]

gitinfo_filter_options = [
    [ "--all-dev",
      {
        "action"  : "store_true",
        "dest"    : "allDev",
        "default" : False,
        "help"    : "Apply actions to every user DEV label"
        }
      ],
    [ "--all-fix",
      {
        "action"  : "store_true",
        "dest"    : "allFix",
        "default" : False,
        "help"    : "Apply actions to every user FIX label"
        }
      ],
    [ "--all-tag",
      {
        "action"  : "store_true",
        "dest"    : "allTag",
        "default" : False,
        "help"    : "Apply actions to every repository label"
        }
      ],
    [
      "--user",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "user_filter",
        "metavar" : "<user_val>",
        "help"    : "Specify user name to filter tags on"
        }
      ],
    [ 
      "--cu",
      "--curruser",
      {
        "action"  : "store_true",
        "dest"    : "curruser",
        "default" : False,
        "help"    : "Alias for --user <myself> when filtering tag and commits."
        }
      ],
    [
      "--grep",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "regexp",
        "metavar" : "<regexp>",
        "help"    : "Specify regexp to look for only in repository commits (scpecify --all-tags/--all-dev/--all-fix to look also among labels)"
        }
      ],
    [
      "--igrep",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "iregexp",
        "metavar" : "<iregexp>",
        "help"    : "Specify regexp to look for only in repository commits, ignoring case (scpecify --all-tags/--all-dev/--all-fix to look also among labels)"
        }
      ]
    ]



gitinfo_generic_options = [
    [ 
      "-i",
      "--info-generic",
      {
        "action"  : "store_true",
        "dest"    : "infogen",
        "default" : False,
        "help"    : "Show generic informations on any reference"
        }
      ],
    [ 
      "-f",
      "--show-files",
      {
        "action"  : "store_true",
        "dest"    : "files",
        "default" : False,
        "help"    : "Show files modified in that commit"
        }
      ],
    [ 
      "-t",
      "--show-by-tag",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "show_by_tag",
        "metavar" : "<tag_type_val>",
        "help"    : "Show from which tag this commit is geneared and into which has been merged"
        }
      ],
    [ 
      "-o",
      "--on-origin",
      {
        "action"  : "store_true",
        "dest"    : "ispushed",
        "default" : False,
        "help"    : "Returns true if reference has already been pushed on origin"
        }
      ],
    [ 
      "--parent",
      {
        "action"  : "store_true",
        "dest"    : "parent",
        "default" : False,
        "help"    : "Returns parent child relationship between upstream and downstream"
        }
      ]
    ]

gitinfo_log_options = [
    [ 
      "--chg",
      "--change-log",
      {
        "action"  : "store_true",
        "dest"    : "chg",
        "default" : False,
        "help"    : "Evaluate changelog"
        }
      ],
    [ 
      "--fix",
      "--fix-log",
      {
        "action"  : "store_true",
        "dest"    : "fix",
        "default" : False,
        "help"    : "Evaluate fixlog"
        }
      ],
    [ 
      "--tkt",
      "--ticket-log",
      {
        "action"  : "store_true",
        "dest"    : "tkt",
        "default" : False,
        "help"    : "Evaluate ticket log"
        }
      ]
    ]


gitinfo_diff_options = [
    [ 
      "-d",
      "--diff",
      {
        "action"  : "store_true",
        "dest"    : "dif",
        "default" : False,
        "help"    : "Show differences between upstream and downstream"
        }
      ],
    [ 
      "-p",
      "--previous-diff",
      {
        "action"  : "store_true",
        "dest"    : "pdif",
        "default" : False,
        "help"    : "Show differences between any reference and its precedessor (NOT in conjunction with -d or -z)"
        }
      ],
    [ 
      "-z",
      "--zero-diff",
      {
        "action"  : "store_true",
        "dest"    : "zdif",
        "default" : False,
        "help"    : "Show differences between any reference and its NEW/BRANCH (NOT in conjunction with -d or -p)"
        }
      ],
    [ 
      "-s",
      "--stat",
      {
        "action"  : "store_true",
        "dest"    : "stat",
        "default" : False,
        "help"    : "Shows diff statistics (Only in conjunction with another diff option)"
        }
      ],
    [ 
      "--cbc",
      "--commit-by-commit",
      {
        "action"  : "store_true",
        "dest"    : "cbc",
        "default" : False,
        "help"    : "Show differences separing commit by commit"
        }
      ],
    [ 
      "--my",
      "--my-commits-only",
      {
        "action"  : "store_true",
        "dest"    : "my",
        "default" : False,
        "help"    : "Show differences regarding only my contributes (implies --cbc/--commit-by-commit)"
        }
      ]
    ]

if __name__ == "__main__":
  main()
