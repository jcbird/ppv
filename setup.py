from setuptools import find_packages, setup

setup(
    name='ppv',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    version='0.0.1',
    description='Tools for dealing with SDSS-V plate files and plate runs.',
    author='Jonathan Bird',
    license='BSD-3')

# setup(name='sdss5ops',
#       version='0.0.1',
#       description='SDSS-V OPS tools',
#       url='http://github.com/jcbird/ops',
#       author='Jonathan Bird',
#       author_email='flyingcircus@example.com',
#       license='MIT',
#       packages=find_packages(where='src'),
#       package_dir={"": "src"},
#       zip_safe=False)
