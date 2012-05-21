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

from Defines import *
from Utils import *
from ObjEnv import *
from ObjCfg import *


class ObjMailBase( ObjCfgMail ):
  DEFAULT_MAIL_CFG = """\
#
# Inside this file user can provide sensible defaults for mail delivery
#
# Please run
#   swgit --tutorial-mailcfg
# for more informations
#
#[%s]
#mailserver-sshuser = 
#mailserver-sshaddr = 
#from               = 
#to                 = 
#to-1               = 
#to-2               = 
#cc                 = 
#cc-1               = 
#cc-2               = 
#bcc                = 
#bcc-1              = 
#bcc-2              = 
#subject            = 
#body-header        = 
#body-footer        = 
#
#[%s]
#mailserver-sshuser = 
#mailserver-sshaddr = 
#from               = 
#to                 = 
#to-1               = 
#to-2               = 
#cc                 = 
#cc-1               = 
#cc-2               = 
#bcc                = 
#bcc-1              = 
#bcc-2              = 
#subject            = 
#body-header        = 
#body-footer        = 
""" % ( SWCFG_STABILIZE_SECT, SWCFG_MAIL_PUSH_SECT )

  CMD_SEND_MAIL_TEMPL = "echo -e \"%s\" | /bin/mail \"%s\" -s \"%s\" %s %s %s"

  def __init__( self, file, section ):
    super(ObjMailBase, self ).__init__( file, section )

  def dump( self ):
    retstr = "\n"
    if self.isValid_ == False:
      retstr += "INVALID "
    retstr += "Mail configuration for %s\n" % self.section_

    retstr += super(ObjMailBase, self ).dump()
    return retstr

  def sanitize_message( self, mess ):
    for clean in [ "'", '"' ]:
      mess = mess.replace( clean, ' ' )
    return mess


  def get_all_body( self, body ):
    allbody = self.sanitize_message( self.bodyH_ )
    if self.bodyH_ != "":
      allbody += "\n"
    allbody += body
    if self.bodyF_ != "":
      allbody += "\n" + self.sanitize_message( self.bodyF_ )
    return allbody

  def get_cc_opt( self ):
    cc_opt = "" 
    if self.cc_ != "":
      cc_opt = " -c \"%s\" " % ( ",".join(self.cc_) )
    return cc_opt

  def get_bcc_opt( self ):
    bcc_opt = "" 
    if self.bcc_ != "":
      bcc_opt = " -b \"%s\" " % ( ",".join(self.bcc_) )
    return bcc_opt

  def get_from_opt( self ):
    from_opt = "" 
    if self.from_ != "":
      from_opt = " -- -f \"%s\" " % ( self.from_ )
    return from_opt

  def get_mail_cmd( self ):
    if self.isValid_ == False:
      return ""

    cmd_send_mail = self.CMD_SEND_MAIL_TEMPL % \
                     ( self.get_all_body( "BODY_HERE" ),
                       ",".join(self.to_),
                       "SUBJECT_HERE",
                       self.get_cc_opt(),
                       self.get_bcc_opt(),
                       self.get_from_opt()
                      )
    if self.sshaddr_ != "":
      return "ssh %s@%s '%s'" % (self.sshuser_, self.sshaddr_, cmd_send_mail )
    return cmd_send_mail

  def sendmail( self, body, debug ):

    if self.isValid_ == False:
      return self.dump(), 1

    cmd_send_mail = self.CMD_SEND_MAIL_TEMPL % \
                     ( self.get_all_body( body ),
                       ",".join(self.to_),
                       self.subj_,
                       self.get_cc_opt(),
                       self.get_bcc_opt(),
                       self.get_from_opt()
                      )

    if self.sshaddr_ != "":
      if debug == True:
        return "%s@%s:\n%s" % (self.sshuser_, self.sshaddr_, cmd_send_mail ), 0
      else:
        return mySSHCommand_fast( cmd_send_mail, self.sshuser_, self.sshaddr_ )
    else:
      if debug == True:
        return "localhost:\n%s" % ( cmd_send_mail ), 0
      else:
        return myCommand_fast( cmd_send_mail )


################
# STABILIZE MAIL #
################
class ObjMailStabilize( ObjMailBase ):
  def __init__( self ):
    super(ObjMailStabilize, self ).__init__( SWFILE_MAILCFG, SWCFG_STABILIZE_SECT )
    self.load_cfg()

#############
# PUSH MAIL #
#############
class ObjMailPush( ObjMailBase ):
  def __init__( self ):
    super(ObjMailPush, self ).__init__( SWFILE_MAILCFG, SWCFG_MAIL_PUSH_SECT )

    #override "to"
    self.fields_mandatory_[1] = [self.set_to, self.get_to, "to" , SWCFG_MAIL_TO, GITCFG_USERMAIL ]

    self.load_cfg()


def main():
  for o in ( ObjMailStabilize, ObjMailPush ):
    obj = o()
    print "\n", '#'*10, o, '#'*10, "\n"
    print obj.show_config_options()
    print ""
    print obj.dump()
    print ""
    print "Sending mail"

    out, errCode = obj.sendmail( "body\nbody", debug = True )
    print out
    #out, errCode = obj.sendmail( "body\nbody", debug = False )


if __name__ == "__main__":
    main()
