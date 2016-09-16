# deseeker

*debseeker* allow you to find easily all the dependencies of a Debian package 
without installing any VM.

# Why?

Working on an archlinux system, I needed the dependencies for some Debian packages
for embedding an application in a UML (User-Mode Linux: linux kernel running as an 
application on a linux system). The project is named
[pythia](https://github.com/pythia-project/pythia-core) and mostly the 
[environments](https://github.com/pythia-project/environments) parts.

# Usage

*debseeker* main help
```
$ python debseeker.py -h
usage: debseeker.py [-h] [-u] {dependencies} ...

debseeker is a Debian package finder

positional arguments:
  {dependencies}
    dependencies  find dependencies for given packages

optional arguments:
  -h, --help      show this help message and exit
  -u, --update    update the packages data
```

Search for the dependencies of *gcc* and *make*
```
python debseeker.py dependencies gcc make
Beginning initializing... Done

gcc cpp cpp-4.9 gcc-4.9-base libdb1-compat libcloog-isl4 libgmp10 libisl10 libmpc3 libmpfr4 zlib1g multiarch-support make libdb1-compat
```
