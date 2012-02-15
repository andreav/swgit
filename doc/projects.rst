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

########
Projects
########

For a quick reference, please refer to :doc:`workflow_project`

.. only:: text

  .. include:: images/ascii/swgit_project.txt

.. else
.. only:: not text

 .. image:: images/static/swgit_project.gif
   :scale: 70 %


Overview
========

| In this context, projects are intended to be more git repositories 
  composed all together.
| Every git user know two solutions exists today:

  * `git submodules`

  * `git subtrees`

In short, to me:

  * `git subtrees` are too difficult to use, above all if you need 
     contributing back to the project (i.e. you want to push something 
     to origin)

  * `git submodules` are good and flexible, but 
    they are not so handy to manage as-is.

swgit chooses `git submodules` as its core implementation. So:

    * swProjects are entirely built around native *git submodules*

    * ``git submodule`` command fully works inside them 
      (it is not :ref:`intercepted <lbl_scripting>` by swgit)

In order to script submodules, swgit introduces a new command::

  swgit proj

This command:

    * | Simplifies submodule usage.
      | Any submodules tricks are hidden to the user.
      | Much more, it helps in diffing with submodules,
        above all during merge conflicts. (:ref:`lbl_proj_diffing`)

    * | Supports single repo workflows to gain in efficiency.
      | :doc:`intbr`, for instance, has a key role inside
        projects.
      | Please refer to :ref:`integration branch inside projects <lbl_proj_dev_cst_repos>`
      
    * | Try minimizing conflicts when using submodules.
      | I'm referring to this annoying problem: 
      | when committing a project 
        you are potentially creating a conflict, despite the 
        content is not conflicting with others contributes. This happens due to 
        the fact that the super-project 
        must store the point at which each submodule
        has been committed, and that contributes quite always conflicts.
      | Please refer to :ref:`lbl_proj_committing`

    * Creates :ref:`lbl_proj_local_submodules`. They let a clone-of-clone
      operation on a project behave like the corresponding operation on a single repo.
      Please see documentation for a more detailed explanation.
      
    * | Creates :ref:`lbl_proj_snapshot_repositories`. This is a client-side response to
        big binaries repositories git problem.
      | When a repository is too large, and history is not meaningful, user can choose to 
        convert it in a snapshot repository, thus downloading only 1 commit instead of
        entire history.


.. note:: 
  At the moment, swgit let the user adding to the project only 
  repositories with shell access (ssh or fs), with this form:

    ::

      ssh://user@addr/path/to/repo
      /path/to/repo

  This limitation will be better explained when analyzing :ref:`lbl_proj_local_submodules`.


.. _lbl_proj_composing:

Creating
========

Command used to add a submodule is very similar to `git submodule` mate::

  swgit proj --add-repo <ssh or fs url> [-b <integration branch>] [<local name>]

This command behaves in this way:

  #. adds a corresponding entry into .gitmodules

  #. executes a :ref:`swgit init <lbl_proj_initializing>` on it

When first repository is added, a new file is created under the project root:

  $PROJ_ROOT/.swdir/cfg/default_int_branches.cfg

| This is the place where swgit puts additional informations about submodules.
| If you specify `-b` option while adding a repository, 
  that branch will became repository "Default integration branch": 
  it will be written inside this file and will decide :ref:`repository kind <lbl_proj_dev_cst_repos>`

  .. note::
  
    | Thought swgit uses information written into this file, this does not 
      break compatibility with native submodules.
    | User can choose working with `git submodule` command as usual,
      or trying to leverage `swgit proj` command taking advantage of this 
      additional information.


.. _lbl_proj_dev_cst_repos:

Dev and Cst subrepositories
===========================

It worth to mention the importance of `-b` option when adding a 
repository to the project.

`-b` not only forces swgit to clone that branch and set HEAD on it,
(like submodule command does),
but also configures default integration branch for that subrepository.

