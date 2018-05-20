from build_shared import log, exec_cmd, stream_cmd, project_dir, project_version, project_name
import os

PROJECT_NAME = project_name()
PROJECT_VERSION = project_version()
PROJECT_DIR = project_dir()

DEBIAN_VERSION = PROJECT_VERSION

os.chdir(PROJECT_DIR)

# Have to convert python version of [x].[y].[z].dev[b] to
# debian version of [x].[y].[z]~dev[b]

if '.dev' in PROJECT_VERSION:
    verparts = PROJECT_VERSION.split('.dev')

    DEBIAN_VERSION = '%s~dev%s' % (verparts[0], verparts[1])

log('Project Name: %s' % PROJECT_NAME)
log('Project Version: %s' % PROJECT_VERSION)
log('Debian Version: %s' % DEBIAN_VERSION)

for line in stream_cmd(['virtualenv', '-p', 'python3', '.debenv']):
    log(line)

venv_activate_file = os.path.join(PROJECT_DIR, '.debenv', 'bin', 'activate_this.py')

exec(open(venv_activate_file).read(), dict(__file__=venv_activate_file))

cmds = [
    ['pip', 'install', 'stdeb'],
    ['python', 'setup.py', '--command-packages=stdeb.command', 'sdist_dsc']
]

for cmd in cmds:
    for line in stream_cmd(cmd):
        log(line)

os.chdir(os.path.join(PROJECT_DIR, 'deb_dist', '%s-%s' % (PROJECT_NAME, DEBIAN_VERSION)))

for line in stream_cmd(['dpkg-buildpackage', '-rfakeroot', '-uc', '-us']):
    log(line)

