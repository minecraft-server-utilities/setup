#!/bin/bash

error() {
  cat <<< "$@" 1>&2;
  exit 1
}

backup=$1
if [ -f "$backup" ]
then
  rm -rf world/
  if ! tar -xzf "$backup";
  then
    error "Could not extract \"$backup\"!"
  fi
else
  error "File \"$backup\" not found!"
fi

# TODO: check java version and set it
if ! java -version;
then
  # TODO: add package manager choice
  if ! sudo apt-get install openjdk-8-jdk -y;
  then
    error "Could not install missing openjdk!"
  fi
fi

java -Xmx7168M -Xms2048M -jar server.jar -nogui
