#!/bin/bash

#declare SWGIT_SCRIPTS_HOME=$( dirname $( readlink -e "${BASH_SOURCE[0]}" ) )

[ "${SWCFG_GITNATIVE_AUTOCOMPLETE}" == "YES" ] && source $SWGIT_HOME/scripts/git-completion.bash

#$( which swgit &>/dev/null ) || { echo "Please ajdust \$PATH in order to find a valid \"swgit\" command" && return 1 ;}
#SWGIT_EXE=${SWGIT_HOME}/swgit

swgitcommand2script=(
  "branch:GitBranch.py"
  "clone:GitClone.py"
  "commit:GitCommit.py"
  "lock:GitLock.py"
  "merge:GitMerge.py"
  "pull:GitPull.py"
  "push:GitPush.py"
  "stabilize:GitStabilize.py"
  "tag:GitTag.py"
  "undo:GitUndo.py"
  "key:ObjKey.py"
  "init:GitInitOneCommit.py"
  "info:GitInfo.py"
  "checkout:GitBranch.py"
  "proj:GitProj.py"
)

function _swgit_getSubCmds()
{
  local ret=""
  for i in $( echo ${swgitcommand2script[@]} )
  do
    ret="$ret"" ""${i%:*}"
  done
  echo $ret
}

_swgit_reference=
_swgit_compute_reference()
{
  [ ! -z "$_swgit_reference" ] && return 0

  #dir=$( git rev-parse --git-dir 2>/dev/null )
  #namedrefs=""
  #for i in HEAD FETCH_HEAD ORIG_HEAD MERGE_HEAD; do
  #  if [ -e "$dir/$i" ]; then namedrefs=$( echo -e "$namedrefs\n$i" ); fi
  #done

  _swgit_reference="$( sort -u - < <( 
      echo "$( git for-each-ref --format='%(refname:short)' 'refs/heads/*/*/*/*/*/*/*' )" \
           "$( git for-each-ref --format='%(refname:short)' 'refs/remotes/*/*/*/*/*/*/*/*' | cut -d '/' -f 2- )" \
           "$( git for-each-ref --format='%(refname:short)' 'refs/tags/*/*/*/*/*/*/*/*/*' )" \
            ) )"
           #"$namedrefs" ) )"

  return 0
}

_swgit_local_branches=
_swgit_compute_local_branches()
{
  [ ! -z "$_swgit_local_branches" ] && return 0
  _swgit_local_branches="$( git for-each-ref --format='%(refname:short)' 'refs/heads/*/*/*/*/*/*/*' )"
  return 0
}
_swgit_remote_branches=
_swgit_compute_remote_branches()
{
  [ ! -z "$_swgit_remote_branches" ] && return 0
  _swgit_remote_branches="$( git for-each-ref --format='%(refname:short)' 'refs/remotes/*/*/*/*/*/*/*/*' )"
  return 0
}

_swgit_branches=
_swgit_compute_branches()
{
  [ ! -z "$_swgit_branches" ] && return 0
  _swgit_compute_local_branches
  _swgit_compute_remote_branches
  _swgit_branches=$( sort -u - < <( echo "$_swgit_local_branches" && echo "$_swgit_remote_branches" ) )
  return 0
}


_swgit_branch_name_val=
_swgit_compute_branch_name_val()
{
  _swgit_compute_local_branches
  _swgit_compute_remote_branches
  _swgit_branch_name_val=$( sort -u - < <( echo "$_swgit_local_branches" | cut -d '/' -f 7 && echo "$_swgit_remote_branches" | cut -d '/' -f 8 ) )
  return 0
}

_swgit_branch_type_val=
_swgit_compute_branch_type_val()
{
  [ ! -z "$_swgit_branch_type_val" ] && return 0
  _swgit_branch_type_val=" INT CST FTR FIX"
  return 0
}

