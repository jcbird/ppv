from setuptools import find_packages, setup

setup(
    name='ppv',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    version='0.36',
    description='Tools for dealing with SDSS-V plate files and plate runs.',
    author='Jonathan Bird',
    url='https://github.com/jcbird/ppv',
    license='BSD-3')
