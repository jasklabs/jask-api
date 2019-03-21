'Install trident_client module'

from os import path
from codecs import open
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='trident_client',
    version='1.2',
    description='JASK Trident API Client',
    long_description=long_description,
    url='https://github.com/jasklabs/jask-api',
    author='JASK Labs',
    author_email='support@jask.io',
    license='',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
    ],
    packages=['trident_client'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests==2.20.0',
        'unicodecsv==0.14.1',
    ],
)
