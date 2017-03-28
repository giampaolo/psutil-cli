import ast
import os
import sys
import stat

from psutil import LINUX
from psutil import OSX
from psutil import POSIX
from psutil import WINDOWS

from psutilcli.test import unittest
from psutilcli.test import sh
from psutilcli.test import SCRIPTS_DIR


SCRIPTS = ["ps.py", "sysmem.py", "procsmem.py"]


class TestScripts(unittest.TestCase):
    """Tests for scripts in the "scripts" directory."""

    def assert_stdout(self, exe, args=None):
        exe = '"%s"' % os.path.join(SCRIPTS_DIR, exe)
        if args:
            exe = exe + ' ' + args
        try:
            out = sh(sys.executable + ' ' + exe).strip()
        except RuntimeError as err:
            if 'AccessDenied' in str(err):
                return str(err)
            else:
                raise
        assert out, out
        return out

    def assert_syntax(self, exe, args=None):
        exe = os.path.join(SCRIPTS_DIR, exe)
        with open(exe, 'r') as f:
            src = f.read()
        ast.parse(src)

    def test_coverage(self):
        # make sure all example scripts have a test method defined
        meths = dir(self)
        for name in SCRIPTS:
            if 'test_' + os.path.splitext(name)[0] not in meths:
                # self.assert_stdout(name)
                self.fail('no test defined for %r script'
                          % os.path.join(SCRIPTS_DIR, name))

    @unittest.skipUnless(POSIX, "POSIX only")
    def test_executable(self):
        for name in SCRIPTS:
            if name.endswith('.py'):
                path = os.path.join(SCRIPTS_DIR, name)
                if not stat.S_IXUSR & os.stat(path)[stat.ST_MODE]:
                    self.fail('%r is not executable' % path)

    def test_ps(self):
        self.assert_stdout('ps.py')

    def test_sysmem(self):
        self.assert_stdout('sysmem.py')

    def test_procsmem(self):
        if OSX or LINUX or WINDOWS:
            self.assert_stdout('procsmem.py')
        else:
            self.assert_syntax('procsmem.py')
