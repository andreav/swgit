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
Download
########

You can download last stable verison at:

  |subst_txt_latest_stb_url|_

If you prefer latest snapshot, refer at repository HEAD, (last develop version) at:

  |subst_txt_latest_dev_url|_

You can choose:

  ZIP version
    
or select one protocol (SSH, HTTP, "Git Read Only"), copy its associated <swgit_url> and issue:

  git clone <swgit_url> -b |subs_txt_latest_stb|

  git clone <swgit_url> -b |subs_txt_latest_dev|



.. note::
  both versions simply refer HEAD of::

    1/0/0/0/swgit/INT/develop
    1/0/0/0/swgit/INT/stable

  this could be the right moment for looking at :doc:`repository_structure` section.

You can now refer to :doc:`getting_started` section.
