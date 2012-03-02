
Repository Lifeclycle
*********************

Every numbered point is commented below.

     1/0/0/0/andreav/INT/develop           1/0/0/0/andreav/INT/stable
              |                                      |                  |
              V    1.                        2.      V                  | time
                                                                        v
              |                                      |
          3.  |                                      |
          .---+                                      |
         /    |                                      |
        X  4. |                                      |
        |     |                                      |
        |     |                                      |
   FIX  Y     |                                      |
        |     |                                      |
        |     |                                      |
   DEV  Z  5. |                                      |
         \    |                                      |
          '---+                                      |
              |                                      |
          .---+                                      |
         /    |                                      |
        T     |                                      |
        |     |                                      |
        |     |                                      |
        W     |                                      |
         \    | 6. STB                        7. STB |     8.
          '---+------>>------->>--------->>----------+----.
              |                                      |     \
              |                                      |      |
              |                                      |      F  9.
              |                                      |      |
          .---+                                      |     /
         /    |                               LIV    +----'
        M     |                                    / |
        |     |                                   /  |
        |     |                                  /   |
        N     |                                 /    |
         \    |                                /     |
          '---+                               /      |
              |                        10.   /       |
              |                             /        |
              +------<<-------<<--------<<-'         |
              |                                      |
              |                                      |

**0. Branches and tags**

   Please refer to *References* for a detailed description.

**1. INT/develop**

   This branch is:

   * Created by Integrator with a command like this:

        "swgit init --rel 1.0.0.0"

   * One per release

   * Is owned by ALL developers: every user has responsibility when
     pushing on it

   * Is usually set as integration branch (see "intbr")

   * If this is the integration branch:

     * It is read/write

     * Branches are created starting from INT/develop. Release is
       deduced by it.

     * DEV Labels are merged into it

   Project developer, please refer to "developing" for more details.

**2. INT/stable**

   This branch:

   * Is created by integrator together with its *INT/develop* twin
     with the command:

        swgit init --rel 1.0.0.0

   * Stores all delivered stable software versions labeled with *LIV*
     tag.

   * Stores candidates software for next drop labeled with *STB* tag.

   * On developer repository, it is read-only.

   * On *integrator repository* it must be read-write.

     The most quickly way to obtain this, is cloning repository with
     option:

        "--integrator"

   Project integrator, please refer to "stabilizing" for more details.

**3. Developer Branch (/FTR/)**

   This branch:

   * Is created by default when issuing this command:

        swgit branch --create 'topic'

   * Has a "FTR" branch type.

   * Has a branch name as provided at creation time.

   * Is used by developers to implement their contributes.

   * Contains all DEV, FIX or user-defined labels (see below)

   Output example could be:

      "1/0/0/0/andreav/FTR/topic"

**4. Commit**

   It is a plain git commit.

   It is used in order to freeze a certain stage of develop.

   In this case no label has been associated to it.

**5. DEV commit**

   This is a special commit.

   Only DEV labels can be merged into an integration branch (usually
   */INT/develop*).

   You can attach a DEV label to a commit in two ways:

      1. while committing with:

            swgit commit --dev

      2. in any moment with:

            swgit tag dev

   Note: Tagging always happens on last commit (HEAD). If you want to tag
     a commit *in past*, you first need to switch on it, then tag:

        swgit branch -s <a reference>
        swgit tag dev

     This will create DEV tag as expected AND a twin tag under PAST/
     namespace. This second tag is a temporary tag, a placeholder, and
     will be deleted at next push time.

**6. 7. STABLE commits**

   These commits:

   * Represent a moment in repository history where contributes have
     been frozen on *stable* branch.

   * Point '7' represents a good candidate from which to create a
     delivery.

   * They are labeled with a "STB" labels like this:

        1/0/0/0/andreav/INT/develop/STB/DROP.A
        1/0/0/0/andreav/INT/stable/STB/DROP.A

   * They are created only into an *integrator repository* with a
     command like this:

        swgit stabilize --stb

   Please refer to *Reporting on INT/stable (STB labels)* for more
   informations.

**8. FIX branch (/FIX/)**

   These branches are used by integrator for two main purposes:

   1. To implement any super-important last minute fix.

   2. To run pre-processing necessary before releasing an official
      drop (for instance setting release number or stuff like this).

   This branch:

   * Is created by default when issuing this command from an
     *INT/stable* branch:

        swgit branch --create 'hotfix'

   * Has a "FIX" branch type, but behaves exactly like any FTR branch.

   * Has a branch name as provided at creation time.

   Output example could be:

      "1/0/0/0/andreav/FIX/hotfix"

**9. FIX commit**

   These commits are created by integrator on a FIX branch.

   As usual, user must mark them with DEV label to be merged on
   *INT/stable* branch before proceeding creating a new delivery.

**10. INT/stable -> INT/develop alignment**

   During drop creation, INT/develop branch is free:

      developers can continue contributing to the project.

   After delivering a new stable software version, contributes
   introduced on *INT/stable* branch by means of FIX branches may be
   automatically merged into *INT/develop*.

   This depends on you repository workflow.

   * When FIX branches contain a super-important last minute fix, you
     should report it on *INT/develop*. This is the default behavior
     when issuing a:

        "swgit stabilize --liv"

   * When FIX branches are used to run pre-processing or stuff like
     setting release number, you may want NOT to merge them on
     *INT/develop*.

        "swgit stabilize --liv --no-merge-back"

   Please refer to "stabilizing" for more informations.

**11. CST/customer**

   Please refer to *lbl_role_customer*
