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

import sys,string,re
from ObjBranch import *
from ObjCfg import *


#############
#    TAG    #
#############
class Tag:
  def __init__( self, tag, root = "." ):
    self.tag_     = tag
    self.fullRef_ = ""
    self.root_    = root
    self.isValid_  = False
    self.matches_  = []
    self.tokens_   = []

    cmd = "cd %s && git show-ref --tags %s" % (self.root_, self.tag_)
    outerr, errCode = myCommand_fast( cmd )
    if errCode != 0:
      return

    for line in outerr.splitlines():
      hash, ref = line.split( ' ' )
      if ref.find( "refs/tags/%s" % SWCFG_TAG_NAMESPACE_PAST ) == 0:
        continue
      if not is_valid_swgit_tag( ref ):
        continue
      self.matches_.append( ref )

    if len( self.matches_ ) != 1:
      return

    self.fullRef_ = self.matches_[0]
    self.isValid_ = True
    self.tokens_  = self.fullRef_.split("/")
    return


  def isValid( self ):
    return self.isValid_

  def getNotValidReason( self ):
    if len( self.getMatches() ) > 0:
      strerr  = "Multiple matches found, please specify one among:\n"
      for b in self.getMatches():
        strerr += "  %s\n" % b[ findnth( b, "/", 2 ) + 1 : ]
      return strerr
    else:
      return "Tag %s does not exists" % self.tag_

  def getMatches( self ):
    return self.matches_

  def getTokens( self ):
    return self.tokens_

  def getFullRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.fullRef_

  def getBrStr( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "/".join( self.tokens_[2:9] )

  def getRepo( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "tags"

  def getRel( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "/".join( self.tokens_[2:6] )

  def getUser( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    r = self.fullRef_
    return r[ rfindnth( r, '/', 5 ) + 1 : rfindnth( r, '/', 4 ) ]

  def getBrType( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[7]

  def getBrName( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[8]

  def getType( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[9]

  def getName( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return self.tokens_[10]

  def getShortRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "/".join( self.tokens_[9:] )

  def getTagShortRef( self ):
    if not self.isValid_:
      return self.getNotValidReason()
    return "/".join( self.tokens_[2:] )


  @staticmethod
  def list_by_branch( br_name_list, typeL="*" ):
    total = []
    #tag must not rely on branch existence. We can delete branch
    for b in br_name_list:

      if not is_valid_swgit_branch( b ):
        print " Tag.list_by_branch() - invalid branch name: %s" % b
        continue

      rel  = br_2_rel( b )
      user = br_2_user( b )
      type = br_2_type( b )
      name = br_2_name( b )

      err, tags = Tag.list( rel, user, type, name, typeL )
      if err != 0:
        print " Tag.list_by_branch() - error in Tag.list"
        continue

      total.extend( tags )

    return 0,total


  @staticmethod
  def list( rel="*/*/*/*", user="*", typeB="*", nameB="*", typeL="*", nameL="*" ):

    ref_into_cmd = "\"refs/tags/%s/%s/%s/%s/%s/%s\"" % (rel,user,typeB,nameB,typeL,nameL)
    cmd="git for-each-ref --sort='*authordate' --format='%%(refname:short)' %s" % ref_into_cmd
    out, errCode = myCommand_fast( cmd )
     
    if errCode !=0:
      return errCode, []
    tags=out.splitlines()

    return errCode, tags


################
#    TAGDSC    #
################

#factory
def create_tag_dsc( type ):
  type = type.upper()

  #builtin tags
  if type == SWCFG_TAG_LIV:
    return TagLIVDsc()
  elif type == SWCFG_TAG_STB:
    return TagSTBDsc()
  elif type == SWCFG_TAG_DEV:
    return TagDEVDsc()
  elif type == SWCFG_TAG_FIX:
    return TagFIXDsc()
  elif type == SWCFG_TAG_RDY:
    return TagRDYDsc()
  elif type == SWCFG_TAG_NGT:
    return TagNGTDsc()
  elif type == SWCFG_TAG_NEW:
    return TagNEWDsc()

  #custom tags
  return TagDsc( type )


class TagDsc( ObjCfgTag ):
  DEFAULT_TAG_INT_LIST   = [ SWCFG_TAG_LIV, SWCFG_TAG_STB, SWCFG_TAG_NGT ]
  DEFAULT_TAG_USER_LIST  = [ SWCFG_TAG_DEV, SWCFG_TAG_FIX, SWCFG_TAG_RDY ]
  DEFAULT_TAG_OTHER      = [ SWCFG_TAG_NEW ]

  DEFAULT_CUSTOMTAG_CFG = """\
#
# Inside this file user can:
#  1. Provide sensible defaults for built-in tags
#  2. Define new tags to be used with "swgit tag" command
#
# Please run
#   swgit --tutorial-customtags
# for more informations
#
#[LABEL-TYPE]            =
#regexp                  =
#push-on-origin          =
#one-x-commit            =
#only-on-integrator-repo =
#allowed-brtypes         =
#denied-brtypes          =
#tag-in-past             =
#hook-pretag-script      =
#hook-pretag-sshuser     =
#hook-pretag-sshaddr     =
#hook-posttag-script     =
#hook-posttag-sshuser    =
#hook-posttag-sshaddr    =
"""

  def __init__( self, tagtype, loadcfg = True ):

    self.isDefault_   = False
    self.type_        = tagtype.upper()

    #start - not configurable, so here instead of ObjCfgTag
    self.merge_on_develop_    = False
    self.merge_on_stable_     = False
    self.merge_on_cst_        = False
    #end

    super(TagDsc, self ).__init__( self.type_ )

    if loadcfg:
      self.load_cfg()


  def dump( self ):
    j = self.justify_
    retstr = ""
    retstr += "Tag Type".ljust( j )              + self.type_
    retstr += "\n" + "Is Deafult Tag".ljust( j ) + str( self.isDefault_ )
    retstr += "\n" + super(TagDsc, self ).dump()
    return retstr

  def get_type( self ):
    return self.type_
  def get_is_default( self ):
    return self.isDefault_

  def get_regexp_optional_field( self, defval ):
    return  [ [ self.set_regexp, self.get_regexp, "Tag argument regexp", SWCFG_KEY_TAGDSC_REGEXP, "", defval ] ]

  def set_merge_on_develop( self, v ):
    self.merge_on_develop_ = v
  def get_merge_on_develop( self ):
    return self.merge_on_develop_
  def set_merge_on_stable( self, v ):
    self.merge_on_stable_ = v
  def get_merge_on_stable( self ):
    return self.merge_on_stable_
  def set_merge_on_cst( self, v ):
    self.merge_on_cst_ = v
  def get_merge_on_cst( self ):
    return self.merge_on_cst_

  def has_numeral_name( self ):
    #no regexp => numeral name
    if len( self.regexp_ ) > 0:
      return False
    return True

  def check_valid_value( self, value ):
    for r in self.get_regexp():
      #print "regexp: %s" % r
      curr_re = re.compile( r )
      matches = curr_re.findall( value )
      if len( matches ) > 0:
        return True
    return False

  @staticmethod
  #
  # You can define tagtypes by file or by config
  #  file:   $REPOROOT/.swDIR/SWFILE_TAGDESC
  #  config: git config swgit.tagtype.<newtagtype>
  #
  def get_all_tagtypes():
    #BUILT-IN
    ret_list = TagDsc.DEFAULT_TAG_INT_LIST + TagDsc.DEFAULT_TAG_USER_LIST + TagDsc.DEFAULT_TAG_OTHER

    #CONFIGUREN by FILE
    config = ConfigParser.RawConfigParser()
    try:
      config.read( "%s/%s" % (Env.getLocalRoot( fexit = False ), SWFILE_TAGDESC) )
    except Exception, e:
      return ret_list

    ret_list += config.sections()

    #CONFIGUREN by git config
    taglist, errCode = get_repo_cfg_regexp( SWCFG_PREFIX + SWCFG_KEY_TAGDSC_TAGTYPE + "*$" )
    #print "[%s]" % taglist[:-1]
    #print taglist.splitlines()
    if errCode == 0:
      config_labels = taglist.splitlines()
      for t in config_labels:
        (key, val) = t.split(' ')
        #print "key[%s], val[%s]", key, val
        tagname = key.replace( SWCFG_PREFIX + SWCFG_KEY_TAGDSC_TAGTYPE, '' )
        tagname = tagname.upper()
        ret_list.append( tagname )

    return ret_list



class TagLIVDsc( TagDsc ):
  def __init__( self ):
    self.type_        = SWCFG_TAG_LIV
    super(TagLIVDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_regexp_optional_field( SWCFG_TAG_LIVREGEXP ) + 
                              self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_           = True
    #if self.regexp_ == [ ObjCfg.NOT_INIT ]:
    #  self.regexp_ = [ SWCFG_TAG_LIVREGEXP ] #default value
    self.merge_on_develop_        = True
    self.merge_on_stable_         = True
    self.merge_on_cst_            = True
    self.push_on_origin_          = True
    self.one_x_commit_            = True
    self.only_on_integrator_repo_ = True
    self.allowed_brtypes_         = [ SWCFG_BR_INT, SWCFG_BR_CST ]
    self.denied_brtypes_          = []
    self.tag_in_past_             = True
    self.isValid_                 = True




class TagSTBDsc( TagDsc ):
  def __init__( self ):
    self.type_      = SWCFG_TAG_STB
    super(TagSTBDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_regexp_optional_field( SWCFG_TAG_LIVREGEXP ) + 
                              self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_               = True
    self.merge_on_develop_        = True
    self.merge_on_stable_         = True
    self.merge_on_cst_            = True
    self.push_on_origin_          = True
    self.one_x_commit_            = True
    self.only_on_integrator_repo_ = True
    self.allowed_brtypes_         = [ SWCFG_BR_INT, SWCFG_BR_CST ]
    self.denied_brtypes_          = []
    self.tag_in_past_             = True
    self.isValid_                 = True



class TagDEVDsc( TagDsc ):
  def __init__( self ):
    self.type_      = SWCFG_TAG_DEV
    super(TagDEVDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_               = True
    self.regexp_                  = []
    self.merge_on_develop_        = True
    self.merge_on_stable_         = True
    self.merge_on_cst_            = True
    self.push_on_origin_          = True
    self.one_x_commit_            = True
    self.only_on_integrator_repo_ = False
    self.allowed_brtypes_         = [ SWCFG_BR_FTR,SWCFG_BR_FIX ]
    self.denied_brtypes_          = []
    self.tag_in_past_             = False
    self.isValid_                 = True


class TagFIXDsc( TagDsc ):
  def __init__( self ):
    self.type_      = SWCFG_TAG_FIX
    super(TagFIXDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_regexp_optional_field( "^Issue[0-9]{5}$%s^[0-9]{7}$" % SWCFG_KEY_TAGDSC_LIST_DELIMITER ) +
                              self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_               = True
    self.merge_on_develop_        = False
    self.merge_on_stable_         = False
    self.merge_on_cst_            = False
    self.push_on_origin_          = True
    self.one_x_commit_            = False
    self.only_on_integrator_repo_ = False
    self.allowed_brtypes_         = [ SWCFG_BR_FTR, SWCFG_BR_FIX ]
    self.denied_brtypes_          = []
    self.tag_in_past_             = True
    self.isValid_                 = True


class TagRDYDsc( TagDsc ):
  def __init__( self ):
    self.type_      = SWCFG_TAG_RDY
    super(TagRDYDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_                = True
    self.regexp_                   = []
    self.merge_on_develop_         = False
    self.merge_on_stable_          = False
    self.merge_on_cst_             = False
    self.push_on_origin_           = False
    self.one_x_commit_             = True
    self.only_on_integrator_repo_  = False
    self.allowed_brtypes_          = []
    self.denied_brtypes_           = []
    self.tag_in_past_              = True
    self.isValid_                  = True


class TagNGTDsc( TagDsc ):

  def __init__( self ):
    self.type_ = SWCFG_TAG_NGT
    super(TagNGTDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_regexp_optional_field( SWCFG_TAG_LIVREGEXP ) +
                              self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_               = True
    self.merge_on_develop_        = True
    self.merge_on_stable_         = True
    self.merge_on_cst_            = True
    self.push_on_origin_          = True
    self.one_x_commit_            = False
    self.only_on_integrator_repo_ = True
    self.allowed_brtypes_         = []
    self.denied_brtypes_          = []
    self.tag_in_past_             = True
    self.isValid_                 = True

class TagNEWDsc( TagDsc ):

  def __init__( self ):
    self.type_ = SWCFG_TAG_NEW
    super(TagNEWDsc, self ).__init__( self.type_, loadcfg = False )

    self.set_fields_mandatory( [] )
    self.set_fields_optional( self.get_regexp_optional_field( SWCFG_TAG_NEWREGEXP ) +
                              self.get_hook_optional_field_default() )

    self.load_cfg()

    self.isDefault_               = True
    self.merge_on_develop_        = False
    self.merge_on_stable_         = False
    self.merge_on_cst_            = False
    self.push_on_origin_          = False #will be pushed by hand
    self.one_x_commit_            = False
    self.only_on_integrator_repo_ = False
    self.allowed_brtypes_         = []
    self.denied_brtypes_          = []
    self.tag_in_past_             = True
    self.isValid_                 = True





def main():

  if len( sys.argv ) == 2:

    print "\nTesting Tag class with ref: " + sys.argv[1] + "\n"
    t = Tag( sys.argv[1] )
    print "  tokens:         [" + " ".join( t.getTokens() ) + "]\n"
    print "  getFullRef:     [" + t.getFullRef() + "]\n"

    print "  isValid:        [" + str( t.isValid() ) + "]\n"
    print "  matches:        [" + "\n".join( t.getMatches() ) + "]\n"

    print "  getRel:         [" + t.getRel() + "]\n"
    print "  getRepo:        [" + t.getRepo() + "]\n"
    print "  getName:        [" + t.getName() + "]\n"
    print "  getType:        [" + t.getType() + "]\n"
    print "  getBrStr:       [" + t.getBrStr() + "]\n"
    print "  getShortRef:    [" + t.getShortRef() + "]\n"
    print "  getTagShortRef: [" + t.getTagShortRef() + "]\n"
    print "  its str branch: [" + t.getBrStr() + "]\n"
    itsBr = Branch( t.getBrStr() )
    print "  its branch:     {" + str(itsBr) + "}\n"

    err, labels = Tag.list_by_branch( [ t.getBrStr() ] )
    print "  tags by branch: {" + " ".join( labels ) + "}\n"

    sys.exit(0)

  elif len( sys.argv ) == 3:
    if sys.argv[1] == "-t":

      print "\nallsections: %s\n" % TagDsc.get_all_tagtypes()
      print "Retrieving description for tag: %s\n" % sys.argv[2]
      d = create_tag_dsc( sys.argv[2] )
      print d.show_config_options()
      print ""
      print d.dump()

      sys.exit(0)

  print "Usage: ObjTag <reference> or ObjTag -t <tagtype>"
  sys.exit(1)


if __name__ == "__main__":
    main()



