#!/bin/bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd $MY_DIR/.. && pwd )"

cd $ROOT_DIR

VERSION="$( python setup.py --version )"
NAME="$( python setup.py --name )"

echo "PROJECT_NAME=$NAME" > envvars.properties
echo "PROJECT_VERSION=$VERSION" >> envvars.properties