This information will be used by ``swgit proj --update`` in order to 
decide in which way to update every sub-repository. 
(see :ref:`Updating projects <lbl_proj_updating>`)

According to this branch kind, subrepository will be considered as:

  .. _lbl_proj_developer_repo:

  * **develop subrepository**: 

      | This is a repository where team will develop into.
      | `-b` argument to ``swgit proj --add`` will be set:

          * as :doc:`intbr` into that repository

          * as `default integration branch` into project containing it.

      To create a *developer repository*, default integration branch provided 
      must be any subrepository valid :ref:`INT branch <lbl_references_branches>`.

      |subs_img_todo| Verify if a FTR branch will behave as INT or CST branch

      Thanks to this integration branch many workflows defined for single repository can
      be re-used inside projects. (:ref:`Updating projects <lbl_proj_updating>`)

  .. _lbl_proj_customer_repo:

  * **customer subrepository**: 

      | This is an ordinary third party repository.
      | Project just references it. When a new, stable, version is released, project
        will update its reference.
      | Team usually does not develop inside this repositories.

      To create a *customer repository*, user may:

        * not provide a `-b` parameter when adding submodule

        * provide a default integration branch with 
          :ref:`CST type <lbl_references_branches>` as `-b` argument 
          to ``swgit proj --add``

  .. note::
  
    If you do not know which branch to clone, you can choose to add submodule
    without specifying `-b` option (thus creating a customer repository) 
    and subsequently editing this value by the command::
  
      swgit proj --edit-repo --set-int-br <def-int-br> <reponame>


.. _lbl_proj_initializing:

Initializing
============

Initializing submodules has a key difference with `git submodules`:

  **When initializing a submodule, 'origin' project 
  repository will be contacted**

This is done to accomplish a task:

  **Understand if submodule is local or remote in respect to 'origin' project**

  * :ref:`lbl_proj_local_submodules` in a nutshell:
  
      When initializing a *local repository*, url inside `.gitmodules` is ignored, 
      instead a repository local to 'origin' project, in the same relative position 
      as the one you are initializing, is attended to be found.
  
      From a `git config` point of view, `submodule.<MYSUBMOD>.url` entry 
      will point to 'origin' project url, justified in the path.
  
  
  * Remote submodules behave exactly as default git submodules:
  
      When initializing a *remote repository*, url inside `.gitmodules` is used.
 
| Moreover, ``swgit --init`` also downloads repository from right url.
| No other command is needed (i.e. no `git submodule update`)


For very big projects, or well split projects, the better swgit proj usage
is this:

  ::

      swgit clone
      swgit proj --init <INTEREST_SUBMODS>

| First command will download only root project repository 
| Second command will initialize (and download) only repositories 
  contained under `INTEREST_SUBMOD` direcotry.

If you prefer combining both behaviors simply choose:

  ::

      swgit clone --recurse

But this will initialize (and download) ALL repositories contained 
under your project.


.. _lbl_proj_updating:

Updating
========

Updating swProjects is a matter of ``swgit proj --update`` command.

Combining `--update` command options and subrepository kind 
(:ref:`developer <lbl_proj_developer_repo>` 
or :ref:`customer <lbl_proj_customer_repo>`), 
user can obtain different results:

Key concepts during update, are:

  #. User works inside `Developer repositories`, no detached-head 
     is welcome.

     | Inside single-repo workflow, after a pull I start developing 
       from INT/develop HEAD.
     | To speed up my work, same must be when using projects.

  #. Projects just reference `Customer repositories`, here 
     detached-head after update is the right choice, fast and reliable.

     It is very uncommon to develop inside that repositories, and if 
     I need to upgrade them, I must explicitly commit their upgrade 
     (see :ref:`Committing Projects <lbl_proj_committing>`)

