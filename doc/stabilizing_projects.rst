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

####################
Stabilizing projects
####################

:doc:`Stabilizing process <stabilizing>` enriches its meaning when 
inside a project.

Projects (like any plain repository with submodules), also store contained
repositories references.

| Stabilization freezes project as a normal repo.
| Stabilization also reports submodules state on *INT/stable* branch.

User can select submodule version to be frozen by -S/--source parameter:

  1. No -S/--source parameter:

     ::

        swgit stabilize --stb Drop.A

     This branch is:

     *  proj repo: stabilize proj HEAD
     *  dev repos: not affected. Continue referring last registered commit.
     *  cst repos: not affected. Continue referring last registered commit.

  2. COMMA-SEPARED -S/--source parameter:

     ::

       swgit stabilize --stb --source ./:HEAD,SUBREPO:1/0/0/0/andreav/INT/develop/LIV/Drop.Z

     | This format is well suited for scripting.
     | For any submodule, user can choose its version.

     Format is:

       REPO:VER[,REPO:VER]...

     | Root project is addressed with '.' repository.
     | Actually, when no parameter is specified, `--source .:HEAD` is used instead.

     The behavior is:

       every repo into src    : checked out before stabilizing project
       every repo NOT into src: Continue referring last registered commit.


  3. FILE -S/--source parameter:

     ::

       swgit stabilize --stb --source filename.cs

     | This format is more human-readable.
     | filename.cs is any file containing output formatted like this:

       REPO:VER [#comments]
       REPO:VER [#comments]

     This output is the same produced by command::

         swgit proj --get-configspec <any_valid_reference>

     Inside that file user can more neatly write commits
     he/she wants to select for each repo.

     The behavior is: 

       same as comma-separed list.

When specifying any submodule with --source parameter, 
another commit will be created on *INT/stable* branch:

  * One commit for merging root repository source reference

  * One commit (only when necessary) for storing changelogs and/or 
    pre-liv-commit processing

  * One commit (only when necessary) for storing submodules upgrades. 
    This last commit is the new one.

