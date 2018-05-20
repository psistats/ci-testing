import os
import sys
import shutil
from build_shared import project_dir
import urllib.request
from urllib.parse import urlparse, unquote

PROJECT_DIR = project_dir()

DOWNLOAD_DIR = os.path.join(PROJECT_DIR, 'artifact_download')

if os.path.exists(DOWNLOAD_DIR):
    shutil.rmtree(DOWNLOAD_DIR)

os.makedirs(DOWNLOAD_DIR)

url = sys.argv[1]

urlparts = urlparse(url)

target_filename = os.path.basename(urlparts.path)

target_filename = unquote(target_filename)
target_filename = os.path.basename(target_filename)


def report_hook(block, size, totalsize):
    total = block * size

    if totalsize > 0:
        percent = total * 1e2 / totalsize

        s = "\r%5.1f%% %*d / %d" % (
                percent,
                len(str(totalsize)),
                total,
                totalsize
        )
        print(s)
    else:
        print(total)

urllib.request.urlretrieve(url, os.path.join(DOWNLOAD_DIR, target_filename), report_hook)

