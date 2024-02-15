import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

import unittest
from test_version_init import VersionInitTestCase
from test_version_comparison import VersionCompareTestCase
from test_version_validation import VersionValidationTestCase


if __name__ == '__main__':
    suite = unittest.TestSuite([
        unittest.makeSuite(VersionInitTestCase),
        unittest.makeSuite(VersionCompareTestCase),
        unittest.makeSuite(VersionValidationTestCase)
    ])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
