import unittest
from semver4.errors import (
    InvalidVersionError
)
from semver4 import Version4,SemVersion


class Version4ValidationTestCase(unittest.TestCase):

    def test_valid_versions(self):
        valid_versions = [
            '1.2.4', '1.2.3-bla', '1.2.3-bla.9',
            '1.2.3-bla.9-bli.5', '1.2.3+b89',
            '1.2.3-bla.9+b6', '1.2.3.6', '1.2.3.6-bla',
            '1.2.3.6-bla.9', '1.2.3.6-bla.9-bli.5',
            '1.2.3.6-bla.9+b6', '1.2.3.6+b89'
        ]
        for version in valid_versions:
            self.assertTrue(Version4.validate(version))

    def test_invalid_versions(self):
        invalid_versions = [
            '1.2.03', '1.02.4', '01.2.4', '1.2.3-', '1.2.3-bla.9+',
            '1.2.3+', '1.2.3.4.5', '1.2.3.04', '1.2.3.', '1.2.3.4-',
            '1.2.3.4+', '1.2.3.4-bla+'
        ]
        for version in invalid_versions:
            self.assertFalse(Version4.validate(version))
            self.assertRaises(InvalidVersionError, Version4.validate, version, raise_err=True)


class StandardVersionValidationTestCase(unittest.TestCase):

    def test_valid_versions(self):
        valid_versions = [
            '1.2.4', '1.2.3-bla', '1.2.3-bla.9',
            '1.2.3-bla.9-bli.5', '1.2.3+b89', '1.2.3-bla.9+b6'
        ]
        for version in valid_versions:
            self.assertTrue(SemVersion.validate(version))

    def test_invalid_versions(self):
        invalid_versions = [
            '1.2.03', '1.02.4', '01.2.4', '1.2.3-', '1.2.3-bla.9+',
            '1.2.3+', '1.2.3.4.5', '1.2.3.04', '1.2.3.', '1.2.3.4-',
            '1.2.3.4+', '1.2.3.4-bla+', '1.2.3.6', '1.2.3.6-bla',
            '1.2.3.6-bla.9', '1.2.3.6-bla.9-bli.5', '1.2.3.6-bla.9+b6', '1.2.3.6+b89'
        ]
        for version in invalid_versions:
            self.assertFalse(SemVersion.validate(version))
            self.assertRaises(InvalidVersionError, SemVersion.validate, version, raise_err=True)
