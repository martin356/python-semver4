import unittest
from semver4.errors import NotComparableError
from semver4 import SemVersion, Version4


class BaseVersionCompareTestCase(unittest.TestCase):

    def test_not_version_obj(self):
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') == 'bla')
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') != 'bla')
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') >= 'bla')
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') <= 'bla')
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') > 'bla')
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') < 'bla')

    def test_compare_prerelease(self):
        self.assertTrue(self.versioncls('1.2.3-beta') > self.versioncls('1.2.3-alpha'))
        self.assertTrue(self.versioncls('1.2.3-alpha.5') > self.versioncls('1.2.3-alpha.48'))
        self.assertTrue(self.versioncls('1.2.3-alpha.5') >= self.versioncls('1.2.3-alpha.5'))
        self.assertFalse(self.versioncls('1.2.3-beta') < self.versioncls('1.2.3-alpha'))
        self.assertFalse(self.versioncls('1.2.3-alpha.5') < self.versioncls('1.2.3-alpha.48'))
        self.assertFalse(self.versioncls('1.2.3-alpha.5') <= self.versioncls('1.2.3-alpha.48'))
        self.assertTrue(self.versioncls('1.2.3-alpha.5') == self.versioncls('1.2.3-alpha.5'))
        self.assertFalse(self.versioncls('1.2.3-alpha.5') != self.versioncls('1.2.3-alpha.5'))

    def test_dont_compare_buildmetadata(self):
        self.assertTrue(self.versioncls('1.2.3-alpha.5+1') == self.versioncls('1.2.3-alpha.5+9'))
        self.assertFalse(self.versioncls('1.2.3-alpha.5+1') != self.versioncls('1.2.3-alpha.5+9'))

    def test_comparable_to_string(self):
        self.assertEqual(self.versioncls('1.2.3'), '1.2.3')
        self.assertRaises(NotComparableError, lambda: self.versioncls('1.2.3') == 'bla.blu.bli')


class Version4ComparisonTestCase(BaseVersionCompareTestCase):

    versioncls = Version4

    def test_greater_than(self):
        self.assertTrue(Version4('1.2.3.4') > Version4('0.7.8.9'))
        self.assertTrue(Version4('1.2.3.4') > Version4('1.1.8.9'))
        self.assertTrue(Version4('1.2.3.4') > Version4('1.2.2.9'))
        self.assertTrue(Version4('1.2.3.4') > Version4('1.2.3.2'))
        self.assertTrue(Version4('1.2.3.4') > Version4('1.2.3'))

        self.assertFalse(Version4('0.7.8.9') > Version4('1.2.3.4'))
        self.assertFalse(Version4('1.1.8.9') > Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.2.9') > Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.3.2') > Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.3.4') > Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.3.4') > Version4('1.2.4'))

    def test_lower_than(self):
        self.assertTrue(Version4('0.7.8.9') < Version4('1.2.3.4'))
        self.assertTrue(Version4('1.1.8.9') < Version4('1.2.3.4'))
        self.assertTrue(Version4('1.2.2.9') < Version4('1.2.3.4'))
        self.assertTrue(Version4('1.2.3.2') < Version4('1.2.3.4'))
        self.assertTrue(Version4('1.2.3') < Version4('1.2.3.4'))

        self.assertFalse(Version4('1.2.3.4') < Version4('0.7.8.9'))
        self.assertFalse(Version4('1.2.3.4') < Version4('1.1.8.9'))
        self.assertFalse(Version4('1.2.3.4') < Version4('1.2.2.9'))
        self.assertFalse(Version4('1.2.3.4') < Version4('1.2.3.2'))
        self.assertFalse(Version4('1.2.3.4') < Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.3.4') < Version4('1.2.3'))

    def test_equal(self):
        self.assertTrue(Version4('1.2.3.4') == Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.3.4') == Version4('1.2.3.0'))
        self.assertFalse(Version4('1.2.3.4') == Version4('1.2.0.4'))
        self.assertFalse(Version4('1.2.3.4') == Version4('1.0.3.4'))
        self.assertFalse(Version4('1.2.3.4') == Version4('0.2.3.4'))
        self.assertTrue(Version4('1.2.3') == Version4('1.2.3.0'))
        self.assertTrue(Version4('1.2.3.2') <= Version4('1.2.3.4'))
        self.assertTrue(Version4('1.2.3.4') >= Version4('1.2.3.4'))
        self.assertFalse(Version4('1.2.3.4') <= Version4('1.2.3.2'))
        self.assertFalse(Version4('1.2.3.4') >= Version4('1.2.3.5'))
        self.assertTrue(Version4('1.2.3') >= Version4('1.2.3.0'))
        self.assertTrue(Version4('1.2.3') <= Version4('1.2.3.0'))

    def test_not_equal(self):
        self.assertTrue(Version4('1.2.3.4') != Version4('1.2.3.0'))
        self.assertTrue(Version4('1.2.3.4') != Version4('1.2.0.4'))
        self.assertTrue(Version4('1.2.3.4') != Version4('1.0.3.4'))
        self.assertTrue(Version4('1.2.3.4') != Version4('0.2.3.4'))
        self.assertFalse(Version4('1.2.3.4') != Version4('1.2.3.4'))


class SemVersionComparisonTestCase(BaseVersionCompareTestCase):

    versioncls = SemVersion

    def test_semversion_comparison(self):
        self.assertTrue(SemVersion('1.2.3') > SemVersion('0.7.8'))
        self.assertFalse(SemVersion('1.2.3') < SemVersion('0.7.8'))
        self.assertTrue(SemVersion('1.2.3') >= SemVersion('1.2.3'))

    def test_semversion_comparison(self):
        self.assertTrue(SemVersion('1.2.3') > Version4('0.7.8.9'))
        self.assertTrue(SemVersion('1.2.3-beta') == Version4('1.2.3.0-beta'))
