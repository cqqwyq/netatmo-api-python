
# python setup.py --dry-run --verbose install

from distutils.core import setup


setup(
    name='lnetatmo',
    version='0.9.2.1-vaillant',  # Should be updated with new versions
    author='Samuel Dumont, forked from Philippe Larduinat',
    author_email='samuel@dumont.ovh, philippelt@users.sourceforge.net',
    py_modules=['lnetatmo'],
    packages=['smart_home'],
    package_dir={'smart_home': 'smart_home'},
    scripts=[],
    data_files=[],
    url='https://github.com/samueldumont/netatmo-api-python',
    license='Open Source',
    description='Simple API to access Vaillant vSmart thermostat data (rebranded Netatmo thermostat)',
    long_description=open('README.md').read()
)
