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

############################
Workflow - Project - General
############################

PROJECT GENERAL DESCRIPTION
---------------------------

.. only:: text

  .. include:: images/ascii/swgit_project.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_project.gif
    :scale: 80 %


A swgit project can be composed in any way you want.

It can contain plain repositories or other projects.

A contained repository (plain or project) can be:

  1. "DEV" repository:

    These repositories are meant to develop inside.

    Its integration branch usually has "INT" kind.

    You can add this repo in this way, 
    thus declaring it is a DEV repo:

      $> swgit proj --add-repo --branch <any_INT_br> ...

    You will always work around that integration  
    branch HEAD.

    Every::

        swgit proj --update 

    will pull this branch.


  2. "CST" repository:

    These repositories are meant to be referenced only.

    This is the ideal repository when no team member develops inside.

    In order to add a CST repository you need:

      1. Add repository without -b option

      2. dd repository with -b option, specifying a CST branch:

        * someone inside origin repository must create a CST branch 
          (using swgit init --cst) in order to
          let you reference it as CST repo.

        * you can add this repo in this way, 
          thus declaring it is a CST repo::

            $> swgit proj --add-repo --branch <that_CST_branch> ...

    Every::

      swgit proj --update  
      
    will put CST-repo HEAD on last commit stored for that CST-repo 
    inside project HEAD



CREATING/ADDING REPO TO PROJECT
-------------------------------

When you add a repository you automatically create a project.
Following commands to realize it::

  swgit branch -c addingrepo

  swgit proj --add-repo
             --repository SUBREPO
             --url ssh://andreav@127.0.0.1/path/to/repo
             --branch 1/0/0/0/andreav/INT/develop

  swgit commit -a -m "added repo" --dev SUBREPO

--repository is not mandatory.
  You specify it when you want to change repo name
  or
  when you want to place repo in a subfolder. (i.e. --repository SUB/FOLDER/REPO)

Remember specifying <SUBREPO> name when committing any subrepo upgrade.

*swgit commit* default behavior ignores subrepo changes (This is done 
in order to treat project directory like any normal repository).


COMMITTING REPOSITORY PROGRESS
------------------------------

When you commit a repository inside a project, you freeze its state.
From now on, if you come back to this just created commit, that repository will be
restored to the state it was when committed::

  swgit commit -a -m "freezing subrepo" --dev <SUBREPO>

Remember specifying <SUBREPO> name when committing any subrepo upgrade.

If you do not specify <SUBREPO>, you will commit ONLY files inside current proj.

| A common problem when splitting repository using submodules is the value stored 
  inside higher repo regarding lower repo HEAD. Often, that value conflicts.
| By this way, you will no more be scared of this. You will commit like in any plain 
  repository.
| Only during stabilization, someone will freeze submodules status 
  into project.


UPDATING PROJECT
----------------

When you want to update your project you can do as follows::

  swgit proj --update

This command will pull project repository,
then it will pull every SUBREPO inside the project.

According to SUBREPO type, the behavior is different:

  * DEV repositories:

    User work always on integration branch HEAD inside these repositories.
    So, swgit proj --update will pull integration branch.

  * CST repositories:

    User reference these repositories, but quite never works there.
    So, swgit proj --update will put that repositories on last frozen commit,
    according to project repository stored information.

swgit provides two options when updating to modifying behavior:

  1. Side merge behavior::

       swgit proj --update -I/--merge-from-int

    * DEV repositories:

       If HEAD is on a topic branch, side pull will be done, i.e., 
       integration branch will be merged on topic branch.

    * CST repositories:

        Like plain `swgit proj --update`
        

  2. No merges at all::

      swgit proj --update -N/--no-merges

    * DEV repositories:

       git submodule update -- <DEV subrepo>

    * CST repositories:

       git submodule update -- <CST subrepo>


TRAVERSE PROJECT HISTORY
------------------------

If you want to checkout an older project state, you just have to issue this command::

  swgit proj --reset <any_valid_project_reference>

For every repository inside the project,
this will checkout the state stored into the commit provided.

This operation will put every repository in DETACHED-HEAD.
Fewer operations are supported in this state.

If you want to come back to develop, go inside project repository
and issue something like this::

  swgit branch -s 1/0/0/0/andreav/INT/develop
  swgit proj --update

proj --update will move every subrepo on the right place, according to its kind.


SHOW PROJECT STRUCTURE
----------------------

You can quickly analyze project state in this way::

  swgit proj --list

    PROJECT/REPO
      Local Path     : .
      Origin         : ssh://user@addr/path/to/origin
      Int Branch     : 1/1/1/1/user/INT/develop
      Checkout       : f604beb91abd6d71fa4a0c34f26d3055a3aecd88
      CurrBr         : 1/1/1/1/user/INT/develop
        |
        '----[A/SUB/REPO]
               Local Path     : A/SUB/REPO
               Origin         : ssh://user@addr/path/to/origin/for/this/repo
               Def int Branch : 6/6/6/6/user/INT/develop
               Act int Branch : 6/6/6/6/user/INT/develop
               Checkout       : cde04856f53949bfc9274045c7330cbbee4273b6
               CurrBr         : 6/6/6/6/user/INT/develop

Some useful informations are shown:

  :Local Path: path relative to super project containing this repo

  :Origin:     url of origin repository

  :Def int Branch: Default integration branch. For every repository and release
                     it can be different. This can be set:

                       1. When adding a repository with "swgit proj --add" by specifying -b option

                       2. After adding a repository with "swgit proj --add" without -b option, by::

                            swgit proj --edit --set-int-br <def-int-br> <reponame>

  :Act int Branch: Sometimes this differs from Def int branch.
                   This can happen because inside that repo, user issued::

                       swgit branch --set-integration <another_branch>

                   to change default value.
                   This is particularly useful when implementing some workflows
                   like :doc:`workflow_team_feature`.

  :Checkout: This show the sha onto which the repository currently is.

  :CurrBr:   This show if you are in DETACHED-HEAD or not.


SHOW "CONFIG SPEC" FOR A PROJECT
--------------------------------

This ClearCase-stolen term is used here with this purpose:

  | every time you make a stabilize on a project
  | or
  | you freeze the project and all its repositories (by adding their name to swgit commit)
  | you register inside project repository the state of all sub repositories.

  ::

    swgit proj --get-configspec <any_valid_reference>

       ./:f604beb91abd6d71fa4a0c34f26d3055a3aecd88
       A/SUB/REPO:cde04856f53949bfc9274045c7330cbbee4273b

This command shows you, for each repo, the sha registered inside project on commit
you specified. The format is

  REPOPATH : SHA [# LABEL]

`LABEL` is specified only when any one exists on that sha.


STABILIZE --STB FOR A PROJECT
-----------------------------

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





