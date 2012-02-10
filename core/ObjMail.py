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
#[STABILIZE]
#MAILSERVER-SSHUSER = 
#MAILSERVER-SSHADDR = 
#FROM               = 
#TO                 = 
#TO                 = 
#CC                 = 
#BCC                = 
#SUBJECT            = 
#BODY-HEADER        = 
#BODY-FOOTER        = 
#
#[PUSH]
#MAILSERVER-SSHUSER = 
#MAILSERVER-SSHADDR = 
#FROM               = 
#TO                 = 
#TO                 = 
#CC                 = 
#BCC                = 
#SUBJECT            = 
#BODY-HEADER        = 
#BODY-FOOTER        = 
"""

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


  def sendmail( self, body, debug ):

    if self.isValid_ == False:
      return self.dump(), 1

    from_opt = "" 
    if self.from_ != "":
      from_opt = " -- -f \"%s\" " % ( self.from_ )

    cc_opt = "" 
    if self.cc_ != "":
      cc_opt = " -c \"%s\" " % ( self.cc_ )

    bcc_opt = "" 
    if self.bcc_ != "":
      bcc_opt = " -b \"%s\" " % ( self.bcc_ )

    allbody = self.sanitize_message( self.bodyH_ )
    if self.bodyH_ != "":
      allbody += "\n"
    allbody += body
    if self.bodyF_ != "":
      allbody += "\n" + self.sanitize_message( self.bodyF_ )

    cmd_send_mail = "echo -e \"%s\" | /bin/mail \"%s\" -s \"%s\" %s %s %s" % \
                    ( allbody,
                      self.to_,
                      self.subj_,
                      cc_opt,
                      bcc_opt,
                      from_opt
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
    super(ObjMailStabilize, self ).__init__( SWFILE_MAILCFG, SWFILE_MAILCFG_STABILIZE_SECT )
    self.load_cfg()

#############
# PUSH MAIL #
#############
class ObjMailPush( ObjMailBase ):
  def __init__( self ):
    super(ObjMailPush, self ).__init__( SWFILE_MAILCFG, SWFILE_MAILCFG_PUSH_SECT )

    #override "to"
    self.fields_mandatory_[1] = [self.set_to, self.get_to, "to" , SWFILE_MAILCFG_TO, GITCFG_USERMAIL ]

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
    #out, errCode = obj.sendmail( "body\nbody", debug = False )


if __name__ == "__main__":
    main()
