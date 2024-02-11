import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

import unittest
import semver4.errors as errors
from semver4 import Version



class VersionInitTestCase(unittest.TestCase):
    
    def test_from_version_type(self):
        from_version = Version(major=4, minor=2, patch=0)
        new_version = Version(version=from_version)
        self.assertEqual(from_version.major, new_version.major)
        self.assertEqual(from_version.minor, new_version.minor)
        self.assertEqual(from_version.patch, new_version.patch)
        self.assertEqual(from_version.fix, new_version.fix)

    def test_from_int_or_str(self):
        version = Version(major=4, minor='2', patch='0')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 0)

    def test_set_fix_version(self):
        version = Version(major=4, minor='2', patch='0', fix=9)
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 9)

    def test_negative_int(self):
        self.assertRaises(
            errors.WrongVersionPart, 
            Version, major=4, minor=-1, patch=0
        )

    def test_non_alpha_string(self):
        self.assertRaises(
            errors.WrongVersionPart, 
            Version, major=4, minor='a', patch=0
        )


if __name__ == '__main__':
    suite = unittest.TestSuite(
        unittest.makeSuite(VersionInitTestCase)
    )
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
