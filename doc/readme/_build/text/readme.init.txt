
Wokflow - Initializing
**********************


Initializing a new swgit repository
===================================

   When you want to create a swgit repository staring from a directory
   empty or with some contents, enter the directory and issue this
   command:

      cd /tmp/swgit-demo
      swgit init --release 1.0.0.0 --liv-label Drop.A

   output:

      Initializing new git repository ...
      DONE
      Initializing swgit repository ...
          Creating dir  /tmp/swgit-demo/.swdir/log/
          Creating dir  /tmp/swgit-demo/.swdir/changelog/1/0/0/0
          Creating dir  /tmp/swgit-demo/.swdir/cfg/
          Creating file /tmp/swgit-demo/.swdir/cfg/custom_tags.cfg
          Creating file /tmp/swgit-demo/.swdir/cfg/mail.cfg
          Creating file /tmp/swgit-demo/.swdir/cfg/snapshot_repos.cfg
          Creating file /tmp/swgit-demo/.gitignore
          Ignoring .swdir/log/*
          Ignoring !.swdir/log/.placeholder
          Ignoring *~
          Ignoring *.swp
          Ignoring *.pyc
          Ignoring !.gitattributes
          Adding all and committing
          DONE
      DONE
      Initializing INT branches ...
          Creating branch 1/0/0/0/andreav/INT/develop ...
          DONE
          Creating label 1/0/0/0/andreav/INT/develop/NEW/BRANCH
          DONE
          Checkout to just created develop branch 1/0/0/0/andreav/INT/develop ...
          DONE
          Deleting branch master
          DONE
          Creating branch 1/0/0/0/andreav/INT/stable ...
          DONE
          Creating label 1/0/0/0/andreav/INT/stable/NEW/BRANCH
          DONE
          Creating label 1/0/0/0/andreav/INT/develop/STB/Drop.A ...
          DONE
          Creating label 1/0/0/0/andreav/INT/stable/STB/Drop.A ...
          DONE
          Creating label 1/0/0/0/andreav/INT/stable/LIV/Drop.A ...
          DONE
          Checkout to just created label 1/0/0/0/andreav/INT/stable/LIV/Drop.A ...
          DONE
      DONE

      PLEASE VERIFY EVERITHING IS OK, THEN:
             If you are on your origin repository, that's all.
             If you are on a clone, push it on origin with:
               swgit branch -s 1/0/0/0/andreav/INT/develop
               or
               swgit branch -s 1/0/0/0/andreav/INT/stable
               and
               swgit push

   This happened:

      1. First, a *git init* is issued, creating .git directory

      2. Then, a *swgit init* is done, creating .swgit directory

      3. *INT/develop* and *INT/stable* branches are created

      4. *LIV/Drop.A* label has been created and checked-out

         --liv-label is not mandatory


Init Options
------------

   1. You can change user owning INT branches:

         swgit init -r 1.0.0.0 --git-user ourteam

      Thus obtaining branches like:

         1/0/0/0/ourteam/INT/develop
         1/0/0/0/ourteam/INT/stable

      That user will also be configured into local repo, inside
      user.name config variable.

   1. You can slightly change develop and stable names:

         swgit init -r 1.0.0.0 --create prodname

      thus obtaining branches like:

         1/0/0/0/andreav/INT/prodname_develop
         1/0/0/0/andreav/INT/prodname_stable

   1. You can create a starting LIV label with the command:

         swgit init -r 1.0.0.0 --liv Drop.A

      thus obtaining also three tags more:

         1/0/0/0/andreav/INT/develop/STB/Drop.A
         1/0/0/0/andreav/INT/stable/STB/Drop.A
         1/0/0/0/andreav/INT/stable/LIV/Drop.A

      For more informations abouy these labels, please refer to
      "stabilizing"

      Note: If you want to modify LIV regexp (for instance allowing any 15
        letters name), fastest solution is:

           swgit config swgit.LIV.regexp '^[a-zA-Z]{0,15}$'

        For a complete reference, please refer to "custom_tags".

   1. --share option is supported. This is forwarded to *git init*.


Intializig a new release
========================

   This creates a new couple *INT/develop* *INT/stable*.

   Optionally it tags also that new commit with a LIV label.

   -- source-reference (starting point) is mandatory.

      swgit init --release 2.0.0.0 --source-reference 1/0/0/0/andreav/INT/stable/LIV/Drop.A

   output:

      Checkout to starting reference 1/0/0/0/andreav/INT/stable/LIV/Drop.A ...
      DONE
      Initializing swgit repository ...
          Creating dir  /tmp/swgit-demo/.swdir/changelog/2/0/0/0
          Adding all and committing
          DONE
      DONE
      Initializing INT branches ...
          Creating branch 2/0/0/ropallea/INT/develop ...
          DONE
          Creating label 2/0/0/0/andreav/INT/develop/NEW/BRANCH
          DONE
          Checkout to just created develop branch 2/0/0/0/andreav/INT/develop ...
          DONE
          Creating branch 2/0/0/0/andreav/INT/stable ...
          DONE
          Creating label 2/0/0/0/andreav/INT/stable/NEW/BRANCH
          DONE
      DONE

      PLEASE VERIFY EVERITHING IS OK, THEN:
             If you are on your origin repository, that's all.
             If you are on a clone, push it on origin with:
               swgit branch -s 2/0/0/0/andreav/INT/develop
               or
               swgit branch -s 2/0/0/0/andreav/INT/stable
               and
               swgit push


Initializing a new product
==========================

   When you want to create more product lines inside the same
   repository.

   -- create option allow you to create *INT/a_product_develop* and
   *INT/a_product_stable* branches.

   Optionally it tags first product commit with a LIV label.

   -- source-reference (starting point) is mandatory.

      swgit init --release 1.0.0.0 --source-reference 1/0/0/0/andreav/INT/stable/LIV/Drop.A --create a_product

   output:

      Initializing swgit repository ...
          Adding all and committing
          DONE
      DONE
      Initializing INT branches ...
          Creating branch 1/0/0/0/andreav/INT/a_product_develop ...
          DONE
          Creating label 1/0/0/0/andreav/INT/a_product_develop/NEW/BRANCH
          DONE
          Checkout to just created develop branch 1/0/0/0/andreav/INT/a_product_develop ...
          DONE
          Creating branch 1/0/0/0/andreav/INT/a_product_stable ...
          DONE
          Creating label 1/0/0/0/andreav/INT/a_product_stable/NEW/BRANCH
          DONE
      DONE

      PLEASE VERIFY EVERITHING IS OK, THEN:
             If you are on your origin repository, that's all.
             If you are on a clone, push it on origin with:
               swgit branch -s 1/0/0/0/andreav/INT/a_product_develop
               or
               swgit branch -s 1/0/0/0/andreav/INT/a_product_stable
               and
               swgit push


Convert git to to swgit repository
==================================

This is accomplished in the same manner as initializing a new swgit
repository.

Just *git init* phase will be jumped.
