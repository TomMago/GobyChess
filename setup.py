from setuptools import setup

CLASSIFIERS = '''\
License :: OSI Approved
Programming Language :: Python :: 3.7 :: 3.8
Topic :: Software Development
'''

DISTNAME = 'gobychess'
AUTHOR = 'Tom Magorsch'
AUTHOR_EMAIL = 'tom.magorsch@tu-dortmund.de'
DESCRIPTION = 'Chess Engine'
LICENSE = 'MIT'
README = 'Simple python chess engine'

VERSION = '0.1.0'
ISRELEASED = False

PYTHON_MIN_VERSION = '3.7'
PYTHON_REQUIRES = f'>={PYTHON_MIN_VERSION}'

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
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    classifiers=[CLASSIFIERS],
    license=LICENSE
)

if __name__ == '__main__':
    setup(**metadata)
