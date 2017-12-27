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


setup(
    name='test_utils',
    version=version,
    description="""Common test utils""",
    long_description=readme,
    author='Ilya Shubkin',
    author_email='ilya.shubkin@gmail.com',
    url='https://github.com/ujlbu4/test_utils',
    include_package_data=True,
    # install_requires=[
    #     "six>=1.7.3",
    #     "PyYAML>=3.11",
    #     "validate-email>=1.2",
    #     "rfc3987>=1.3.4",
    #     "requests>=2.4.3",
    #     "strict-rfc3339>=0.7",
    #     "click>=3.3",
    #     "jsonpointer>=1.7",
    # ],
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