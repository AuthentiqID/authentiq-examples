#!/usr/bin/env bash
##
# This section should match your Makefile
##
BROWSERSYNC=${BROWSERSYNC:-browser-sync}

BASEDIR=$(pwd)

SRV_PID=$BASEDIR/examples_srv.pid

function usage(){
  echo "usage: $0 (stop) (start) (restart) [port]"
  echo "This starts BrowserSync to help site development."
  exit 3
}

function alive() {
  kill -0 $1 >/dev/null 2>&1
}

function shut_down(){
  PID=$(cat $SRV_PID)
  if [[ $? -eq 0 ]]; then
    if alive $PID; then
      echo "Stopping BrowserSync"
      kill $PID
    else
      echo "Stale PID, deleting"
    fi
    rm $SRV_PID
  else
    echo "BrowserSync PIDFile not found"
  fi
}

function start_up(){
  local port=$1
  echo "Starting up BrowserSync and HTTP server"
  shift
  $BROWSERSYNC start --server --port $port --index "index.html" --files "**/*" &
  srv_pid=$!
  echo $srv_pid > $SRV_PID

  sleep 1
  if ! alive $srv_pid ; then
    echo "The BrowserSync didn't start. Is there another service using port" $port "?"
    return 1
  fi
  echo 'BrowserSync processes now running in background.'
}

###
#  MAIN
###
[[ ($# -eq 0) || ($# -gt 2) ]] && usage
port=8090
[[ $# -eq 2 ]] && port=$2


if [[ $1 == "stop" ]]; then
  shut_down
elif [[ $1 == "restart" ]]; then
  shut_down
  start_up $port
elif [[ $1 == "start" ]]; then
  if ! start_up $port; then
    shut_down
  fi
else
  usage
fi
