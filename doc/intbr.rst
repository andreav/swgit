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

.. _lbl_intbr:

##################
Integration branch
##################

This is a key concept to leverage `swRepositories`.

  **Integration branch is THE central branch: everything turns around it.**

When creating a branch, pulling, pushing or merging, 
everything happens in relation to the current integration branch.

You can also do a subset of operation without it, but sooner or later 
an error message will appear requesting for setting it.

On the other side, when working with an integration branch many operations 
will considerably speed up.

Setting it
==========

You can set an integration branch in different ways:

  * By cloning with -b option::

      swgit clone <url> -b <intbr>

    this is like declaring:

      `Inside this repository I will work around this release or feature`

  * By issuing the command::

      swgit branch --set-integration-br <local or remote branch>

All necessary operations will be carried on by swgit tool.

You can set any valid branch as an integration branch.

| Normally, you specify an INT `develop` branch.
| In this way you declare to be a 'conventional' developer 
  interested in contributing to the project in a general way.

| Sometimes, like in :doc:`workflow_team_feature`, you specify a FTR branch.
| In this way you will see the project history flows independently 
  from your contributes.
| Only develops regarding your feature will be merged to you.


Taking advantage of it
======================

Here some examples for speeding up your develop work.

Integration branch is especially useful when on a side branch 
(a FTR branch for instance) and wanting to merge, push to origin, 
updating from origin in one shot command.

  .. note::
  
    These examples refer to a scenario with an hypothetical
  
    #. 1/0/0/0/andreav/INT/develop branch
  
    #. user needs to create a FTR/topic branch
  
    #. user tags with ``swgit tag dev -m 'ready'`` before 
       trying merge or push operations

1. **branch creation**::

      swgit branch -c "topic"

   instead of::

      swgit branch -c "topic" --src 1/0/0/0/andreav/INT/develop

.. _lbl_repo_sidemerge:

2. **side merge**::

      swgit merge -I

   instead of::

      swgit branch -i
      swgit merge 1/0/0/0/andreav/FTR/topic/DEV/000

.. _lbl_repo_sidepush:

3. **side push**::

      swgit push -I

   instead of::

      swgit branch -i
      swgit merge 1/0/0/0/andreav/FTR/topic/DEV/000
      swgit push

   Please refer to :ref:`lbl_repo_push_fromftr` for a graphical 
   interpretation.


.. _lbl_repo_sidepull:

4. **side pull**::

      swgit pull -I

   instead of::

      swgit branch -i
      swgit pull
      swgit branch -s 1/0/0/0/andreav/FTR/topic
      swgit merge 1/0/0/0/andreav/INT/develop

   Please refer to :ref:`lbl_repo_pull_fromftr` for a graphical 
   interpretation.