_swgit_tags=
_swgit_compute_tags()
{
  [ ! -z "$_swgit_tags" ] && return 0
  _swgit_tags="$( git for-each-ref --format='%(refname:short)' 'refs/tags/*/*/*/*/*/*/*/*/*' )"
  return 0
}

_swgit_tag_name_val=
_swgit_compute_tag_name_val()
{
  _swgit_compute_tags
  _swgit_tag_name_val=$( sort -u - < <( echo "$_swgit_tags" | cut -d '/' -f 9 ) )
  return 0
}

_swgit_tag_type_val=
_swgit_compute_tag_type_val()
{
  _swgit_compute_tags
  _swgit_tag_type_val=$( sort -u - < <( echo "$_swgit_tags" | cut -d '/' -f 8 ) )
  return 0
}

_swgit_release_val=
_swgit_compute_release_val()
{
  [ ! -z "$_swgit_release_val" ] && return 0
  _swgit_compute_reference
  _swgit_release_val=$( sort -u - < <( echo "$_swgit_reference" | cut -d '/' -f 1-4 ) )
  return 0
}

_swgit_user_val=
_swgit_compute_user_val()
{
  [ ! -z "$_swgit_user_val" ] && return 0
  _swgit_compute_reference
  _swgit_user_val=$( sort -u - < <( echo "$_swgit_reference" | cut -d '/' -f 5 ) )
  return 0
}


_swgit_longoptions=
_swgit_compute_longoptions() #takes subcommand
{
  _swgit_longoptions="$(SWHELPMAC="PRINT" ${SWGIT_HOME}/swgit "$1" )"
  return 0
}

_swgit_complete_options() #subcmd #cur
{
  local opts=$( echo "$_swgit_longoptions" | cut -d ':' -f 1 )
  COMPREPLY=( $(compgen -W "$opts" -- ${2}) )
  return 0
}

_swgit_getnumargs() #subcmd #cur
{
  local arg=$( echo "$_swgit_longoptions" | grep -e "^$2:" |  cut -d ':' -f 2 )
  [ -z "$arg" ] && return 1
  echo $arg
  return 0
}

_swgit_complete_metavar() #opt #cur
{
  local opts="$( echo "$_swgit_longoptions" | grep -e "^$1:" | cut -d ':' -f 3 )"
  #echo "[$opts]"
  COMPREPLY=( $(compgen -W ": $opts" -- ${2}) ) #this space ensure at least 2 options
  return 0
}

_swgit_complete_metavar_expand() #opt #cur
{
  local metavar="$( echo "$_swgit_longoptions" | grep -e "^$1:" | cut -d ':' -f 3 | tr -d '<' |tr -d '>')"
  #echo "[$metavar]"
  case "$metavar" in 
    "branch_name") 
      _swgit_compute_branches
      COMPREPLY=( $(compgen -W "$_swgit_branches" -- ${2}) )
      return 0
      ;;
    "branch_name_val") 
      _swgit_compute_branch_name_val
      COMPREPLY=( $(compgen -W "$_swgit_branch_name_val" -- ${2}) )
      return 0
      ;;
    "branch_type_val") 
      _swgit_compute_branch_type_val
      COMPREPLY=( $(compgen -W "$_swgit_branch_type_val" -- ${2}) )
      return 0
      ;;
    "reference") 
      _swgit_compute_reference
      COMPREPLY=( $(compgen -W "$_swgit_reference" -- ${2}) )
      return 0
      ;;
    "release_val") 
      _swgit_compute_release_val
      COMPREPLY=( $(compgen -W "$_swgit_release_val" -- ${2}) )
      return 0
      ;;
    "tag_name") 
      _swgit_compute_tags
      COMPREPLY=( $(compgen -W "$_swgit_tags" -- ${2}) )
      return 0
      ;;
    "tag_name_val") 
      _swgit_compute_tag_name_val
      COMPREPLY=( $(compgen -W "$_swgit_tag_name_val" -- ${2}) )
      return 0
      ;;
    "tag_type_val") 
      _swgit_compute_tag_type_val
      COMPREPLY=( $(compgen -W "$_swgit_tag_type_val" -- ${2}) )
      return 0
      ;;
    "user_val") 
      _swgit_compute_user_val
      COMPREPLY=( $(compgen -W "$_swgit_user_val" -- ${2}) )
      return 0
      ;;
    "shared_mode") 
      COMPREPLY=( $(compgen -W "false true umask group all world everybody 0xx" -- ${2}) )
      return 0
      ;;
    *)
      ;;
  esac
  _swgit_complete_metavar "$1" "$2"
  return
}


