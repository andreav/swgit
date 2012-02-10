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

import string
from optparse import OptionParser
import sys
from re import *
from Common import * 
from ObjStatus import * 
from ObjTag import * 
import Utils
import Utils_All

g_tag_type    = None
g_tag_value   = None
g_cb_sr       = ""
g_cb          = None
g_cb_strerr   = ""
g_tag_in_past = False



def intToChar(num):
  if num == 0:
    num="000"
  elif num<10:
    num="00"+str(num)
  elif num<100:
    num="0"+str(num)
  return num


def getLastNumber(type):
  brname = g_cb.getShortRef()
  cmd="git for-each-ref --format='%(refname:short)' refs/tags/"+brname+"/"+type+"/ "
  out,errCode = myCommand( cmd, GLog.D )
  if errCode != 0:
    GLog.f( GLog.E, out )
    return errCode,-2

  tmp=out.splitlines()
  if len(tmp) > 0:
    label=tmp[-1]
    pos = string.rfind(label,"/")
    num=label[pos+1:]
    num=int(num)+1
  else:
    num=0
  return errCode,num



def check( options ):

  global g_tag_in_past
  global g_cb_sr, g_cb, g_cb_strerr
  g_cb_sr, g_cb_strerr = Utils.eval_curr_branch_shortref( "HEAD" )
  g_cb = Branch( g_cb_sr )

  if options.list == True or options.rel != None or options.user != None or \
     options.typeB != None or options.nameB != None or options.typeL != None or options.nameL != None or \
     options.int == True or \
     options.custtag_list == True or \
     options.custtag_showcfg != None or \
     len( sys.argv ) == 1:
    return 0

  if options.delete != None or options.erase != None:

    if options.delete != None:
      tbd_tag = options.delete
    else:
      tbd_tag = options.erase

    #valid ref
    tbdTag = Tag( tbd_tag )
    if not tbdTag.isValid():
      GLog.f( GLog.E, "FAILED - Please specify a valid tag to be deleted" )
      return 1

    if tbdTag.getType() == SWCFG_TAG_NEW:
      GLog.f( GLog.E, "FAILED - '%s' tags can be deleted only by deleting associated branch" % SWCFG_TAG_NEW )
      return 1

    #if only on integrator create => only on integrator delete
    tbdTagDsc = create_tag_dsc( tbdTag.getType() )
    if not tbdTagDsc.isValid():
      strerr  = "FAILED - Tag \"%s\" is not well defined.\n" % tbdTag.getType()
      strerr += "         Try issueing 'swgit tag --custom-tag-show-cfg %s'." % tbdTag.getType()
      GLog.f( GLog.E, strerr )
      return 1

    if tbdTagDsc.get_only_on_integrator_repo() and not is_integrator_repo():
      strerr  = "FAILED - This repository has been created as a 'developer' one.\n"
      strerr += "         Tag %s can be created/deleted only on 'integrator' repositories.\n" % tbdTagDsc.get_type()
      strerr += "         You can:\n"
      strerr += "          clone with --integrator\n"
      strerr += "         or\n"
      strerr += "          convert this repo with 'git config --bool swgit.integrator True'"
      GLog.f( GLog.E, strerr )
      return 1

    #not already pushed
    if options.erase == None:
      if is_ref_pushed_on_origin( options.delete ):
        strerr  = "FAILED - Cannot delete a tag already pushed on origin\n"
        strerr += "         If you really want, try issueing 'swgit tag -E'"
        GLog.f( GLog.E, strerr )
        return 1

    #check remote if erase
    if options.erase != None:

      if len( Remote.get_remote_list() ) > 1:

        brObj = Branch( tbdTag.getBrStr() )
        if not brObj.isValid():
          strerr  = "FAILED - There is more than one remote,\n"
          strerr += "         and cannot find a local tracked branch associated to tag '%s'\n" % tbdTag.getTagShortRef()
          strerr += "         Without it, we cannot understand onto which remote to delete this tag.\n"
          strerr += "         Please issue a swgit branch --track <aremote>/%s to solve this problem." % tbdTag.getBrStr()
          GLog.f( GLog.E, strerr )
          return 1

        br_repo, errCode = brObj.branch_to_remote()
        if errCode != 0:
          strerr  = "FAILED - %s\n" % br_repo
          strerr += "         Cannot evaluate on which remote deleting this tag %s" % tbdTag.getTagShortRef()
          GLog.f( GLog.E, strerr )
          return 1

    return 0

  if g_tag_type == None:
    GLog.f( GLog.E, "FAILED - Please specify a tag you want to create, one among {%s}" % "|".join( TagDsc.get_all_tagtypes() ) )
    return 1

  if g_tag_type == SWCFG_TAG_NEW:
    GLog.f( GLog.E, "FAILED - '%s' tags can be created only by creating associated branch" % SWCFG_TAG_NEW )
    return 1

  tagDsc = create_tag_dsc( g_tag_type )
  if not tagDsc.isValid():
    strerr  = "FAILED - Tag \"%s\" is not well defined.\n" % tbdTag.getType()
    strerr += "         Try issueing 'swgit tag --custom-tag-show-cfg %s'." % tbdTag.getType()
    GLog.f( GLog.E, strerr )
    return 1

  if options.reuse_message == True and options.msg != "":
      GLog.f( GLog.E, "FAILED - Please specify only one among -M and -m option." )
      return 1

  if options.reuse_message == False:
    if options.msg == "" and tagDsc.get_hook_pretag_script() == "":
      GLog.f( GLog.E, "FAILED - Please specify option -m or -M or specify a pre-tag hook for label %s" % tagDsc.get_type() )
      return 1


  #detached head
  startb = Branch.getCurrBr()
  if not startb.isValid():
    if not tagDsc.get_tag_in_past():
      strerr  = "ERROR - You are in deatched head or onto a non valid branch."
      strerr  = "        Label \"%s\" is not configured to be put in past.\n" % tagDsc.get_type()
      strerr += "        Issue 'swgit tag --custom-tag-show-cfg %s' to investigate" % tagDsc.get_type()
      GLog.f( GLog.E, strerr )
      return 1
    if not g_cb.isValid():
      strerr  = "ERROR - Tagging in detached head:\n"
      strerr += indentOutput( g_cb_strerr, 1 )
      GLog.f( GLog.E, strerr )
      return 1
    g_tag_in_past = True


  if tagDsc.get_only_on_integrator_repo() and not is_integrator_repo():
    strerr  = "FAILED - This repository has been created as a 'developer' one.\n"
    strerr += "         Tag %s can be created/deleted only on 'integrator' repositories.\n" % tagDsc.get_type()
    strerr += "         You can:\n"
    strerr += "          clone with --integrator\n"
    strerr += "         or\n"
    strerr += "          convert this repo with 'git config --bool swgit.integrator True'"
    GLog.f( GLog.E, strerr )
    return 1

  if len( tagDsc.get_allowed_brtypes() ) > 0:
    if g_cb.getType() not in tagDsc.get_allowed_brtypes():
      GLog.f( GLog.E, "FAILED - Label %s cannot be put on branch type %s, but only on %s" % 
              ( tagDsc.get_type(), g_cb.getType(), tagDsc.get_allowed_brtypes()) )
      return 1
  if len( tagDsc.get_denied_brtypes() ) > 0:
    if g_cb.getType() in tagDsc.get_denied_brtypes():
      GLog.f( GLog.E, "FAILED - Label %s cannot be put on branch type %s, (list of denies: %s)" % 
              ( tagDsc.get_type(), g_cb.getType(), tagDsc.get_denied_brtypes()) )
      return 1
  
  if g_tag_value != None:
    if tagDsc.check_valid_value( g_tag_value ) == False:
      GLog.f( GLog.E, "FAILED - Invalid input. For option %s, please specify any input satisfying this/these regular expression/s %s" %
              ( tagDsc.get_type(), " or ".join( tagDsc.get_regexp() ) ) )
      return 1

  errCode, dev, num = find_describe_label( g_cb.getNewBrRef() )
  if errCode == 0 and num == "0":
    GLog.f( GLog.E, "FAILED - You must have a new commit to tag" )
    return 1
 
  errCode, dev, num = find_describe_label("%s/%s/*" % ( g_cb.getShortRef(), g_tag_type) )
  if errCode == 0:
    if num == "0" and tagDsc.get_one_x_commit():
      GLog.f( GLog.E, "FAILED - You already have a %s label on this commit: %s " % ( g_tag_type, dev ) )
      return 1
  
  if is_ref_pushed_on_origin( "HEAD" ):
    if not tagDsc.get_tag_in_past():
      strerr  = "ERROR - Commit you are tagging is already pushed on origin.\n"
      strerr += "        Label \"%s\" is not configured to be put in past.\n" % tagDsc.get_type()
      strerr += "        Issue 'swgit tag --custom-tag-show-cfg %s' to investigate" % tagDsc.get_type()
      GLog.f( GLog.E, strerr )
      return 1
    else:
      g_tag_in_past = True

  label_name = calculateLblName( options.replace )

  ## Check already pushed  or exists
  lbl = Tag( label_name )
  if lbl.isValid() == True:
    if options.replace == False:
      GLog.f( GLog.E, "FAILED - Already exists label named \"" + label_name + "\".  Try use \"swgit tag --replace\" option" )
      return 1
    else:
      if is_ref_pushed_on_origin( label_name ):
        GLog.f( GLog.E, "FAILED - Label \"" + label_name + "\" already pushed on origin, cannot be replaced." )
        return 1

  return 0


