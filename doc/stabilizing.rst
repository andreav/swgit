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

      swgit stabilize --stb --source <reference> Drop.A 


  `Drop.A` is the name of next delivery. This name will be matched against
  STB label regexp configuration parameter; default value is:

    ::

        ^Drop\.[A-Z]{1,3}(_[0-9]{1,3})?$

  If you want to change `STB` regexp, please refer to 
  :ref:`lbl_tags_analyzing` and :ref:`lbl_tags_setting`.

  This command will:

  * Merge --source <reference> argument into target *INT/stable*

  * | Create 1/0/0/0/andreav/INT/develop/STB/Drop.A - This mark *INT/develop* starting point.
    | Only if --start-point-label option is provided.

  * Create 1/0/0/0/andreav/INT/stable/STB/Drop.A  - This mark *INT/stable* arrival point.


  .. note::
    | By default, --source argument must be a NGT tag. 
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

      swgit stabilize --stb --liv --source <reference> Drop.A 2/0/0/0/andreav/CST/customer


  This command will:
  
  1. Merge starting reference onto CST target branch.

  2. Create a STB label on target branch

  3. Create a LIV label on target branch.


  If you prefer, you can separately issue --stb and --lib options, thus obtaining:

    ::

      swgit stabilize --stb --source <reference> Drop.A
    
      swgit stabilize --liv Drop.A


.. _lbl_stabilizing_configuration:

