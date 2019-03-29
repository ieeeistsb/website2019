#!/bin/bash

. $(dirname $0)/variables.sh
echo "Starting Database backup to "${BACKUP_FOLDER}/${BACKUP_NAME_PREFIX}${BACKUP_NAME_SUFFIX}${EXTENSION}
mysqldump -u ${DATABASE_USER} -p${DATABASE_USER_PW} ${DATABASE_NAME} > \
${BACKUP_FOLDER}/${BACKUP_NAME_PREFIX}${BACKUP_NAME_SUFFIX}${EXTENSION}
