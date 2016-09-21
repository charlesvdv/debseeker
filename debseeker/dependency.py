from .search import PackageSeeker, PackageNotFoundError
from .package import Package

class DependencySeeker:
    def __init__(self, pkgs):
        self.pkgs = pkgs
        self.searcher = PackageSeeker(self.pkgs)
        # Already checked package during the dependency check.
        # Allow to improve performance while checking for optional pkg.
        self._checked = set()

    def get_dependencies(self, pkgname, optional_dep=False):
        """
        Search recursively for the dependencies of the package.

        Return the dependencies for a given package and also the
        optional dependencies (which still need to be searched over).
        """
        dependencies = set()
        optional_dependencies = set()

        to_check = set([pkgname])
        while len(to_check) > 0:
            currentcheck = to_check.pop()
            if currentcheck in self._checked:
                continue
            self._checked.add(currentcheck)

            if '|' in currentcheck:
                # We have an OR dependencies.
                pkg = self._handle_or_dependencies(currentcheck)
            else:
                pkg = self.searcher.find_dependency(currentcheck)

            if type(pkg) is list:
                # In case of a Source package, we have multiple package.
                to_check.update([p.get_name() for p in pkg[1:]])
                pkg = pkg[0]

            dependencies.add(pkg.get_name())

            pkgdeps = pkg.get_required_dependencies()
            optional_dependencies.update(pkg.get_optional_dependencies())

            for dep in pkgdeps:
                if dep not in self._checked:
                    to_check.add(dep)

        # Recursively search for the optional dependencies
        if optional_dep and len(optional_dependencies) > 0:
            # Clean the optional package to remove already checked package
            optional_dependencies -= self._checked
            for opt_pkg in optional_dependencies:
                # As an optional package is not that important, it's not a problem 
                # if the user can't find it. We just print a warning to the user.
                try:
                    dependencies.update(self.get_dependencies(opt_pkg))
                except PackageNotFoundError as e:
                    print('Can\'t find optional package or his dependencies: *%s*' % e.pkgnotfound)
        return dependencies

    def _get_less_dependencies_pkg(self, *pkgs):
        """
        Choose the OR dependency that has the least amount
        of dependency at the first level.
        """
        best = Package(dict())
        bestname = ''
        bestscore = 100
        for pkgname in pkgs[0]:
            try:
                pkg = self.searcher.find_dependency(pkgname)
                if type(pkg) is list:
                    # Handle Source package
                    for sourcepkg in pkg:
                        if len(sourcepkg.get_required_dependencies()) <= bestscore and \
                                sourcepkg.get_search_score() >= best.get_search_score():
                            best = sourcepkg
                            bestname = pkgname
                            bestscore = len(sourcepkg.get_required_dependencies())
                else:
                    if len(pkg.get_required_dependencies()) <= bestscore and \
                            pkg.get_search_score() >= best.get_search_score():
                        best = pkg
                        bestname = pkgname
                        bestscore = len(pkg.get_required_dependencies())
            except PackageNotFoundError:
                pass
        if len(best.get_dict()) == 0:
            raise PackageNotFoundError('', ' '.join(pkgs[0]))
        return best

    def _handle_or_dependencies(self, or_dep):
        """
        An OR dependencies is multiple package possible to be the
        dependency of a given package. We have split them and choose
        one between all of them.
        """
        orpkgs = [pkg.strip() for pkg in or_dep.split('|')]
        return self._get_less_dependencies_pkg(orpkgs)
