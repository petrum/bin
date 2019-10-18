#!/bin/bash

UNTIL=$1

function doSleep {
    NOW=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - sleeping $1 seconds until '$2'..." 1>&2
    sleep $1
    #sleep 0
    NOW=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - done sleeping" 1>&2
    exit 0
}

re='^[0-9]+$'

if [[ $UNTIL =~ $re ]] ; then
    doSleep $UNTIL done
fi

LEN=${#UNTIL}

TODAY=$(date +"%Y-%m-%d")
TOMORROW=$(date -d "1 day" +"%Y-%m-%d")
NOW=$(date +%s)

if [[ $LEN -eq 5 || $LEN -eq 8 ]]; then
    D=$(date -d "$TODAY $UNTIL" +%s)
    if [[ $D -lt $NOW ]]; then
        D=$(date -d "$TOMORROW $UNTIL" +%s)
    fi
    SEC=$((D - NOW))
    doSleep $SEC "$UNTIL"
fi

if [[ $LEN -eq 19 ]]; then
    D=$(date -d "$UNTIL" +%s)
    SEC=$((D - NOW))
    if [[ $SEC -lt 0 ]]; then
        echo "The date '$UNTIL' is in the past..." 1>&2
        exit -1
    fi
    doSleep $SEC "$UNTIL"
fi

echo "I don't know what to do! What does '$UNTIL' mean?" 1>&2
echo "(supported formats are: 'N' (sec), '09:30', '09:30:45', or '2019-10-17 09:30:24')" 1>&2
exit -1
