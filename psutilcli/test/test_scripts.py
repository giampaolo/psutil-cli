from psutilcli.test import unittest
from psutilcli.test import runscript


class TestSysmem(unittest.TestCase):

    def test_h_opt(self):
        runscript("sysmem.py -h")

    def test_b_opt(self):
        runscript("sysmem.py -b")
        runscript("sysmem.py --bytes")

    def test_p_opt(self):
        runscript("sysmem.py -p")
        runscript("sysmem.py --parsable")

    def test_n_opt(self):
        runscript("sysmem.py -N")
        runscript("sysmem.py --nocolors")


class TestProcsmem(unittest.TestCase):

    def test_h_opt(self):
        runscript("procsmem.py -h")

    def test_s_opt(self):
        runscript("procsmem.py -s uss")
        runscript("procsmem.py -s pss")
        runscript("procsmem.py -s swap")
        runscript("procsmem.py -s rss")
        with self.assertRaises(RuntimeError):
            runscript("procsmem.py -s xxx")
