#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = '0.6.7'

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
    install_requires=[
        "Jinja2==2.9.6",
        "humanize==0.5.1",
        "pytz==2017.2",
        "pyhocon==0.3.38",
        "python-dateutil==2.6.0",
        "requests==2.18.1",
    ],
    license="MIT",
    zip_safe=False,
    packages=find_packages(exclude=["*tests*"]),

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        # If any package contains configs/*.conf and templates/* files, include them:
        '': [
            '*templates/*',  # at least generator package
            '*configs/*.conf'  # at least validator package
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: QA Developers',
        'Topic :: Software Development :: QA Testing Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
)
