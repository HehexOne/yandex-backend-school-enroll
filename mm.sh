#!/bin/bash

sudo chmod 777 "/var/run/docker.sock"

if [[ $1 == "build" ]]
then
  docker-compose build
elif [[ $1 == "run" ]]
then
  docker-compose up -d
elif [[ $1 == "stop" ]]
then
  docker-compose stop
elif [[ $1 == "rebuild" ]]
then
  docker-compose stop
  docker containers prune -f
  docker images prune -f
  docker-compose build
  docker-compose up -d
else
  echo "Неверная команда! Список доступных команд: build, run, stop, rebuild"
fi