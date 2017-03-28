.. image:: https://img.shields.io/travis/giampaolo/psutil-cli/master.svg?maxAge=3600&label=Linux%20/%20OSX
    :target: https://travis-ci.org/giampaolo/psutil-cli
    :alt: Linux tests (Travis)

.. image:: https://coveralls.io/repos/github/giampaolo/psutil-cli/badge.svg?branch=master
    :target: https://coveralls.io/github/giampaolo/psutil-cli?branch=master
    :alt: Test coverage (coverall.io)

.. image:: https://img.shields.io/pypi/v/psutil-cli.svg?label=pypi
    :target: https://pypi.python.org/pypi/psutil/
    :alt: Latest version

.. image:: https://img.shields.io/github/stars/giampaolo/psutil-cli.svg
    :target: https://github.com/giampaolo/psutil/
    :alt: Github stars

.. image:: https://img.shields.io/pypi/l/psutil-cli.svg
    :target: https://pypi.python.org/pypi/psutil/
    :alt: License

Cross-platform command line utilities based on
`psutil <https://github.com/giampaolo/psutil/>`__.

Motivation
==========

There is a set of well known command line utilities such as ps, top, netstat
etc. which are available on pretty much all UNIX platforms (but not Windows).
Most of them work similarly but all have minor or major differences regarding
the command line options and the printed output, both of which are not
standarized.

The aim of this project is to provide clones of the most famous UNIX CLI
utilities such as ps, top, netstat, etc. which are portable across all UNIX
platforms and Windows and which all provide the same interface in terms of
cmdline parsing and printed output.

NOTE: still a work in progress.

Utilities
=========

* `psutil-sysmem <https://github.com/giampaolo/psutil-cli/blob/master/psutilcli/sysmem.py>`__: system memory info.
* `psutil-procsmem <https://github.com/giampaolo/psutil-cli/blob/master/psutilcli/procsmem.py>`__: shows "real" (USS) memory usage for all processes.