Following, three update possibilities are presented.

  **1. Default update** ::

   swgit proj --update

  This translates in:

  * For every `Developer repositories`::

      swgit branch -i
      swgit pull

  * For every `Customer repositories`::

      git submodule update -- <CST subrepo>

  Result is:

    * Inside `Developer repositories`, all commits are pulled and user
      is on INT/develop HEAD, ready to implement starting from last
      pushed contribute.

    * Every `Customer repositories`, will be in detached-head, 
      and user project will select last committed label for that 
      repository.


  **2. Update and merge** ::

     swgit proj --update -I/--merge-from-int

  This translates in:

  * For every `Developer repositories`::

      swgit pull -I

  * For every `Customer repositories`::

      git submodule update -- <CST subrepo>

  Result is:

    * | Inside `Developer repositories`, all commits are pulled.
      | If starting from integration branch (or from detached-head), 
        now HEAD will be moved on last puled commit.
      | If starting from a develop branch, a merge will be done, 
        from integration branch to develop branch.

      This merge behaves like executing single repo :ref:`side pull <lbl_repo_sidepull>`

    * Every `Customer repositories`, will be in detached-head, 
      and user project will select last committed label for that 
      repository.


  **3. Update without merge**

  ::

     swgit proj --update -N/--no-merges

  This translates in:

  * For every `Developer repositories`::

      git submodule update -- <INT subrepo>

  * For every `Customer repositories`::

      git submodule update -- <CST subrepo>

  Result is:

    | This behaves exactly as native ``git submodule update``
    | No merge at all, only if a commit is needed, it is downloaded.
    | ``git fetch`` (in contrast to previous pulls) is the 
      operation behind the scenes.


    .. note::
      Differently from others methods, this one does not 
      automatically pulls project repository.



.. _lbl_proj_committing:

Committing
==========

| Committing inside a project has a different behavior in respect to native git.
| It leverages git `partial commits` in this way:

    | Into project repository, there are any special-files: :term:`commit file`
    | Those files represent submodules HEAD at commit instant.
    | Those files are treated separately from all other ordinary repository files.

This is realized following this principle:

  **'Submodules commit files' are never automatically added to the index**

This choice is taken to minimize a usual `git submodule` problem:

  | When committing inside a project, every :term:`commit file` stores its 
    corresponding submodule HEAD.
  | These `commit` files often causes a conflict during merge, also when 
    submodule content is not conflicting.

So, without implicitly committing those files, you work around this behavior.

When working with swProjects, you can follow one among two schemas:

  #. | **Project repository is just a container**.
     | Its main (quite unique) goal is to register 'magical' alignments 
       among subrepositories. 
     | Every repository evolves by its own.
     | Project maintainer task is choosing when freezing a 'lucky combination'
       (maybe after successful test passing) of all submodules.
     | When and only when this happens, `commit files` are updated.

     In this scenario, `swgit commit` does not improve in respect to `git commit`,
     because you quite never commit inside project directory (except for registering
     new alignments)

  #. | **Project repository is a real repository containing any developer repositories**.
     | Maybe you work only into project repo, maybe you develop also 
       into a subrepo. 

     | Thanks to `swgit commit`, when you commit project repo, 
       you will not commit subrepo status (you will not add `commit files` to the index).
     | Now, when merging, no conflict will be found on that file.

So for instance:

  ::

    swgit commit -a

will commit all contributes into your project, without adding submodules.

If you want to freeze submodules status, you will issue one among:

  ::

      swgit commit -A
      swgit commit <A_SUBREPO>

| in order to commit all or just one submodule status.
| Note, nothing will be committed into your repository but that submodules status.

It is perfectly allowed a command like this:

  ::

      swgit commit -aA

for committing both repository contributes and submodules updates.


.. 
  In both scenarios things are simplified because we assume only one figure
  freezes the project.
  | I think this is right, because committing projects is a project-level task. 
  | A single developer cannot stat if his/her contribute is good for 


.. _lbl_proj_diffing:

Diffing
=======

Diffing submodules content is also somehow cumbersome from a project point of view.