_sw_git()

{
  #Do not clean twice during same command
  if [ "$COMP_CWORD" -lt 3 ]; then
    _swgit_local_branches=
    _swgit_remote_branches=""
    _swgit_branches=""
    _swgit_branch_name_val=""
    _swgit_branch_type_val=""
    _swgit_tags=""
    _swgit_tag_name_val=""
    _swgit_tag_type_val=""
    _swgit_release_val=""
    _swgit_user_val=""
  fi

  local cur prev base
  COMPREPLY=()
  #cur could be also partially complete
  cur="${COMP_WORDS[COMP_CWORD]}"
  #prev is the last completed work
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  cl_cmd="${COMP_WORDS[0]}"
  cl_subcmd="${COMP_WORDS[1]}"

  #echo "subcommands: $(_swgit_getSubCmds)"

  #
  #  Complete the arguments to some of the basic commands.
  #
  #echo -e "\n>> words: [${COMP_WORDS[@]}] <<"
  #echo -e ">> Cword: [${COMP_CWORD}] <<"

  #echo -e ">> cl_cmd:    [$cl_cmd] <<"
  #echo -e ">> cl_subcmd: [$cl_subcmd] <<"

  #echo -e ">> prev: [${prev}] <<"
  #echo ">> cur: [${cur}] <<"

  all_sub_cmds=$( _swgit_getSubCmds )

  if [ $COMP_CWORD == 1 ]
  then
    COMPREPLY=( $(compgen -W "${all_sub_cmds}" -- ${cur}) )
    return 0

  elif [ $COMP_CWORD -eq 2 ]
  then
    if echo "${all_sub_cmds}" | grep -w "${prev}" &>/dev/null
    then
      _swgit_compute_longoptions $cl_subcmd
      _swgit_complete_options $cl_subcmd $cur
      return $?
    else
      if [ "${SWCFG_GITNATIVE_AUTOCOMPLETE}" == "YES" ]; then
        _git
        return $?
      else:
        return 0
      fi
    fi

  else # 3args
    _swgit_compute_longoptions $cl_subcmd

    #last completed word is exactly [-- ] or [- ] (with space)
    if [ "${prev}" == "--" ] || [ "${prev}" == "-" ]; then

      return 0

    #last completed word is an option (valid or not)
    elif [ ${prev:0:2} == "--" ] || [ ${prev:0:1} == "-" ]; then

      local longopt=$prev
      if [ ${prev:1:1} != "-" ]; then #short option (second char is not -)
        longopt="$(SWHELPMAC="S2L@$prev" ${SWGIT_HOME}/swgit $cl_subcmd )"
        if [ "$?" -ne 0 ]; then
          #not long option found, return
          return 0
        fi
      fi

      local arg=""
      arg=$( _swgit_getnumargs $cl_subcmd $longopt )
      if [ "$?" -ne 0 ]; then
        #not option found, return
        return 0
      fi

      if [ $arg -eq 0 ]
      then
        _swgit_complete_options $cl_subcmd $cur
        return $?
      else
        if [ "${SWCFG_METAVAR_EXPAND}" == "YES" ]; then
          _swgit_complete_metavar_expand $longopt $cur
        else
          _swgit_complete_metavar $longopt $cur
        fi
        return $?
      fi

    #last completed word is not an option => provide option list
    else

      _swgit_complete_options $cl_subcmd $cur
      return $?

    fi
  fi
}
complete  -o bashdefault -o default -o nospace -F _sw_git swgit

