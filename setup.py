from setuptools import find_packages, setup

setup(
    name='ppv',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    package_data={"": ["data/platePlans_sdss5.fits"]},
    version='0.0.1',
    description='Tools for dealing with SDSS-V plate files and plate runs.',
    author='Jonathan Bird',
    url='https://github.com/jcbird/ppv',
    license='BSD-3')
