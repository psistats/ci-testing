from build_shared import log, exec_cmd, stream_cmd, project_dir, project_version, project_name
import sys
import os
import subprocess

ISCC=os.path.join('c:/','Program Files (x86)','Inno Setup 5','iscc.exe')

PROJECT_NAME = project_name()
PROJECT_VERSION = project_version()
PROJECT_DIR = project_dir()

WINDOWS_VERSION = PROJECT_VERSION

# Have to convert python version of [x].[y].[z].dev[b] to
# windows version of [x].[y].[z].[b]
if '.dev' in PROJECT_VERSION:
    verparts = PROJECT_VERSION.split('.dev')
    WINDOWS_VERSION + '%s.%s' % (verparts[0], verparts[1])

log('Project Directory: %s' % PROJECT_DIR)

os.chdir(PROJECT_DIR)

cmds = [
    ['pyinstaller', 'citest\\w32\\console.py'],
    ['pyinstaller', 'citest\\w32\\service.py'],
    [ISCC, 'building\\w32installer.iss', '/DMyAppVersion=%s' % windows_version]
]

for cmd in cmds:
    log(cmd)
    for output in stream_cmd(cmd):
        log(output)

