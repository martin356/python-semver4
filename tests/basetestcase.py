import unittest
from semver4 import Version4


class BaseTestCase(unittest.TestCase):

    def assert_for_version4(self, assertfnc):
        if self.versioncls is Version4:
            assertfnc()
