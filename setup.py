#!/usr/bin/env python3

# python setup.py develop
from setuptools import setup


CLASSIFIERS = '''\
License :: OSI Approved
Programming Language :: Python :: 3.7 :: 3.8
Topic :: Software Development
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
'''

DISTNAME = 'gobychess'
AUTHOR = 'Tom Magorsc'
AUTHOR_EMAIL = 'tom.magorsch@tu-dortmund.de'
DESCRIPTION = 'Chess Engine'
LICENSE = 'MIT'
README = 'Simple python chess engine'

VERSION = '0.1.0'
ISRELEASED = False

PYTHON_MIN_VERSION = '3.7'
PYTHON_REQUIRES = f'>={PYTHON_MIN_VERSION}'

INSTALL_REQUIRES = [
    'gmpy2'
]

PACKAGES = [
    'gobychess',
    'tests',
    'benchmarks'
]

metadata = dict(
    name=DISTNAME,
    version=VERSION,
    long_description=README,
    packages=PACKAGES,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    classifiers=[CLASSIFIERS],
    license=LICENSE
)

if __name__ == '__main__':
    setup(**metadata)
