#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = '0.1'

readme = open(os.path.join(DIR, 'README.md')).read()

# todo: pack modules inside test_utils (now they packing out of test_utils)

setup(
    name='test_utils',
    version=version,
    description="""Common test utils""",
    long_description=readme,
    author='Ilya Shubkin',
    author_email='ilya.shubkin@gmail.com',
    url='https://github.com/ujlbu4/test_utils',
    include_package_data=True,
    install_requires=[
        "pitz==2017.2",
    ],
    license="BSD???",
    zip_safe=False,
    packages=find_packages(exclude=["tests", "tests.*"]),
    # classifiers=[
    #     'Development Status :: 2 - Pre-Alpha',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: BSD License',
    #     'Natural Language :: English',
    #     'Programming Language :: Python :: 2',
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.3',
    #     'Programming Language :: Python :: 3.4',
    # ],
)