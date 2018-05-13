#!/usr/bin/env python
import os, sys, re, argparse

parser = argparse.ArgumentParser(description='Change Version Number')
parser.add_argument('--inc-major', help='Increments the major version', action='store_true')
parser.add_argument('--inc-minor', help='Increments the minor version', action='store_true')
parser.add_argument('--inc-patch', help='Increments the patch number', action='store_true')
parser.add_argument('--inc-build', help='Increments the build number', action='store_true')
parser.add_argument('--set-version', help='Manually set the version number', type=str)
parser.add_argument('--set-major', help='Sets the major version', type=int)
parser.add_argument('--set-minor', help='Sets the minor version', type=int)
parser.add_argument('--set-patch', help='Sets the patch number', type=int)
parser.add_argument('--set-build', help='Sets the build number', type=int)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.realpath(os.path.join(SCRIPT_DIR, '..'))


def parse_version_line(line):

    r1 = r"version\='(.*)'"

    result = re.compile(r1).findall(line)

    if len(result) == 0:
        raise Exception("Could not parse version line: %s" % line)

    sVersion = result[0]

    return parse_version(sVersion)


def parse_version(sVersion):

    print("wtf are we parsing? %s" % sVersion)

    rexp = r"([0-9]+)\.([0-9]+)\.([0-9]+)(\.dev([0-9]*))*"

    prog = re.compile(rexp)

    result = prog.findall(sVersion)

    if len(result) == 0:
        raise Exception("Could not parse version: %s" % sVersion)

    version = [int(result[0][0]), int(result[0][1]), int(result[0][2])]

    if len(result[0]) == 5:
        if result[0][4] != '':
            version.append(int(result[0][4]))
        else:
            version.append(0)
    else:
        version.append(0)

    print("and? %s" % version)

    return tuple(version)

def set_new_version(version, major, minor, patch, build):
    new_version = list(version)
    if major != None:
        new_version[0] = int(major)

    if minor != None:
        new_version[1] = int(minor)

    if patch != None:
        new_version[2] = int(patch)

    if build != None:
        new_version[3] = int(build)

    return tuple(new_version)

def inc_new_version(version, major, minor, patch, build):
    new_version = list(version)

    if major is True:
        new_version[0] = new_version[0] + 1

    if minor is True:
        new_version[1] = new_version[1] + 1

    if patch is True:
        new_version[2] = new_version[2] + 1

    if build is True:
        new_version[3] = new_version[3] + 1

    return tuple(new_version)




args = vars(parser.parse_args())
print(args)


f = open(os.path.join(PROJECT_DIR, 'setup.py'))
setuppy = f.readlines()

for lineno, line in enumerate(setuppy):

    line = line.strip('\n')
    if line.startswith('      version=\''):
        current_version = parse_version_line(line)


        if (args['set_version'] != None):
            new_version = parse_version(args['set_version'])

        elif (args['set_major'] or args['set_minor'] or args['set_patch'] or args['set_build']):
            new_version = set_new_version(current_version, args['set_major'], args['set_minor'], args['set_patch'], args['set_build'])

        elif (args['inc_major'] or args['inc_minor'] or args['inc_patch'] or args['inc_build']):
            new_version = inc_new_version(current_version, args['inc_major'], args['inc_minor'], args['inc_patch'], args['inc_build'])

        sNewVersion = '%s.%s.%s' % (new_version[0], new_version[1], new_version[2])

        if new_version[3] > 0:
            sNewVersion += '.dev%s' % new_version[3]

        print("current version: %s - new version: %s (%s)" % (current_version, new_version, sNewVersion))

        setuppy[lineno] = '      version=\'%s\',' % sNewVersion
    else:
        setuppy[lineno] = line


f.close()

f = open(os.path.join(PROJECT_DIR, 'setup.py'), 'w')
f.write('\n'.join(setuppy))
f.close()




f.close()
