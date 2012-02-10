#!/bin/bash

DRY_RUN=true
[ $# -ge 1 ] && DRY_RUN=false

DOC_DIR=$( dirname $0 )
BUILD_ROOT="${DOC_DIR}/_build/"

FTP_USER="andreav@swgit.net"
FTP_ADDR="ftp.swgit.net"
FTP_PROXY="http://gnetcache.alcatel.fr:3128"

TIMESTAMP=$( date +%s )
DATE_FROMTIMESTAMP=$( date -d @$TIMESTAMP "+%Y-%m-%d %T" )

echo "Deploying directory: $BUILD_ROOT"
echo "Target:              $FTP_ADDR"
echo "Date:                $DATE_FROMTIMESTAMP"
echo "Timestamp:           $TIMESTAMP"
echo ""

if $DRY_RUN
then

  echo "###################"
  echo "##### DRY-RUN #####"
  echo "###################"

  lftp -c "
  set ftp:ssl-allow false
  set ftp:proxy $FTP_PROXY
  open $FTP_ADDR
  echo \"User:     ${FTP_USER}\"
  login ${FTP_USER}
  lcd ${BUILD_ROOT}
  mirror -R --dry-run ./html
  "

else

  lftp -c "
  open ${FTP_ADDR}
  set ftp:ssl-allow false
  set ftp:proxy ${FTP_PROXY}
  echo \"User:     ${FTP_USER}\"
  login ${FTP_USER}
  lcd ${BUILD_ROOT}
  mv html html.${TIMESTAMP}
  mirror -R ./html
  "

fi

