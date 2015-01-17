#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import importlib
import sys

root_package_dir = 'packages'
packages = find_packages(root_package_dir)
main_package = 'backup-to-s3'

name = 'backup-to-s3'
description = 'An incremental backup to s3 service'
url = 'http://github.com/behos/backup-to-s3'
author = 'Giorgos Georgiou'
author_email = 'giorgos.georgiou@outlook.com'
license = 'GPL'

install_requires = [
    'boto',
]


def get_version(package):
    module = importlib.import_module('.'.join([root_package_dir, package]))
    return module.__version__


setup(
    name=name,
    version=get_version(main_package),
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=packages,
    package_dir={'': root_package_dir},
    install_requires=install_requires,
    script_args=sys.argv[1:],
    include_package_data=True,
)
