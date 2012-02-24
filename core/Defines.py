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

import time, sys, os, pwd

# HOME DIRECOTRY => use ~
#   because 
#     $HOME depends only on UID
#   but
#     when UID != EUID => ~ looks on the right direcotry (that of EUID)
EUID_NAME = "%s" % pwd.getpwuid( os.geteuid() )[0]
EUID_HOME = "~%s" % EUID_NAME
EUID_HOME = os.path.expanduser( EUID_HOME )

SWGIT_SSH_IDENTITY_NOPASS_NAME = "swgit_sshid_nopass"
SWGIT_SSH_IDENTITY_NOPASS_PRIV = "%s/.ssh/%s" % (EUID_HOME, SWGIT_SSH_IDENTITY_NOPASS_NAME)
SWGIT_SSH_IDENTITY_NOPASS_PUB  = "%s.pub"     % (SWGIT_SSH_IDENTITY_NOPASS_PRIV)

#Ssh
SWCFG_SSH_SECT             = "ssh"
SWCFG_SSH_BIN              = "bin"
SWCFG_SSH_IDENTITY         = 'identity'
SWCFG_SSH_USE_NOPASS_ID    = "use-nopassw-id"
SWCFG_SSH_TESTACCESS_TIMEOUT   = 10

#script files
SWGIT = os.path.abspath( os.path.dirname( os.path.abspath( __file__ ) ) + "/../swgit" )
SWGIT_DIR = os.path.abspath( os.path.dirname( os.path.abspath( __file__ ) ) + "/.." )


#repo files
SWREPODIR               = ".swdir/"
SWDOTGIT                = ".git/"
SWDIR_LOG               = SWREPODIR + "log/"
SWDIR_CFG               = SWREPODIR + "cfg/"
SWDIR_CHANGELOG         = SWREPODIR + "changelog/"
SWDIR_LOCK              = SWREPODIR + "lock/"
SWFILE_DOTGITIGNORE     = ".gitignore"
SWFILE_INITLOG          = SWDIR_LOG + "init.log"
SWFILE_PLACEHOLDER      = ".placeholder"
SWFILE_LOGPLACEHOLDER   = SWDIR_LOG + SWFILE_PLACEHOLDER
SWFILE_PROJMAP          = ".gitmodules"
SWFILE_MERGEHEAD        = SWDOTGIT + "MERGE_HEAD"
SWFILE_LOCK             = "swgit_lock"
SWFILE_BRANCH_LAST      = SWDOTGIT + "swgit_last_br"
SWFILE_DEFBR            = SWDIR_CFG + "default_int_branches.cfg"
SWFILE_TAGDESC          = SWDIR_CFG + "custom_tags.cfg"
SWFILE_SNAPCFG          = SWDIR_CFG + "snapshot_repos.cfg"
SWFILE_MAILCFG          = SWDIR_CFG + "mail.cfg"
SWFILE_SNAPCFG_CURRVER  = ".swgit_curr_ver.sha"
SWFILE_SNAPCFG_GOTFNAME = ".swgit_expand_this"
SWFILE_GENERICCFG       = SWDIR_CFG + "generic.cfg"

SWNAME_ORIGIN_REMOTE = "origin"

#user cfg
SWCFG_USER_REGEXP  = '^[a-zA-Z_]+$'

#rel cfg
SWCFG_REL_SLASHES = 4
SWCFG_REL_REGEXP  = '^[0-9]{1,2}[/.][0-9]{1,2}[/.][0-9]{1,2}[/.][0-9]{1,2}$'

#stabilize cfg
SWCFG_STABILIZE_CHGLOG_FILE_FORMAT = """\
From:    %(*authorname) %(*authoremail)
Date:    %(*authordate)
Ref:     %(refname)

    %(subject)
"""
SWCFG_STABILIZE_FIXLOG_FILE_FORMAT = SWCFG_STABILIZE_CHGLOG_FILE_FORMAT
SWCFG_STABILIZE_CHGLOG_MAIL_FORMAT = SWCFG_STABILIZE_CHGLOG_FILE_FORMAT
SWCFG_STABILIZE_CHGLOG_MAIL_SORT = "*authorname"
SWCFG_STABILIZE_FIXLOG_MAIL_FORMAT = SWCFG_STABILIZE_CHGLOG_FILE_FORMAT

#branch cfg
SWCFG_BR_NUM_SLASHES_LOCAL       = 6
SWCFG_BR_NUM_SLASHES_LOCAL_FULL  = 8
SWCFG_BR_NUM_SLASHES_REMOTE      = 7 #when visualized like swgit branch (with remote prepended)
SWCFG_BR_NUM_SLASHES_REMOTE_FULL = 9
SWCFG_BR_INT        = "INT"
SWCFG_BR_CST        = "CST"
SWCFG_BR_FTR        = "FTR"
SWCFG_BR_FIX        = "FIX"
SWCFG_BR_NAME_REGEXP    = '^[a-zA-Z0-9_]{1,15}$'
SWCFG_BR_NAME_MAXLEN    = 15