| Suppose user wants to diff HEAD~1 and HEAD into project.
| What about submodules? 
| You need to understand at which submodule commit, project stored them in both instants.

This is exactly what ``swgit --diff`` does::

  swgit proj -D/--diff [ref1] [ref2] [<A_SUBREPO>...]

Both references are optional, and behaves similar to ``git diff``:

  ::

    swgit proj -D
    swgit proj -D HEAD~1 HEAD

If you do not specify any input:

  ref1 = HEAD
  ref2 = Submodule working dir

If you do specify only ref1:

  ref2 = Submodule working dir


.. note::
  | `ref1` and `ref2` refer to project commits. 
  | Output reports differences inside every submodule, 
    between versions of subrepositories registered at ref1 and ref2 
    inside project.

.. note::
  | When a pending merge is in act, `ref1` and `ref2` are ignored
    and HEAD and MERGE_HEAD are used instead.
  | This will show also merge conflicts.


.. _lbl_proj_analyzing:

Analyzing
=========

A couple of tools to analyze repositories::

  swgit proj -l/--list
  swgit proj -C/--get-configspec

The former is better explained with an output example:

  .. code-block:: cfg

     TEST_PROJ_REPO_PLAT
       Local Path     : .
       Curr remote    : (origin) ssh://andreav@127.0.0.1/TEST_PROJ_REPO_PLAT
       Int Branch     : 2/0/0/0/swgittestuser/INT/develop
       Checkout       : 7c9b4a24b9d471c2f8ba5594e51406ec9266a7ae
       CurrBr         : 2/0/0/0/swgittestuser/INT/develop
         |    
         |----[TEST_PROJ_REPO_APP]
         |      Local Path     : TEST_PROJ_REPO_APP
         |      Origin         : ssh://andreav@127.0.0.1/TEST_PROJ_REPO_APP
         |      Def int Branch : 8/0/0/0/swgittestuser/INT/develop
         |      Act int Branch : 8/0/0/0/swgittestuser/INT/develop
         |      Checkout       : 45fc08a0478b36804db78d1d2a9fdebba36e81c8
         |      CurrBr         : 8/0/0/0/swgittestuser/INT/develop
         |    
         '----[TEST_PROJ_REPO_FS]
                Local Path     : TEST_PROJ_REPO_FS
                Origin         : ssh://andreav@127.0.0.1/TEST_PROJ_REPO_FS
                Def int Branch : 7/0/0/0/swgittestuser/INT/develop
                Act int Branch : 7/0/0/0/swgittestuser/INT/develop
                Checkout       : a8bf589b323d0be01715c36d7a00a9cfd85a8be7
                CurrBr         : 7/0/0/0/swgittestuser/INT/develop


this simple command immediately shows project situation.

It reports many interesting informations, directly from the project directory.

The latter command (whose name has been stolen from ClearCase) 
shows commits registered into project for each submodule.

An output example is:

  .. code-block:: cfg

      ./:7c9b4a24b9d471c2f8ba5594e51406ec9266a7ae
      TEST_PROJ_REPO_APP:45fc08a0478b36804db78d1d2a9fdebba36e81c
      TEST_PROJ_REPO_FS:a8bf589b323d0be01715c36d7a00a9cfd85a8b

Referring to the same example above.



.. _lbl_proj_local_submodules:

Local submodules
================

| Why submodules behave differently from single repositories?
| Why when I clone a cloned-repo, every push goes to middle clone, 
  while if I clone a project with submodules, they by default refer 
  to 'origin' repository, ignoring father projects clone relationship?

  .. figure:: images/static/swgit_repo_clone_of_clo.gif
    :scale: 65 %
    :align: center

    default behavior for clone of clone with single repo


  .. figure:: images/static/swgit_project_clone_of_clo_example.gif
    :scale: 65 %
    :align: center

    default behavior for clone of clone with projects.

While projects repositories maintain same relative relationship 
like previous single-repo example,
submodules repositories, by default, always refer to a common 'origin' repository. 

