import unittest
from semver4.errors import (
    DecreaseVersionError
)
from semver4 import Version4, SemVersion


class UpdateVersionPartTestCase(unittest.TestCase):

    def setUp(self):
        self.version = Version4('1.2.3.4')

    def test_increase_major(self):
        v = self.version.inc_major()
        self.assertEqual(self.version.major, 2)
        self.assertIs(self.version, v)

    def test_increase_minor(self):
        v = self.version.inc_minor()
        self.assertEqual(self.version.minor, 3)
        self.assertIs(self.version, v)

    def test_increase_patch(self):
        v = self.version.inc_patch()
        self.assertEqual(self.version.patch, 4)
        self.assertIs(self.version, v)

    def test_increase_fix(self):
        v = self.version.inc_fix()
        self.assertEqual(self.version.fix, 5)
        self.assertIs(self.version, v)

    def test_decrease_major(self):
        v = self.version.dec_major()
        self.assertEqual(self.version.major, 0)
        self.assertIs(self.version, v)

    def test_decrease_minor(self):
        v = self.version.dec_minor()
        self.assertEqual(self.version.minor, 1)
        self.assertIs(self.version, v)

    def test_decrease_patch(self):
        v = self.version.dec_patch()
        self.assertEqual(self.version.patch, 2)
        self.assertIs(self.version, v)

    def test_decrease_fix(self):
        v = self.version.dec_fix()
        self.assertEqual(self.version.fix, 3)
        self.assertIs(self.version, v)

    def test_dec_zero(self):
        version = Version4('0.1.2')
        self.assertRaises(DecreaseVersionError, version.dec_major)
        self.assertRaises(DecreaseVersionError, version.dec_fix)

    def test_chaining(self):
        v = self.version.inc_major().inc_patch().dec_minor().inc_major().inc_fix()
        self.assertEqual(self.version.major, 3)
        self.assertEqual(self.version.minor, 1)
        self.assertEqual(self.version.patch, 4)
        self.assertEqual(self.version.fix, 5)
        self.assertIs(self.version, v)