#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import importlib
import sys

root_package_dir = 'packages'
main_package = 'backup_to_s3'

name = 'backup-to-s3'
description = 'An incremental backup to s3 service'
url = 'http://github.com/behos/backup-to-s3'
author = 'Giorgos Georgiou'
author_email = 'giorgos.georgiou@outlook.com'
license = 'GPL'

install_requires = [
    'boto==2.35.1',
    'sqlalchemy==0.9.8',
    'inflection==0.2.1',
    'pyyaml==3.11',
    'FileChunkIO==1.6'
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
    packages=[main_package],
    package_dir={'': root_package_dir},
    install_requires=install_requires,
    script_args=sys.argv[1:],
    include_package_data=True,
)
