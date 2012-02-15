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
    swgit tag       --custom-tag-show-cfg

Usually output not only lists current values, but also way to modify them.

  ::

    Mandatory fields:
    
     * from        by "git config swgit.push.from <val>"
                   or by file:   .swdir/cfg/mail.cfg, section push, key from
     * to          by "git config swgit.push.to(-1, -2, ...) <val>"
                   or by file:   .swdir/cfg/mail.cfg, section push, key to(-01, -02, ...)
                   by "git config user.email <val>"

    Optional fields:
    
     * subject     by "git config swgit.push.subject <val>"
                   or by file:   .swdir/cfg/mail.cfg, section push, key subject
     * body header by "git config swgit.push.body-header <val>"
                   or by file:   .swdir/cfg/mail.cfg, section push, key body-header

From this output we can see at least two solutions exists:

  * :ref:`lbl_configure_local`

  * :ref:`lbl_configure_clonable`


.. _lbl_configure_local:

Local configuration
-------------------

**This configuration is local to current repository**

This is accomplished with ``git config`` command.

It is always higher priority, and is the way to override clonable configuration.

Usually it is used to change behavior on a per repository basis.


.. _lbl_configure_clonable:

Clonable configuration
----------------------

**This configuration is cloned with the repository**

This is accomplished by creating a section inside some file under directory:

  ::

    ${REPO_ROOT}/.swdir/cfg/

File and section are always specified into command output.

Formatting must honor Python configuration file format.

However an example is always reported and can be un-commented.


.. _lbl_configure_values:

Bool and List values
--------------------

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


