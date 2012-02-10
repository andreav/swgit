
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

   1. storing all delivered stable software versions, labelled with
      *LIV* tag.

   2. storing candidates software for next drop, labelled with *STB*
      tag.

   3. letting the integartor shift aside from the "develop process"
      (tourning around *INT/develop* branch).On *INT/stable* he/she cat take necessary time for preparing,
      and in case  fixing, next delivery.

In this context *Integrator* referes to project maintainer, who
reports contributes on *INT/stable*.


NGT tag
=======

   This tag is a *built-in swgit tag*.

   It is used by the Integrator, and is put only on *INT/develop*
   worthful commits.

   *NGT* refers to 'nightly tests'. The idea here is:

      At night, a test suite will check if repository HEAD is valuable.If so, a NGT tag will mark that reference

   Day after, when integartor arrives at his/her desk, a NGT tag will
   be a good candidate to be stabilized.

   Of course, Integartor will decide, according to feature list, if
   it's time for preparing a new delivery.


Reporting on *INT/stable*
=========================

   Periodically Integartor will report a worthful *INT/develop* commit
   onto *INT/stable* by:

      swgit stabilize --stb Drop.A --src <reference>

      *Drop.A* is the name of next delivery. This name will be matched
      against STB label regexp configuration parameter; default value
      is:

            ^Drop\.[A-Z]{1,3}(_[0-9]{1,3})?$

      If you want to change *STB* regexp, please refere to *Analizig
      tags configuration* and *Setting tag values*.

      Note: By default, --src argument must be a NGT tag.
        This encourages continuous testing agile principle.If you need to stabilize any reference, please issue inside you repository:

           swgit config swgit.stabilize-anyref True

   This command will merge --src reference argument on *INT/stable*.

   This command will create two *STB* labels:

      * 1/0/0/0/andreav/INT/develop/STB/Drop.A - This mark
        *INT/develop* starting point.

      * 1/0/0/0/andreav/INT/stable/STB/Drop.A  - This mark
        *INT/stable* arrival point.

   Note: In order to strengthen concept that only Integartor can issue this command,
     swgit will deny this operation on any repository but *integrator repository*This is a weak, easely workaroundable, limit. However this avoids accidental
     command execution on a Developer repository.


Creating a delivery
===================

   Integartor decides to release a delivery.

   1. He/She will go into an *integrator repository*,

   2. go onto stable branch with:

         swgit branch -s 1/0/0/0/andreav/INT/stable

   3. Build and verify everything is ok.

         * If so, he/she will "stabilize --liv" this commit (see
           below).

         * If anything has to be done, he/she will create a branch:

              swgit branch -c "hotfix"

           thus creating a *FIX branch*:

              1/0/0/0/andreav/FIX/hotfix

           from which to do what next drop needs.

           When fix is  done, he/she will "swgit tag dev" any
           contribute and he/she will merge on *INT/stable* branch
           that label. Like any developer should do, except for
           merging on *INT/stable*.

   In the end, when everithing is ok, Integartor will issue:

      swgit stabilize --liv Drop.A

   This command will:

   1. Create three files under directory:

         ${REPO_ROOT}/.swdir/changelog/<REL>/

      * **Changelog**: containiinig all DEV labels from last
        repository LIV till now.

      * **Fixlog**: containing all FIX labels from last repository LIV
        till now.

      * **Ticketlog**: a machine readable file, containing only
        Tickect numbers. (i.e. tagName for every FIX label)

   1. Add everything to the index and committing

   2. Tag with a LIV label:

         1/0/0/0/andreav/INT/stable/LIV/Drop.A

   3. Merge */INT/stable* on */INT/develop*

   4. Push everithing on 'origin'

   Note: In order to strengthen concept that only Integartor can issue this command,
     swgit will deny this operation on any repository but *integrator repository*This is a weak, easely workaroundable, limit. However this avoids accidental
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
