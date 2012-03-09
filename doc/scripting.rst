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

.. _lbl_scripting:

################
Script mechanism
################

swgit is a bunch of python scripts trying to build useful functionalities 
around git tool.

Key concept here is:

  **let git do what git is best able to do**

So swgit *intercepts* only a subset of git commands, in order to add 
swgit functionalities and implement swgit workflows.

So, for instance, ``git log`` or ``git diff`` are left untouched.

You can issue:

  ::

    git log -1

or:

  ::

    swgit log -1

and obtain the same result (swgit forwards transparently to git).

  .. image:: images/static/swgit_scripting.gif
    :scale: 60


| Following, a list of intercepted commands.
| (Otherwise, you can issue ``swgit <TAB> <TAB>`` and only swgit intercepted commands will be presented)

  * branch
  * checkout
  * clone
  * commit
  * init
  * merge
  * pull
  * push
  * tag

swgit introduces also any new commands:

  * info
      a ``git log`` friend, a place where to put useful swgit 
      specific retrieve operations

      Please refer to :doc:`infocmd` for some information.

  * ssh
      ssh management

      Please refer to :doc:`ssh` for some information.

  .. * lock
      No more used, was intended to lock remote repositories during push

  * proj
      This is a ``git submodule`` friend. By this command, user can 
      leverage git submodules in a simpler (though similar) form.

      Please refer to :doc:`projects` for some information.

  * stabilize
      This command manages 'stable branch matters'. User reports onto `stable` branch
      contributes candidate to be delivered, creates STB and LIV labels (see :ref:`lbl_references_tags`),
      creates changelogs and fixlogs.

      Please refer to :doc:`stabilizing` for some information.



