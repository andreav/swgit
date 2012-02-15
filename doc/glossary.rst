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

.. _lbl_glossary:

########
Glossary
########

.. glossary::
  :sorted:

  commit file
    Is a file present only into repositories containing submodules.
    One file exist for each submodule.
    They stores submodule HEAD when committing project repository.
    Try issuing::

      git ls-files HEAD

    in order to see those `commit` elements

  integrator repository
  track-all repository
    | It is a repository crated to manage releases and execute builds or deliveries.
    | It is a repository with both INT/develop and INT/stable local branches.
    | The most quickly way to obtain this, is cloning repository with option:

        ``--integrator``

    | Otherwise you can track it locally by issuing:

        | ``swgit branch --track <.../INT/stable>``
        | ``swgit config --bool swgit.integrator True``


  named tag
    | A tag with `regexp` field set.
    | swgit will match user input against that/those regexp
    | When configuring a regexp list, a string must be provided where 
      entries are separed by this field:

        |subs_txt_regexpseparator|

  numbered tag
    | A tag without `regexp` field set.
    | swgit will evaluate tag name starting from 000 on.
