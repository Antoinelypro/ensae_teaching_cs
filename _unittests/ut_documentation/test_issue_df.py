"""
@brief      test log(time=93s)
"""

import sys
import os
import unittest
import pandas
from pyquickhelper.loghelper.flog import fLOG


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src


class TestIssueDf(unittest.TestCase):

    def test_notebook_cov(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        fold = os.path.dirname(__file__)
        name = "notebook.ensae_teaching_cs.txt"
        dff = os.path.join(fold, name)
        if os.path.exists(dff):
            df = pandas.read_csv(dff, sep="\t", encoding="utf-8")
            self.assertTrue(df.shape[0] > 0)


if __name__ == "__main__":
    unittest.main()
