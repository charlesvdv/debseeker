import os
import re
from collections import OrderedDict

from .package import Package

def parse(filepath):
    """
    Read the file given and parse it to return
    a list of Package information.
    """
    rawdata = _readfile(filepath)
    return _parse_rawdata(rawdata)


def _readfile(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError
    with open(filepath, 'r') as f:
        return f.read()

def _parse_rawdata(rawdata):
    # Precompile the regex to not recompile it everytime
    # in the double loop. Remove everything in the parenthese inclusive.
    regex = re.compile(r'\(.*?\)', re.ASCII)

    pkgs = []
    for pkg_info in rawdata.split('\n\n'):
        pkg = OrderedDict()
        for line in pkg_info.split('\n'):
            if line == '':
                continue

            key = ''
            if line[0] == ' ' or not line[0].isupper():
                # We have a multiline information value
                key = next(reversed(pkg))
                value = line
                # Special case for Description we add a linebreak.
                if key == 'Description':
                    value = '\n' + line.strip()
            else:
                key, value = line.split(':', 1)

            # Do not strip \n for Description value
            key, value = key.strip(), value.strip(' ')

            # Remove the version constrains for the package
            # information.
            if key in ['Depends', 'Pre-Depends', 'Recommends',
                       'Suggests', 'Replaces', 'Provides', 'Conflicts']:
                # Remove the :any that appears on "python:any" which
                # means choose between python2.6 and python2.7 but
                # we will use the default python which is "python".
                value = value.replace(':any', '')
                value = regex.sub('', value).split(',')
                value = [val.strip() for val in value]
            
            # Check if we need to create or append value to the key.
            if key in pkg:
                pkg[key] += value
            else:
                pkg[key] = value

        if pkg != OrderedDict():
            pkgs.append(Package(pkg))
    return pkgs
