""" debseeker allows you to find search Debian package without apt or even
    without a linux machine. """

import argparse
import sys

import debseeker.download as pkgdownloader
import debseeker.parser as pkgparser
from debseeker import DependencySeeker
from debseeker import PackageSeeker, PackageNotFoundError

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='debseeker is a Debian package finder')
    parser.add_argument('-u', '--update', help='update the packages data', action='store_true')

    subparsers = parser.add_subparsers(dest='action')
    #  search_parser = subparsers.add_parser('search', help='search if given packages exist')
    #  search_parser.add_argument('packages', nargs='*')
    #  search_parser.add_argument('-m', '--exact-match', help='show only if package exactly match',
    #                             action='store_true')

    dep_parser = subparsers.add_parser('dependencies', help='find dependencies for given packages')
    dep_parser.add_argument('packages', nargs='*')
    #  dep_parser.add_argument('-o', '--or-dependency', help='''allow choosing the or dependencies
    #                           of the package''', action='store_true')
    dep_parser.add_argument('-p', '--optional-package', help='''pick also the falcultative
            package''', action='store_true')

    args = parser.parse_args()

    pkgpath = pkgdownloader.check_packages_update(args.update)

    sys.stdout.write('Beginning initializing... ')
    pkgs = pkgparser.parse(pkgpath)
    print('Done\n')

    if args.action == 'dependencies':
        depsearcher = DependencySeeker(pkgs)
        dependencies = set()
        for pkg in args.packages:
            try:
                dependencies.update(depsearcher.get_dependencies(pkg, args.optional_package))
            except PackageNotFoundError as e:
                print('Can\'t find package %s...' % e.pkgnotfound)

        print(' '.join(dependencies))
