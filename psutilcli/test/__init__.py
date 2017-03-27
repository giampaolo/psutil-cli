"""Test utilities."""

import subprocess
import sys
import os
import warnings

from psutilcli._compat import PY3

if sys.version_info < (2, 7):
    import unittest2 as unittest  # requires "pip install unittest2"
else:
    import unittest  # NOQA


ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'psutilcli')
TOX = os.getenv('TOX') or '' in ('1', 'true')
VERBOSITY = 1 if os.getenv('SILENT') or TOX else 2


def sh(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """run cmd in a subprocess and return its output.
    raises RuntimeError on error.
    """
    p = subprocess.Popen(cmdline, shell=True, stdout=stdout, stderr=stderr)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise RuntimeError(stderr)
    if stderr:
        if PY3:
            stderr = str(stderr, sys.stderr.encoding or
                         sys.getfilesystemencoding())
        warnings.warn(stderr, UserWarning)
    if PY3:
        stdout = str(stdout, sys.stdout.encoding or
                     sys.getfilesystemencoding())
    return stdout.strip()
