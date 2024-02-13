import unittest
from semver4.errors import NotComparableError
from semver4 import Version


class VersionCompareTestCase(unittest.TestCase):

    def test_greater_than(self):
        self.assertTrue(Version('1.2.3.4') > Version('0.7.8.9'))
        self.assertTrue(Version('1.2.3.4') > Version('1.1.8.9'))
        self.assertTrue(Version('1.2.3.4') > Version('1.2.2.9'))
        self.assertTrue(Version('1.2.3.4') > Version('1.2.3.2'))

        self.assertFalse(Version('0.7.8.9') > Version('1.2.3.4'))
        self.assertFalse(Version('1.1.8.9') > Version('1.2.3.4'))
        self.assertFalse(Version('1.2.2.9') > Version('1.2.3.4'))
        self.assertFalse(Version('1.2.3.2') > Version('1.2.3.4'))
        self.assertFalse(Version('1.2.3.4') > Version('1.2.3.4'))

    def test_lower_than(self):
        self.assertTrue(Version('0.7.8.9') < Version('1.2.3.4'))
        self.assertTrue(Version('1.1.8.9') < Version('1.2.3.4'))
        self.assertTrue(Version('1.2.2.9') < Version('1.2.3.4'))
        self.assertTrue(Version('1.2.3.2') < Version('1.2.3.4'))

        self.assertFalse(Version('1.2.3.4') < Version('0.7.8.9'))
        self.assertFalse(Version('1.2.3.4') < Version('1.1.8.9'))
        self.assertFalse(Version('1.2.3.4') < Version('1.2.2.9'))
        self.assertFalse(Version('1.2.3.4') < Version('1.2.3.2'))
        self.assertFalse(Version('1.2.3.4') < Version('1.2.3.4'))

    def test_equal(self):
        self.assertTrue(Version('1.2.3.4') == Version('1.2.3.4'))
        self.assertFalse(Version('1.2.3.4') == Version('1.2.3.0'))
        self.assertFalse(Version('1.2.3.4') == Version('1.2.0.4'))
        self.assertFalse(Version('1.2.3.4') == Version('1.0.3.4'))
        self.assertFalse(Version('1.2.3.4') == Version('0.2.3.4'))
        self.assertTrue(Version('1.2.3.2') <= Version('1.2.3.4'))
        self.assertTrue(Version('1.2.3.4') >= Version('1.2.3.4'))
        self.assertFalse(Version('1.2.3.4') <= Version('1.2.3.2'))
        self.assertFalse(Version('1.2.3.4') >= Version('1.2.3.5'))

    def test_not_equal(self):
        self.assertTrue(Version('1.2.3.4') != Version('1.2.3.0'))
        self.assertTrue(Version('1.2.3.4') != Version('1.2.0.4'))
        self.assertTrue(Version('1.2.3.4') != Version('1.0.3.4'))
        self.assertTrue(Version('1.2.3.4') != Version('0.2.3.4'))
        self.assertFalse(Version('1.2.3.4') != Version('1.2.3.4'))

    def test_not_version_obj(self):
        self.assertRaises(NotComparableError, lambda: Version('1.2.3') == 'bla')
        self.assertRaises(NotComparableError, lambda: Version('1.2.3') != 'bla')
        self.assertRaises(NotComparableError, lambda: Version('1.2.3') >= 'bla')
        self.assertRaises(NotComparableError, lambda: Version('1.2.3') <= 'bla')
        self.assertRaises(NotComparableError, lambda: Version('1.2.3') > 'bla')
        self.assertRaises(NotComparableError, lambda: Version('1.2.3') < 'bla')