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

import ConfigParser
from Defines import *
from ObjEnv import *

##########
# OBJCFG #
##########
#
# Every subclass must 
#   initialize its fields
#      self.f_string = "SOMETHING"
#      self.f_bool   = True or False
#      self.f_list   = [ "something" ]
#
#   declare its self.fields_mandatory_ array with
#     set accessor | get accessor | key for file and config  | high priority config alias
#   declare its self.fields_optional_ array with
#     set accessor | get accessor | key for file and config  | high priority config alias | default val
#
class ObjCfg( object ):

  NOT_INIT = "@@ MANDATORY FIELD NOT INITIALIZED @@"

  def __init__( self, file, section ):

    self.isValid_ = False
    self.file_    = file
    self.section_ = section
    self.justify  = 35
    self.error_fields_  = []

    self.config_  = ConfigParser.RawConfigParser()
    try:
      self.config_.read( "%s/%s" % (Env.getLocalRoot( fexit = False ), self.file_) )
    except Exception, e:
      return



  def load_cfg( self ):

    self.isValid_ = True

    #
    # Mandatory
    #
    for (ms, mg, d, k, hpa) in self.fields_mandatory_:
      #print ">> MANDAT: ", d, self.section_
      v = "@@ Mandatory field not set @@"
      try:
        v = self.load_mandatory_field( k, hpa )

        if isinstance( mg(), list ): #list mgt
          v = self.split_filed_list( v )
        elif isinstance( mg(), bool ): #bool mgt
          if v.upper() == "TRUE":
            v = True
          elif v.upper() == "FALSE":
            v = False
          else:
            v = "@@ Not Valid bool @@"
            raise Exception( "Invalid input in field %s" % ( key ) )

        ms( v )
      except Exception, e:
        #print ">> EXCEPTION MANDAT: ", d
        self.isValid_ = False
        self.error_fields_.append( k )
        ms( v )

    #
    # Optional
    #
    for (ms, mg, d, k, hpa, df) in self.fields_optional_:
      #print ">> OPION: ", d, self.section_

      v = self.load_optional_field( k, hpa, df )

      #list mgt
      if isinstance( mg(), list ):
        v = self.split_filed_list( v )
      elif isinstance( mg(), bool ):
        #bool mgt
        if v.upper() == "TRUE":
          v = True
        elif v.upper() == "FALSE":
          v = False
        else:
          ms( "@@ Not Valid bool @@" )
          self.isValid_ = False
          self.error_fields_.append( k )
          continue

      ms( v )


  def isValid( self ):
    return self.isValid_

  def dump( self ):
    j = self.justify_
    retstr = "Is valid".ljust(j) + "%s" % self.isValid_
    for (ms, mg, d, k, hpa) in self.fields_mandatory_:
      retstr += "\n" + ("%s" % d).ljust(j) + "%s" % mg()
    for (ms, mg, d, k, hpa, df) in self.fields_optional_:
      retstr += "\n" + ("%s" % d).ljust(j) + "%s" % mg()

    if len( self.error_fields_ ) > 0:
      retstr += "\n\nFor each wrong field, you can set it in this way:"

    for e in self.error_fields_:
      #print self.section_,  e
      retstr += self.show_config_options_byfield( e )
    return retstr + "\n"


  def show_config_options_byfield_int( self, d, k, hpa ):
    j = self.justify_
    retstr = ("\n * %s" % d).ljust( j )

    if hpa != "":
      retstr += "by \"git config %s <val>\"" % (hpa)
      retstr += "\n ".ljust(j)
    retstr += "by \"git config %s.%s.%s <val>\"" % (SWCFG_PREFIX, self.section_, k)
    retstr += "\n ".ljust( j ) + "or by editing file: %s, section %s, key %s" % (self.file_,self.section_,k)
    return retstr

  def show_config_options_byfield( self, key ):
    for (ms, mg, d, k, hpa) in self.fields_mandatory_:
      if k == key:
        return self.show_config_options_byfield_int( d, k, hpa )
    for (ms, mg, d, k, hpa, df) in self.fields_optional_:
      if k == key:
        return self.show_config_options_byfield_int( d, k, hpa )


  def show_config_options( self ):
    j = self.justify_
    retstr = ""

    if len( self.fields_mandatory_ ) > 0:
      retstr += "\nMandatory fields:\n"
      for (ms, mg, d, k, hpa) in self.fields_mandatory_:
          retstr += self.show_config_options_byfield( k )

    if len( self.fields_optional_ ) > 0:
      retstr += "\nOptional fields:\n"
      for (ms, mg, d, k, hpa, df) in self.fields_optional_:
          retstr += self.show_config_options_byfield( k )

    return retstr

  #
  # This method loads a field:
  #  1. look among hp_config as is (high prio)
  #  2. look among config swgit.section.key
  #  3. look among file/section/key
  #
  #  mandatory => raises exception if not found
  #  optional  => just return "" if not found
  #
  #  some hp_cfg_alias example: user.name or user.email
  #
  def load_mandatory_field( self, key, alias ):
    try:
      #1.1 local
      if alias != "":
        val, errCode = get_repo_cfg( alias )
        if errCode == 0:
          if val[:-1] == "":
            raise Exception( "Empty value not allowed for mandatory field %s in section %s" % ( key, self.section_ ) )
          else:
            return val[:-1]

      #1.2 global
      if alias != "":
        val, errCode = get_repo_cfg( alias, fglobal = True )
        if errCode == 0:
          if val[:-1] == "":
            raise Exception( "Empty value not allowed for mandatory field %s in section %s" % ( key, self.section_ ) )
          else:
            return val[:-1]

      #2.
      config_key = "%s.%s.%s" % ( SWCFG_PREFIX, self.section_, key )
      val, errCode = get_repo_cfg( config_key )
      if errCode == 0:
        if val[:-1] == "":
          raise Exception( "Empty value not allowed for mandatory field %s in section %s" % ( key, self.section_ ) )
        else:
          return val[:-1]

      #3.
      val =  self.config_.get( self.section_, key ) #this will raise exception if not exists
      if val[:-1] == "":
        raise Exception( "Empty value not allowed for mandatory field %s in section %s" % ( key, self.section_ ) )
      else:
        return val
    except Exception, e:
      #print e
      #raise Exception( "Not found mandatory field %s nor its alias %s for cfg %s" % ( key, alias, self.section_ ) )
      raise e


  def load_optional_field( self, key, alias, defval ):
    #1.
    val, errCode = get_repo_cfg( "%s" % ( alias ) )
    if errCode == 0:
      return val[:-1]

    #2.
    val, errCode = get_repo_cfg( "%s.%s.%s" % ( SWCFG_PREFIX, self.section_, key ) )
    if errCode == 0:
      return val[:-1]

    #3.
    try:
      val = self.config_.get( self.section_, key ) #this will raise exception if not exists
      return val
    except Exception, e:
      #not found optional field, not an error
      pass

    return defval

  def split_filed_list( self, field ):
    listfield = []
    listfield = field.split( SWCFG_KEY_TAGDSC_LIST_DELIMITER )
    for a in listfield:
      if a == "":
        listfield.remove( a )
    return listfield

  def set_fields_mandatory( self, v ):
    self.fields_mandatory_ = v
  def get_fields_mandatory( self ):
    return self.fields_mandatory_
  def set_fields_optional( self, v ):
    self.fields_optional_ = v
  def get_fields_optional( self ):
    return self.fields_optional_



