import unittest
from semver4.errors import (
    FixPartNotSupported,
    InvalidVersionPartError,
    InvalidVersionError
)
from semver4 import Version4, SemVersion, BaseVersion


class BaseInitTestCase(unittest.TestCase):

    def assert_for_version4(self, assertfnc):
        if self.versioncls is Version4:
            assertfnc()

    def test_from_version_type(self):
        from_version = self.versioncls(major=4, minor=2, patch=0)
        new_version = self.versioncls(version=from_version)
        self.assertEqual(from_version.major, new_version.major)
        self.assertEqual(from_version.minor, new_version.minor)
        self.assertEqual(from_version.patch, new_version.patch)
        self.assert_for_version4(lambda: self.assertEqual(from_version.fix, new_version.fix))

    def test_from_str_mandatory_parts(self):
        version = self.versioncls(version='4.2.0')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assert_for_version4(lambda: self.assertEqual(version.fix, 0))
        self.assertIsNone(version.prerelease)
        self.assertIsNone(version.build)

    def test_from_str_without_fix(self):
        version = self.versioncls(version='4.2.0-alpha.9+989898')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assert_for_version4(lambda: self.assertEqual(version.fix, 0))
        self.assertEqual(version.prerelease, 'alpha.9')
        self.assertEqual(version.build, '989898')

    def test_from_str_wrong_format(self):
        self.assertRaises(InvalidVersionError, self.versioncls, major=4, minor=-1, patch=0)
        self.assertRaises(InvalidVersionError, self.versioncls, major=4, minor='a', patch=0)
        for invalid_v in ['1.2.a', '1.2.5.a', '1.2.3.5.6', '1.2', '1.02.3']:
            self.assertRaises(InvalidVersionError, self.versioncls, version=invalid_v)

    def test_from_str_wrong_type(self):
        self.assertRaises(InvalidVersionError, self.versioncls, version=99)

    def test_get_item(self):
        version = self.versioncls('4.2.0-alpha+56')
        self.assertEqual(4, version['major'])
        self.assertEqual(2, version['minor'])
        self.assertEqual(0, version['patch'])
        self.assert_for_version4(lambda: self.assertEqual(0, version['fix']))
        self.assertEqual('alpha', version['prerelease'])
        self.assertEqual('56', version['build'])

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


class Version4InitTestCase(BaseInitTestCase):

    versioncls = Version4

    def test_from_str_with_fix(self):
        version = Version4(version='4.2.0.9-alpha-beta.9+989898')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 9)
        self.assertEqual(version.prerelease, 'alpha-beta.9')
        self.assertEqual(version.build, '989898')

    def test_from_keywords(self):
        version = Version4(major=4, minor='2', patch='0', fix=9, prerelease='alpha.5', build='989529')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertEqual(version.fix, 9)
        self.assertEqual(version.prerelease, 'alpha.5')
        self.assertEqual(version.build, '989529')

    def test_iterator(self):
        version = Version4(major=4, minor='2', patch='0', prerelease='alpha', build='123')
        self.assertEqual({'major': 4, 'minor': 2, 'patch': 0, 'fix': 0, 'prerelease': 'alpha', 'build': '123'}, dict(version))

    def test_repr(self):
        self.assertEqual('type Version4|2.3.6.9', Version4('2.3.6.9').__repr__())

    def test_to_string(self):
        self.assertEqual('1.2.3', Version4('1.2.3.0').version)
        versions = ['1.2.3', '1.2.3-pre', '1.2.3-pre+build', '1.2.3.4', '1.2.3.4-pre', '1.2.3.4-pre+build']
        for v in versions:
            self.assertEqual(v, Version4(v).version)
            self.assertEqual(v, str(Version4(v)))


class SemVersionInitTestCase(BaseInitTestCase):

    versioncls = SemVersion

    def test_from_str_wrong_semver20_format(self):
        self.assertRaises(InvalidVersionError, SemVersion, '1.2.3.4')

    def test_from_keywords(self):
        version = SemVersion(major=4, minor='2', patch='0', prerelease='alpha.5', build='989529')
        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 0)
        self.assertRaises(FixPartNotSupported, lambda: version.fix)
        self.assertEqual(version.prerelease, 'alpha.5')
        self.assertEqual(version.build, '989529')

    def test_iterator(self):
        version = SemVersion(major=4, minor='2', patch='0', prerelease='alpha', build='123')
        self.assertEqual({'major': 4, 'minor': 2, 'patch': 0, 'prerelease': 'alpha', 'build': '123'}, dict(version))

    def test_repr(self):
        self.assertEqual('type SemVersion|2.3.6', SemVersion('2.3.6').__repr__())

    def test_to_string(self):
        versions = ['1.2.3', '1.2.3-pre', '1.2.3-pre+build']
        for v in versions:
            self.assertEqual(v, SemVersion(v).version)
            self.assertEqual(v, str(SemVersion(v)))
