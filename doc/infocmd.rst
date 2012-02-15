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

############
Info command
############

This command allows retrieving many useful informations about repository and/or 
developer commits.

Accept parameters can be grouped into 2 categories:

  1. Input parameters: 

      * single commit
       
      * range of commits
       
      * list of commits

      Commits can be filtered to refine results.
  
  2. Actions: operations to accomplish on result commit(s)

Some actions need just 1 parameter, other actions need a range of them.


1. Input parameters
-------------------

As input parameter, user can specify:

  * Single reference::

      swgit info -r <reference>

    By using -r parameter, you can tell swgit info to operate on a specific reference
    It can be a commit, a branch, a tag.


  * Nothing

    This is a shortcut to "-r HEAD" option.


  * Range::

      swgit info --upstream <ref> --downstream <ref>

    --upstream <ref> 
      let the user specify oldest reference

    --downstream <ref> 
      let the user specify newest reference delimiting the range
      It is optional; by omitting it, swgit info uses HEAD instead.


  * Two commits

    Any actions requires just 2 commits. 
    In these cases, --upstream and --downstream does not define a range, 
    instead thy provide a way to input just that 2 commits.


  * "Grepped" list of commits::

      swgit info --grep  <regexp>
      swgit info --igrep  <regexp>

    These options let the user select a list of commits whose comment 
    matches the regular expression provided as parameter.

    --igrep matches ignore-case regular expression


  * List of commits by user::

      swgit info --user <username>
      swgit info --curruser

    --user <username> 
      This option can be used with --grep/--igrep option to search only commit for only one user.
      It can fast the search on big repositories

    --curruser
      This is a shortcut for --user <my_user_name>


  * List of tags::

      swgit info --all-dev
      swgit info --all-fix
      swgit info --all-tag

    --all-dev
      Looks only among DEV labels

    --all-fix
      Looks only among FIX labels

    --all-tag
      Looks among all labels into the repository


  * File filter

    If you append a file name at the end of the command,
    action will act only over commits modified that file



2. Actions
----------

  ::

    swgit info -h 

  will show which action a user can invoke on the input reference list.

Here, we will report some examples useful in every-day developer-life:

Files modified
++++++++++++++

  ::

    swgit info -r <a_ref> -f


Describe a reference
++++++++++++++++++++

  ::

    swgit info -r 1/0/0/0/andreav/FTR/topic/FIX/1234567 -t LIV

      reference :	1/0/0/0/andreav/FTR/topic/FIX/1234567
      upstream  :	1/0/0/0/andreav/INT/stable/LIV/DROP.AJ	(217 commits backwards )
      downstream:	1/0/0/0/andreav/INT/stable/LIV/DROP.AK	(110 commits forwards  )


  -t accept any kind of label.
    You can issue, for instance, -t NGT in order to describe the entered reference 
    in respect to NGT tags.

  upstream shows previous LIV label
  downstream shows, if it exists, which LIV label the reference has been merged into.

  ::

    swgit info -t LIV

      reference :	HEAD
      upstream  :	1/0/0/0/andreav/INT/stable/LIV/DROP.D	(  8 commits backwards )
      downstream:	NOT yet merged into any "LIV" label


Pushed on origin?
+++++++++++++++++

  ::

    swgit info -o

  This checks if HEAD has already been pushed on origin


Diff between commits
++++++++++++++++++++

  ::

    swgit info -d --upstream <ref1> --downstream <ref2>
    swgit info -d --upstream <ref1> --downstream <ref2> --commit-by-commit
    swgit info -d --upstream <ref1> --downstream <ref2> --commit-by-commit --my-commits-only

  This show file by file differences.

  `--commit-by-commit`
    separates commit

  `--my-commits-only`
    eliminates merges

  ::

    swgit info -d --upstream <ref1> --downstream <ref2> <filename>

  This show differences regarding that file

Previous diff
+++++++++++++

  ::

    swgit info -p -r <ref>

Zero diff
+++++++++

  ::

    swgit info -z -r <ref> [--commit-by-commit] [--my-commits-only]

  | Makes a difference with /NEW/BRANCH.
  | This shows is all work done on a topic branch.

  `--commit-by-commit`
    separates commit

  `--my-commits-only`
    eliminates merges


.. todo::
  Complete list


