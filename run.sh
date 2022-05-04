#!/bin/bash
set -o allexport
source .env
set +o allexport

PARAMS="main:app --app-dir ./src --host $HOST --port $PORT --workers $WORKERS"

if [[ -n "$SSL_KEYFILE" ]]
then
    PARAMS="$PARAMS --ssl-keyfile $SSL_KEYFILE --ssl-certfile $SSL_CERTFILE --ssl-keyfile-password $SSL_KEYFILE_PASSWORD"
fi
uvicorn $PARAMS