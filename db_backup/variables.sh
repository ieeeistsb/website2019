#!/bin/bash
DATABASE_NAME=ieee_ist_db
DATABASE_USER=ieeeist
DATABASE_USER_PW=ieeeistdb
BACKUP_FOLDER=$HOME
BACKUP_NAME_PREFIX=db_backup_
BACKUP_NAME_SUFFIX="$(date +'%Y%m%d')"
EXTENSION=.sql