from .search import PackageSeeker, PackageNotFoundError

class DependencySeeker:
    def __init__(self, pkgs):
        self.pkgs = pkgs
        self.searcher = PackageSeeker(self.pkgs)

    def get_dependencies(self, pkgname, optional_dep=False):
        """
        Search recursively for the dependencies of the package.
        """
        dependencies = set()

        to_check = set([pkgname])
        while len(to_check) > 0:
            currentcheck = to_check.pop()
            if '|' in currentcheck:
                # We have an OR dependencies.
                pkg = self._handle_or_dependencies(currentcheck)
            else:
                pkg = self.searcher.find_dependency(currentcheck)

            if type(pkg) is list:
                # In case of a Source package, we have multiple package.
                dependencies.add(pkg[0].get_name())
                if len(pkg) > 1:
                    to_check.add([p.get_name() for p in pkg[1:]])
                pkg = pkg[0]
            else:
                dependencies.add(pkg.get_name())

            pkgdeps = pkg.get_required_dependencies()
            if optional_dep:
                pkgdeps += pkg.get_optional_dependencies()

            for dep in pkgdeps:
                if dep not in dependencies:
                    to_check.add(dep)
        return dependencies


    def _get_less_dependencies_pkg(self, *pkgs):
        """
        Choose the OR dependency that has the least amount
        of dependency at the first level.
        """
        best = None
        bestscore = 100
        for pkgname in pkgs[0]:
            try:
                pkg = self.searcher.find_dependency(pkgname)
                if type(pkg) is list:
                    # Handle Source package
                    for sourcepkg in pkg:
                        if len(sourcepkg.get_required_dependencies()) < bestscore:
                            best = sourcepkg
                            bestscore = len(sourcepkg.get_required_dependencies())
                else:
                    if len(pkg.get_required_dependencies()) < bestscore:
                        best = pkg
                        bestscore = len(pkg.get_required_dependencies())
            except PackageNotFoundError:
                pass
        return best

    def _handle_or_dependencies(self, or_dep):
        """
        An OR dependencies is multiple package possible to be the
        dependency of a given package. We have split them and choose 
        one between all of them.
        """
        orpkgs = [pkg.strip() for pkg in or_dep.split('|')]
        return self._get_less_dependencies_pkg(orpkgs)
