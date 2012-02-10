
Wokflow - Update Repo
*********************


pull executed on integartion branch
===================================

      swgit branch --current-branch
         1/0/0/0/andreav/INT/develop
      swgit pull

This last command updates develop branch on your local repository

It leaves untouched all other branches.

        ''''''''''''''''''''''''''
         Before pull from develop
        ..........................


   origin/develop         local develop branch
         |                       |
         v                       v

                                       FTR branch
                                         |
         |                       |       V

     .-<-X                       X -->--.
    '                                    '
   |     |                               |     Before pull, your local branch
   c     |                               A     is here, after pull,
   |     |                                     it will be untouched
   .
    '--> Y


        '''''''''''''''''''''''''
         After pull from develop
        .........................


   origin/develop         local develop branch
         |                       |
         v                       v


         |                       |

     .-<-X                  .-<- X -->--.
    '                      '             '
   |     |     pull       |      |       |     Before pull, your local branch
   c     |     --->       c      |       A     is here, after pull,
   |     |                |      |             it will be untouched
   .                      .
    '--> Y                 '-->  Y


pull executed on FTR branch
===========================

      swgit branch --current-branch
         1/0/0/0/andreav/FTR/topic
      swgit pull -I/--merge-from-int

This last command updates integartion branch on your local repository

After this it will merge local integartion branch on your current
branch

This command may be usefull in order to update an old branch and
keeping on developing on that branch.

Note: If you are going beginning a new work, do not update an old branch!
  It it better creating a new branch just after pulling from origin:

     swgit branch --current-branch
         1/0/0/0/andreav/FTR/topic
     swgit pull
     swgit branch -c new_topic

        '''''''''''''''''''''''''''''
         Before pull from FTR branch
        .............................


   origin/develop         local develop branch
         |                       |
         v                       v

                                       FTR branch
                                         |
         |                       |       V

     .-<-X                       X -->--.
    '                                    '
   |     |                               |     Before pull, your local branch
   c     |                               A     is here, after pull,
   |     |                                     it will be merge with develop
   .                                           contributes
    '--> Y


        ''''''''''''''''''''''''''''
         After pull from FTR branch
        ............................


   origin/develop         local develop branch
         |                       |
         v                       v


         |                       |

     .-<-X                  .-<- X -->--.
    '                      '             '
   |     |     pull       |      |       |
   c     v     --->       c      v       A
   |     |                |      |       |
   |     |                |      |       v
   .                      .              |     'B' is the merge commit generated
    '--> Y                 '-->  Y --->  B     in order to update your local
                                               brannch with contributes from
                                               origin/develop


push executed from integartion br
=================================

      swgit branch --current-branch
         1/0/0/0/andreav/INT/develop
      swgit push

This last command updates origin repository with your local
integartion branch.

         ''''''''''''''''''''''''''
          Before push from develop
         ..........................


    origin/develop         local develop branch
          |                       |
          v                       v

                                        FTR branch
                                          |
          |                       |       V

     .-<- X                       X -->--.
    '                                     '
   |      |                       |       |
   c      v                       v       A
   |      |                       |       |
   .                                      .
    '-->  Y                       B <----'


         '''''''''''''''''''''''''
          After push from develop
         .........................


                                local develop branch
                                       |
        *********                      v
       * PHASE 1 *
        *********                            FTR branch
                                               |
                                       |       V

        First pull form       .-<----- X ----->--.
          origin and         '      /    \        '
           update           |      |      |       |
          -------->         c      |      |       A
           local            |      |      |       |
          repository        .                     .
                             '-->  Y      B <----'

                                   |      |
                                   |      |
                                   '      '
                                    \    /
                                       Z



       origin develop branch
              |
              v                      *********
                                    * PHASE 2 *
                    FTR branch       *********
                      |
              |       V

     .-<----- X ----->--.        Then actually
    '      /    \        '        push on origin
   |      |      |       |         result from your
   c      |      |       A     <-----------
   |      |      |       |          local repository
   .                     .
    '-->  Y      B <----'

          |      |
          |      |
          '      '
           \    /
              Z


push executed from FTR branch
=============================

      swgit branch --current-branch
         1/0/0/0/andraev/FTR/topic
      swgit push -I/--merge-on-int

This command executes also a merge on integartion branch.

   1. Update local repository.

      This is done to push always on HEAD and avoid non-ff pushes

   2. merge last FTR/topic/DEV/nnn label on integration branch

      This merge is always "--no-ff".

   3. push everything on origin.

         ''''''''''''''''''''''''''
          Before push from develop
         ..........................


    origin/develop         local develop branch
          |                       |
          v                       v

                                        FTR branch
                                          |
          |                       |       V

     .-<- X                       X -->--.
    '                                     '
   |      |                       |       |
   c      v                       v       A  DEV/000
   |      |                       |
   .
    '-->  Y                       B


         '''''''''''''''''''''''''
          After push from develop
         .........................


                                local develop branch
                                       |
        *********                      v
       * PHASE 1 *
        *********                            FTR branch
                                               |
                                       |       V

        First pull form       .-<----- X ----->--.
          origin and         '      /    \        '
           update           |      |      |       |
          -------->         c      |      |       A  DEV/000
           local            |      |      |
          repository        .
                             '-->  Y      B

                                   |      |
                                   |      |
                                   '      '
                                    \    /
                                       Z


                                local develop branch
                                       |
        *********                      v
       * PHASE 2 *
        *********                            FTR branch
                                               |
                                       |       V

        Then merge last           .-<- X -->--.
          DEV label              '             '
           on int br            |      |       |
          -------->             c      v       A  DEV/000
           local                |      |
          repository            .              |
                                 '-->  Y       |
                                       |       |
                                       |       |
                                               .
                                       B <----'



   origin develop branch
          |
          v

                FTR branch             *********
                  |                   * PHASE 3 *
          |       V                    *********

     .-<- X -->--.
    '             '
   |      |       |                Then actually
   c      v       A  DEV/000        push on origin
   |      |                          result from your
   .              |              <-----------
    '-->  Y       |                   local repository
          |       |
          |       |
                  .
          B <----'
