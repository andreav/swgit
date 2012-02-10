
Automatic mail delivery
***********************

User can configure parameters for automatic mail delivery.

Mails are automatically delivered at LIV-creation time and push time.User can always turn on/off this feature by command line options.

Configuration happens inside file:

      ${REPO_ROOT}/.swdir/cfg/mail.cfg

Configuration can be checked by issueing:

      swgit push      --show-mail-cfg
      swgit stabilize --show-mail-cfg

Mail delivery configuration can be tested using:

      swgit push      --test-mail-cfg
      swgit stabilize --test-mail-cfg

As any other swgit configuration, values written inside *mail.cfg*
file represent a default value for repository they are defined inside.User can always overload that default value by git config command, as described
by *--show-mail-cfg* option for both commands.

In order to send mails, a command must exists:

      /bin/mail

Mail server can be local or remote.In the latter case, ssh user/addr must be provided.

   Note: For push mail delivery, 'to' field will be choosed among:

        1. git config --get --local user.email
        2. git config --get --global user.email
        2. git config --get swgit.PUSH.TO
        3. ${REPO_ROOT}/.swdir/cfg/mail.cfg, section PUSH, key TO

Following a file configuration example:

   [STABILIZE]
   MAILSERVER-SSHUSER = andreav
   MAILSERVER-SSHADDR = 213.92.16.171
   FROM               = andreav.pub@gmail.com
   TO                 = andreav.pub@gmail.com another.developer@yahoo.com
   CC                 =
   BCC                =
   SUBJECT            = swgit stabilize notification
   BODY-HEADER        = Hi All!\nA new drop has been released\n"
   BODY-FOOTER        =

   [PUSH]
   MAILSERVER-SSHUSER = andreav
   MAILSERVER-SSHADDR = 213.92.16.171
   FROM               = andreav.pub@gmail.com
   TO                 =
   SUBJECT            = swgit push mail notification
