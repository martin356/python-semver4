from semver4.errors import (
    DecreaseVersionError
)
from basetestcase import BaseTestCase
from semver4.errors import InvalidVersionPartError
from semver4 import Version4, SemVersion


class BaseUpdateVersionPartTestCase(BaseTestCase):

    def test_increase_major(self):
        v = self.version.inc_major()
        self.assertEqual(self.version.major, 2)
        self.assertEqual('2.0.0', str(v))
        self.assertIs(self.version, v)

    def test_increase_minor(self):
        v = self.version.inc_minor()
        self.assertEqual(self.version.minor, 3)
        self.assertEqual('1.3.0', str(v))
        self.assertIs(self.version, v)

    def test_increase_patch(self):
        v = self.version.inc_patch()
        self.assertEqual(self.version.patch, 4)
        self.assertEqual('1.2.4', str(v))
        self.assertIs(self.version, v)

    def test_decrease_major(self):
        v = self.version.dec_major()
        self.assertEqual(self.version.major, 0)
        self.assertEqual('0.0.0', str(v))
        self.assertIs(self.version, v)

    def test_decrease_minor(self):
        v = self.version.dec_minor()
        self.assertEqual(self.version.minor, 1)
        self.assertEqual('1.1.0', str(v))
        self.assertIs(self.version, v)

    def test_decrease_patch(self):
        v = self.version.dec_patch()
        self.assertEqual(self.version.patch, 2)
        self.assertEqual('1.2.2', str(v))
        self.assertIs(self.version, v)

    def test_set_prerelease(self):
        version = self.versioncls('4.2.0-alpha+56')
        version.prerelease = 'beta'
        self.assertEqual('beta', version.prerelease)
        version['prerelease'] = 'gama'
        self.assertEqual('gama', version.prerelease)

    def test_set_buildmetadata(self):
        version = self.versioncls('4.2.0-alpha+56')
        version.metadata = '123'
        self.assertEqual('123', version.metadata)
        self.assertEqual('123', version.build)
        version.build = '456'
        self.assertEqual('456', version.metadata)
        self.assertEqual('456', version.build)
        version['metadata'] = '789'
        self.assertEqual('789', version.metadata)
        self.assertEqual('789', version.build)
        version['build'] = '1011'
        self.assertEqual('1011', version.metadata)
        self.assertEqual('1011', version.build)

    def test_set_buildmetadata_invalid_value(self):
        version = self.versioncls('4.2.0-alpha+56')
        for invalid_char in '\/*_()[]{}"?!\'+':
            with self.assertRaises(InvalidVersionPartError):
                version.build = f'5{invalid_char}99'
            with self.assertRaises(InvalidVersionPartError):
                version.metadata = f'5{invalid_char}99'

    def test_set_prerelease_invalid_value(self):
        version = self.versioncls('4.2.0-alpha+56')
        for invalid_char in '\/*_()[]{}"?!\'+':
            with self.assertRaises(InvalidVersionPartError):
                version.prerelease = f'5{invalid_char}99'


class UpdateVersion4PartTestCase(BaseUpdateVersionPartTestCase):

    versioncls = Version4

    def setUp(self):
        self.version = Version4('1.2.3.4')

    def test_chaining(self):
        v = self.version.inc_major().inc_patch().dec_patch().inc_major().inc_fix()
        self.assertEqual('3.0.0.1', str(v))
        self.assertIs(self.version, v)

    def test_dec_zero(self):
        version = self.versioncls('0.1.2')
        self.assertRaises(DecreaseVersionError, version.dec_major)
        self.assertRaises(DecreaseVersionError, version.dec_fix)

    def test_decrease_fix(self):
        v = self.version.dec_fix()
        self.assertEqual(self.version.fix, 3)
        self.assertEqual('1.2.3.3', str(v))
        self.assertIs(self.version, v)

    def test_increase_fix(self):
        v = self.version.inc_fix()
        self.assertEqual(self.version.fix, 5)
        self.assertEqual('1.2.3.5', str(v))
        self.assertIs(self.version, v)


class UpdateSemVersionPartTestCase(BaseUpdateVersionPartTestCase):

    versioncls = SemVersion

    def setUp(self):
        self.version = SemVersion('1.2.3')

    def test_chaining(self):
        v = self.version.dec_minor().inc_major().inc_patch().inc_minor().inc_patch()
        self.assertEqual('2.1.1', str(v))
        self.assertIs(self.version, v)

    def test_dec_zero(self):
        version = self.versioncls('0.1.2')
        self.assertRaises(DecreaseVersionError, version.dec_major)
