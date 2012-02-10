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

##############
ssh management
##############

swgit supported urls for cloning are:

  * ssh urls, i.e. ``ssh://user@addr/path/to/repo``

  * filesystem urls, i.e. ``/path/to/repo``

(main reason is explained :ref:`here <lbl_proj_local_submodules>`)

However, communication over ssh does not require user 
to enter ssh password every time local repository needs 
to contact 'origin' repository 
(i..e. with `clone`, `pull`, `push`, and `git submodule add` operations)

| swgit tool creates a new identity with no password 
  at first clone time.
| User can find this identity under:

    ~/.ssh/swgit_sshKey.pub

    ~/.ssh/swgit_sshKey

When cloning a repository, swgit will check if ssh shell access is allowed
for current user at remote host.

If not, swgit will copy user public identity (swgit_sshKey.pub) remotely.

Remote password is asked to the user, and from now on, every communication 
will be transparent.

swgit key command
-----------------

  In order to check ssh key management, swgit provides this command::

    swgit key <user> <remotehost>

  This will check if swgit identity has been created and copied onto 
  that machine.

  ::

    swgit key -c <user> <remotehost>

  Will do necessary things to create and/or copy swgit identity 
  onto remote host.


.. todo::
  defines a different workflow for supporting ssh-agent