def calculateLblName( replace ):
  
  brname = g_cb.getShortRef()
  tagDsc = create_tag_dsc( g_tag_type )
  if tagDsc.has_numeral_name() == True:

    errCode,num = getLastNumber( g_tag_type )
    if errCode != 0:
      GLog.f( GLog.E, "Error during evaluation of tag %s number" % g_tag_type )
      return errCode
    if replace == True and num > 0:
      num = num -1
    label_name = brname+"/" + g_tag_type + "/" + intToChar(num)

  else:

    label_name = "%s/%s/%s" % ( brname, g_tag_type, g_tag_value )

  return label_name


def create_label( msg, replace ):
  opt = ""
  if replace == True :
    opt="-f"

  label_name = calculateLblName( replace )
  errCode, shaHEAD = getSHAFromRef( "HEAD" )

  #
  # hook pretag
  #   must manage -m in many cases
  #
  tagDsc = create_tag_dsc( g_tag_type )
  hook_pretag_script = tagDsc.get_hook_pretag_script()
  hook_pretag_sshuser = tagDsc.get_hook_pretag_sshuser()
  hook_pretag_sshaddr = tagDsc.get_hook_pretag_sshaddr()
  ssherr = ""

  if hook_pretag_script != "":

    #execute script
    cmd_hook_pretag = "%s %s %s" % ( hook_pretag_script, label_name, shaHEAD )

    if hook_pretag_sshuser != "" and hook_pretag_sshaddr != "":

      ssherr = "%s@%s " % (hook_pretag_sshuser, hook_pretag_sshaddr)
      GLog.s( GLog.S, "Executing pre-tag hook %s%s ..." %  (ssherr, cmd_hook_pretag) )
      pretagout,pretagerr = mySSHCommand( cmd_hook_pretag, hook_pretag_sshuser, hook_pretag_sshaddr )

    elif hook_pretag_sshuser == "" and hook_pretag_sshaddr == "":

      GLog.s( GLog.S, "Executing pre-tag hook %s ..." %  (cmd_hook_pretag) )
      pretagout,pretagerr = myCommand( cmd_hook_pretag )

    else:
      GLog.f( GLog.E, "%s pre-tag hook not well defined. Specify both or nothing among sshuser and sshaddr." % tagDsc.get_type() )
      sys.exit(1)

    #manage error (and correlate with -m option)
    if pretagerr != 0:
      GLog.f( GLog.E, "FAILED - %s pre-tag hook (%s%s) returned error." % (tagDsc.get_type(), ssherr, cmd_hook_pretag) )
      sys.exit(1)

    if pretagout[:-1] != "":
      GLog.f( GLog.E, indentOutput(pretagout[:-1], 1) )
    else:
      if msg == "":
        GLog.f( GLog.E, "FAILED - %s pre-tag hook (%s%s) returned empty string. Please specify at least -m option" % (tagDsc.get_type(), ssherr, cmd_hook_pretag) )
        sys.exit(1)

    GLog.s( GLog.S, "DONE" )

    msg = pretagout[:-1] + "\n" + msg


  #
  # label creation
  #
  GLog.s( GLog.S, "Creating tag " + label_name + " ... " )

  cmd_tag = "git tag %s %s -m \"%s\"" % ( label_name, opt, msg )
  out, tagerrcode = myCommand( cmd_tag )
  GLog.logRet( tagerrcode )
  if tagerrcode != 0:
    return tagerrcode

  #when tagging in past, create also refs/tags/PAST/... label to be pushed
  startb = Branch.getCurrBr()
  if g_tag_in_past:
    if tagDsc.get_push_on_origin():
      GLog.s( GLog.S, "Tagging in past creates also tag %s/%s (this only-local tag will be deleted at next push) ..." % (SWCFG_TAG_NAMESPACE_PAST, label_name) )
      cmd_tag = "git tag %s/%s %s -m \"%s\"" % ( SWCFG_TAG_NAMESPACE_PAST, label_name, opt, msg )
      out, tagerrcode = myCommand( cmd_tag )
      GLog.logRet( tagerrcode )
      if tagerrcode != 0:
        return tagerrcode
    else:
      # if not push on origin => do not create a PAST marker
      pass


  #
  # hook post tag
  #
  hook_posttag_script = tagDsc.get_hook_posttag_script()
  hook_posttag_sshuser = tagDsc.get_hook_posttag_sshuser()
  hook_posttag_sshaddr = tagDsc.get_hook_posttag_sshaddr()
  ssherr = ""

  if hook_posttag_script != "":

    #execute script
    cmd_hook_posttag = "%s %s %s" % ( hook_posttag_script, label_name, shaHEAD )

    if hook_posttag_sshuser != "" and hook_posttag_sshaddr != "":

      ssherr = "%s@%s " % (hook_posttag_sshuser, hook_posttag_sshaddr)
      GLog.s( GLog.S, "Executing post-tag hook %s%s ..." %  (ssherr, cmd_hook_posttag) )
      posttagout,posttagerr = mySSHCommand( cmd_hook_posttag, hook_posttag_sshuser, hook_posttag_sshaddr )

    elif hook_posttag_sshuser == "" and hook_posttag_sshaddr == "":

      GLog.s( GLog.S, "Executing post-tag hook %s ..." %  (cmd_hook_posttag) )
      posttagout,posttagerr = myCommand( cmd_hook_posttag )

    else:
      GLog.f( GLog.E, "%s post-tag hook not well defined. Specify both or nothing among sshuser and sshaddr." % tagDsc.get_type() )
      sys.exit(1)

    #manage error
    if posttagerr != 0:
      GLog.f( GLog.E, indentOutput(posttagout[:-1], 1) )
      GLog.s( GLog.S, "FAILED (not critical)" )
    else:
      GLog.s( GLog.S, "DONE" )


  #ignore hook return values
  return tagerrcode