#############
# MAIL BASE #
#############
class ObjCfgMail( ObjCfg ):

  def __init__( self, file, section ):

    super(ObjCfgMail, self ).__init__( file, section )

    self.justify_ = 16

    self.sshuser_ = ObjCfg.NOT_INIT
    self.sshaddr_ = ObjCfg.NOT_INIT
    self.from_    = ObjCfg.NOT_INIT
    self.to_      = ObjCfg.NOT_INIT
    self.cc_      = ObjCfg.NOT_INIT
    self.bcc_     = ObjCfg.NOT_INIT
    self.subj_    = ObjCfg.NOT_INIT
    self.bodyH_   = ObjCfg.NOT_INIT
    self.bodyF_   = ObjCfg.NOT_INIT

    self.fields_mandatory_ = [ 
        [self.set_from   , self.get_from   , "from"       , SWFILE_MAILCFG_FROM              , "" ],
        [self.set_to     , self.get_to     , "to"         , SWFILE_MAILCFG_TO                , "" ],
        ]

    self.fields_optional_ = [ 
        [self.set_sshuser, self.get_sshuser, "sshuser"    , SWFILE_MAILCFG_MAILSERVER_SSHUSER, "", "" ],
        [self.set_sshaddr, self.get_sshaddr, "sshaddr"    , SWFILE_MAILCFG_MAILSERVER_SSHADDR, "", "" ],
        [self.set_cc     , self.get_cc     , "cc"         , SWFILE_MAILCFG_CC                , "", "" ],
        [self.set_bcc    , self.get_bcc    , "bcc"        , SWFILE_MAILCFG_BCC               , "", "" ],
        [self.set_subj   , self.get_subj   , "subject"    , SWFILE_MAILCFG_SUBJ              , "", "" ],
        [self.set_bodyH  , self.get_bodyH  , "body header", SWFILE_MAILCFG_BODY_HEADER       , "", "" ],
        [self.set_bodyF  , self.get_bodyF  , "body footer", SWFILE_MAILCFG_BODY_FOOTER       , "", "" ],
        ]


  def set_sshuser( self, v ):
    self.sshuser_ = v
  def get_sshuser( self ):
    return self.sshuser_
  def set_sshaddr( self, v ):
    self.sshaddr_ = v
  def get_sshaddr( self ):
    return self.sshaddr_
  def set_from( self, v ):
    self.from_ = v
  def get_from( self ):
    return self.from_
  def set_to( self, v ):
    self.to_ = v
  def get_to( self ):
    return self.to_
  def set_cc( self, v ):
    self.cc_ = v
  def get_cc( self ):
    return self.cc_
  def set_bcc( self, v ):
    self.bcc_ = v
  def get_bcc( self ):
    return self.bcc_
  def set_subj( self, v ):
    self.subj_ = v
  def get_subj( self ):
    return self.subj_
  def set_bodyH( self, v ):
    self.bodyH_ = v
  def get_bodyH( self ):
    return self.bodyH_
  def set_bodyF( self, v ):
    self.bodyF_ = v
  def get_bodyF( self ):
    return self.bodyF_


