
Stabilizing
***********

   1/0/0/0/andreav/INT/develop           1/0/0/0/andreav/INT/stable
            |                                      |                  |
            V                                      V                  | time
                                                                      v
            |                                      |
            |                                      |
            | INT/develop/STB/Drop.A               |
            +------>>------->>--------->>----------+ INT/stable/STB/Drop.A
            |                                      | INT/stable/LIV/Drop.A
            |                                      |
        .---+                                      |
       /    |                                      |
      X     |                                      |
      |     |                                      |
      |     |                                      |
      X     |                                      |
       \    | INT/develop/STB/Drop.B               | INT/stable/STB/Drop.B
        '---+------>>------->>--------->>----------+----.
            |                                      |     \
            |                                      |      |
            |                                      |      X
            |                                      |      |
        .---+                                      |     /
       /    |                                      +----'
      X     |                                    / | INT/stable/LIV/Drop.B
       \    |                                   /  |
        '---+                                  /   |
            |                                 /    |
            |                                /     |
            +------<<-------<<--------<<----'      |
            |                                      |
            |                                      |

Every software project needs to identify stable versions.Developers contribute to the project; sometimes a line must be drawn.According to agile principles, as frequent as possible.

These requirements are met by swgit by introducing **INT/stable**
branch.

Main branch goals are:

   1. storing all delivered stable software versions, labeled with
      *LIV* tag.

   2. storing candidates software for next drop, labeled with *STB*
      tag.

   3. letting the integrator shift aside from the "develop process"
      (turning around *INT/develop* branch).On *INT/stable* he/she cat take necessary time for preparing,
      and in case  fixing, next delivery.

In this context *Integrator* refers to project maintainer, who reports
contributes on *INT/stable*.


NGT tag
=======

   This tag is a *built-in swgit tag*.

   It is used by the Integrator, and is put only on *INT/develop*
   worth commits.

   *NGT* refers to 'nightly tests'. The idea here is:

      At night, a test suite will check if repository HEAD is valuable.If so, a NGT tag will mark that reference

   Day after, when integrator arrives at his/her desk, a NGT tag will
   be a good candidate to be stabilized.

   Of course, Integrator will decide, according to feature list, if
   it's time for preparing a new delivery.


Reporting on *INT/stable* (STB labels)
======================================

   Periodically Integrator will report a worth *INT/develop* commit
   onto *INT/stable* by:

         swgit stabilize --stb --src <reference> Drop.A

   *Drop.A* is the name of next delivery. This name will be matched
   against STB label regexp configuration parameter; default value is:

         ^Drop\.[A-Z]{1,3}(_[0-9]{1,3})?$

   If you want to change *STB* regexp, please refer to *Analyzing tags
   configuration* and *Setting tag values*.

   This command will:

   * Merge --src <reference> argument into target *INT/stable*

   * Create 1/0/0/0/andreav/INT/develop/STB/Drop.A - This mark
     *INT/develop* starting point.

   * Create 1/0/0/0/andreav/INT/stable/STB/Drop.A  - This mark
     *INT/stable* arrival point.

   Note: By default, --src argument must be a NGT tag.
     This encourages continuous testing agile principle.If you need to stabilize any reference, please issue inside you repository:

        **swgit config swgit.stabilize-anyref True**

   Note: In order to strengthen concept that only Integrator can issue this command,
     swgit will deny this operation on any repository but *integrator repository*This is a weak, easily workaroundable, limit. However this avoids accidental
     command execution on a Developer repository.

-[ Target branch selection ]-

======================================================================

   Target branches onto which to stabilize contributes always are
   INT/stable or CST/customer branches.

   In order to select target branch, *Integrator* can:

      1. Provide it on command line (last argument):

            swgit stabilize --stb Drop.A 1/0/0/0/andreav/INT/stable

      2. Switch on it:

            swgit branch -s 1/0/0/0/andreav/INT/stable
            swgit stabilize --liv Drop.A

      3. Select appropriate integration branch (*INT/develop* or
         *INT/stable* are equivalent, they both translate to
         *INT/stable*):

            swgit branch --set-integration-br 1/0/0/0/andreav/INT/stable
            swgit stabilize --liv Drop.A


Creating a delivery (LIV labels)
================================

   Integrator decides to release a delivery.

   1. He/She will go into an *integrator repository*,

   2. go onto stable branch thus selecting last stabilized commit:

         swgit branch -s 1/0/0/0/andreav/INT/stable

   3.1 If everything is ok he/she will "stabilize --liv" this commit
   (see below).

   3.2 If something has to be done before releasing, he/she will
   create a branch:

         swgit branch -c "hotfix"

      thus creating a *FIX branch*:

         1/0/0/0/andreav/FIX/hotfix

      from which to do necessary actions.

      When fix is  done, he/she will merge on *INT/stable*:

         swgit tag dev -m "hotfix for Drop.A"
         swgit branch -s 1/0/0/0/andreav/INT/stable
         swgit merge 1/0/0/0/andreav/FIX/hotfix/DEV/000

      Now he/she cal create a delivery.

      swgit stabilize --liv Drop.A

   This command will:

   1. Create three files under directory:

         ${REPO_ROOT}/.swdir/changelog/<REL>/

      * **Changelog**: containing all DEV labels from last repository
        LIV till now.

      * **Fixlog**: containing all FIX labels from last repository LIV
        till now.

      * **Ticketlog**: a machine readable file, containing only Ticket
        numbers. (i.e. tagName for every FIX label)

   1. Add everything to the index and committing

   2. Tag with a LIV label:

         1/0/0/0/andreav/INT/stable/LIV/Drop.A

   3. Merge */INT/stable* on */INT/develop* (this step can be jumped
      by providing option --no-merge-back when stabilizing --liv)

   4. Push everything on 'origin'

   When issuing **swgit stabilizing --liv**, target branch (branch to
   be labelled) will be selected like for **swgit stabilizing --stb**
   (see *here*).

   Note: You can stabilize both --stb and --liv in one shot.Just provide *--liv* option when issuing *swgit stabilize --stb*.

   Note: In order to strengthen concept that only Integrator can issue this command,
     swgit will deny this operation on any repository but *integrator repository*This is a weak, easily workaroundable, limit. However this avoids accidental
     command execution on a Developer repository.


Reporting on CST/customer
=========================

       1/0/0/0/andreav/INT/stable         1/0/0/0/user/CST/acustomer
                 |                                  |
                 V                                  V               |
                                                                    | time
                 |                                 |                v
                 | INT/stable/STB/Drop.A           |
                 | INT/stable/LIV/Drop.A           |
   -->>----------+---------------.                 |
                /|                '------->>-------X  CST/acustomer/LIV/Drop.A
               / |                                 |
              /  |                                 |
   ----<<----'   |                                 |
                 |                                 |
                 |                                 |
                 |                                 |
                 | INT/stable/STB/Drop.B           |
                 | INT/stable/LIV/Drop.B           |
   -->>----------+---------------.                 |
                /|                '------->>-------X CST/acustomer/LIV/Drop.B
               / |                                 |
              /  |                                 |
   ----<<----'   |                                 |
                 |                                 |
                                                   |
