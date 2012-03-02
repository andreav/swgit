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

#####
Roles
#####

Inside a swRepository, we can recognize three roles:

.. _lbl_role_integrator:

Integrators
===========

This is the repository maintainer.

He/She initializes the repository with a::

  swgit init --rel 1.0.0.0

command.

This command creates two branches::

  1/0/0/0/andreav/INT/develop
  1/0/0/0/andreav/INT/stable
    
Developers will work with INT/develop branch.

Integrator will report INT/develop contributes onto INT/stable thus obtaining many results:

  #. Shifting build/packaging/delivery on a different branch

  #. Letting users continue working on INT/develop

  #. In case, creating fix contributes to deliver a new fully working package.

When reporting contributes on INT/stable he/she will issue a command::

  swgit stabilize --stb --source <stabilized_reference> Drop.A

After packaging a new drop, he/she will collect changelogs and fixlogs, 
and will tag *INT/stable* commit with a LIV label by the command::

  swgit stabilize --liv Drop.A

Integrator works on a :term:`track-all repository`, i.e., a repository with 
INT/develop and INT/stable local branches.

Integrator is firstly interested into :doc:`Workflow - Stabilize <stabilizing>`.


.. _lbl_role_developer:

Developers
==========

Everyone contributing to the project is a Developer.

Developers starts developing from an :ref:`lbl_intbr` 
and integrate their contributes into the same :ref:`lbl_intbr`.

Developers usually work on a repository where `INT/stable` branch in remote,
though this is not mandatory.

Developers are firstly interested into :doc:`Workflow - Develop <developing>`.


.. _lbl_role_customer:

Customers
=========

Customers are represented in a swRepository by *CST* branch types.

Every time an Integrator decides to support a new customer, he/she issues a 
command like this::

  swgit init --rel 1.0.0.0 --cst <google> --source 1/0/0/0/andreav/INT/stable

This command creates this branch::

  1/0/0/0/andreav/CST/google

From now on, Integrator is responsible for keeping up to date with right contributes 
this branch.

Once again, Integrator best friend command is *stabilize*::

  swgit stabilize --stb --source <stabilized_reference_for_customer> Drop.A

This branch behaves similarly to INT/stable branch, but essentially stores all 
customer specific requirements.

When customer will reference our repository, hopefully he/she will select commits only
from his/her dedicated branch.

Integrator in a customer context is firstly interested into :doc:`workflow_customer`.

