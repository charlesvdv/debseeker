import pytest
from debseeker import parser

def test_parse_rawdata():
    pkgs = parser._parse_rawdata(PARSERDATA)
    assert pkgs[0].get_name() == '2ping'
    assert pkgs[3].get_name() == 'libds-admin-serv0'
    assert pkgs[0].get_dict()['Depends'] == ['perl']
    assert pkgs[2].get_dict()['Depends'][0] == 'libadminutil0'
    assert pkgs[0].get_dict()['Description'] == 'Ping utility to determine ' \
        'directional packet loss\nAn other line to test this'



# Data used to test the parser.
# Extracted directly from the Package file
# provided by Debian. (extracted the 09/17/2016)
# Just modified a little for test purpose
PARSERDATA = """Package: 2ping
Version: 2.1.1-1
Installed-Size: 135
Maintainer: Ryan Finnie <ryan@finnie.org>
Architecture: all
Depends: perl
Recommends: perl-modules, libio-socket-inet6-perl
Suggests: libdigest-sha-perl, libdigest-crc-perl
Description: Ping utility to determine directional packet loss
 An other line to test this
Homepage: http://www.finnie.org/software/2ping/
Description-md5: 2543c220a763445976d1348c5b593743
Tag: implemented-in::perl, interface::commandline, protocol::ip,
 role::program, scope::utility, use::analysing, use::measuring,
 works-with::network-traffic
Section: net
Priority: optional
Filename: pool/main/2/2ping/2ping_2.1.1-1_all.deb
Size: 28018
MD5sum: 8ebead27d793b86471b48b93404e8727
SHA1: 09e1bebe6e0f17b1f66887f0b2a75e1ffa4803d8
SHA256: 93f4377d1fcaff754fe1ed8d0852d14c8e1ab5c8eb4628f8f33c765d21253a85

Package: 2vcard
Version: 0.5-3
Installed-Size: 108
Maintainer: Martin Albisetti <argentina@gmail.com>
Architecture: all
Description: perl script to convert an addressbook to VCARD file format
Description-md5: f6f2cb6577ba2821b51ca843d147b3e1
Tag: implemented-in::perl, role::program, use::converting, works-with::pim
Section: utils
Priority: optional
Filename: pool/main/2/2vcard/2vcard_0.5-3_all.deb
Size: 14300
MD5sum: d831fd82a8605e9258b2314a7d703abe
SHA1: e903a05f168a825ff84c87326898a182635f8175
SHA256: 2be9a86f0ec99b1299880c6bf0f4da8257c74a61341c14c103b70c9ec04b10ec

Package: 389-admin
Version: 1.1.35-2
Installed-Size: 1192
Maintainer: Debian 389ds Team <pkg-fedora-ds-maintainers@lists.alioth.debian.org>
Architecture: i386
Depends: libadminutil0 (>= 1.1.8), libc6 (>= 2.7), libds-admin-serv0 (= 1.1.35-2), libicu52 (>= 52~m1-1~), libldap-2.4-2 (>= 2.4.7), libnspr4 (>= 2:4.9-2~) | libnspr4-0d (>= 1.8.0.10), libnss3 (>= 2:3.13.4-2~) | libnss3-1d (>= 3.12.0~1.9b1), libsasl2-2, libnss3-tools, libmozilla-ldap-perl, libapache2-mod-nss, 389-ds-base, apache2
Pre-Depends: debconf (>= 0.5) | debconf-2.0, multiarch-support
Description: 389 Directory Administration Server
Homepage: http://directory.fedoraproject.org
Description-md5: 54d5378a9195f30f9bb174c93052507a
Section: net
Priority: optional
Filename: pool/main/3/389-admin/389-admin_1.1.35-2_i386.deb
Size: 257840
MD5sum: f252679c7d5f8d8fcf7970c6fa65c8e3
SHA1: bba24c81b8b0382ad2184f510d4cdf75c39a6f2e
SHA256: eee7a50f243b2947808f9cd58e0af421d817e25d82e56bd584a0a991f76fbfce

Package: libds-admin-serv0
Source: 389-admin
Version: 1.1.35-2
Installed-Size: 167
Maintainer: Debian 389ds Team <pkg-fedora-ds-maintainers@lists.alioth.debian.org>
Architecture: i386
Depends: libadminutil0 (>= 1.1.8), libc6 (>= 2.4), libldap-2.4-2 (>= 2.4.7), libnspr4 (>= 2:4.9-2~) | libnspr4-0d (>= 1.8.0.10)
Pre-Depends: debconf (>= 0.5) | debconf-2.0, multiarch-support
Description: Libraries for the 389 Directory Administration Server
Multi-Arch: same
Homepage: http://directory.fedoraproject.org
Description-md5: 598e92132ec24840f97ba737d3ebafb6
Tag: role::shared-lib
Section: libs
Priority: optional
Filename: pool/main/3/389-admin/libds-admin-serv0_1.1.35-2_i386.deb
Size: 48208
MD5sum: 8a487d4766e894a2f0e3dd74540e3bb3
SHA1: 828c1b306f21adf83b74598dba5bd40510dbf90e
SHA256: b52d73bbe0163676a36e64a156e8a5edabb36841b20599cbbe64bc34b580637e"""
