import unittest
from semver4.errors import NotComparableError
from semver4 import BaseVersion, SemVersion, Version4


class BaseVersionCompareTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        BaseVersion._valid_version_regex = '^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<fix>0|[1-9]\d*))?(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'

    def test_greater_than(self):
        self.assertTrue(BaseVersion('1.2.3.4') > BaseVersion('0.7.8.9'))
        self.assertTrue(BaseVersion('1.2.3.4') > BaseVersion('1.1.8.9'))
        self.assertTrue(BaseVersion('1.2.3.4') > BaseVersion('1.2.2.9'))
        self.assertTrue(BaseVersion('1.2.3.4') > BaseVersion('1.2.3.2'))
        self.assertTrue(BaseVersion('1.2.3.4') > BaseVersion('1.2.3'))

        self.assertFalse(BaseVersion('0.7.8.9') > BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.1.8.9') > BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.2.9') > BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.2') > BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') > BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') > BaseVersion('1.2.4'))

    def test_lower_than(self):
        self.assertTrue(BaseVersion('0.7.8.9') < BaseVersion('1.2.3.4'))
        self.assertTrue(BaseVersion('1.1.8.9') < BaseVersion('1.2.3.4'))
        self.assertTrue(BaseVersion('1.2.2.9') < BaseVersion('1.2.3.4'))
        self.assertTrue(BaseVersion('1.2.3.2') < BaseVersion('1.2.3.4'))
        self.assertTrue(BaseVersion('1.2.3') < BaseVersion('1.2.3.4'))

        self.assertFalse(BaseVersion('1.2.3.4') < BaseVersion('0.7.8.9'))
        self.assertFalse(BaseVersion('1.2.3.4') < BaseVersion('1.1.8.9'))
        self.assertFalse(BaseVersion('1.2.3.4') < BaseVersion('1.2.2.9'))
        self.assertFalse(BaseVersion('1.2.3.4') < BaseVersion('1.2.3.2'))
        self.assertFalse(BaseVersion('1.2.3.4') < BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') < BaseVersion('1.2.3'))

    def test_equal(self):
        self.assertTrue(BaseVersion('1.2.3.4') == BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') == BaseVersion('1.2.3.0'))
        self.assertFalse(BaseVersion('1.2.3.4') == BaseVersion('1.2.0.4'))
        self.assertFalse(BaseVersion('1.2.3.4') == BaseVersion('1.0.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') == BaseVersion('0.2.3.4'))
        self.assertTrue(BaseVersion('1.2.3') == BaseVersion('1.2.3.0'))
        self.assertTrue(BaseVersion('1.2.3.2') <= BaseVersion('1.2.3.4'))
        self.assertTrue(BaseVersion('1.2.3.4') >= BaseVersion('1.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') <= BaseVersion('1.2.3.2'))
        self.assertFalse(BaseVersion('1.2.3.4') >= BaseVersion('1.2.3.5'))
        self.assertTrue(BaseVersion('1.2.3') >= BaseVersion('1.2.3.0'))
        self.assertTrue(BaseVersion('1.2.3') <= BaseVersion('1.2.3.0'))

    def test_not_equal(self):
        self.assertTrue(BaseVersion('1.2.3.4') != BaseVersion('1.2.3.0'))
        self.assertTrue(BaseVersion('1.2.3.4') != BaseVersion('1.2.0.4'))
        self.assertTrue(BaseVersion('1.2.3.4') != BaseVersion('1.0.3.4'))
        self.assertTrue(BaseVersion('1.2.3.4') != BaseVersion('0.2.3.4'))
        self.assertFalse(BaseVersion('1.2.3.4') != BaseVersion('1.2.3.4'))

    def test_not_version_obj(self):
        self.assertRaises(NotComparableError, lambda: BaseVersion('1.2.3') == 'bla')
        self.assertRaises(NotComparableError, lambda: BaseVersion('1.2.3') != 'bla')
        self.assertRaises(NotComparableError, lambda: BaseVersion('1.2.3') >= 'bla')
        self.assertRaises(NotComparableError, lambda: BaseVersion('1.2.3') <= 'bla')
        self.assertRaises(NotComparableError, lambda: BaseVersion('1.2.3') > 'bla')
        self.assertRaises(NotComparableError, lambda: BaseVersion('1.2.3') < 'bla')


class SemVersionComparisonTestCase(unittest.TestCase):

    def test_semversion_comparison(self):
        self.assertTrue(SemVersion('1.2.3') > SemVersion('0.7.8'))
        self.assertFalse(SemVersion('1.2.3') < SemVersion('0.7.8'))
        self.assertTrue(SemVersion('1.2.3') >= SemVersion('1.2.3'))

    def test_semversion_comparison(self):
        self.assertTrue(SemVersion('1.2.3') > Version4('0.7.8.9'))
        self.assertTrue(SemVersion('1.2.3-beta') == Version4('1.2.3.0-beta'))
