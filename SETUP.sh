#!/bin/bash

error() {
  cat <<< "$@" 1>&2;
  exit 1
}

if ! java -version;
then
  if ! sudo apt-get install openjdk-17-jre -y;
  then
    error "Could not install missing openjdk!"
  fi
fi

if [ ! -d "venv" ]
then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
python setup.py $@

rm -rf venv
