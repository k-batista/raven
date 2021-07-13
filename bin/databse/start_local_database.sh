#!/usr/bin/env bash
set +e
EXEC_OPTION=$1
SCRIPT_DIR=$(dirname $0)
SOURCE_DIR=$(pwd)

# set -euo pipefail
# IFS=$'\n\t'

IMAGE_DB_NAME=postgres-raven
CONTAINER_DB_NAME=postgres-raven-container
GRADLE_DB_SERVER=local

stop_container() {
  if [[ -n $(docker ps -q -f name=$CONTAINER_DB_NAME) ]]; then
    echo "Stopping container ${CONTAINER_DB_NAME}"
    docker stop $(docker ps -q -f name=$CONTAINER_DB_NAME)
  fi
}

remove_container() {
  if [[ -n $(docker ps -q -a -f name=$CONTAINER_DB_NAME) ]]; then
    echo "Removing container ${CONTAINER_DB_NAME}"
    docker rm $(docker ps -q -a -f name=$CONTAINER_DB_NAME)
  fi
}

remove_image() {
  if [[ -n $(docker  images -q $IMAGE_DB_NAME) ]]; then
    echo "Removing image ${IMAGE_DB_NAME}"
    docker rmi $(docker  images -q $IMAGE_DB_NAME)
  fi
}

build_image() {
  echo "Building image ${IMAGE_DB_NAME}"
  docker build --no-cache -t $IMAGE_DB_NAME .
}

start_container() {
  echo "Starting container ${CONTAINER_DB_NAME}"
  docker run --name=$CONTAINER_DB_NAME --restart=unless-stopped -p 5405:5432 -d $IMAGE_DB_NAME
}

migrate() {
  cd $SOURCE_DIR
  ./jenkins/gradle/gradlew -b jenkins/gradle/build.gradle databaseMigration -Dserver=$GRADLE_DB_SERVER --stacktrace --info
}

repair() {
  cd $SOURCE_DIR
  ./jenkins/gradle/gradlew -b jenkins/gradle/build.gradle databaseRepair -Dserver=$GRADLE_DB_SERVER --stacktrace --info
}

build_image_process() {
  cd $SCRIPT_DIR
  stop_container
  remove_container
  remove_image
  build_image
  start_container
}

recreate_container_process() {
  stop_container
  remove_container
  start_container
}

run() {
  if [[ $EXEC_OPTION == "build_image" ]]; then
    build_image_process
  # elif [[ $EXEC_OPTION == "migrate" ]]; then
  #   migrate
  # elif [[ $EXEC_OPTION == "recreate" ]]; then
  #   recreate_container_process
  #   sleep 10s
  #   migrate
  elif [[ -z $EXEC_OPTION ]]; then
    build_image_process
    # sleep 10s
    # migrate
  fi
}

run




