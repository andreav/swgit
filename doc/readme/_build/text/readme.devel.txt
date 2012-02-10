
Developing
**********

    1/0/0/0/andreav/INT/develop
             |                                          |
             V                                          | time
                                                        v
             |
             |   1/0/0/0/user/FTR/topic/NEW/BRANCH

             A ----->---.
                         \
             |            \
             |             \
             |              X
             |              |
             |              |
             |              Y  1/0/0/0/user/FTR/topic/FIX/1234567
             |              |
             |              |
   origin    |              Z  1/0/0/0/user/FTR/topic/DEV/000
      \      |              |  1/0/0/0/user/FTR/topic
       \                    |
        '->> B              |
                            |
             |              .
    origin   |             /
       \     |            /
        \                /
         '<< C -----<---'

             |
             |


Collaborative Development Model
===============================

swgit first goal is speeding up contributes development and
integartion into 'origin' repository.

Every developer, in this context, covers also integartor role, meaning
that he/she will be responsible for merging its contributes into
"intbr".

We know two popular Collaborative Development Models exists (cut&paste
from github):

   1. The *Fork + Pull Model*

      lets anyone fork an existing repository
      and push changes to their personal fork without requiring access
      be granted to the source repository.The changes must then be pulled into the source repository by
      the project maintainer.This model reduces the amount of friction for new contributors
      and is popular with open source projects because
      it allows people to work independently without
      upfront coordination.

   2. The *Shared Repository Model*

      is more prevalent with small teams
      and organizations collaborating on private projects.Everyone is granted push access to a single shared repository
      and topic branches are used to isolate changes.

**swgit chooses `Shared Repository Model` as its collaboartive model**


Cloning repository
==================

   Only ssh and file system urls are supported.

   If this is the first time, and ssh url is specified, ssh management
   will occur. ("ssh")

      swgit clone ssh://user@addr/path/to/repo -b 1/0/0/0/andreav/INT/develop

   or:

      $> swgit clone /path/to/repo -b 1/0/0/0/andreav/INT/develop

   or:

      swgit clone ssh://user@addr/path/to/repo
      swgit branch --set-integartion-br 1/0/0/0/andreav/INT/develop

   Note: "intbr" is set once, and will speed up other operations.


Creating a topic branch
=======================

      swgit branch -c "topic"

   output:

      Creating branch 1/0/0/0/andreav/FTR/topic starting from HEAD ...
      DONE
      Creating starting branch label: 1/0/0/0/andreav/FTR/topic/NEW/BRANCH ...
      DONE

   A **NEW/BRANCH** tag will be put on the commit where the branch starts from.This tag reveals usefull in many cases, above all after
   criss-cross merges.
   To retrieve all differences introduced by this branch:

         swgit info -z/--zero-diff


Committing/labelling
====================

   * one shot:

        swgit commit -a -m "fixed issue 1234567" --fix 1234567 --dev

     output:

        Committing your contributes ...
        DONE
        Creating tag 1/0/0/0/andreav/FTR/topic/DEV/000 ...
        DONE
        Creating tag 1/0/0/0/andreav/FTR/topic/FIX/1234567 ...
        DONE

   * step-by-step:

        swgit commit -a -m "fixed issue 1234567"
        swgit tag fix 1234567 -M
        swgit tag dev -M

     Note: *-M* option reuses commit comment*-m* let the user provide a comment*Customizing pre-tag hook* is another
       way to avoid providing comment.


Merging
=======

   * one shot:

        swgit merge -I

     output:

        Switching to 1/0/0/0/andreav/INT/develop ...
        DONE
        First update your local repository ...
         Fetching origin
         Already up-to-date.
        DONE
        Merging refs/tags/1/0/0/0/vallea/FTR/topic/DEV/000 into refs/heads/1/0/0/0/andreav/INT/develop ...
         Merge made by recursive.
          a.txt |    1 +
          1 files changed, 1 insertions(+), 0 deletions(-)
          create mode 100644 a.txt
        DONE

     This command leverages integartion branch.It is called *side merge*It looks for last DEV tag on your topic branch and
     will merge that reference into integration branch.

   * step-by-step:

        swgit branch -i/--to-integration
        swgit merge 1/0/0/0/andreav/FTR/topic/DEV/000

   Merge operation (except for when providing -I option) always need a
   DEV label as argument.

      **Only DEV tags can be merged into integration branch**

   This is not mandatory for any other branch type.

   swgit assures user always merges on integartion branch HEAD.This is accomplished by issueing an

      **integartion branch pull before merging**

   This does not happen when merging into another branch.


Pushing
=======

   From integartion branch, after merging on it, user should test its
   contributes against integration branch HEAD.

   Eventually he/she will push on 'origin'.

      swgit push

   output:

      Check swgitdemo-clone repository push ...
        WARNING cannot send mail due to wrong configuration.
        Try issueing 'swgit push --show-mail-cfg' to investigate.
      DONE
      Push swgitdemo-clone contributes on origin ...
        First update swgitdemo-clone repository. Pulling 1/0/0/0/andreav/INT/develop from origin ...
                Fetching origin
                Already up-to-date.
        DONE
        Now push contributes, branches and labels ...
                To /tmp/swgitdemo-orig
                   6e67eed..fdb6719  1/0/0/0/andreav/INT/develop -> 1/0/0/0/andreav/INT/develop
                 * [new tag]         1/0/0/0/vallea/FTR/topic/FIX/1234567 -> 1/0/0/0/vallea/FTR/topic/FIX/1234567
                 * [new tag]         1/0/0/0/vallea/FTR/topic/DEV/000 -> 1/0/0/0/vallea/FTR/topic/DEV/000
                 * [new branch]      1/0/0/0/vallea/FTR/topic -> 1/0/0/0/vallea/FTR/topic
                 * [new tag]         1/0/0/0/vallea/FTR/topic/NEW/BRANCH -> 1/0/0/0/vallea/FTR/topic/NEW/BRANCH

                Files updated:
                 a.txt |    1 +
                 1 files changed, 1 insertions(+), 0 deletions(-)
        DONE
      DONE

   swgit assures user always pushes on integartion branch HEAD, i.e.
   every push is Fast-Forward.This is accomplished by issueing an

      **integartion branch pull before pushing**.

   There is a big difference with native git:

      **You cannot directly push on 'origin' any branch but
      integration branch**.

   This behaviour can be workarounded like in "workflow_team_feature",
   but is useful to:

      * keep 'origin' as much clean as possible

      * assure only few HEADs exist in repository. Every HEAD has a
        precise role:

           1. develop/stabel branches

           2. team feature branches

           3. customer branches


Merging and pushing in one shot
===============================

   From a topic branch, user can join merge and push operations
   toghether:

      swgit push -I

   This is called *side push*Issued directly from topic branch, this command will:

      * pull integartion branch

      * merge last topic DEV tag

      * push everithing onto 'origin'


Pulling
=======

   Updating your repository can be done in two ways:

      * from integration branch:

           swgit pull

        This operation is a plain "git pull", but is allowed ONLY on
        integartion branches.

      * from a topic branch:

           swgit pull -I

         This is called *side pull*Issued directly from topic branch, this command will:

            * pull integartion branch

            * merge integartion branch on current topic branch
