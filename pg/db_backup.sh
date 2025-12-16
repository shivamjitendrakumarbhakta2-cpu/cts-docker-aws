#!/bin/bash


# Set the PostgreSQL connection details
PG_HOST=postgres
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=1518
DATABASE_NAME=c2s_dev_test

# Set the backup directory
BACKUP_DIR=/postgres


TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S") 
echo "Backing up..."

pg_dump -h $PG_HOST -p $PG_PORT -U $PG_USER -d $DATABASE_NAME -w > $BACKUP_DIR/backup_$TIMESTAMP.sql

echo "Backup created"