def execute( options ):
  #
  # -l list tag
  # 
  if len( sys.argv ) == 1:

    err, total = Tag.list()
    if options.quiet == False:
      print "\n".join(total)
    return 0

  elif options.int == True:

    for tt in TagDsc.get_all_tagtypes():
      td = create_tag_dsc( tt )
      if SWCFG_BR_INT in td.get_allowed_brtypes():
        if options.quiet == False:
          err, total = Tag.list( typeL = tt )
          if len( total ) > 0:
            print "\n".join(total)

    # works only on shell, because it to expansion
    #err, total = Tag.list( "*", "*", "*", "*", "*", "{LIV,STB,SLC,DAT,G2C,PLT,ZIC,NGT}", "*" )
    return 0

  elif options.custtag_list == True:

    for tt in TagDsc.get_all_tagtypes():
      td = create_tag_dsc( tt )
      #if td.get_is_default():
      #  continue
      if options.quiet == False:
        print td.dump()
    return 0

  elif options.custtag_showcfg != None:

    options.custtag_showcfg = options.custtag_showcfg.upper()
    if not options.custtag_showcfg in TagDsc.get_all_tagtypes():
      print "Tag \"%s\" is not defined indide this repository." % options.custtag_showcfg
      return 1

    td = create_tag_dsc( options.custtag_showcfg )
    if options.quiet == False:
      print "\nCurrent configuration for tag \"%s\" is:\n" % options.custtag_showcfg
      print indentOutput( td.dump(), 1 )
      print "\nConfigurable parameters for tag \"%s\" are:" % options.custtag_showcfg
      print indentOutput( td.show_config_options(), 1 )
      print ""
    return 0


  elif options.list == True or options.rel != None or options.user != None or \
       options.typeB != None or options.nameB != None or options.typeL != None or \
       options.nameL != None:

    rel   = "*/*/*/*"
    user  = "*"
    typeB = "*"
    nameB = "*"
    typeL = "*"
    nameL = "*"

    myb = Branch.getCurrBr()
    if g_cb.isValid():
      myb = g_cb

    if options.list == True:
      if myb.isValid(): #-l and on br
        rel   = myb.getRel()
        user  = myb.getUser()
        typeB = myb.getType()
        nameB = myb.getName()
      else: #-l and detached
        user  = Env.getCurrUser()

    if options.rel != None:
      rel, ret = check_release( options.rel )
      if ret != 0:
        print rel
        sys.exit( ret )

    if options.user != None: 
      user = options.user
    if options.typeB != None: 
      typeB = options.typeB
    if options.nameB != None: 
      nameB = options.nameB
    if options.typeL != None: 
      typeL = options.typeL
    if options.nameL != None: 
      nameL = options.nameL

    #print "rel :     ", rel
    #print "user:     ", user
    #print "type:     ", typeB
    #print "name:     ", nameB
    #print "tag type: ", typeL
    #print "tag name: ", nameL
    #print ""
    err, total = Tag.list( rel, user, typeB, nameB, typeL, nameL )
    if options.quiet == False:
      if len(total) == 0:
        print "No tags found for ref:  %s/%s/%s/%s/%s/%s "  % ( rel, user, typeB, nameB, typeL, nameL )
      else:
        print "\n".join(total)

    return 0

  elif options.delete != None or options.erase != None:

    if options.delete != None:
      tbdTag = Tag( options.delete )
    else:
      tbdTag = Tag( options.erase )

    errCode, shaTag = getSHAFromRef( tbdTag.getTagShortRef() )

    #delete tag
    GLog.s( GLog.S, "Deleting local tag %s ..." % tbdTag.getTagShortRef() )
    cmd_tag_delete = "git tag -d %s" % tbdTag.getTagShortRef()
    out,errCode = myCommand( cmd_tag_delete )
    if errCode != 0:
      GLog.f( GLog.E, indentOutput( out[:-1], 1) )
      GLog.logRet( errCode )
      return 1
    GLog.logRet( errCode )


    if options.erase != None:

      GLog.s( GLog.S, "Deleting also remote tag %s ..." % tbdTag.getTagShortRef() )

      remote_list = Remote.get_remote_list()
      if len( remote_list ) > 1:
        brObj = Branch( tbdTag.getBrStr() )
        br_repo, errCode = brObj.branch_to_remote()
      else:
        br_repo = remote_list[0]

      cmd_tag_delete = "git push %s  :refs/tags/%s" % ( br_repo, tbdTag.getTagShortRef() )
      out,errCode = myCommand( cmd_tag_delete )
      GLog.f( GLog.E, indentOutput( out[:-1], 1) )

      GLog.logRet( errCode )

    return errCode


  else:

    if options.reuse_message == True:
      comment, err = get_commit_subject( "HEAD" )
      options.msg = comment

    #tag creation
    ret = create_label( options.msg, options.replace )
    if ret != 0:
      return 1

  return 0



