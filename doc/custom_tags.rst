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

###########
Custom tags
###########

Tags are an essential part of a well structured and info filled repository.

swgit ships with a set of built-in labels (see :ref:`lbl_references_tags`).

| These tags try to cover as many scenarios as possible.
| Of course, however, every repository has its own history! ;)

| swgit lets the user modify tags behavior to better meet her needs.
| There are two levels of freedom in customizing tags.

  #. modifying hooks and regular expressions for built-in tags

  #. creating completely new tags, defining their mandatory and 
     optional characteristics

.. _lbl_tags_analyzing:

Analyzing tags configuration
============================

In order for the user to analyze a tag configuration, she can issue two command:

  1. ``swgit tag --custom-tag-list``

    By this command user can see every tag defined in current repository
    and its configuration

  2. ``swgit tag --custom-tag-show <TagType>``

    Given one TagType (like DEV, FIX or any user-defined one), user can see:

      * current tag configuration

      * configurable fields

      * wrong configured fields, if any


.. _lbl_tags_setting:

Setting tag values
==================

In order to modify any allowed tag parameter, user can choose among:

  #. Persistent way:
  
     By editing file 
  
       ``.swdir/cfg/custom_tags.cfg``

     under root repository (next to .git directory)

  * Volatile way:

     By issuing a ``swgit config`` command like this:

       ``swgit config swgit.FIX.regexp <val>``

     In this case user would override, for FIX tag, matched regexp 
     at creation time.




Modifying built-in tags behavior
=================================

For every built-in tag, user can override its optional fields.

Configurable fields change according to the tag.

In order to discover which ones, please run:

  ``swgit tag --custom-tag-show-cfg {LIV|STB|NGT|DEV|FIX|RDY}``


Creating a new tag
==================

You can define a new tag type.

This tag will behave exactly as you want, and will be integrated in all workflows like any built-in tag.

As an example, lets implement a tag to mark the blessed commit from which we created our project final release version.

We will give it a `REL` type.

#. Define new `REL` tag:

   * Persistent way:

      Open file ``.swdir/cfg/custom_tags.cfg`` and create a section like this:

        ``[REL]``

   * Volatile way:

      Issue this command:

        ``swgit config swgit.tagtype.REL blah``

#. Define this tag as :term:`numbered tag` or :term:`named tag`.

   * Numbered tags are created in this way:

        ``swgit tag REL``

   * Named tags requires the user provides another input parameter when creating tag:
     
        ``swgit tag REL meaningful_information_here``

     Tags fall into one or another category according to **regexp** field.

     | If `regexp` field is not provided, it's a numbered tag. swgit will evaluate tag name from 000 on.
     | Otherwise it's a named tag.


   Let's REL tag be a named tag, accepting 2 fields: 

     date, in the format HHHH-MM-DD

     or any sequence shorter that 15 characters.


   * Persistent way:

      immediately under [REL] section, add this row:

        ``regexp = ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ &@& ^[a-zA-Z]{0,15}$``

   * Volatile way:

      Issue this command:

        ``swgit config swgit.REL.regexp '^[0-9]{4}-[0-9]{2}-[0-9]{2}$ &@& ^[a-zA-Z]{0,15}$'``


   .. warning::
     When you need to specify a list of fields, 
     you must separator fields with this token:

       |subs_txt_regexpseparator|


#. Configure mandatory fields:

   They are:

     #. **push-on-origin**:
          Determines if this label will be pushed on origin (like DEV or FIX) 
          on will be only local (like RDY)

     #. **one-x-commit**:
          | Determines if more than 1 label can be put on same commit.
          | FIX labels behave in this way.
          | DEV label no.

     #. **only-on-trackall**:
          Determines if this tag can be created only on :term:`integrator repository`
          (like LIV or STB tags)


   * Persistent way:

      Under [REL] section, add these row:

        .. code-block:: c

          push-on-origin          = True
          one-x-commit            = True
          only-on-integrator-repo = True

   * Volatile way:

      Issue these commands:

        .. code-block:: c

          swgit swgit.REL.push-on-origin          True
          swgit swgit.REL.one-x-commit            True
          swgit swgit.REL.only-on-integrator-repo True

#. Configure Optional fields:

   They are:

     #. **allowed-brtypes**: (list)
          Allow tagging only on these branches.
          Not assigned means: all branches are allowed.

     #. **denied-brtypes**: (list)
          Deny tagging only on these branches.
          Not assigned means: never deny.

     #. **tag-in-past**:
          Let the tagger tag a commit already pushed on origin.

     #. all **pre-/post- tag hooks**:
          see (:ref:`tag hooks <lbl_tags_hooks>`)


.. _lbl_tags_hooks:
  
Pre- and post- tag hooks
------------------------
  
  swgit introduces a pre-tag hook and a post-tag hook configurable 
  for every label.

  They are optional configurable fields.
  
  Hook are defined by specifying a scripts to be invoked locally or remotely.

  In this second case, ssh user and address for remote machine must be specified too.
  
  User may provide:

    * **hook-pretag-script**:

        | Specify a script to be invoked before creating tag.
        | Arguments passed to the script:
        |   $1 = tag name to be created
        |   $2 = commit on which tag will be put
        | Script output will be used as tag comment, in addition to -m argument
          (if provided)
        | If the return value if different from 0, tag creation will fail.

    * **hook-pretag-sshuser**:

        If specified, invoke `hook-pretag-script` over ssh, with specified user

    * **hook-pretag-sshaddr**:

        If specified, invoke `hook-pretag-script` over ssh, toward specified IP address
    
    * **hook-posttag-script**:

        | Specify a script to be invoked after tag creation.
        | Arguments passed to the script:
        |   $1 = tag name just created
        |   $2 = commit on which tag has been put
        | Note: this hook will be triggered when tag is created locally.
        |       If you want a trigger when tag is pushed, use built-in git hooks.

    * **hook-posttag-sshuser**:

        If specified, invoke `hook-posttag-script` over ssh, with specified user

    * **hook-posttag-sshaddr**:

        If specified, invoke `hook-posttag-script` over ssh, toward specified IP address
  


