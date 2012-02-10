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

import time, sys, os

#script files
SWGIT = os.path.abspath( os.path.dirname( os.path.abspath( __file__ ) ) + "/../swgit" )
SWGIT_DIR = os.path.abspath( os.path.dirname( os.path.abspath( __file__ ) ) + "/.." )

SWGIT_SSHKEY = "swgit_sshKey"

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
SWFILE_SNAPCFG_CURRVER  = ".swgit_curr_ver.sha"
SWFILE_SNAPCFG_GOTFNAME = ".swgit_expand_this"

SWNAME_ORIGIN_REMOTE = "origin"

#user cfg
SWCFG_USER_REGEXP  = '^[a-zA-Z_]+$'

#rel cfg
SWCFG_REL_SLASHES = 4
SWCFG_REL_REGEXP  = '^[0-9]{1,2}[/.][0-9]{1,2}[/.][0-9]{1,2}[/.][0-9]{1,2}$'

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
SWFILE_MAILCFG                    = SWDIR_CFG + "mail.cfg"
SWFILE_MAILCFG_STABILIZE_SECT     = "STABILIZE"
SWFILE_MAILCFG_PUSH_SECT          = "PUSH"
SWFILE_MAILCFG_MAILSERVER_SSHUSER = "MAILSERVER-SSHUSER"
SWFILE_MAILCFG_MAILSERVER_SSHADDR = "MAILSERVER-SSHADDR"
SWFILE_MAILCFG_FROM               = "FROM"
SWFILE_MAILCFG_TO                 = "TO"
SWFILE_MAILCFG_CC                 = "CC"
SWFILE_MAILCFG_BCC                = "BCC"
SWFILE_MAILCFG_SUBJ               = "SUBJECT"
SWFILE_MAILCFG_BODY_HEADER        = "BODY-HEADER"
SWFILE_MAILCFG_BODY_FOOTER        = "BODY-FOOTER"

#snapcfg
SWFILE_SNAPCFG_URL       = "URL"
SWFILE_SNAPCFG_BRANCH    = "BRANCH"
SWFILE_SNAPCFG_AR_FORMAT = "AR-TYPE"
SWFILE_SNAPCFG_AR_TOOL   = "AR-TOOL"
#SWFILE_SNAPCFG_ALWAYSUPD = "ALWAYS-UPDATE"

#sw cfg defines
SWCFG_PREFIX           = "swgit"
SWCFG_UNSET            = "swgit_unset_cfg"
SWCFG_INTBR            = SWCFG_PREFIX + ".intbranch"
SWCFG_STABILIZE_ANYREF = SWCFG_PREFIX + ".stabilize-anyref"
SWENV_PREFIX           = "SWGIT_"


#sw custom tags defines
SWCFG_KEY_TAGDSC_LIST_DELIMITER = " &@& "
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