def main():
  usagestr =  """\
Usage: swgit tag [list options]
   or: swgit tag [-m <comment>] [--replace] {%s} [<tag-argument>] """ % "|".join( TagDsc.get_all_tagtypes() )

  parser       = OptionParser( usage = usagestr,
                               description='>>>>>>>>>>>>>> swgit - Tag Management <<<<<<<<<<<<<<' )
  mgt_group    = OptionGroup( parser, "Management options" )
  rtrv_group   = OptionGroup( parser, "Retrieve options" )
  custtag_group   = OptionGroup( parser, "Custom tag options" )
  output_group = OptionGroup( parser, "Output options" )

  load_command_options( mgt_group, gittag_mgt_options )
  load_command_options( rtrv_group, gittag_rtrv_options )
  load_command_options( custtag_group, gittag_custtag_options )
  load_command_options( output_group, arr_output_options )

  parser.add_option_group( mgt_group )
  parser.add_option_group( rtrv_group )
  parser.add_option_group( custtag_group )
  parser.add_option_group( output_group )
  
  (options, args)  = parser.parse_args()

  help_mac( parser )

  GLog.initGitLogs( options )
  
  errCode = 0
  
  global g_tag_type
  global g_tag_value

  if len(args) > 2:
    parser.error("Too many arguments")

  GLog.s( GLog.I, " ".join( sys.argv ) )

  if len(args) == 1:
    g_tag_type = args[0].upper()

    if g_tag_type not in TagDsc.get_all_tagtypes():
        GLog.f( GLog.E, "Tag \"%s\" is not defined indide this repository." % args[0] )
        sys.exit(1)

    tagDsc = create_tag_dsc( args[0] )
    if tagDsc.has_numeral_name() == False:
      GLog.f( GLog.E,"Too few arguments: tag \"%s\" requires a name argument" % ( tagDsc.get_type() ) )
      sys.exit(1)

  elif len(args) == 2:
    g_tag_type  = args[0].upper()
    g_tag_value = args[1]

    if g_tag_type not in TagDsc.get_all_tagtypes():
        GLog.f( GLog.E, "Tag \"%s\" is not defined indide this repository." % args[0] )
        sys.exit(1)

    tagDsc = create_tag_dsc( args[0] )
    if not tagDsc.isValid():
      GLog.f( GLog.E, "Tag \"%s\" is not well defined. Please set all mandatory fields." % tagDsc.get_type() )
      sys.exit(1)

    if tagDsc.has_numeral_name() == True:
      GLog.f( GLog.E,"Too many arguments: tag \"%s\" does not require a name argument" % tagDsc.get_type() )
      sys.exit(1)


  if options.all == True:
    ret = All( options )
    sys.exit( ret )

  if os.environ.get('SWCHECK') != "NO":
    if check(options) != 0:
      sys.exit(1)
  
  if os.environ.get('SWCHECK') == "ONLY":
    sys.exit(0)

  ret = execute(options)
  if ret != 0:
    sys.exit( 1 )
  sys.exit( 0 )

  
