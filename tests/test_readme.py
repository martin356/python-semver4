import unittest
from semver4 import Version4, SemVersion


class ReadmeTestCase(unittest.TestCase):

    def test_sample_usage(self):
        v = Version4('2.4.4.0-alpha+123')
        self.assertEqual('2.4.4-alpha+123', str(v))

        v = Version4(major=2, minor=4, patch=4, prerelease='beta', build='12346')
        self.assertEqual('2.4.4-beta+12346', str(v))
        self.assertEqual('4 0', f'{v.minor} {v.fix}')
        self.assertEqual('2.4.4', v.core)
        self.assertTrue(v > Version4('0.4.2.4'))

        v.inc_fix()
        self.assertEqual('2.4.4.1', str(v))
        self.assertEqual(1, v.fix)

        v.prerelease = 'rc'
        v.metadata = '987'
        self.assertEqual('2.4.4.1-rc+987', str(v))
        self.assertEqual('2.4.4.1', v.core)

        v.inc_minor().inc_major().inc_patch()
        self.assertEqual('3.0.1', str(v))

        v = SemVersion('1.2.3-alpha+007')
        self.assertEqual('1.2.3-alpha+007', str(v))