#tag cfg
SWCFG_TAG_NUM_SLASHES      = 8
SWCFG_TAG_NUM_SLASHES_FULL = 10
SWCFG_TAG_NAMESPACE_PAST = "PAST"
SWCFG_TAG_NAMESPACE_TBD  = "TBD"
SWCFG_TAG_LIV            = "LIV"
SWCFG_TAG_STB            = "STB"
SWCFG_TAG_NGT            = "NGT"
SWCFG_TAG_DEV            = "DEV"
SWCFG_TAG_FIX            = "FIX"
SWCFG_TAG_RDY            = "RDY"
SWCFG_TAG_NEW            = "NEW"
SWCFG_TAG_NEW_NAME       = "BRANCH"
SWCFG_TAG_NEWREGEXP      = "^BRANCH$"
SWCFG_TAG_LIVREGEXP      = '^Drop\.[A-Z]{1,3}(_[0-9]{1,3})?$'

#mailcfg
SWCFG_MAIL_STABILIZE_SECT     = "stabilize"
SWCFG_MAIL_PUSH_SECT          = "push"
SWCFG_MAIL_MAILSERVER_SSHUSER = "mailserver-sshuser"
SWCFG_MAIL_MAILSERVER_SSHADDR = "mailserver-sshaddr"
SWCFG_MAIL_FROM               = "from"
SWCFG_MAIL_TO                 = "to"
SWCFG_MAIL_CC                 = "cc"
SWCFG_MAIL_BCC                = "bcc"
SWCFG_MAIL_SUBJ               = "subject"
SWCFG_MAIL_BODY_HEADER        = "body-header"
SWCFG_MAIL_BODY_FOOTER        = "body-footer"

#SNAPCfg
SWCFG_SNAP_URL       = "url"
SWCFG_SNAP_BRANCH    = "branch"
SWCFG_SNAP_AR_FORMAT = "ar-type"
SWCFG_SNAP_AR_TOOL   = "ar-tool"

#sw cfg defines
SWCFG_PREFIX           = "swgit"
SWCFG_LIST_REGEXP      = "\(-[0-9]+\)?"
SWCFG_UNSET            = "swgit_unset_cfg"
SWCFG_INTBR            = SWCFG_PREFIX + ".intbranch"
SWCFG_STABILIZE_ANYREF = SWCFG_PREFIX + ".stabilize-anyref"
SWENV_PREFIX           = "SWGIT_"


#sw custom tags defines
#these are only config options
SWCFG_KEY_TAGDSC_TAGTYPE                 = ".tagtype."
#these are all file or config options
SWCFG_KEY_TAGDSC_REGEXP                  = "regexp"
SWCFG_KEY_TAGDSC_MERGEONDEVELOP          = "merge-on-develop"
SWCFG_KEY_TAGDSC_MERGEONSTABLE           = "merge-on-stable"
SWCFG_KEY_TAGDSC_MERGEONCST              = "merge-on-cst"
SWCFG_KEY_TAGDSC_PUSH_ON_ORIGIN          = "push-on-origin"
SWCFG_KEY_TAGDSC_ONE_X_COMMIT            = "one-x-commit"
SWCFG_KEY_TAGDSC_ONLY_ON_INTEGRATOR_REPO = "only-on-integrator-repo"
SWCFG_KEY_TAGDSC_ALLOWED_BRTYPES         = "allowed-brtypes"
SWCFG_KEY_TAGDSC_DENIED_BRTYPES          = "denied-brtypes"
SWCFG_KEY_TAGDSC_TAG_IN_PAST             = "tag-in-past"
SWCFG_KEY_TAGDSC_HOOK_PRETAG_SCRIPT      = "hook-pretag-script"
SWCFG_KEY_TAGDSC_HOOK_PRETAG_SSHUSER     = "hook-pretag-sshuser"
SWCFG_KEY_TAGDSC_HOOK_PRETAG_SSHADDR     = "hook-pretag-sshaddr"
SWCFG_KEY_TAGDSC_HOOK_POSTTAG_SCRIPT     = "hook-posttag-script"
SWCFG_KEY_TAGDSC_HOOK_POSTTAG_SSHUSER    = "hook-posttag-sshuser"
SWCFG_KEY_TAGDSC_HOOK_POSTTAG_SSHADDR    = "hook-posttag-sshaddr"


#git cfg defines
GITCFG_USERNAME = "user.name"
GITCFG_USERMAIL = "user.email"
GITCFG_URL_ORIGIN = "remote.origin.url"
GITCFG_BRANCH_REMOTE_TEMPLATE = "branch.%s.remote"

