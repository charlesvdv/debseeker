""" debseeker allows you to find search Debian package without apt or even
    without a linux machine. """

import argparse
import gzip
import os.path
import os
import sys
import time
import urllib.request

from packages import Packages, PackageNotFoundError
from utils import *


URL_PACKAGES = 'http://ftp.be.debian.org/debian/dists/stable/main/binary-i386/Packages.gz'
PACKAGE_FILE_NAME = 'Packages'

def download_packages_file():
    urllib.request.urlretrieve(URL_PACKAGES, 'Packages.gz')
    with gzip.open('Packages.gz', mode='rb') as f:
        data = f.read().decode('utf-8')
        with open(PACKAGE_FILE_NAME, 'w') as p:
            p.write(data)
    os.remove('Packages.gz')

def read_packages_file():
    if not os.path.exists(PACKAGE_FILE_NAME):
        raise FileNotFoundError
    with open(PACKAGE_FILE_NAME, 'r') as f:
        return f.read()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='debseeker is a Debian package finder')
    parser.add_argument('-u', '--update', help='update the packages data', action='store_true')

    subparsers = parser.add_subparsers(dest='action')
    search_parser = subparsers.add_parser('search', help='search if given packages exist')
    search_parser.add_argument('packages', nargs='*')
    search_parser.add_argument('-m', '--exact-match', help='show only if package exactly match',
            action='store_true')

    dep_parser = subparsers.add_parser('dependencies', help='find dependencies for given packages')
    dep_parser.add_argument('packages', nargs='*')
    dep_parser.add_argument('-o', '--or-dependency', help='''allow choosing the or dependencies
            of the package''', action='store_true')
    dep_parser.add_argument('-f', '--facultative-package', help='''pick also the falcultative
            package''', action='store_true')

    args = parser.parse_args()
    print(args)

    pkg_handler = Packages()

    lastweek = time.time() - 7*24*3600
    if args.update or not os.path.exists(PACKAGE_FILE_NAME) \
            or os.stat(PACKAGE_FILE_NAME).st_mtime < lastweek:
        sys.stdout.write('Downloading packages information... ')
        download_packages_file()
        print('Done')


    sys.stdout.write('Beginning initializing... ')
    pkg_handler.parse(read_packages_file())
    print('Done\n')

    if args.action == 'search':
        for pkg in args.packages:
            try:
                p = pkg_handler.find_package(pkg)
                if pkg == p['Name']:
                    print('package found: %s' % pkg)
                else:
                    print('package %s found as %s' % (pkg, p['Name']))
            except PackageNotFoundError:
                print('Can\'t find package %s' % pkg)

            print()

    elif args.action == 'dependencies':
        dependencies = []
        for pkg in args.packages:
            try:
                dependencies += pkg_handler.list_dependencies(pkg)
            except PackageNotFoundError:
                print('Can\'t find package %s' % pkg)

        remove_duplicates(dependencies)
        print(' '.join(dependencies))
