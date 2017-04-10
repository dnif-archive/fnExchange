from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

dependencies = [
    'click',
    'requests>=2.4.2',
]

setup(
    name='fnexchange',
    version='0.0.10',
    url='https://github.com/dnif/fnExchange',
    license='Apache',
    author='Bhumil Haria',
    author_email='bhumilharia@gmail.com',
    description='fnExchange API router and management CLI',
    long_description=long_description,
    keywords='fnexchange api router orchestration',
    platforms='any',

    install_requires=dependencies,

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'fnexchange-cli = fnexchange.cli:cli',
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
