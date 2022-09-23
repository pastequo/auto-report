#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io

from setuptools import setup, find_packages

def read_file(name):
    with io.open(os.path.join(os.path.dirname(__file__), name), encoding='utf8') as f:
        return f.read()

def read_reqs(name):
    return [line for line in read_file(name).split('\n') if line and not line.strip().startswith('#')]

ROOT = os.path.dirname(__file__)

if sys.version_info < (3, 6, 0):
    sys.exit("Python 3.6.0 is the minimum required version for building this package")

setup(
    name='auto-report',
    version="0.0.1",
    description='Automate reporting',
    long_description=read_file('README.md'),
    author='RedHat',
    author_email='unknown',
    url='https://github.com/openshift-assisted/auto-reporter',
    packages=find_packages('.'),
    package_dir={'': '.'},
    include_package_data=True,
    license="Apache License 2.0",
    zip_safe=False,
    keywords='automate report elasticsearch',
    python_requires='>=3.6',
    install_requires=read_reqs('requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': ["auto_report = auto_report.__main__:cli"],
    },
)
