import unittest
from semver4.errors import (
    InvalidVersionPartError,
    InvalidVersionError
)
from semver4 import Version


class VersionInitTestCase(unittest.TestCase):

    def test_from_version_type(self):
        from_version = Version(major=4, minor=2, patch=0)
        new_version = Version(version=from_version)
        self.assertEqual(from_version.major, new_version.major)
        self.assertEqual(from_version.minor, new_version.minor)
        self.assertEqual(from_version.patch, new_version.patch)
        self.assertEqual(from_version.fix, new_version.fix)

    def test_from_str_without_fix(self):
        version = Version(version='4.2.0')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 0)

    def test_from_str_with_fix(self):
        version = Version(version='4.2.0.9')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 9)

    def test_from_str_wrong_format(self):
        for invalid_v in ['1.2.a', '1.2.5.a', '1.2.3.5.6', '1.2', '1.02.3']:
            self.assertRaises(InvalidVersionError, Version, version=invalid_v)

    def test_from_str_wrong_type(self):
        self.assertRaises(InvalidVersionError, Version, version=99)

    def test_set_major_minor_patch(self):
        version = Version(major=4, minor='2', patch='0')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 0)

    def test_set_major_minor_patch_fix(self):
        version = Version(major=4, minor='2', patch='0', fix=9)
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 9)

    def test_version_part_negative_int(self):
        self.assertRaises(
            InvalidVersionError,
            Version, major=4, minor=-1, patch=0
        )

    def test_version_part_non_alpha_string(self):
        self.assertRaises(
            InvalidVersionError,
            Version, major=4, minor='a', patch=0
        )

    def test_iterator(self):
        version = Version(major=4, minor='2', patch='0')
        self.assertEqual({'major': 4, 'minor': 2, 'patch': 0, 'fix': 0}, dict(version))

    def test_get_item(self):
        version = Version('4.2.0')
        self.assertEqual(4, version['major'])
        self.assertEqual(2, version['minor'])
        self.assertEqual(0, version['patch'])
        self.assertEqual(0, version['fix'])
