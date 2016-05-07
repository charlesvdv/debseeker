""" This package allow you to find package dependency of a given debian package without aptitude """

import argparse
import gzip
import os.path
import os
import re
import time
import urllib.request


URL_PACKAGES = 'http://ftp.be.debian.org/debian/dists/stable/main/binary-i386/Packages.gz'
PACKAGE_FILE_NAME = 'Packages'

def getPackageFile():
    """
    Download the packages informations from the ftp mirror
    """
    urllib.request.urlretrieve(URL_PACKAGES, 'Packages.gz')
    with gzip.open('Packages.gz', mode='rb') as f:
        data = f.read().decode('utf-8')
        with open(PACKAGE_FILE_NAME, 'w') as p:
            p.write(data)
    os.remove('Packages.gz')

def parsePackageInfo(rawdata):
    """
    Parse a package information from the "Package" file. Take as argument an str representing
    the package data directly extracted from the "Package" file and return a dictionnary with
    all the information parsed.
    """
    pkginfo = {}

    lines = rawdata.split('\n')
    for line in lines:
        info = line.split(':')
        if len(info) < 2:
            # FIXME: what to do when we don't have a key/value pair
            # Is it possible ?
            continue
        key = info[0]
        # it's possible to have ':' in the line so we join the value with nothing
        value = ''.join(info[1:])
        # remove the version info as package dependencies have this form: pkgname (>/</= version)
        if key in ['Depends', 'Pre-Depends', 'Recommends', 'Suggests', 'Replaces', 'Provides']:
            p = re.compile(r'\(.*?\)', re.MULTILINE)
            pkgdepends = p.sub('', value)
            pkginfo[key.strip()] = stripStrList(pkgdepends.strip().split(','))
        else:
            pkginfo[key.strip()] = value.strip()
    return pkginfo

def parsePackages(rawdata):
    """
    Parse a list of raw data containing package information.
    Return a list of maps.
    """
    pkgs = []
    for pkg in rawdata:
        pkgs.append(parsePackageInfo(pkg))
    return pkgs

def getPackageDependencies(pkg, suggest=False, recommanded=False):
    """
    Extract the package dependency from a dictionnary containing the package information.
    We can also ask for suggested package and recommanded package optionnaly.
    Return a list of package name.
    """
    depends = []
    # mandatory package
    if 'Pre-Depends' in pkg:
        depends += pkg['Pre-Depends']
    if 'Depends' in pkg:
        depends += pkg['Depends']

    # optional package
    if suggest and 'Suggests' in pkg:
        depends += pkg['Suggests']
    if recommanded and 'Recommends' in pkg:
        depends += pkg['Recommends']

    return depends

def findPackage(packages, name):
    # TODO: cleared explication over here ...
    """
    Find a package in a list of maps containing package information.
    The package is searched with his name. The function may not return
    a package that has this name but has other field as "Replaces", "Provides", ...
    that have the same information.
    Return the dictionnary with the package information or None if nothing was found
    """
    for pkg in packages:
        if 'Package' in pkg and pkg['Package'] == name:
            return pkg
        elif 'Replaces' in pkg and name in pkg['Replaces']:
            return pkg
        elif 'Provides' in pkg and name in pkg['Provides']:
            return pkg
        elif 'Source' in pkg and pkg['Source'] == name:
            return pkg
    return None

# iterative function to find all the dependents packages from a given package name
def findPackageDependencies(packages, pkgname):
    """
    Find the all packages dependencies for a given package name. It will iterate for
    each package dependency and find his own dependencies.
    Return a list of all packages names that depends from the given package.
    """
    dependencies = []
    # set the packageName in the dependencies lists
    pkg = findPackage(packages, pkgname)
    if pkg is None:
        return

    name = pkgname
    dependencies.append(pkgname)
    # preference for the XOR package choice
    preferencies = []
    # package that we still need to iterate
    toiterate = []
    # package that we already checked and don't need to be iterated
    checked = []
    while True:
        pkg = findPackage(packages, name)
        if pkg is None:
            return

        pkgdependencies = getPackageDependencies(pkg)
        for dependency in pkgdependencies:
            pkgdepend = {}
            # we have a XOR dependency
            if '|' in dependency:
                xorpkgs = stripStrList(dependency.split('|'))
                for xorpkg in xorpkgs:
                    if xorpkg in preferencies:
                        pkgdepend = findPackage(packages, xorpkg)
                        break
                else:
                    for index, xorpkg in enumerate(xorpkgs):
                        print('\t%d. %s' % (index, xorpkg))
                    choosed = int(input('Choose a package: '))
                    preferencies.append(xorpkgs[choosed])
                    pkgdepend = findPackage(packages, xorpkgs[choosed])
            else:
                pkgdepend = findPackage(packages, dependency)

            if pkgdepend is None:
                print('Could not find package dependency with name: %s' % dependency)
                return

            if not pkgdepend['Package'] in dependencies:
                dependencies.append(pkgdepend['Package'])

            if not pkgdepend['Package'] in checked:
                toiterate.append(pkgdepend['Package'])

        checked.append(pkg['Package'])

        # end of the iteration
        # we don't have any package to check left
        if len(toiterate) == 0:
            return dependencies

        # put the next name to check and delete it from to_iterate
        name = toiterate[0]
        del toiterate[0]


# ---- UTILS ----

def stripStrList(strlist):
    """
    Trim each string in a list
    """
    newstr = []
    for str in strlist:
        newstr.append(str.strip())
    return newstr

def removeDuplicate(elements):
    """
    Remove duplicates existing in a list
    """
    baselist = []
    for i in elements:
        if not i in baselist:
            baselist.append(i)

    return baselist

# --- main program ---

def init():
    """
    Initialize the program by downloading the "Packages" file and parse it to return
    a list of dictionnaries of packages informations
    """
    # Check if we need to download the data again
    lastweek = time.time() - 7*24*60*60
    if not os.path.exists(PACKAGE_FILE_NAME) or os.stat(PACKAGE_FILE_NAME).st_mtime < lastweek:
        print('Downloading packages informations')
        getPackageFile()
        print('Download done!')

    with open(PACKAGE_FILE_NAME, 'r') as f:
        return parsePackages(f.read().split('\n\n'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find Debian dependencies without apt')
    parser.add_argument('search', help='Search the dependencies of a given package')
    parser.add_argument('packages', nargs='*', help='packages names')
    args = parser.parse_args()

    if args.search:
        print('Beginning initialization...')
        packages = init()
        print('Initialization done!\n')
        output = ''
        dependencies = []
        for packageName in args.packages:
            pkgdepends = findPackageDependencies(packages, packageName)
            if pkgdepends is None:
                print('An error occured while searching', packageName)
                break
            dependencies += pkgdepends

        dependencies = removeDuplicate(dependencies)
        out = ''
        for dep in dependencies:
            out += dep + ' '
        print()
        print(out)
