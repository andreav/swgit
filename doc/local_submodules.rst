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


.. _lbl_proj_local_submodules:

################
Local submodules
################

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

