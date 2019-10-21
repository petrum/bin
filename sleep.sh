#!/bin/bash

set -e
UNTIL=$1
NOW_SEC=$(date +%s)

function doSleep {
    WAIT_SEC=$1
    if [[ $WAIT_SEC -lt 0 ]]; then
        echo "The wait time $WAIT_SEC is negative" 1>&2
        exit -1
    fi
    NOW=$(date -d @$NOW_SEC +"%Y-%m-%d %H:%M:%S")
    END_SEC=$((NOW_SEC + WAIT_SEC))
    END=$(date -d @$END_SEC +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - sleeping $WAIT_SEC seconds until '$END'..." 1>&2
    sleep $WAIT_SEC
    NOW=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - done sleeping" 1>&2
    exit 0
}
re='^[0-9]+$'
if [[ $UNTIL =~ $re ]] ; then
    echo "Specifying directly the wait time $UNTIL sec..." 1>&2
    WSEC=$UNTIL
else
    UNTIL_TIME=0 && echo "$UNTIL" | grep -q '^....-..-..' || UNTIL_TIME=1
    echo "Specifying a time = $UNTIL_TIME..." 1>&2
    WSEC=$(($(date -d "$UNTIL" +%s) - NOW_SEC))
    if [[ $WSEC -lt 0 && $UNTIL_TIME = 1 ]]; then
        echo "Too late for today, going for next day..." 1>&2
        WSEC=$(($(date -d "$UNTIL 1 day" +%s) - NOW_SEC))
    fi
fi
doSleep $WSEC
