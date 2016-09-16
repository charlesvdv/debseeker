import appdirs
import gzip
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request

URL_PACKAGES = 'http://ftp.us.debian.org/debian/dists/stable/main/binary-all/Packages.gz'
PACKAGE_PATH = '%s/Packages' % appdirs.user_cache_dir()
PACKAGE_ARCHIVES_PATH = '%s/Packages.gz' % tempfile.gettempdir()

def check_packages_update(force_update=False):
    lastweek = time.time() - 7*24*3600
    if force_update or not os.path.exists(PACKAGE_PATH) \
            or os.stat(PACKAGE_PATH).st_mtime < lastweek:
        sys.stdout.write("Downloading package information... ")
        try:
            _download_packages_file()
        except urllib.error.HTTPError:
            print('Fail (check your connection)')
        else:
            print('Done')
    return PACKAGE_PATH


def _download_packages_file():
    urllib.request.urlretrieve(URL_PACKAGES, PACKAGE_ARCHIVES_PATH)
    with gzip.open(PACKAGE_ARCHIVES_PATH, mode='rb') as f:
        data = f.read().decode('utf-8')
        with open(PACKAGE_PATH, 'w') as p:
            p.write(data)
    os.remove(PACKAGE_ARCHIVES_PATH)
