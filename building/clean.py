#!/usr/bin/env python
import os, sys
import shutil
import logging
import glob

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

PATHS = [
    'psireporter/**/*.pyc',
    'htmlcov/',
    'deb_dist/',
    'dist/',
    '.debenv/',
    '.tox/',
    '.pytest_cache/',
    'build/',
    '.coverage/',
    'coverage.xml']

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))


for path in PATHS:

    root_path = os.path.join(ROOT_DIR, path)

    globbed = glob.glob(root_path, recursive=True)

    for deltarget in reversed(globbed):
        if os.path.exists(deltarget):
            logging.info('Delete: %s' % deltarget)
            if os.path.isfile(deltarget):
                try:
                    os.remove(deltarget)
                except PermissionError as e:
                    logging.error('Permission error: %s' % deltarget)
            else:
                shutil.rmtree(deltarget)

sys.exit()

def out(msg, nl=False):
    sys.stdout.write(msg)
    if nl:
        sys.stdout.write(os.linesep)


def remove_path(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            remove_path(path)
        else:
            if os.path.isfile(fn):
                os.remoregister_archive_formatve(fn)
            else:
                os.rmdir(fn)
            out("deleted: %s" % fn, True)
    else:
       out("%s does not exist" % fn, True)

dirs = ['./htmlcov', './dist', './.tox', './.pytest_cache', './build']
files = ['./.coverage', './coverage.xml']

for dirname in dirs:
    if os.path.exists(dirname):
        shutil.rmtree(dirname)

for fn in files:
    if os.path.exists(fn):
        os.remove(fn)

