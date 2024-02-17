import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

import unittest
from test_version_init import Version4InitTestCase
from test_version_comparison import BaseVersionCompareTestCase
from test_version_validation import Version4ValidationTestCase


if __name__ == '__main__':
    suite = unittest.TestSuite([
        unittest.makeSuite(Version4InitTestCase),
        unittest.makeSuite(BaseVersionCompareTestCase),
        unittest.makeSuite(Version4ValidationTestCase)
    ])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