#######
# TAG #
#######
class ObjCfgTag( ObjCfg ):

  def __init__( self, tagtype ):

    self.type_                = tagtype.upper()

    super(ObjCfgTag, self ).__init__( SWFILE_TAGDESC, self.type_ )

    self.justify_              = 35

    self.regexp_               = [ ObjCfg.NOT_INIT ]
    self.push_on_origin_       = False
    self.one_x_commit_         = False
    self.only_on_integrator_repo_     = False
    self.allowed_brtypes_      = [ ObjCfg.NOT_INIT ]
    self.denied_brtypes_       = [ ObjCfg.NOT_INIT ]
    self.tag_in_past_          = False
    self.hook_pretag_script_   = ObjCfg.NOT_INIT
    self.hook_pretag_sshuser_  = ObjCfg.NOT_INIT
    self.hook_pretag_sshaddr_  = ObjCfg.NOT_INIT
    self.hook_posttag_script_  = ObjCfg.NOT_INIT
    self.hook_posttag_sshuser_ = ObjCfg.NOT_INIT
    self.hook_posttag_sshaddr_ = ObjCfg.NOT_INIT

    self.fields_mandatory_ = [ 
          [ self.set_push_on_origin, 
            self.get_push_on_origin,
            "Pushable on origin"         , SWCFG_KEY_TAGDSC_PUSH_ON_ORIGIN      , "" ],
          [ self.set_one_x_commit, 
            self.get_one_x_commit,
            "One tag per commit"         , SWCFG_KEY_TAGDSC_ONE_X_COMMIT        , "" ],
          [ self.set_only_on_integrator_repo, 
            self.get_only_on_integrator_repo,
            "Issueable only on integrator repo", SWCFG_KEY_TAGDSC_ONLY_ON_INTEGRATOR_REPO   , "" ],
          ]

    self.fields_optional_ = [ 
          [ self.set_regexp, 
            self.get_regexp,
            "Tag argument regexp"        , SWCFG_KEY_TAGDSC_REGEXP              , "", "" ],
          [ self.set_allowed_brtypes, 
            self.get_allowed_brtypes,
            "Allowed branch types"       , SWCFG_KEY_TAGDSC_ALLOWED_BRTYPES     , "", "" ],
          [ self.set_denied_brtypes, 
            self.get_denied_brtypes,
            "Denied  branch types"       , SWCFG_KEY_TAGDSC_DENIED_BRTYPES      , "", "" ],
          [ self.set_tag_in_past, 
            self.get_tag_in_past,
            "Allow tagging in past"      , SWCFG_KEY_TAGDSC_TAG_IN_PAST, "", "False" ],
          ] + self.get_hook_optional_field_default()

  #reused in subclasses
  def get_hook_optional_field_default( self ):
    return [
          [ self.set_hook_pretag_script, 
            self.get_hook_pretag_script,
            "Hook pre-tag script"        , SWCFG_KEY_TAGDSC_HOOK_PRETAG_SCRIPT  , "", "" ],
          [ self.set_hook_pretag_sshuser, 
            self.get_hook_pretag_sshuser,
            "Hook pre-tag ssh user"      , SWCFG_KEY_TAGDSC_HOOK_PRETAG_SSHUSER , "", "" ],
          [ self.set_hook_pretag_sshaddr, 
            self.get_hook_pretag_sshaddr,
            "Hook pre-tag ssh addr"      , SWCFG_KEY_TAGDSC_HOOK_PRETAG_SSHADDR , "", "" ],
          [ self.set_hook_posttag_script, 
            self.get_hook_posttag_script,
            "Hook post-tag script"       , SWCFG_KEY_TAGDSC_HOOK_POSTTAG_SCRIPT , "", "" ],
          [ self.set_hook_posttag_sshuser, 
            self.get_hook_posttag_sshuser,
            "Hook post-tag ssh user"     , SWCFG_KEY_TAGDSC_HOOK_POSTTAG_SSHUSER, "", "" ],
          [ self.set_hook_posttag_sshaddr, 
            self.get_hook_posttag_sshaddr,
            "Hook post-tag ssh addr"     , SWCFG_KEY_TAGDSC_HOOK_POSTTAG_SSHADDR, "", "" ],
          ]


  def set_regexp( self, v ):
    self.regexp_ = v
  def get_regexp( self ):
    return self.regexp_
  def set_push_on_origin( self, v ):
    self.push_on_origin_ = v
  def get_push_on_origin( self ):
    return self.push_on_origin_
  def set_one_x_commit( self, v ):
    self.one_x_commit_ = v
  def get_one_x_commit( self ):
    return self.one_x_commit_
  def set_only_on_integrator_repo( self, v ):
    self.only_on_integrator_repo_ = v
  def get_only_on_integrator_repo( self ):
    return self.only_on_integrator_repo_
  def set_allowed_brtypes( self, v ):
    self.allowed_brtypes_ = v
  def get_allowed_brtypes( self ):
    return self.allowed_brtypes_
  def set_denied_brtypes( self, v ):
    self.denied_brtypes_ = v
  def get_denied_brtypes( self ):
    return self.denied_brtypes_
  def set_tag_in_past( self, v ):
    self.tag_in_past_ = v
  def get_tag_in_past( self ):
    return self.tag_in_past_
  def set_hook_pretag_script( self, v ):
    self.hook_pretag_script_ = v
  def get_hook_pretag_script( self ):
    return self.hook_pretag_script_
  def set_hook_pretag_sshuser( self, v ):
    self.hook_pretag_sshuser_ = v
  def get_hook_pretag_sshuser( self ):
    return self.hook_pretag_sshuser_
  def set_hook_pretag_sshaddr( self, v ):
    self.hook_pretag_sshaddr_ = v
  def get_hook_pretag_sshaddr( self ):
    return self.hook_pretag_sshaddr_
  def set_hook_posttag_script( self, v ):
    self.hook_posttag_script_ = v
  def get_hook_posttag_script( self ):
    return self.hook_posttag_script_
  def set_hook_posttag_sshuser( self, v ):
    self.hook_posttag_sshuser_ = v
  def get_hook_posttag_sshuser( self ):
    return self.hook_posttag_sshuser_
  def set_hook_posttag_sshaddr( self, v ):
    self.hook_posttag_sshaddr_ = v
  def get_hook_posttag_sshaddr( self ):
    return self.hook_posttag_sshaddr_