Configurations
--------------

  Stabilizing process can be customized according to user needs:

  1. Start point STB label:

     ::

       swgit stabilize --stb --start-point-label

     If user wants to mark --source reference, he/she can provide previous option
     in order to create /INT/develop/STB label.

     This option is ignored when stabilizing onto CST branches.

  2. Do not create changelog, fixlog and ticketlog:

     ::

       swgit stabilize --liv --no-chglogs

     | This option will not create those 3 files.
     | When this option is specified, and no hook pre-liv-commit (see below) 
       is configured, no brand-new liv commit will be created.
     | LIV label will be placed onto last INT/stable or CST/customer commit.

  3. Merge back INT/stable onto INT/develop after LIV creation:

     ::

       swgit stabilize --liv --merge-back

     | Attention, this will merge *INT/develop* and *INT/stable* histories.
     | This is not always a bad thing, but could not be what you want.
     | If you once need reporting  *INT/stable* onto *INT/develop*, please
       consider using patch mechanism instead.

  4. Hook pre-liv-commit: 

     User can intercept stabilize process right before creating LIV commit.
     This could be useful in many scenarios, for instance if user need to modify 
     some version file.

     ::

       swgit stabilize --show-cfg

     output:

     ::

        =================
        * PRE-COMMIT-HOOK
        =================
          --------------------------------------------------
          Is valid                           False
          Hook pre-liv-commit script         @@ Mandatory field not set @@
          Hook pre-liv-commit ssh user       
          Hook pre-liv-commit ssh addr       
          --------------------------------------------------
          
          Mandatory fields:
          
           * Hook pre-liv-commit script     - 'git config swgit.stabilize.hook-pre-liv-commit-script <val>'
                                            - file        .swdir/cfg/generic.cfg
                                              sect        stabilize
                                              key         hook-pre-liv-commit-script
          Optional fields:
          
           * Hook pre-liv-commit ssh user   - 'git config swgit.stabilize.hook-pre-liv-commit-sshuser <val>'
                                            - file        .swdir/cfg/generic.cfg
                                              sect        stabilize
                                              key         hook-pre-liv-commit-sshuser
           * Hook pre-liv-commit ssh addr   - 'git config swgit.stabilize.hook-pre-liv-commit-sshaddr <val>'
                                            - file        .swdir/cfg/generic.cfg
                                              sect        stabilize
                                              key         hook-pre-liv-commit-sshaddr
        

     | In this example, no hook has been configured.
     | To configure it, please follow instructions at :doc:`configure`

     * **hook-pre-liv-commit-script**:

         | Specify a script to be invoked before creating LIV commit.
         | Arguments passed to the script:
         |   $1 = LIV label going to be created
         |   $2 = target branch during stabilize process (*INT/stable* or *CST/customer*)
         | If return value if different from 0, stabilization process will fail.

     * **hook-pre-liv-commit-sshuser**:

         If specified, invoke `hook-pre-liv-commit-script` over ssh, with specified user

     * **hook-pre-liv-commit-sshaddr**:

         If specified, invoke `hook-pre-liv-commit-script` over ssh, toward specified IP address



  5. Hook pre/post-liv-tag:

     As for any other swgit label, user can configure pre- and post- tag hooks
     also for STB and LIV label.

     This hook should be preferred (in respect to previous one) if user 
     does not need to modify working tree.

     To configure them, please refer to :doc:`custom_tags`.

     ::

       swgit tag --show-cfg LIV

     output:

     ::

       Current configuration for tag "LIV" is:
       
         Tag Type                           LIV
         Is Default Tag                     True
         Is valid                           True
         Tag argument regexp                ['^Drop\\.[A-Z]{1,3}(_[0-9]{1,3})?$']
         Hook pre-tag script                
         Hook pre-tag ssh user              
         Hook pre-tag ssh addr              
         Hook post-tag script               
         Hook post-tag ssh user             
         Hook post-tag ssh addr             
         
       
       Configurable parameters for tag "LIV" are:
         
         Optional fields:
         
          * Tag argument regexp            - 'git config swgit.LIV.regexp(-1, -2, ...) <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         regexp(-1, -2, ...)
          * Hook pre-tag script            - 'git config swgit.LIV.hook-pretag-script <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         hook-pretag-script
          * Hook pre-tag ssh user          - 'git config swgit.LIV.hook-pretag-sshuser <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         hook-pretag-sshuser
          * Hook pre-tag ssh addr          - 'git config swgit.LIV.hook-pretag-sshaddr <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         hook-pretag-sshaddr
          * Hook post-tag script           - 'git config swgit.LIV.hook-posttag-script <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         hook-posttag-script
          * Hook post-tag ssh user         - 'git config swgit.LIV.hook-posttag-sshuser <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         hook-posttag-sshuser
          * Hook post-tag ssh addr         - 'git config swgit.LIV.hook-posttag-sshaddr <val>'
                                           - file        .swdir/cfg/custom_tags.cfg
                                             sect        LIV
                                             key         hook-posttag-sshaddr
       


  6. Changelog and Fixlog output format:

     | These files are created during stabilize --liv (except if --no-chglogs option is specified).
     | They are formatted using ``git for-each-ref --format='X'`` command.
     | User can change `--format` parameter provided to previous git command to change 
       file or mail output.
     | Mail output also supports configurable sort option.
     | In order to configure a multiline value, please refer to :ref:`lbl_configure_values`.

     ::

       swgit stabilize --show-cfg

     output:

     ::

       ====================
       * CHGLOG FILE FORMAT
       ====================
         --------------------------------------------------
         Is valid                           True
         CHGLOG file format                 From:    %(*authorname) %(*authoremail)
         Date:    %(*authordate)
         Ref:     %(refname)
         
             %(subject)
         
         --------------------------------------------------
         
         Optional fields:
         
          * CHGLOG file format             - 'git config swgit.stabilize.chglog-fmt-file <val>'
                                           - file        .swdir/cfg/generic.cfg
                                             sect        stabilize
                                             key         chglog-fmt-file
         
       ====================
       * FIXLOG FILE FORMAT
       ====================
         --------------------------------------------------
         Is valid                           True
         FIXLOG file format                 From:    %(*authorname) %(*authoremail)
         Date:    %(*authordate)
         Ref:     %(refname)
         
             %(subject)
         
         --------------------------------------------------
         
         Optional fields:
         
          * FIXLOG file format             - 'git config swgit.stabilize.fixlog-fmt-file <val>'
                                           - file        .swdir/cfg/generic.cfg
                                             sect        stabilize
                                             key         fixlog-fmt-file
         
       ====================
       * CHGLOG MAIL FORMAT
       ====================
         --------------------------------------------------
         Is valid                           True
         CHGLOG mail format                 From:    %(*authorname) %(*authoremail)
         Date:    %(*authordate)
         Ref:     %(refname)
         
             %(subject)
         
         --------------------------------------------------
         
         Optional fields:
         
          * CHGLOG mail format             - 'git config swgit.stabilize.chglog-fmt-mail <val>'
                                           - file        .swdir/cfg/generic.cfg
                                             sect        stabilize
                                             key         chglog-fmt-mail
         
       ===========================
       * CHGLOG MAIL SORT CRITERIA
       ===========================
         --------------------------------------------------
         Is valid                           True
         CHGLOG mail sort criteria          *authorname
         --------------------------------------------------
         
         Optional fields:
         
          * CHGLOG mail sort criteria      - 'git config swgit.stabilize.chglog-sort-mail <val>'
                                           - file        .swdir/cfg/generic.cfg
                                             sect        stabilize
                                             key         chglog-sort-mail
         

     If you want to test these parameters without issuing a swgit stabilize, 
     try modifying some value and issuing for instance:

     ::

        swgit info --change-log --upstream 1/0/0/0/swgit/INT/stable/LIV/Drop.A
        swgit info --fix-log    --upstream 1/0/0/0/swgit/INT/stable/LIV/Drop.A

     Output will be formatted according to chglog-fmt-file and fixlog-fmt-file.

     For some information about ``swgit info`` please refer to :doc:`infocmd`.

