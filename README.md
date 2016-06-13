# deseeker

*debseeker* allow you to search Debian package without installing a VM and use *aptitude*.

You can also find dependencies of Debian package.

# Usage

*debseeker* main help
```
$ python debseeker.py --help
usage: debseeker.py [-h] [-u] {search,dependencies} ...

debseeker is a Debian package finder

positional arguments:
  {search,dependencies}
    search              search if given packages exist
    dependencies        find dependencies for given packages

optional arguments:
  -h, --help            show this help message and exit
  -u, --update          update the packages data
```

Update the packages data and search if *gcc* and *pkg-not-existing* exist or not.
```
$ python debseeker.py -u search gcc pkg-not-existing
Downloading packages information... Done
Beginning initializing... Done

package found: gcc

Can't find package pkg-not-existing
```

Search for the dependencies of *gcc* and *make*
```
python debseeker.py dependencies gcc make
Beginning initializing... Done

gcc cpp cpp-4.9 gcc-4.9-base libdb1-compat libcloog-isl4 libgmp10 libisl10 libmpc3 libmpfr4 zlib1g multiarch-support make libdb1-compat
```
