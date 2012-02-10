#!/bin/bash
LOCK_PATH=$1
USER=$2
TYPE=$3
FILE="$LOCK_PATH.$TYPE.$USER"


if [ "$TYPE" == "forced" ]; then
  if [ $( ls -1 $LOCK_PATH.* 2>/dev/null | wc -l ) -eq 0  ] || [ $( ls -1 $FILE 2>/dev/null | wc -l ) -ne 0 ]; then
    echo "free ... "
    touch $FILE 
    exit 0
  else
    echo "already lock ... "
    exit 1
  fi
elif [ "$TYPE" == "write" ] ; then
 # { [ $( ls -1 $LOCK_PATH.* 2>/dev/null | wc -l ) -eq 0  ] || [ $( ls -1 $LOCK_PATH.*.$USER 2>/dev/null | wc -l ) -ne 0  ]; } && { touch $FILE && exit 0; } || exit 1;
#  if [ $( ls -1 $LOCK_PATH.* 2>/dev/null | wc -l ) -eq 0  ]; then
#    echo "free ... "
#    touch $FILE 
#    exit 0
#  elif [ $( ls -1 $LOCK_PATH.*.$USER 2>/dev/null | wc -l ) -ne 0  ] && [ $( ls -1 $LOCK_PATH.* 2>/dev/null | grep -v $USER  2>/dev/null | wc -l ) -eq 0  ]; then
#    echo "already lock by me ... "
#    touch $FILE 
#    exit 0
#  else
#    echo "lock by other ... "
#    exit 1
#  fi
  if [ $( ls -1 $LOCK_PATH.* 2>/dev/null | grep -v $USER  2>/dev/null | wc -l ) -eq 0  ]; then
    echo "free ... "
    touch $FILE 
    exit 0
  else
    echo "lock by other ... "
    exit 1
  fi
elif [ "$TYPE" == "read" ]; then
 # { [ $( ls -1 $LOCK_PATH.write.* 2>/dev/null | wc -l ) -eq 0 ] || [ $( ls -1 $LOCK_PATH.*.$USER 2>/dev/null | wc -l ) -ne 0 ]; } && { touch $FILE && exit 0; } || exit 1;
  if [ $( ls -1 $LOCK_PATH.write.* 2>/dev/null | wc -l ) -eq 0 ]; then
    echo "free ... "
    touch $FILE 
    exit 0
  elif [ $( ls -1 $LOCK_PATH.*.$USER 2>/dev/null | wc -l ) -ne 0 ]; then
    echo "already lock by me ... "
    touch $FILE
    exit 0
  else
    exit 1
  fi
fi
  
