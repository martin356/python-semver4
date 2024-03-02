import unittest
import json
from semver4 import Version4, SemVersion


class BaseVersionSerialisation(unittest.TestCase):

    @classmethod
    def get_data(cls):
        return {
            'version': cls.versioncls('0.4.2'),
            'string': 'memento homo...',
            'bool': True,
            'number': 98,
            'list': [0, 1, 2, 3]
        }

    def test_json_encode(self):
        expected_data = self.get_data()
        expected_data['version'] = '0.4.2'
        expected = json.dumps(expected_data)
        self.assertEqual(json.dumps(self.get_data(), default=self.versioncls.json_encode_function), expected)

    def test_json_decode(self):
        json_to_load = self.get_data()
        json_to_load['version'] = '0.4.2'
        json_to_load = json.dumps(json_to_load)

        result = json.loads(json_to_load, object_hook=self.versioncls.json_decode_function)
        expected = self.get_data()

        self.assertEqual(result, expected)


class Version4Serialisation(BaseVersionSerialisation):

    versioncls = Version4


class SemVersionSerialisation(BaseVersionSerialisation):

    versioncls = SemVersion
