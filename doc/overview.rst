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
Overview
########

**The primary goal of swgit is to provide git users with a complete solution
for managing projects with developers' team.**

  .. image:: images/static/swgit_overview_repo.gif
    :scale: 40 %


swgit organizes your git repository in a structured way
-------------------------------------------------------

swgit provides and supports application level workflows over git repositories.

It is built turning special attention to:

  * releases management

  * periodically delivering software packages 

  * team working

  * supported customers

It chooses a 'Shared Repository' collaborative model:

  * team members are responsible for integrating and pushing to 'origin' their work

  * however central integrator figure still exists, responsible for delivering software 
    packages

Preferred communication mechanism is :doc:`ssh <ssh>`.

When working with :doc:`projects`, shell access on 'origin' repository must be available.

| At the moment, swgit only works on Linux platforms.
| Thanks to its python nature, Windows porting should be not too difficult. 
| Anyone who wishes to contribute is welcome!


History full of informations
----------------------------

  **Enriching repository with lots of informations retrievable at a glance.**
 
  Personally I do not like straight, single commit lined up, git histories.
 
  During team or standalone development I need many tags, from different kinds,
  representative for me at a glance.
  Too lazy to run fantastic git commands for retrieving basic informations 
  or to compose smart aliases.
 
  .. image:: images/static/swgit_topic.png
    :align: center


  * Organizing branches and labels in hierarchical way, leveraging git namespaces. (:doc:`references`)
 
  * Built-in management of release and sub-releases.
  


Defining Integrator and Developers Roles
----------------------------------------

  Integration happens at two levels:

    1. Every **Developer** is responsible for merging his/her contributes

    2. An **Integrator** is responsible for delivering software product 
       stable versions.

  Thanks to repository structure, both roles can continue working in the same repository
  without  getting in each others way:
 
  * | *Developers* do not interfere with build/delivery process.
    | *Developers* work around *INT/develop* branch.
 
  * | *Integrator* can take his time to build/deliver
      without stopping developers at all.
    | *Integrator* work around *INT/stable* branch.
 
  .. image:: images/static/swgit_stb.png
    :align: center

 Please refer to :doc:`roles`.


Agile natural support
---------------------

  Encourage agile principles by providing natural care toward:
  
    * team working
  
    * continuous integration
  
    * continuous testing
  
    * frequent delivery
  
    See :doc:`repository_structure`, :doc:`developing` and :doc:`stabilizing`.



Defining repository customers
-----------------------------

  Particularly useful when supporting client-specific requirements.

  | swgit let the *Integrator* create customer-specific branches.
  | These branches receives special treatment according to different workflows.

  .. image:: images/static/swgit_cst.png
    :align: center

  Please refer to :ref:`lbl_role_customer` and :doc:`workflow_customer`


Repository modularity
---------------------

  Personally I find *submodules* a bit tricky.

  In my opinion they are fantastic if used for third party libraries,
  but practically very difficult to leverage when deciding to split your
  repository into sub repositories and develop inside all of them.

  Also, *git subtrees* alternative is not suitable for me, simply too complicated.

  In synthesis: 
    *both submodules and subtrees are difficult to leverage especially when contributing back to origin repository, and, for newbies, quite unusable at all.*

  swgit boosts repository modularity with :doc:`projects`:
  
    * They are completely compatible with 'git submodule' leveraging their main features

    * They reuses every single-repository workflow
  
    * They introduce 2 new workflows:
  
      * **Local submodule** encourage users to adopt submodules not only 
        for third-party libraries but above all for splitting his/her 
        repositories in modules (see :ref:`lbl_proj_local_submodules`)
  
         .. image:: images/static/swgit_project.gif
           :align: center
           :scale: 50 %

      * **Snapshot repositories** represent a client-side solution to
        big-binaries repositories problem for DVCSs 
        (see :ref:`lbl_proj_snapshot_repositories`)


Simplifying git usage for newbies
---------------------------------

  1.  Many *Deny Scenarios* are implemented to:

       * Avoid dangerous behaviors/commands

       * Force user following built-in workflows

  2. Some operations are automatically carried out by the tool:

       * tracking branches when necessary

       * pulling repository to guarantee fast-forward pushes

       * ...

  3. Some functionalities are moved under logical command they belong to:

       * Deleting a tag remotely is done by ``swgit tag`` command instead of 
         pushing an empty reference on 'origin'

       * Moving around repository is realized by ``swgit branch`` command,
         instead of ``git checkout``

       * ...

  4. Well defined workflows are supported in order to shorten and simplify 
     development when following them. (:doc:`workflows`)


Customization
-------------

  swgit lets the user customize workflows (:doc:`custom_tags`) by providing:
  
    * possibility in defining new labels, integrated in existent workflows
  
    * changing tags behaviors
  
    * specifying pre- and post- tagging hooks

    * ...


Automatic mail delivery
-----------------------

  It is possible to configure your repository for automatically 
  delivering mails at push and deploy time.

  This reveals comfortable to track developments by email.

  Please refer to :doc:`mail`

Logging everything
------------------

  Every operation, its output, beginning and final commits are logged on 
  a per-user basis.
 
  Every time you need troubleshooting a problem, you can count on this 
  precious resource.

  Please refer to :doc:`logs`

