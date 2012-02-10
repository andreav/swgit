
Wokflow - Project - General
***************************


PROJECT GENERAL DESCRIPTION
===========================

                       +------------+
                       | swgit PROJ |
                       +------------+
                             ^
                             |
                             |
                             |
       +-----------+---------+--+------------------+
       ^           ^            ^                  ^
       |           |            |                  |
       |           |            |                  |
   +---+---+   +---+---+    +---+---+          +---+---+
   |DEVREPO|   |CSTREPO|    |DEVPROJ|          |CSTPROJ|
   +-------+   +-------+    +---+---+          +---+---+
                                ^                  ^
                                |                  |
                                |                  |
                             +--+---+              +-+-------+
                             ^      ^                ^       ^
                             |      |                |       |
                             |      |                |       |
                         +---+---+               +---+---+
                         |DEVREPO| ...           |CSTREPO| ...
                         +-------+               +-------+

A swgit project can be composed in any way you want.

It can contain plain repositories or other projects.

A contained repository (plain or project) can be:

   1. "DEV" repository:

      These repositories are meant to develop inside.

      Its integration branch usually has "INT" kind.

      You can add this repo in this way, thus declaring it is a DEV
      repo:

         $> swgit proj --add-repo --branch <any_INT_br> ...

      You will always work around that integration branch HEAD.

      Every:

         swgit proj --update

      will pull this branch.

   1. "CST" repository:

      These repositories are meant to be referenced only.

      This is the ideal repository when no team member develops
      inside.

      In order to add a CST repository you need:

         1. Add repository without -b option

         2. dd repository with -b option, specifying a CST branch:

            * someone inside origin repository must create a CST
              branch (using swgit init --cst) in order to let you
              reference it as CST repo.

            * you can add this repo in this way, thus declaring it is
              a CST repo:

                 $> swgit proj --add-repo --branch <that_CST_branch> ...

      Every:

         swgit proj --update

      will put CST-repo HEAD on last commit stored for that CST-repo
      inside project HEAD


CREATING/ADDING REPO TO PROJECT
===============================

When you add a repositoty you automatically create a project.
Following commands to realize it:

   swgit branch -c addingrepo

   swgit proj --add-repo
              --repository SUBREPO
              --url ssh://andreav@127.0.0.1/path/to/repo
              --branch 1/0/0/0/andreav/INT/develop

   swgit commit -a -m "added repo" --dev SUBREPO

--repository is not mandatory.
   You specify it when you want to change repo name or when you want
   to place repo in a subfoler. (i.e. --repository SUB/FOLRER/REPO)

Remember specifying <SUBREPO> name when committing any subrepo
upgrade.

*swgit commit* default behaviour ignores subrepo changes (This is done
in order to treat project directory like any normal repository).


COMMITTING REPOSITORY PROGRESS
==============================

When you commit a repository inside a project, you freeze its state.
From now on, if you come back to this just created commit, that
repository will be restored to the its state when it has been
committed:

   swgit commit -a -m "freezing subrepo" --dev <SUBREPO>

Remember specifying <SUBREPO> name when committing any subrepo
upgrade.

If you do not specify <SUBREPO>, you will commit ONLY all file inside
proj.

By this way, when you work inside project repository, you can ignore
SUREPO presence.


UPDATING PROJECT
================

When you want to update your project you can do as follows:

   swgit proj --update

This command will pull project repository, then it will pull every
SUBREPO inside the project.

According to SUBREPO type, the behaviour is different:

   * DEV repositories:

     User work always on integartion branch HEAD inside these
     repositories. So, swgit proj --update will pull integration
     branch.

   * CST repositories:

     User reference these repositories, but quite never works there.
     So, swgit proj --update will put that repositories on last
     freezed commit, according to project repository stored
     information.

swgit provides two options when updating to modifying behaviour:

   1. Side merge behaviour:

         swgit proj --update -I/--merge-from-int

      * DEV repositories:

           If HEAD is on a topic branch, side pull will be done, i.e.,
           integartion branch will be merged on topic branch.

      * CST repositories:

           Like plain *swgit proj --update*

   1. No merges at all:

         swgit proj --update -N/--no-merges

      * DEV repositories:

           git submodule update -- <DEV subrepo>

      * CST repositories:

           git submodule update -- <CST subrepo>


TRAVERSE PROJECT HISTORY
========================

If you want to checkout an older project state, you just have to issue
this command:

   swgit proj --reset <any_valid_project_reference>

For every repository inside the project, this will checkout the state
stored into the commit provided.

This operation will put every repository in DETACHED-HEAD. Fewer
operations are supported in this state.

If you want to come back to develop, go inside project repository and
issue something like this:

   swgit branch -s 1/0/0/0/andreav/INT/develop
   swgit proj --update

proj --update will move every subrepo on the right place, according to
its kind.


SHOW PROJECT STRUCTURE
======================

You can quickly analize project state in this way:

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

Some usefull informatins are shown:

   Local Path:
      path relative to super project conatining this repo

   Origin:
      url of origin repository

   Def int Branch:
      Default integration branch. For every repository and release it
      can be different. This can be set:

         1. When adding a repository with "swgit proj --add" by
            specifying -b option

         2. After adding a repository with "swgit proj --add" without
            -b option, by:

               swgit proj --edit --set-int-br <def-int-br> <reponame>

   Act int Branch:
      Sometimes this differs from Def int branch. This can happen
      because inside that repo, user issued:

         swgit branch --set-integration <another_banch>

      to change default value. This is particulary usefull when
      implementing some workflows like "workflow_team_feature".

   Checkout:
      This show the sha onto which the repository currently is.

   CurrBr:
      This show if you are in DETACED-HEAD or not.


SHOW "CONFIG SPEC" FOR A PROJECT
================================

This ClearCase-stolen term is used here with this purpose:

   every time you make a stabilize on a projectoryou freeze the project and all its repositories (by adding their name to swgit commit)you register inside project repository the state of all sub repositories.

      swgit proj --get-configspec <any_valid_reference>

         ./:f604beb91abd6d71fa4a0c34f26d3055a3aecd88
         A/SUB/REPO:cde04856f53949bfc9274045c7330cbbee4273b

This command shows you, for each repo, the sha registered inside
project on commit you specified. The format is

   REPOPATH : SHA

You can add --pretty option to obtain a more human readable output.
Every sha is described regarding to last LIV and STB inside that repo.


STABILIZE --STB FOR A PROJECT
=============================

When inside a project, swgit stabilize --stb enriches its meaning.

Not only it stabilizes project as a normal repo, but also it reports
subrepos state on stable branch.

You can use different --src values:

   1. TAG DROP WITH HEAD

      $> swgit stabilize --stb --src HEAD

         The behaviour is:

            proj repo: stabilize proj HEAD dev repos: register subrepo
            HEAD into project commit cst repos: not affected. Register
            last registered commit

   2. TAG DROP WITH COMMA-SEPARED LIST

         swgit stabilize --stb --src ./:HEAD,A/SUBREPO:af2145bc

      In this way you can choose to freeze a different commit for
      every repo.

      The behaviour is:

         every repo into src    : checked out before stabilizing
         project every repo NOT into src: same as --src HEAD (see
         previous point)

   3. TAG DROP WITH "CONFIG SPEC"

         swgit stabilize --stb --src filename.cs

      filename.cs is a file containing same output as:

         swgit proj --get-configspec <any_valid_reference>

      Inside that file you can more neatly write commits you want to
      select for each repo.

      The behaviour is

         same as comma separed list.
