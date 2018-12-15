
# python setup.py --dry-run --verbose install

from distutils.core import setup
import setuptools


setup(
    name='pyatmo',
    version='1.4.1-vaillant',  # Should be updated with new versions
    author='Samuel Dumont, based on Hugo Dupras',
    author_email='samuel@dumont.ovh',
    py_modules=['pyatmo'],

    packages=['smart_home'],
    package_dir={'smart_home': 'smart_home'},
    scripts=[],
    data_files=[],

    url='https://github.com/samueldumont/netatmo-api-python',
    license='MIT',
    description='Simple API to access Netatmo weather station data from any python script. '
                'Design for Home-Assitant (but not only)',
    long_description=open('README.md').read()
)