gittag_mgt_options = [
    [ 
      "-d",
      "--delete",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "delete",
        "metavar" : "<tag_name>",
        "help"    : "Deleted local tag"
        }
      ],
    [ 
      "-e",
      "--erase",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "erase",
        "metavar" : "<tag_name>",
        "help"    : "Deleted tag also on remote repository"
        }
      ],
    [ 
      "--replace",
      {
        "action"  : "store_true",
        "dest"    : "replace",
        "default" : False,
        "help"    : 'Move down last tag created (DEV or RDY) over last commit done'
        }
      ],
    [ 
      "-m",
      "--message",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "msg",
        "default" : "",
        "metavar" : "<message>",
        "help"    : "Specify tag message"
        }
      ],
     [ 
      "-M",
      "--reuse-message",
      {
        "action"  : "store_true",
        "dest"    : "reuse_message",
        "default" : False,
        "help"    : "Use message from attached commit"
        }
     ],
     [ 
      "--all",
      {
        "action"  : "store_true",
        "dest"    : "all",
        "default" : False,
        "help"    : "Execute tag over all repositories of current project"
        }
     ]
   ]


gittag_rtrv_options = [
    [ 
      "--int",
      {
        "action"  : "store_true",
        "dest"    : "int",
        "default" : False,
        "help"    : 'List all integration tags'
        }
      ],
    [ 
      "-l",
      "--list",
      {
        "action"  : "store_true",
        "dest"    : "list",
        "default" : False,
        "help"    : 'Shortcut for listing all current branch labels.'
        }
      ],
    [ 
      "-R",
      "--release-selector",
      {
         "nargs"   : 1,
        "action"  : "store",
        "dest"    : "rel",
        "metavar" : "<release_val>",
        "help"    : 'List all tags given a specified release'
        }
      ],
    [
      "-U",
      "--user-selector",
      {
        "nargs"   : 1,
        "action"  : "store",
        "dest"    : "user",
        "metavar" : "<user_val>",
        "help"    : 'List all tags given a specific user'
        }
      ],
     [
       "-B",
       "--branch-type-selector",
       {
         "nargs"   : 1,
         "action"  : "store",
         "dest"    : "typeB",
         "metavar" : "<branch_type_val>",
         "help"    : 'List all tags given a specific branch type (i.e. FTR or FIX)'
         }
       ],
     [
       "-N",
       "--branch-name-selector",
       {
         "nargs"   : 1,
         "action"  : "store",
         "dest"    : "nameB",
         "metavar" : "<branch_name_val>",
         "help"    : 'List all tags given a specific branch name'
         }
       ],
     [
       "-T",
       "--tag-type-selector",
       {
         "nargs"   : 1,
         "action"  : "store",
         "dest"    : "typeL",
         "metavar" : "<tag_type_val>",
         "help"    : 'List all tags given a specific tag type ( one among {%s} )' % "|".join( TagDsc.get_all_tagtypes() )
         }
       ],
     [
       "-L",
       "--tag-label-selector",
       {
         "nargs"   : 1,
         "action"  : "store",
         "dest"    : "nameL",
         "metavar" : "<tag_name_val>",
         "help"    : 'List all tags given a specific tag name'
         }
       ]
    ]

gittag_custtag_options = [
    [ 
      "--custom-tag-list",
      {
        "action"  : "store_true",
        "dest"    : "custtag_list",
        "default" : False,
        "help"    : 'List all user defined tags'
        }
      ],
    [ 
      "--custom-tag-show-cfg",
      {
        "nargs"   : 1,
        "type"    : "string",
        "action"  : "callback",
        "callback": check_input,
        "dest"    : "custtag_showcfg",
        "metavar" : "<tag_type_val>",
        "help"    : "Specify tag type and get configuration options"
        }
      ]

    ]


if __name__ == "__main__":
  main()
  
