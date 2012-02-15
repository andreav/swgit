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

##############
Workflow - ssh
##############

This workflow will describe any ssh communication scenarios. 

It is only an hint on how to organize your repository in the most
frequent scenario:

  **when you have an ssh server with shell access**

ssh will guarantee secure communication and user differentiation, 
so it is ideal:

  * during development phase 

  * when managing team work


ssh identity management
=======================

User can configure ssh identities by modifying ~/.ssh/ssh_config file.

| ``swgit ssh`` command is available too.
| It will leverage GIT_SSH environment variable. (see :doc:`ssh`)
| In this context, this is a different way for accomplishing similar result.

1. **swgit no password identity**

  This is the fastest ssh identity set up.

    ::

      swgit ssh --create-nopassw-id
      swgit ssh --copy-identity <remote-user> <server-addr> 

  This will avoid any further password management.
  It will:

    * create no-password identity under ~/.ssh/swgit_sshid_nopass

    * copy it under ~<remote-user>/.ssh/authorized_keys @ <server-addr>

    * every time ssh communication with remote-addr will happen (for instance during
      pull or push) this identity will be provided, and no password will be asked

    * no ssh-agent is required

    * try issuing:
      
      ::

        swgit ssh swgit ssh --show-local-cfg

      for further analyzing.

  .. note::
    Empty password can be used only when you are sure 
    no one can break your ~/.ssh directory


2. **ssh identity and ssh-agent**
 
    ::

      ssh key-gen -t rsa -f ~/.ssh/myswgit_ssh_id    #just an example

      swgit ssh --copy-identity --identity ~/.ssh/myswgit_ssh_id <remote-user> <server-addr> 

      ssh-agent
      #cut&paste output of this command into same shell
      SSH_AUTH_SOCK=/tmp/ssh-szxaUHJ30562/agent.30562; export SSH_AUTH_SOCK;
      SSH_AGENT_PID=30563; export SSH_AGENT_PID;

      ssh-add ~/.ssh/myswgit_ssh_id

  It will:

    * create identity with passphrase

    * copy it under ~<remote-user>/.ssh/authorized_keys @ <server-addr>

    * launch ssh agent, export ssh-agent env var, add private identity

      .. note::
        maybe you already have an ssh-agent spawn 
        (i.e. see `github <http://help.github.com/ssh-key-passphrases/>`_).
        In this case just add your identity.




Main-User workflow
==================

   |subs_img_todo| add image

1.  Only one main-user account on server.

2.  Repository is created on server with plain ``swgit init``:

    ::

      swgit init -r 1.0.0.0

3.  From every team user workstation, ssh identity configuration may be 
    accomplished by this commands:

    ::

      swgit ssh --create-nopassw-id
      swgit ssh --copy-identity <main-user> <server-addr> 

    Password will be asked.
    If password cannot be broadcasted, ask server maintainer
    to manually add your public half identity (should be under 
    `~me/.ssh/swgit_sshid_nopass.pub`) to 
    `~<main-user>/.ssh/authorized_keys`

4.  Every team user will clone with <main-user> account:

    ::

      swgit clone ssh://<main-user>@<server-addr>/path/to/repo

    From now on, every communication will occur transparently.



One user-one accounts workflow
==============================

   |subs_img_todo| add image

1.  Each user can log into remote-addr with its own account.

    All users belong to same group.

2.  Repository is created on server by any user belonging to team group:

    ::

      swgit init -r 1.0.0.0 --shared group

    --shared will be transparently passed to ``git init``


3.  From every team user workstation, ssh identity configuration may be 
    accomplished by this commands:

    ::

      swgit ssh --create-nopassw-id
      swgit ssh --copy-identity <me> <server-addr> 

    Password will be asked.
    If password cannot be broadcasted, ask server maintainer
    to manually add your public half identity (should be under 
    `~me/.ssh/swgit_sshid_nopass.pub`) to 
    `~<main-user>/.ssh/authorized_keys`


4.  Every team user will clone with his own account:

    ::

      swgit clone ssh://<me>@<server-addr>/path/to/repo





