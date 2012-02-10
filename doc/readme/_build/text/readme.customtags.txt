
Custom tags
***********

Tags are an essential part of a well structured and info filled
repository.

swgit ships with a set of buil-in labels (see *Tags*).

These tags try to cover as many scenarios as possible.Of course, however, every repository has its own history! ;)

swgit lets the user modify tags behaviour to better meet her needs.There are two levels of freedom in customizing tags.

   1. modifying hooks and regular expressions for built-in tags

   2. creating completely new tags, defining their mandatory and
      optional characteristics


Analizig tags configuration
===========================

In order for the user to analyse a tag configuration, she can issue
two command:

   1. "swgit tag --custom-tag-list"

      By this command user can see every tag defined in current
      repository and its configuration

   1. "swgit tag --custom-tag-show <TagType>"

      Given one TagType (like DEV, FIX or any user-defined one), user
      can see:

         * current tag configuration

         * configurable fields

         * wrong configured fields, if any


Setting tag values
==================

In order to modify any allowed tag parameter, user can choose among:

   1. Persistent way:

      By editing file

         ".swdir/cfg/custom_tags.cfg"

      under root repository (next to .git directory)

   * Volatile way:

        By issueing a "swgit config" command like this:

           "swgit config swgit.FIX.regexp <val>"

        In this case user would override, for FIX tag, matched regexp
        at creation time.


Modifying built-in tags behaviour
=================================

For every built-in tag, user can override its optional fields.

Configurable fields change according to the tag.

In order to discover which ones, please run:

   "swgit tag --custom-tag-show-cfg {LIV|STB|NGT|DEV|FIX|RDY}"


Creating a new tag
==================

You can define a new tag type.

This tag will behave exactly as you want, and will be integrated in
all workflows like any built-in tag.

As an example, lets implement a tag to mark the blessed commit from
which we created our project final release version.

We will give it a *REL* type.

1. Define new *REL* tag:

   * Persisten way:

        Open file ".swdir/cfg/custom_tags.cfg" and create a section
        like this:

           "[REL]"

   * Volatile way:

        Issue this command:

           "swgit config swgit.tagtype.REL blah"

2. Define this tag as *numbered tag* or *named tag*.

   * Numbered tags are created in this way:

        "swgit tag REL"

   * Named tags requires the user provides another input parameter
     when creating tag:

        "swgit tag REL meaningful_information_here"

     Tags fall into one or another category according to **regexp**
     field.

     If *regexp* field is not provided, it's a numbered tag. swgit will evaluate tag name from 000 on.Otherwise it's a named tag.

   Let's REL tag be a named tag, accepting 2 fields:

      date, in the format HHHH-MM-DD

      or any sequence shorter that 15 characters.

   * Persisten way:

        immedeately under [REL] section, add this row:

           "regexp = ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ &@&
           ^[a-zA-Z]{0,15}$"

   * Volatile way:

        Issue this command:

           "swgit config swgit.REL.regexp
           '^[0-9]{4}-[0-9]{2}-[0-9]{2}$ &@& ^[a-zA-Z]{0,15}$'"

   Warning: When you need to specify a list of fields, you must separator
     fields with this token:

        " &@& " (i.e. <space>&@&<space>)

3. Configure mandatory fields:

   They are:

      1. **push-on-origin**:
            Determines if this label will be pushed on origin (like
            DEV or FIX) on will be only local (like RDY)

      2. **one-x-commit**:
            Determines if more than 1 label can be put on same commit.FIX labels behave in this way.DEV label no.

      3. **only-on-trackall**:
            Determines if this tag can be created only on *integrator
            repository* (like LIV or STB tags)

   * Persisten way:

        Under [REL] section, add these row:

              push-on-origin          = True
              one-x-commit            = True
              only-on-integrator-repo = True

   * Volatile way:

        Issue these commands:

              swgit swgit.REL.push-on-origin          True
              swgit swgit.REL.one-x-commit            True
              swgit swgit.REL.only-on-integrator-repo True

4. Configure Optional fields:

   They are:

      1. **allowed-brtypes**: (list)
            Allow tagging only on these branches. Not valorized means:
            all branches are allowed.

      2. **denied-brtypes**: (list)
            Deny tagging only on these branches. Not valorized means:
            never deny.

      3. **tag-in-past**:
            Let the tagger tag a commit already pushed on origin.

      4. all **pre-/post- tag hooks**:
            see (*tag hooks*)


Pre- and post- tag hooks
------------------------

   swgit introduces a pre-tag hook and a post-tag hook configurable
   for every label.

   They are optional configurable fields.

   Hook are denifed by specifying a scripts to be invoked locally or
   remotely.

   In this second case, ssh user and address for remote machine must
   be specified too.

   User may provide:

      * **hook-pretag-script**:

           Specify a script to be invoked before creating tag.Arguments passed to the script:

           $1 = tag name to be created$2 = commit on wich tag will be put

           Script output will be used as tag comment, in addition to -m argument
           (if provided)If the return value if different from 0, tag creation will fail.

      * **hook-pretag-sshuser**:

           If specified, invoke *hook-pretag-script* over ssh, with
           specified user

      * **hook-pretag-sshaddr**:

           If specified, invoke *hook-pretag-script* over ssh, toward
           specified IP address

      * **hook-posttag-script**:

           Specify a script to be invoked aftre tag creation.Arguments passed to the script:

           $1 = tag name just created$2 = commit on wich tag has been put

           Note: this hook will be triggered when tag is created locally.

           If you want a trigger when tag is pushed, use built-in git hooks.

      * **hook-posttag-sshuser**:

           If specified, invok *hook-posttag-script* over ssh, with
           specified user

      * **hook-posttag-sshaddr**:

           If specified, invoke *hook-posttag-script* over ssh, toward
           specified IP address
