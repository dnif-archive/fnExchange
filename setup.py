"""
fnExchange is a scalable, open source API layer (also called an API
"router") that provides a consistent proxy web interface for invoking
various web APIs without the caller having to write separate,
special-purpose code for each of them.

fnExchange is packaged as a command line interface executable
``fnexchange`` which starts the web service. The CLI also supports a
mode to run the service as a daemon.

Installation, usage and plugin development instructions can be found
on the project's `GitHub page <http://github.com/dnif/fnExchange>`_
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

dependencies = [
    'click==6.7',
    'PyYAML==3.12',
    'requests>=2.4.2',
    'six==1.10.0',
    'tornado==4.4.2',
]

setup(
    name='fnexchange',
    version='0.2.1',
    url='https://github.com/dnif/fnExchange',
    license='Apache',
    author='Bhumil Haria',
    author_email='bhumilharia@gmail.com',
    description='fnExchange API router and management CLI',
    long_description=__doc__,
    keywords='fnexchange api router orchestration',
    platforms='any',

    install_requires=dependencies,

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'fnexchange = fnexchange.cli:cli',
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
