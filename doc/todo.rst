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

|subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo|

+++++
TODOs
+++++

|subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo| |subs_img_todo|

DOCUMENTATION
-------------

* scrivere che i progetti si prestano bene a far fare le commit solo a uno

  * Project-like-contaner workflow:

    #. Very similiar to working in N indipendent repos
       Reusing every single-repo mechanism

    #. every developer works like in single repo workflows

    #. project direcotry only register submodules alignments
       when tests are passed
       This is an integrator task

    #. at proj --update time, every repo will be updated, 
       instead of beeing on just fetched and in detached-head 
       you will find on develop HEAD => you start working from there 
       (not from the project level stored commit)
       or
       you can choose update -I and merging develop on you branch

  * Project-plus-contained workflow:
     
    #. Project directory has a complete history like any repository,
       and moreover it stores submodule updates.
       This is the most critical because conflicts are frequent 
       every time two developers modifies super and sub modules.,
       Also if no conflict exists in submodules, super project will
       has registered two different commits for subrepo and will conflict

    #. swgit commit command never automatically add subproject 
       to  super project commit.
       So, no conlfict will happen when both developers will update their 
       repositories
       Like in previous scenario, Also here only 1 central authority will run test suite, 
       an will freeze repositories alignment, in case of success. I.e.
       One developer => Zero conflicts!


* Licenza


DEVELOP
-------

* cosa succede se setto come def-int-br un branch valido ma non di tipo INT??
  Diventa un CST?
  Sarebbe meglio di no...

* faccio una stabilize --cst che magari ha un conflitto.
  Chi la mette la LIV??
  Bisognerebbe distinguere tra STB e LIV come si fa nell'altro caso => 
  aggiungere l'opzione --cst sia a stb che a liv

* la stabilize si deve settare a mano gli integartion branches
  e devo esigere che l'intbr sia stable se faccio --stb, stable se faccio --liv


* le variabili per autocompletion sono scritte li dentro, ma commentate.
  cosi se uno le mette da fuori, puo' sceglierlo lui

* quando committin su develop che non potresti, suggerisci nell'output di fare git stash

* clone con fs url con path relativo non funziona 

* swgit branch --list-track fa casino ... ma quelle API sono da rifare tutte...

* verificare nei progetti che si comportano da CST se:

    1. ho un CST branch settato

    2. Non ho settato per niente un CST

    3. Ho settato un branch che e' tipo 'master'

* testa che nel wokflow team feature con coppia INT, possa mettere una DEV su develop, 
  e la push funzioni.


* init --git-user resotra il vecchio user alla fine del comando (non lo setta in locale)

