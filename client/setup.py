# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='polycode',
    version='1.0.2',
    description='Translate your code to a different spoken language',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/froothacks/polycode',
    author='David Gu',
    py_modules=["polycode"],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'polycode=polycode:main',
        ],
    },
)