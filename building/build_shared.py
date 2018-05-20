import subprocess
import os

def log(msg):
    print('[INFO] %s' % msg)

def exec_cmd(cmd):
    log(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        raise RuntimeError("Command failed: %s" % result.returncode)
    return result.stdout.decode('utf-8').rstrip()

def stream_cmd(cmd):
    log(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)

    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line.decode('utf-8').rstrip()

    process.communicate()

    if process.returncode != 0:
        raise RuntimeError("Command failed: %s" % process.returncode)

def project_dir():
    my_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.realpath(os.path.join(my_dir, '..'))
    return project_dir

def project_version():
    return exec_cmd(['python', 'setup.py', '--version'])

def project_name():
    return exec_cmd(['python', 'setup.py', '--name'])




