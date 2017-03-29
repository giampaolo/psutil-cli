#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = "0.1"


setup(
    name='psutil-cli',
    version=VERSION,
    keywords=[],
    author='Giampaolo Rodola',
    author_email='g.rodola@gmail.com',
    url='https://github.com/giampaolo/psutil-cli',
    platforms='Platform Independent',
    license='BSD',
    packages=['psutilcli', 'psutilcli.compat', 'psutilcli.test'],
    install_requires=['psutil', 'docopt'],
    entry_points={
        "console_scripts": [
            "psutil-sysmem=psutilcli.sysmem:main",
        ]},
)
