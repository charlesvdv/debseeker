import re

from utils import *

class Packages:
    def __init__(self):
        self.packages = []

    def parse(self, raw_data):
        """
        Parse the 'Packages' file downloaded from the Debian ftp.

        return a list of each package represented by a dictionnary
        """
        for pkg_data in raw_data.split('\n\n'):
            pkg = {}
            for l in pkg_data.split('\n'):
                key_value = l.split(':')
                if len(key_value) < 2:
                    # FIXME: what to do in there ?
                    continue
                key = key_value[0].strip()
                value = ''.join(key_value[1:])

                if key in ['Depends', 'Pre-Depends', 'Recommends',
                        'Suggests', 'Replaces', 'Provides']:
                    # remove the package version constraint
                    regex = re.compile(r'\(.*?\)', re.MULTILINE)
                    special_infos = regex.sub('', value).split(',')
                    pkg[key] = strip_str_list(special_infos)
                else:
                    pkg[key] = value.strip()
            self.packages.append(pkg)


    def list_dependencies(self, pkg_name):
        """
        Find all the dependencies of a given package.

        pkg_name: name of the package for which we have to find
            the dependencies
        return a list of string representing the name of the dependencies
        throw PackageNotFoundError if a package is not found
        """
        dependencies = []

        to_check = [pkg_name]
        checked = []
        while len(to_check) > 0:
            pkg = {}
            try:
                pkg = self.find_package(to_check[0])
            except PackageNotFoundError:
                raise

            del to_check[0]

            if pkg['Package'] not in dependencies:
                dependencies.append(pkg['Package'])
                # the package name ('Package') and the package searched name
                # 'Name' could be different.
                checked.append(pkg['Name'])

            deps = self._find_package_dependencies(pkg)
            for dep in deps:
                name = dep
                if '|' in dep:
                    name = self._handle_or_dependencies(dep)

                if name not in to_check and name not in checked:
                    to_check.append(name)

        return dependencies

    def _handle_or_dependencies(self, or_dep_data):
        """
        Handle the package dependencies where we have more than
        one choice for a given package.

        or_dep_data: string wich contain raw_data for the
            choice of package
        return the name of the package that we choosed
        """
        if '|' not in or_dep_data:
            return or_dep_data

        or_deps = strip_str_list(or_dep_data.split('|'))
        return self._best_or_pkg_callback(or_deps)

    def _best_or_pkg_callback(self, or_deps):
        """
        Choose the package that has the least dependencies of
        one level.

        or_deps: list of possible packages
        return the name of the choosed package
        throw PackageNotFoundError if a package is not found
        """
        best_pkg_name = ''
        best_pkg_dep_num = 100
        for dep in or_deps:
            pkg = {}
            try:
                pkg = self.find_package(dep)
            except PackageNotFoundError:
                raise
            dep_pkg_dep_num = len(self._find_package_dependencies(pkg))
            if dep_pkg_dep_num < best_pkg_dep_num:
                best_pkg_name = pkg['Package']
                best_pkg_dep_num = dep_pkg_dep_num
        return best_pkg_name

    def _find_package_dependencies(self, pkg, optional_keys=[]):
        """
        Find a package dependencies with a possibility to choose
        also the optional package given.

        pkg: the package dictionnary
        optional_keys: list of key that we have also to take into account
        return a list of a package one-level dependencies
        """
        dep = []
        depend_keys = ['Pre-Depends', 'Depends']
        for key in depend_keys:
            if key in pkg:
                dep += pkg[key]

        for key in optional_keys:
            if key in pkg:
                dep += pkg[key]

        return dep

    def find_package(self, pkg_name):
        """
        Search a package in the packages list

        pkg_name: the name of the package to find
        return the pkg dictionnary
        throw PackageNotFoundError if we can't find the package
        """
        keys = ['Package', 'Source', 'Replaces', 'Provides']

        for pkg in self.packages:
            found = False
            for key in keys:
                if key in pkg:
                    if isinstance(pkg[key], list) and pkg_name in pkg[key]:
                        # It could be possible to have packages sources that
                        # have multiples packages choices
                        found = True
                    elif pkg_name == pkg[key]:
                        found = True
                if found:
                    # Save the key type to know if the package is a replacement package, ...
                    pkg['Name'] = pkg_name
                    return pkg
        raise PackageNotFoundError('Could not find the package %s' % pkg_name)


class PackageNotFoundError(Exception):
    def __init__(self, message):
        super(PackageNotFoundError, self).__init__(message)
