import unittest

import yaml

from lib.rule_based_dft import execute
from utils.capitalize_struct_boolean import generate_struct_capitalization_rule
from utils.playfield_manager import get_playfield
from utils.remove_pentaxid import generate_crystal_removal_rule


class TestPlayfieldManipulation(unittest.TestCase):

    def test_basic(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        self.assertTrue(isinstance(playfield, dict))

    def test_basic(self):
        playfield = get_playfield("a/garbage/path/playfield.yaml")
        self.assertIs(playfield, None)

    def test_pentaxid_removal(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        from utils.remove_pentaxid import remove_pentaxid
        actual = remove_pentaxid(playfield)
        result1 = yaml.dump(actual).__contains__("Pentaxid")
        result2 = yaml.dump(actual).__contains__("crystal")

        self.assertFalse(result1 and result2)


    def test_resource_nerfing(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        from utils.nerf_resources import nerf_resources
        old_count = playfield['RandomResources'][0].get('CountMinMax')
        self.assertEqual(old_count, [4, 7])
        old_size = playfield['RandomResources'][0].get('SizeMinMax')
        self.assertEqual(old_size, [8, 14])

        actual = nerf_resources(playfield)
        new_count = actual['RandomResources'][0].get('CountMinMax')
        self.assertEqual(new_count, [10, 18])
        new_size = actual['RandomResources'][0].get('SizeMinMax')
        self.assertEqual(new_size, [3, 5])

    def test_rulebased_crystal_removal(self):
        rule = generate_crystal_removal_rule()
        rule_dict = {"remove crystals": rule}

        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")

        actual = execute(rule_dict, playfield)

        dump = yaml.dump(actual)

        result1 = "Pentaxid" in dump
        result2 = "crystal" not in dump

        self.assertTrue(result1 and result2)

    def test_struct_bool_capitalization(self):
        rule = generate_struct_capitalization_rule()
        rule_dict = {"capitalize struct values": rule}

        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")

        actual = execute(rule_dict, playfield)

        dump = yaml.dump(actual)

        result1 = "Struct: 'True'" in dump
        result2 = "Struct: true" not in dump

        self.assertTrue(result1 and result2)


if __name__ == '__main__':
    unittest.main()