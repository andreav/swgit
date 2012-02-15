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

######################
Workflow - Update Repo
######################

.. _lbl_repo_pull_fromint:

pull executed on integration branch
-----------------------------------

  ::

    swgit branch --current-branch
       1/0/0/0/andreav/INT/develop
    swgit pull

This last command updates develop branch on your local repository

It leaves untouched all other branches.

.. only:: text

  .. include:: images/ascii/swgit_repo_update_intbr.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_repo_update_intbr.gif
    :scale: 80 %

.. _lbl_repo_pull_fromftr:

pull executed on FTR branch
---------------------------

  ::

    swgit branch --current-branch
       1/0/0/0/andreav/FTR/topic
    swgit pull -I/--merge-from-int

This last command updates integration branch on your local repository

After this it will merge local integration branch on your current branch

This command may be useful in order to update an old branch 
and keeping on developing on that branch.

.. note::
   If you are going beginning a new work, do not update an old branch!
   It it better creating a new branch
   just after pulling from origin::
  
      swgit branch --current-branch
          1/0/0/0/andreav/FTR/topic
      swgit pull
      swgit branch -c new_topic

.. only:: text

  .. include:: images/ascii/swgit_repo_update_ftrbr.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_repo_update_ftrbr.gif
    :scale: 80 %

.. _lbl_repo_push_fromint:

push executed from integration br
---------------------------------

  ::

    swgit branch --current-branch
       1/0/0/0/andreav/INT/develop
    swgit push

This last command updates origin repository with your 
local integration branch.

.. only:: text

  .. include:: images/ascii/swgit_repo_push_intbr.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_repo_push_intbr.gif
    :scale: 80 %

.. _lbl_repo_push_fromftr:

push executed from FTR branch
-----------------------------

  ::

     swgit branch --current-branch
        1/0/0/0/andreav/FTR/topic
     swgit push -I/--merge-on-int

This command executes also a merge on integration branch.

  1. Update local repository.

     This is done to push always on HEAD and avoid non-ff pushes

  2. merge last FTR/topic/DEV/nnn label on integration branch

     This merge is always ``--no-ff``.

  3. push everything on origin.


.. only:: text

  .. include:: images/ascii/swgit_repo_push_ftrbr.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_repo_push_ftrbr.gif
    :scale: 80 %


