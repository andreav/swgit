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

###########
Stabilizing
###########

.. only:: text

  .. include:: images/ascii/swgit_stabilizing_stb.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_stabilizing_stb.gif
    :scale: 70 %


| Every software project needs to identify stable versions.
| Developers contribute to the project; sometimes a line must be drawn.
| According to agile principles, as frequent as possible.

These requirements are met by swgit by introducing **INT/stable** branch.

Main branch goals are:

  #. storing all delivered stable software versions, labeled with
     :ref:`LIV <lbl_references_tags>` tag.

  #. storing candidates software for next drop, labeled with
     :ref:`STB <lbl_references_tags>` tag.

  #. | letting the integrator shift aside from the :doc:`develop process <developing>` 
       (turning around *INT/develop* branch).
     | On *INT/stable* he/she cat take necessary time for preparing,
       and in case  fixing, next delivery.

In this context `Integrator` refers to project maintainer, who reports 
contributes on `INT/stable`.

.. _lbl_stabilizing_ngt:

NGT tag
-------

  This tag is a :ref:`built-in swgit tag <lbl_references_tags>`.

  It is used by the Integrator, and is put only on *INT/develop* worth commits.

  `NGT` refers to 'nightly tests'. The idea here is:
 
    | At night, a test suite will check if repository HEAD is valuable.
    | If so, a NGT tag will mark that reference

  Day after, when integrator arrives at his/her desk, a NGT tag will 
  be a good candidate to be stabilized.

  Of course, Integrator will decide, according to feature list, if it's time
  for preparing a new delivery.


.. _lbl_stabilizing_reporting_stb:

Reporting on *INT/stable* (STB labels)
--------------------------------------

  Periodically Integrator will report a worth *INT/develop* commit onto 
  *INT/stable* by:

    ::

      swgit stabilize --stb --src <reference> Drop.A 


  `Drop.A` is the name of next delivery. This name will be matched against
  STB label regexp configuration parameter; default value is:

    ::

        ^Drop\.[A-Z]{1,3}(_[0-9]{1,3})?$

  If you want to change `STB` regexp, please refer to 
  :ref:`lbl_tags_analyzing` and :ref:`lbl_tags_setting`.

  This command will:

  * Merge --src <reference> argument into target *INT/stable*

  * Create 1/0/0/0/andreav/INT/develop/STB/Drop.A - This mark *INT/develop* starting point.

  * Create 1/0/0/0/andreav/INT/stable/STB/Drop.A  - This mark *INT/stable* arrival point.


  .. note::
    | By default, --src argument must be a NGT tag. 
      This encourages continuous testing agile principle.
    | If you need to stabilize any reference, please issue inside you repository:

        **swgit config swgit.stabilize-anyref True**


  .. note::
    | In order to strengthen concept that only Integrator can issue this command, 
      swgit will deny this operation on any repository but :term:`integrator repository`
    | This is a weak, easily workaroundable, limit. However this avoids accidental 
      command execution on a Developer repository.


.. _lbl_stabilizing_target_branch_selection:

.. rubric:: Target branch selection
-----------------------------------


  Target branches onto which to stabilize contributes always are
  INT/stable or CST/customer branches.

  In order to select target branch, *Integrator* can:

    1. Provide it on command line (last argument)::

         swgit stabilize --stb Drop.A 1/0/0/0/andreav/INT/stable

    2. Switch on it::

         swgit branch -s 1/0/0/0/andreav/INT/stable
         swgit stabilize --liv Drop.A

    3. Select appropriate integration branch 
       (*INT/develop* or *INT/stable* are equivalent, 
       they both translate to *INT/stable*)::

         swgit branch --set-integration-br 1/0/0/0/andreav/INT/stable
         swgit stabilize --liv Drop.A

 

.. _lbl_stabilizing_creating_liv:

Creating a delivery (LIV labels)
--------------------------------

  Integrator decides to release a delivery.

  1. He/She will go into an :term:`integrator repository`, 

  2. go onto stable branch thus selecting last stabilized commit::

      swgit branch -s 1/0/0/0/andreav/INT/stable

  3.1 If everything is ok he/she will ``stabilize --liv`` this commit (see below).

  3.2 If something has to be done before releasing, he/she will create a branch:
      
      ::

          swgit branch -c "hotfix"

      thus creating a :ref:`FIX branch <lbl_references_branches>`::

           1/0/0/0/andreav/FIX/hotfix

      from which to do necessary actions.

      When fix is  done, he/she will merge on *INT/stable*::

          swgit tag dev -m "hotfix for Drop.A"
          swgit branch -s 1/0/0/0/andreav/INT/stable
          swgit merge 1/0/0/0/andreav/FIX/hotfix/DEV/000

      
      Now he/she cal create a delivery.

  ::

    swgit stabilize --liv Drop.A

  This command will:
  
  1. Create three files under directory:

      ${REPO_ROOT}/.swdir/changelog/<REL>/

    * **Changelog**: containing all DEV labels from last repository LIV till now.

    * **Fixlog**: containing all FIX labels from last repository LIV till now.

    * **Ticketlog**: a machine readable file, containing only Ticket numbers. 
      (i.e. tagName for every FIX label)

  2. Add everything to the index and committing

  3. Tag with a LIV label:

      1/0/0/0/andreav/INT/stable/LIV/Drop.A 

  4. Merge */INT/stable* on */INT/develop* (this step can be jumped by providing option
     --no-merge-back when stabilizing --liv)

  5. Push everything on 'origin'


  When issuing **swgit stabilizing --liv**, target branch (branch to be labelled)
  will be selected like for **swgit stabilizing --stb** (see :ref:`here <lbl_stabilizing_target_branch_selection>`).

  .. note::
    | You can stabilize both --stb and --liv in one shot.
    | Just provide *--liv* option when issuing *swgit stabilize --stb*.

  .. note::
    | In order to strengthen concept that only Integrator can issue this command, 
      swgit will deny this operation on any repository but :term:`integrator repository`
    | This is a weak, easily workaroundable, limit. However this avoids accidental 
      command execution on a Developer repository.

.. _lbl_stabilizing_reporting_cst:

Reporting on CST/customer
-------------------------

.. only:: text

  .. include:: images/ascii/swgit_stabilizing_cst.txt

.. else
.. only:: not text

  .. image:: images/static/swgit_stabilizing_cst.gif
    :scale: 70 %

  When Integrator defines a :ref:`repository customer <lbl_role_customer>` by creating
  a CST branch, he/she is responsible for releasing stable software versions to him.

  This operation is a plain stabilization, with the exception that no merge back on *INT/develop*
  and no *INT/develop/STB/Drop.X* label will occur.

  CST target branch will be selected like for **swgit stabilizing --stb** and 
  **swgit stabilizing --liv** (see :ref:`here <lbl_stabilizing_target_branch_selection>`).

    ::

      swgit stabilize --stb --liv --src <reference> Drop.A 2/0/0/0/andreav/CST/customer


  This command will:
  
  1. Merge starting reference onto CST target branch.

  2. Create a STB label on target branch

  3. Create a LIV label on target branch.


  If you prefer, you can separately issue --stb and --lib options, thus obtaining:

    ::

      swgit stabilize --stb --src <reference> Drop.A
    
      swgit stabilize --liv Drop.A