class ObjCfgSnap( ObjCfg ):

  def __init__( self, section ):

    super(ObjCfgSnap, self ).__init__( SWFILE_SNAPCFG, section )

    self.justify_ = 35

    self.url_    = ObjCfg.NOT_INIT
    self.branch_ = ObjCfg.NOT_INIT
    self.format_ = ObjCfg.NOT_INIT
    self.bintar_ = ObjCfg.NOT_INIT

    self.fields_mandatory_ = [ 
        [self.set_url   , self.get_url    , "url"   , SWFILE_SNAPCFG_URL   , "" ],
        [self.set_branch, self.get_branch , "branch", SWFILE_SNAPCFG_BRANCH, "" ],
        ]

    self.fields_optional_ = [ 
        [self.set_format, self.get_format, "archive type (tar,zip)",     SWFILE_SNAPCFG_AR_FORMAT, "", "tar" ],
        [self.set_bintar, self.get_bintar, "archive tool (/bin/tar...)", SWFILE_SNAPCFG_AR_TOOL,   "", "tar" ],
        ]

  def set_url( self, v ):
    self.url_ = v
  def get_url( self ):
    return self.url_
  def set_branch( self, v ):
    self.branch_ = v
  def get_branch( self ):
    return self.branch_
  def set_format( self, v ):
    self.format_ = v
  def get_format( self ):
    return self.format_
  def set_bintar( self, v ):
    self.bintar_ = v
  def get_bintar( self ):
    return self.bintar_
  #def set_alwaysupd( self, v ):
  #  self.alwaysupd_ = v
  #def get_alwaysupd( self ):
  #  return self.alwaysupd_




def main():

  objs = []

  objcfg = ObjCfgMail( SWFILE_MAILCFG, SWFILE_MAILCFG_STABILIZE_SECT )
  objs.append( objcfg )
  objcfg = ObjCfgMail( SWFILE_MAILCFG, SWFILE_MAILCFG_PUSH_SECT )
  objs.append( objcfg )

  for o in objs:
    print "\n", '#'*10, o, '#'*10, "\n"
    print o.dump()
    print ""
    print o.show_config_options()


if __name__ == "__main__":
    main()
