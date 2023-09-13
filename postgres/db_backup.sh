#!/bin/bash

set -e

CONTAINER_ID=$(docker ps -q --filter name=postgres-1)
echo "Backing up..."
if [[ ! -z $CONTAINER_ID ]]; then
    docker exec $CONTAINER_ID pg_dumpall -U postgres -f /backup.sql
    docker cp $CONTAINER_ID:/backup.sql ./backup.sql
fi
echo "Backup created"