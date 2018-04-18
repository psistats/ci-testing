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

if [ -z "$BUILD_NUMBER" ]
then
  BUILD_NUMBER=1
fi

if [ -d "$DEB_DIST_DIR" ]; then
  rm -r $DEB_DIST_DIR
fi

if [ ! -d "$ENV_DIR" ]; then
  virtualenv -p python3 $ENV_DIR
fi

source $ENV_DIR/bin/activate

pip install stdeb

python setup.py sdist
python setup.py --command-packages=stdeb.command sdist_dsc --debian-version "$BUILD_NUMBER"dev

#cd $DIST_DIR

#py2dsc $NAME-$VERSION.tar.gz

cd $DEB_DIST_DIR/$NAME-$VERSION

dpkg-buildpackage -rfakeroot -uc -us
