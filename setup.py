#!/usr/bin/env python

'''The setup and build script for the TOPdesk-api library.'''

import os

from setuptools import setup, find_packages

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
        name='topdesk-api',
        version='1.0.0',
        author='Digizone ICT',
        author_email='support@digizone.nl',
        license='GNU GPLv3',
        url='https://github.com/DigizoneICT/topdesk-api-python',
        keywords='topdesk',
        description='Python library for TOPdesk API',
        long_description=(read('README.rst')),
        packages=find_packages(exclude=['tests*']),
        install_requires=['requests'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3.0',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
)