.. Copyright (C) 2012 Andrea Valle
   
   This file is part of swgit.
   
   swgit is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   swgit is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with swgit.  If not, see <http://www.gnu.org/licenses/>.

.. include:: globals.rst

.. toctree::
  :hidden:

#############
Configuration
#############

User can configure many swgit aspects, here some:

  ::

    swgit ssh       --show-local-cfg
    swgit push      --show-mail-cfg
    swgit stabilize --show-mail-cfg
    swgit stabilize --show-cfg
    swgit tag       --show-cfg <tagtype>

Usually output not only lists current values, but also way to modify them.

  ::

    Mandatory fields:
    
     * from        - 'git config swgit.push.from <val>'
                   - file        .swdir/cfg/mail.cfg
                     sect        push
                     key         from
     * to          - 'git config swgit.push.to(-1, -2, ...) <val>'
                   - file        .swdir/cfg/mail.cfg
                     sect        push
                     key         to(-1, -2, ...)
                   - 'git config user.email <val>'

    Optional fields:

     * subject     - 'git config swgit.push.subject <val>'
                   - file        .swdir/cfg/mail.cfg
                     sect        push
                     key         subject
     * body header - 'git config swgit.push.body-header <val>'
                   - file        .swdir/cfg/mail.cfg
                     sect        push
                     key         body-header


From this output we can see at least two solutions exists:

  * :ref:`lbl_configure_local`

  * :ref:`lbl_configure_clonable`


.. _lbl_configure_local:

Local configuration
-------------------

**This configuration is local to current repository**

This is accomplished with ``git config`` command.

It is always higher priority, and is the way to override cloned configuration 
(see next section).

Usually it is used to change behavior on a per repository basis.

Any configuration key is always structured in this way:

  **swgit . <section> . <key> [-xy] <value>**

Where:

  :swgit:     Simply represents a namespace under which ALL swgit comfigurations
              are stored.

  :section:   Groups many options referring same domain.
              For each *<section>*, a corresponding file portion can be created 
              inside configuration files (see next section)

  :key:       Addresses a certain option inside section group
  
  :[-xy]:     When specifying list values, user must suffix each entry with a dash
              and a number. (see also :ref:`lbl_configure_values`)

Some examples:

  ::

    git config swgit.ssh.bin /usr/local/ssh
  
    git config swgit.push.to      email@company.com
    git config swgit.push.to-01   email1@company.com
    git config swgit.push.to-02   email2@company.com
  
    git config swgit.stabilize.hook-pre-liv-commit-script   pre-liv-hook
  
    swgit.FIX.regexp              ^Issue[0-9][0-9]$


.. _lbl_configure_clonable:

Clonable configuration
----------------------

**This configuration is cloned with the repository**

This is accomplished by creating a section inside some file under directory:

  ::

    ${REPO_ROOT}/.swdir/cfg/

In order to discover which file, section and key to fill, user can issue any command 
showing configuration. (those commands are listed at top of this paragraph).

Output will list how to modify values:

  ::

	   * ssh executable     by "git config swgit.ssh.bin <val>"
	                        or by file:   .swdir/cfg/generic.cfg, section ssh, key bin


Formatting must honor Python *configparser* module file format.

Defining a new tag marking release commit: 

  ::

    [REL]
    regexp                  = ^[0-9]{4}-[0-9]{2}-[0-9]{2}$
    regexp-01               = ^[a-zA-Z]{0,15}$
    push-on-origin          = True
    one-x-commit            = True
    only-on-integrator-repo = True
    allowed-brtypes         = 
    denied-brtypes          = 
    tag-in-past             = True
    hook-pretag-script      = 
    hook-pretag-sshuser     = 
    hook-pretag-sshaddr     = 
    hook-posttag-script     = 
    hook-posttag-sshuser    = 

                    (file: .swdir/cfg/custom_tags.cfg)


.. _lbl_configure_values:

Bool, List, Multiline values
----------------------------

Allowed boolean values (case insensitive) are: 

  * true/false
  * yes/no
  * t/f
  * 1/0

When user needs to configure a list value he/she can suffix 
base configuration parameter with -1 -2 ... thus providing more values:

  ::

    git config swgit.push.to    <a_user>
    git config swgit.push.to-1  <another_user>
    git config swgit.push.to-2  <third_user>


Sometimes (i.e. with output format like changelog/fixlog) user may need
to specify multiline values: according to Python *configparser* module,
user can specify it by indenting netx lines in respect to first line:

  ::

    [stabilize]
    fixlog-fmt-file  = MyRefFmt:  %(refname)
      Date:  %(*authordate)

Note *"Date:"* line is indented in respect to previous (and first) line.
