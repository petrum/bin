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
    #sleep 0
    NOW=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$NOW - done sleeping" 1>&2
    exit 0
}
re='^[0-9]+$'
if [[ $UNTIL =~ $re ]] ; then
    echo "Specifying directly the wait time $UNTIL sec..." 1>&2
    WSEC=$UNTIL
elif echo "$UNTIL" | grep -q '^....-..-..'; then # starts with a date (like '2019-12-20')
    echo "Specifying a datetime..." 1>&2
    WSEC=$(($(date -d "$UNTIL" +%s) - NOW_SEC))
else
    echo "Specifying a time..." 1>&2
    WSEC=$(($(date -d "$UNTIL" +%s) - NOW_SEC))
    if [[ $D -lt $NOW_SEC ]]; then
        echo "Too late for today, going for next day..." 1>&2
        WSEC=$(($(date -d "$UNTIL 1 day" +%s) - NOW_SEC))
    fi
fi

doSleep $WSEC