Submodules do not maintain their own projects relative relationship, 
thus making difficult respecting intuitive single repository contribute chain.

This is because submodules are primarily intended to be used with 
third party repositories, with libraries.
In that scenario, could be better referencing the common, original, library repository.

| But when you split your repository into submodules, and you want
  to develop inside all of them, single-repo behavior is preferred.
| Of course submodules support it, but another time, it has been not 
  so easy to understand *HOW*.
| Response is this: at `git submodule init` time, manually configure
  submodule 'origin' url with a value different from that value written 
  into .gitmodules.

Local submodules implement this requirement, i.e. they initialize
differently submodules according to 'origin' project status.

Given a submodule, two possibilities exist:

  #. 'origin' project just contains an empty directory in place 
     of that submodule

      | A **Remote submodule** will be initialized inside my project clone,
      | i.e. 
      |   .gitmodules url will be used during initialization.

  #. 'origin' project has a local clone for that submodule:

      | A **Local submodule** will be initialized inside my project clone,
      | i.e. 
      |   .gitmodules url will be ignored
      |   'origin' project url will be used instead, justified in path 
          in order to let my subrepo pointing to submodule local clone 
          under 'origin' project.

| An image will hopefully clarify.
| Please compare git default behavior vs swgit default behavior:

  .. figure:: images/static/swgit_project_clone_of_clo_gitnative.gif
    :scale: 75 %
    :align: center

    git default behavior when cloning 'cloned projects'

  .. figure:: images/static/swgit_project_clone_of_clo_swgit.gif
    :scale: 75 %
    :align: center

    swgit default behavior when cloning 'cloned projects'


This is why ``swgit proj --add`` only let the user add repositories with shell access:

  **`swgit init` need to contact 'origin' project to check if we are cloning
  a local or remote subrepository.**

To sum up, when you need a library-like behavior, you will configure 'origin' project 
without a local clone under it by issuing a command like this on 'origin' repository:

  ::

     swgit proj --un-init <REMOTE_SUBREPO_DIR>

Instead when you need a single-repo-like clone-of-clone behavior, 
you will configure 'origin' project with a local clone under it by
issuing a command like this on 'origin' repository:

  ::

     swgit proj --init <LOCAL_SUBREPO_DIR>


.. _lbl_proj_snapshot_repositories:

Snapshot repositories
=====================

A common feature among Distributed Version Control Systems is they must store
entire history inside every clone.

| This is a problem when you need to store big binaries, because they cannot be 
  significantly compressed.
| Furthermore, most of the time all previous versions are not useful.

  * swgit propose a solution client-side:
  
      #. Let the project define a centralized place where to store these binaries
      
      #. Add that repository to your project as a snapshot repository::
  
          swgit proj --add-repo --snapshot
  
      #. **From now on, only 1 commit will be downloaded when cloning this project**.
  

      .. figure:: images/static/swgit_project_snapshot_repo.gif
        :scale: 65 %
        :align: center

  
  * When you want another binary version, suppose that stored on LIV/Drop.A, just issue this
    command from inside project directory::
  
      swgit proj --reset 1/0/0/0/andreav/INT/stable/LIV/Drop.A <SNAP_REPO>
  
    This will download commit stored inside project at label LIV/Drop.A.
  
    .. note::
      Reference is relative to project history.
      Indeed, no history at all is present inside <SNAP_REPO>.
  
  
  * swgit stores all snapshot configuration under:
  
      $PROJ_ROOT/.swdir/cfg/snapshot_repos.cfg
  
    You can also customize:
    
      * compression format: `tar` or `zip` (default is `tar`)
    
      * de-compression tool path: this tool will be invoked to locally decompress 
        binary. (default is `tar`)
  
  
  * You can always transform you snapshot submodule into a regular one, just issuing::
    
      swgit proj --init <SNAP_REPO>
  
    But this could take a long time, because entire history will be pulled.

