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

#######################
Automatic mail delivery
#######################

User can configure parameters for automatic mail delivery.
  
| Mails are automatically delivered at LIV-creation time and push time.
| User can always turn on/off this feature by command line options.
  
Configuration happens inside file:

  ::

    ${REPO_ROOT}/.swdir/cfg/mail.cfg

Configuration can be checked by issueing:

  ::

    swgit push      --show-mail-cfg
    swgit stabilize --show-mail-cfg

Mail delivery configuration can be tested using:

  ::

    swgit push      --test-mail-cfg
    swgit stabilize --test-mail-cfg


| As any other swgit configuration, values written inside `mail.cfg`
  file represent a default value for repository they are defined inside.
| User can always overload that default value by git config command, as described
  by `--show-mail-cfg` option for both commands.
  
In order to send mails, a command must exists:

  ::
    
    /bin/mail

| Mail server can be local or remote. 
| In the latter case, ssh user/addr must be provided.

  .. todo::
    Let also /bin/mail be configurable


  .. note::
    For push mail delivery, 'to' field will be choosed among::

      1. git config --get --local user.email
      2. git config --get --global user.email
      2. git config --get swgit.PUSH.TO
      3. ${REPO_ROOT}/.swdir/cfg/mail.cfg, section PUSH, key TO


Following a file configuration example::

  
    [stabilize]
    mailserver-sshuser = andreav
    mailserver-sshaddr = 213.92.16.171
    from               = andreav.pub@gmail.com
    to                 = andreav.pub@gmail.com another.developer@yahoo.com
    cc                 = 
    bcc                = 
    subject            = swgit stabilize notification
    body-header        = Hi All!\nA new drop has been released\n"
    body-footer        = 
    
    [push]
    mailserver-sshuser = andreav
    mailserver-sshaddr = 213.92.16.171
    from               = andreav.pub@gmail.com
    to                 = 
    subject            = swgit push mail notification


