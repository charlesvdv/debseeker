import gzip
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
import appdirs

PACKAGE_ARCHIVES_PATH = '%s/Packages.gz' % tempfile.gettempdir()

ARCHITECTURE_SUPPORTED = ['amd64', 'arm64', 'armel', 'armhf', 'i386', \
                          'mips', 'mipsel', 'powerpc', 'ppc64el', 's390x']

def check_packages_update(force_update=False, arch='amd64'):
    if arch not in ARCHITECTURE_SUPPORTED:
        print('Architecture %s is not supported.')
        exit(1)

    pkgpath = _get_packages_path(arch)
    lastweek = time.time() - 7*24*3600
    if force_update or not os.path.exists(pkgpath) \
            or os.stat(pkgpath).st_mtime < lastweek:
        sys.stdout.write("Downloading package information... ")
        try:
            _download_packages_file(arch)
        except urllib.error.HTTPError:
            print('Fail (check your connection)')
        else:
            print('Done')
    return pkgpath


def _download_packages_file(arch):
    urllib.request.urlretrieve(_get_packages_url(arch), PACKAGE_ARCHIVES_PATH)
    with gzip.open(PACKAGE_ARCHIVES_PATH, mode='rb') as f:
        data = f.read().decode('utf-8')
    with open(_get_packages_path(arch), 'w') as p:
        p.write(data)
    os.remove(PACKAGE_ARCHIVES_PATH)

def _get_packages_path(arch):
    return '%s/Packages-%s' % (appdirs.user_cache_dir(), arch)

def _get_packages_url(arch):
    return 'http://ftp.us.debian.org/debian/dists/stable/main/binary-%s/Packages.gz' % arch
