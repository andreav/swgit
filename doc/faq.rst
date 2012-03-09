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

###
FAQ
###

  * :ref:`lbl_faq_repo`

    #. :ref:`lbl_faq_repo_mail`

  * :ref:`lbl_faq_projects`

    #. :ref:`lbl_faq_projects_reset`

    #. :ref:`lbl_faq_projects_diff`



.. _lbl_faq_repo:

FAQ - Repository
================

.. _lbl_faq_repo_mail:

Is there automatic email delivery at push time?
-----------------------------------------------

  | Yes, mail is always automatically sent.
  | Only condition is correct configuration.
  | Please check and test mail configuration by issuing these commands:

  ::

     swgit push --show-mail-cfg
     swgit push --test-mail-cfg

  For more informations, please refer to :doc:`mail`.



.. _lbl_faq_projects:

FAQ - Projects
==============

.. _lbl_faq_projects_reset:

How can I inspect a submodule version stored at a certain project reference?
----------------------------------------------------------------------------

  ::

     swgit proj --reset LIV/Drop.A <reponame>

  This will checkout into your working directory the submodule version 
  stored at LIV/Drop.A into project repository.

  This is particularly useful when wanting to test a different submodule
  version keeping still all around.

  If you do not provide <reponame>, this command will:

    1. checkout provided reference into project repository

    2. checkout every submodule stored version into provided project commit



.. _lbl_faq_projects_diff:

How can I see submodules differences having two project versions?
-----------------------------------------------------------------

  ::

     swgit proj --diff [-R] [<ref1>] [<ref2>] [<reponame>...] [-- <diff options>...]

  | This command accepts references from project (container) repository.
  | This command outputs differences for submodules (contained) repositories.

  If you do not specify repositories, root directory and all first level submodules
  will be evaluated.

  You can ask to descend recursively into contained projects

  You can specify options to git diff underline engine to configure output.

  Anything after first '--' will be transparently passed to git diff (also another '--').
  

