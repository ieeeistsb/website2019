#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Please pass filename of db dump as argument"
    exit -1
fi

FILE="$1"
if ! [ -f "$FILE" ];
then
    echo "File $FILE does not exist" >&2
    exit -2
fi

. $(dirname $0)/variables.sh

mysql -u ${DATABASE_USER} -p${DATABASE_USER_PW} -D ${DATABASE_NAME} < ${FILE}