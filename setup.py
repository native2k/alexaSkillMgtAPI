#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
#history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='alexaSkillMgtAPI',
    version='0.1.0',
    description='Python implementation of the Amazon Alexa Skill Management API.',
    long_description=readme
    author='Sven Richter',
    author_email='native2k@gmail.com',
    url='https://github.com/native2k/alexaSkillMgtAPI',
    packages=[
        'alexaSkillMgtAPI',
    ],
    package_dir={'alexaSkillMgtAPI': 'alexaSkillMgtAPI'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='alexaSkillMgtAPI',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
