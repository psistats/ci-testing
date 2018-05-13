#!/bin/bash
###############################################################################
# Creates a debian source package then creates a deb file                     #
###############################################################################

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd $MY_DIR/.. && pwd )"
ENV_DIR=$ROOT_DIR/.debenv
DIST_DIR=$ROOT_DIR/dist
DEB_DIST_DIR=$ROOT_DIR/deb_dist

echo "Root directory: $ROOT_DIR"

cd $ROOT_DIR

VERSION="$( python setup.py --version )"
NAME="$( python setup.py --name )"

if [[ $VERSION = *"dev"* ]]; then
  echo ">>> DEV VERSION <<<"
  IFS=".dev" read -r -a array <<< "$VERSION"
  BUILD_NUMBER="${array[-1]}"
  echo ">>> MAJOR:        ${array[0]}   <<<"
  echo ">>> MINOR:        ${array[1]}   <<<"
  echo ">>> PATCH:        ${array[2]}   <<<"
  echo ">>> BUILD NUMBER: $BUILD_NUMBER <<<"
  DEBIAN_VERSION="${array[0]}.${array[1]}.${array[2]}~dev$BUILD_NUMBER"
else
  DEBIAN_VERSION=$VERSION
fi

echo ">>> FINAL DEBIAN VERSION: $DEBIAN_VERSION <<<"
  

if [ -d "$DEB_DIST_DIR" ]; then
  rm -r $DEB_DIST_DIR
fi

if [ ! -d "$ENV_DIR" ]; then
  virtualenv -p python3 $ENV_DIR
fi

source $ENV_DIR/bin/activate

pip install stdeb

python setup.py sdist
python setup.py --command-packages=stdeb.command sdist_dsc

#cd $DIST_DIR

#py2dsc $NAME-$VERSION.tar.gz

cd $DEB_DIST_DIR/$NAME-$DEBIAN_VERSION

dpkg-buildpackage -rfakeroot -uc -us
