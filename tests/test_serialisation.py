import unittest
import json
import yaml
import semver4.yaml
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

    def test_yaml_encode(self):
        expected_data = self.get_data()
        expected_data['version'] = '0.4.2'
        expected = yaml.dump(expected_data)
        result = yaml.dump(self.get_data(), Dumper=self.yaml_dumper)
        self.assertEqual(result, expected)

    def test_yaml_decode(self):
        to_load = self.get_data()
        to_load['version'] = '0.4.2'
        to_load = yaml.dump(to_load)

        result = yaml.load(to_load, Loader=self.yaml_loader)
        expected = self.get_data()

        self.assertEqual(result, expected)


class Version4Serialisation(BaseVersionSerialisation):

    versioncls = Version4
    yaml_dumper = property(lambda _: semver4.yaml.get_version4_dumper())
    yaml_loader = property(lambda _: semver4.yaml.get_version4_loader())


class SemVersionSerialisation(BaseVersionSerialisation):

    versioncls = SemVersion
    yaml_dumper = property(lambda _: semver4.yaml.get_semversion_dumper())
    yaml_loader = property(lambda _: semver4.yaml.get_semversion_loader())

    def test_json_decode_classic_semver_only(self):
        json_to_load = self.get_data()
        json_to_load['version'] = '0.4.2'
        json_to_load['version4'] = '0.4.2.1'
        json_to_load = json.dumps(json_to_load)

        result = json.loads(json_to_load, object_hook=self.versioncls.json_decode_function)
        expected = self.get_data()
        expected['version4'] = '0.4.2.1'

        self.assertEqual(result, expected)
