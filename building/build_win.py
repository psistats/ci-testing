import sys
import os
import subprocess

ISCC=os.path.join('c:/','Program Files (x86)','Inno Setup 5','iscc.exe')

def log(msg):
    print('[INFO] %s' % msg)

my_dir = os.path.dirname(os.path.realpath(__file__))

project_dir = os.path.realpath(os.path.join(my_dir, '..'))

log('Project Directory: %s' % project_dir)

os.chdir(project_dir)


def exec_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise RuntimeError("Command failed: %s" % result.returncode)
    
    return result.stdout

def stream_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break;
        yield line
     
    process.communicate()
    if process.returncode != 0:
        raise RuntimeError("Command failed: %s" % process.returncode)
        

project_version = exec_cmd(['python', 'setup.py', '--version']).decode('utf-8').strip()
project_name    = exec_cmd(['python', 'setup.py', '--name']).decode('utf-8').strip()

log('%s:%s' % (project_name, project_version))

cmds = [
    ['pyinstaller', 'citest\\w32\\console.py'],
    ['pyinstaller', 'citest\\w32\\service.py'],
    [ISCC, 'building\\w32installer.iss', '/DMyAppVersion=%s' % project_version]
]

for cmd in cmds:
    log(cmd)
    for output in stream_cmd(cmd):
        log(output)

