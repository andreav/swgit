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

.. _lbl_proj_snapshot_repositories:

#####################
Snapshot repositories
#####################

A common feature among Distributed Version Control Systems is they must store
entire history inside every clone.

| This is a problem when you need to store big binaries, because they cannot be 
  significantly compressed.
| Furthermore, most of the time all previous versions are not useful.

  * swgit propose a solution client-side:
  
      #. Let the project define a centralized place where to store these binaries
      
      #. Add that repository to your project as a snapshot repository::
  
          swgit proj --add-repo --snapshot
  
      #. **From now on, only 1 commit will be downloaded when cloning this project**.
  

      .. figure:: images/static/swgit_project_snapshot_repo.gif
        :scale: 65 %
        :align: center

  
  * When you want another binary version, suppose that stored on LIV/Drop.A, just issue this
    command from inside project directory::
  
      swgit proj --reset 1/0/0/0/andreav/INT/stable/LIV/Drop.A <SNAP_REPO>
  
    This will download commit stored inside project at label LIV/Drop.A.
  
    .. note::
      Reference is relative to project history.
      Indeed, no history at all is present inside <SNAP_REPO>.
  
  
  * swgit stores all snapshot configuration under:
  
      $PROJ_ROOT/.swdir/cfg/snapshot_repos.cfg
  
    You can also customize:
    
      * compression format: `tar` or `zip` (default is `tar`)
    
      * de-compression tool path: this tool will be invoked to locally decompress 
        binary. (default is `tar`)
  
  
  * You can always transform you snapshot submodule into a regular one, just issuing::
    
      swgit proj --init <SNAP_REPO>
  
    But this could take a long time, because entire history will be pulled.


