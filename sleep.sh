#!/bin/bash

set -e
UNTIL=$1
NOW_SEC=$(date +%s)

function doSleep {
    WAIT_SEC=$1
    NOW=$(date -d @$NOW_SEC +"%Y-%m-%d %H:%M:%S")
    END_SEC=$((NOW_SEC + WAIT_SEC))
    END=$(date -d @$END_SEC +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - sleeping $1 seconds until '$END'..." 1>&2
    sleep $WAIT_SEC
    #sleep 0
    NOW=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - done sleeping" 1>&2
    exit 0
}
re='^[0-9]+$'
if [[ $UNTIL =~ $re ]] ; then
    echo "Specifying directly the wait time $UNTIL sec..."
    WSEC=$UNTIL
elif echo "$UNTIL" | grep -q '^20..-..-..'; then # starts with a date (like '2019-12-20')
    echo "Specifying a datetime..."
    D=$(date -d "$UNTIL" +%s)
    WSEC=$((D - NOW_SEC))
    if [[ $WSEC -lt 0 ]]; then
        echo "The date '$UNTIL' is in the past..." 1>&2
        exit -1
    fi
else
    echo "Specify a time..."
    D=$(date -d "$UNTIL" +%s)
    if [[ $D -lt $NOW_SEC ]]; then
        echo "Too late for today, going for next day..."
        D=$(date -d "$UNTIL 1 day" +%s)
    fi
    WSEC=$((D - NOW_SEC))
fi

doSleep $WSEC
