class PackageSeeker:
    def __init__(self, pkgs):
        self.pkgs = pkgs

    def find_dependency(self, pkgname):
        """
        Find information about the package for his dependencies.

        Some package could not be found just by their name so
        we need to look also for some others information key like
        'Source' or 'Provides'.

        /!\ BE CAREFUL ! This function can return a Package object or
        a list of Package object. You should be able to handle both.
        This is because the Source is actually a folder where multiples
        dependencies lives so we need to use get all of them.
        """
        # Search for direct name hit
        for pkg in self.pkgs:
            if pkg.get_name() == pkgname:
                return pkg

        # Search for Source directory package.
        # FIXME: move this code somewhere else
        # because it return a list instead of a Package object
        pkgsources = []
        for pkg in self.pkgs:
            if pkg.is_info_exist('Source') and \
                    pkg.get_source() == pkgname:
                pkgsources.append(pkg)
        if len(pkgsources) != 0:
            return pkgsources

        # In last resort, search for package that provide
        # this package.
        for pkg in self.pkgs:
            for pkgprov in pkg.get_provides():
                if pkgprov == pkgname:
                    return pkg

        # In very very last resort, we check if we not have a
        # package that could conflict (thus giving the same files)
        # as a given package.
        for pkg in self.pkgs:
            for pkgconf in pkg.get_conflicts():
                if pkgconf == pkgname:
                    return pkg

        raise PackageNotFoundError('No package was found by the name: ' + pkgname, pkgname)

    def find_fuzzy(self, pkgname, threshold=80):
        pass

class PackageNotFoundError(Exception):
    def __init__(self, message, pkgname):
        super(PackageNotFoundError, self).__init__(message)
        self.pkgnotfound = pkgname
