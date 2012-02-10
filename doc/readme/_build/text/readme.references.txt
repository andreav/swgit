
References
**********

Every reference (branches or tags) inside a swgit repository has a
well defined shape.

*SwReferences* present a nested informations structure built by git
namespaces.

By this way, all standard git commands can work with them
trasparently.

                                *************************************
   1/0/0/0/andreav/INT/develop  ** branch shared by all developers **
      |                         *************************************
      V

      |
      |  1/0/0/0/user/FTR/topic/NEW/BRANCH

      A ----->---.            ********************************
                  \          * Topic branch was created here, *
      |            \         * NEW/BRANCH marks this commit   *
      |             \         ********************************
      |              X
      |              |
      |              |
      |              |       ******************************
      |              |      * FIX: this tag declares an    *
      |              |      * issue has been resolved here *
      |              |       ******************************
      |              |
      |              Y  1/0/0/0/user/FTR/topic/FIX/1234567
      |              |
      |              |
      |              Z  1/0/0/0/user/FTR/topic/DEV/000
      |              |  1/0/0/0/user/FTR/topic
      |              |
      |              |        ***************************************
      |              |       * DEV: develop declares hos contribute  *
      |              .       *      is ready to be merged into       *
      |             /        *      INT/develop and pushed to origin *
      |            /          ***************************************
                  /
      B -----<---'

      |
      |


Branches
========

A branch reference has this configuration:

   **<Release>/<SubRel>/<Maint>/<Opt>/<User>/<BrType>/<BrName>**

   * <Release>/<SubRel>/<Maint>/<Opt>:
        Release informations for this branch

   * <User>
        User owner of this branch

   * <BrType>
        Branch type. There are four branch types:

        * INT:
             Special branches *develop* and *stable* have this branch
             type. These branches are usually created/managed by the
             repository maintainer. See "repository_structure" for
             more informations about these branches.

        * FTR:
             Any developer creates this kind of branch. These branches
             will contain many different kind of tags (marking
             different code phases) according to user needs. (see tags
             and "custom_tags")

        * FIX:
             This is a special case of FTR branches, created only for
             hot-fix before product delivery. This kind of branch
             starts from *stable* branches. Their contributes should
             be reported on *develop* branches as soon as possible
             (better if by patch mechanis, in order to avoid merging
             *develop* and *stable* histroies)

        * CST:
             This branch takes care about special customers and their
             needs. In most cases, for every release, your repository
             will contain one develop/stable branches to develop onto,
             and many customer branches to keep special configuration
             onto.

   * <BrName>
        This is a name user-provided to identify this branch.
        *develop* and *stable* branches can be modified pre-pending a
        BrName. For FTR, FIX and CST branches, name is completely
        arbitrary.

   Examples:

      1/0/0/0/auser/INT/develop
      1/0/0/0/auser/INT/stable
      1/0/0/0/auser/INT/aproduct_develop
      1/0/0/0/andreav/FTR/aNiceFeature
      1/0/0/0/andreav/FIX/lastminute_fix


Tags
====

A *swTag* is always created srarting from a *swBranch*.

So its name is composed by the complete branch name, followed by a
TagType and TagName:

   **<FullBrName>/<TagType>/<TagName>**

   * <FullBrName>:
        As described at branches

   * <TagType>:
        swgit provides any built-in tag types.

        However, user can customize tags according to its needs, both
        slightly modifying built-in tags behaviour, or completly
        defining new tags and its behaviour as described at
        "custom_tags"

        * Management tag types:

          * LIV:
               This tag is used to mark a sofware delivery. It is
               placed on *stable* branches. User cannot manually
               create it, only "swgit stabilize --liv" command can
               create it.

          * STB:
               This tag is used to mark a sofware ready to be
               delivered. Hoever, it differs from LIV tag because we
               can mark many times a software as 'stable' before
               deciding to deliver it (and tag with LIV). STB labels
               indicate a commit ready to be delivered. User cannot
               manually create it, only "swgit stabilize --stb"
               command can.

          * NGT:
               This tag is used to mark a sofware having passed
               'nightly tests'. This tag is very useful inside agile
               project. If your project foresee automatic tests, after
               every passed session you can tag current commit with
               this label. NGT commits are good candidates to be
               'stabilized'.

        * Development tag types:

          * DEV:
               This is the most commom label.It indicates work if finished and ready to be integrated.In order for a developer to push her contributes on 'origin', she must
               tag last work commit with a DEV label.Furthermore, DEV labels are collected during delivery in order to create
               changelog.

          * FIX:
               This label is used to mark a commit as fixing some issue.This is very useful when looking for changes introduced to fix
               a certain issue.Furthermore, FIX labels are collected during delivery in order to
               create fixlog.

          * RDY:
               This label is used to mark a commit as having reached any
               interesting phase.Main feature of this tag: it is *local*, not pushed on 'origin'.It can be very useful inside team working, for indicating an
               interesting commit
               without having to share long and error-prone md5sum commit sha.

   * <TagName>:
        Tag Names are used to identify a tag. They can be
        automatically evaluated by swgit, or user provided.

        * Automatically evaluated tag names:

          DEV, and RDY fall in this category.Their names are from 000 on.

        * User provided tag names:

          All other built-in labels need the user supplies a parameter
          when creating a tag.This argument must match a user-definable list of regular expressions.Every tag has its default regular expression list, but user can change it.For instance:

             FIX labels must declare which issue they fix. Its name depends on the context.STB/LIV labels take the delivery name. This also will be choosed by the user.To customize tags, please refere to :doc:custom_tags

   Examples:

      1/0/0/0/auser/INT/develop/NGT/Drop.A
      1/0/0/0/auser/INT/develop/STB/Drop.A
      1/0/0/0/auser/INT/stable/STB/Drop.A
      1/0/0/0/auser/INT/stable/LIV/Drop.A
      1/0/0/0/andreav/FTR/aNiceFeature/DEV/000
      1/0/0/0/andreav/FTR/aNiceFeature/DEV/001
      1/0/0/0/andreav/FTR/aNiceFeature/FIX/Issue1234
      1/0/0/0/andreav/FTR/aNiceFeature/RDY/000
