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

.. toctree::
  :hidden:

##############
ssh management
##############

swgit supports any git url (because it transparently passes them to git)

| However swgit pays special attention to company workflows.
| Companies, often rely on ssh communication. Thus swgit foresees 
  some special ssh handling.

First of all, ssh can of course be configured by changing ~/.ssh/ssh_config file

Instead, swgit leverages SSH_GIT environment variable:

  | This variable in used by git during ssh communication.
  | We can think to it as a 'ssh alias'.

By this variable, user can specify on per repository basis:

  * which ssh binary to use
    
  * which ssh identities to provide

Also, a default swgit no-password identity can be created and added remotely 
to simplify communication, leading to some advantages:

  * no password at all will be asked

  * no ssh-agent must be used

| Just a note: this is nothing new, it's plain ssh management.
| However, a command exposing an interface to analyze, test and change ssh configuration
  can speed up these steps.
| This command is:

  ::

    swgit ssh -h
  
    Usage: swgit ssh --create-nopassw-id
           swgit ssh --show-local-cfg
           swgit ssh --test-remote-access [<user>] <address>
           swgit ssh --copy-identity [--identity <identity>] [<user>] <address> 

Please refer to :doc:`workflow_ssh` for any examples.

Analyzing ssh configuration
---------------------------

By issuing:

  ::

    swgit ssh --show-local-cfg

output example:

  ::

    * ssh local repository configuration:
    	Is valid                           True
    	ssh executable                     ssh
    	provided identities                []
    	use nopassw swgit identity         True
    	
    * Configuration:
    	
    	Optional fields:
    	
    	 * ssh executable                 by "git config swgit.ssh.bin <val>"
    	                                  or by file:   .swdir/cfg/generic.cfg, section ssh, key bin
    	 * provided identities            by "git config swgit.ssh.identity(-1, -2, ...) <val>"
    	                                  or by file:   .swdir/cfg/generic.cfg, section ssh, key identity(-01, -02, ...)
    	 * use nopassw swgit identity     by "git config swgit.ssh.use-nopassw-id <val>"
    	                                  or by file:   .swdir/cfg/generic.cfg, section ssh, key use-nopassw-id
    
    * No-password identity:
    	/home/andreav/.ssh/swgit_sshid_nopass       Created
    	/home/andreav/.ssh/swgit_sshid_nopass.pub   Created
    
    * GIT_SSH:
    	ssh -i /users/andreav/.ssh/swgit_sshid_nopass
	

user can check current repository ssh state.

Remember, ssh final behavior can be affected also by ~/.ssh/ssh_config configuration.

Following, an explanation for every output section:

  1. ``ssh local repository configuration``

     Here current values are listed.

  2. ``Configuration``

     Here user can see how to change default values.

     User has always at least two choices:

      * by `git config`: higher priority, this configuration always wins.

      * by editing a configuration file under ``${REPO_ROOT}/.swdir/cfg/`` directory
        
     For more informations about swgit tool configuration, please refer to :doc:`configure`

  3. ``No-password identity``

     This section reports informations about default swgit no-password identity.

     By default, if created, it is always provided to server at ssh communication time.

     To create it, just issue:

       ::

         swgit ssh --create-nopassw-id

  4. ``GIT_SSH``

     This variable is exported during every swgit command.

     Here, its value, is printed.

     After modifying swgit ssh configuration, you will notice changes here.

Testing ssh remote access
-------------------------

User can check ssh reachability toward remote server hosting 'origin' repository:

  ::

    swgit ssh --test-remote-access [<user>] <address>

output example:

  ::

    Testing reachability for current user 'andreav' toward 'andreav@localhost'
    REACHABLE!
    
    Testing shell access for current user 'andreav' toward 'andreav@localhost'
    SHELL ACCESS!

| First test will check if server is reachable. This means ssh communication works.

| Second test will check if shell access is provided. 
| From a swgit point of view, this means:

  1. You can automatically copy ssh public identity under ``~<user/.ssh/authorized_keys`` by
     issuing:

     ::
     
        swgit ssh --copy-identity --identity <a_public_id_half> [<user>] <remote_addr>

  2. When cloning :doc:`projects`, swgit can check if cloning local or remotes subrepositories
     (please refer to :ref:`lbl_proj_local_submodules`)


During both operations password may be asked. Any reasons can be:

  1. no public key has already been copied onto server side

  2. no private key has already been configured to be offered when connecting neither inside 
     ``~/.ssh/ssh_config`` nor by ``git config swgit.ssh.identity <a_priv_id>`` (see below)

  3. identities are correctly configured, but not loaded into ssh-agent


Adding ssh identities
---------------------

When user wants to provide a new identity, he/she can issue:

  ::

    git config swgit.ssh.identity <a_private_id>

From now on, when using ssh connections, this identity will be added.

| Try issuing ``swgit ssh --show-local-cfg``
| Now, configuration will change
| from:

  ::

    ssh local repository configuration:
      ...
      provided identities                []
      ...

    GIT_SSH:
    	ssh

to:

  ::

    ssh local repository configuration:
      ...
      provided identities                [ '<a_private_id>' ]
      ...

    GIT_SSH:
    	ssh -i <a_private_id>

Now, is up to user copying public identity half on the server, or, given shell access is provided,
he/she can try:

  ::

    swgit ssh --copy-identity --identity <a_public_id_half> [<user>] <remote_addr>


Please refer to :doc:`workflow_ssh` for any examples.
