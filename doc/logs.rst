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

#######
Logging
#######

swgit logs everything is done inside your repository.

File log is contained into 

  ``.swdir/log/``

directory, next to .git directory.

There, for each user managing the repository, you will find 2 files:

  #. **<username>_slim.log**:

      | This file is intended to review operations from a general point of view.
      | Only issued command are listed here.

  #. **<username>_full.log**:

      | This file is a detailed log containing all operations a user issued,
        their output, and some details about the context the user issued them into.
      | When you need troubleshooting a problem, this is the first place from where to start.
