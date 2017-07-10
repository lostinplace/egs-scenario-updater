import unittest

import yaml
from playfield_manager import get_playfield


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

    def test_generic_child_remover(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        from lib.child_remover import remove_children
        actual = remove_children(playfield, lambda x: isinstance(x, dict) and x.get('Name') == 'PentaxidResource')
        result = yaml.dump(actual).__contains__("Pentaxid")
        self.assertFalse(result)

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


if __name__ == '__main__':
    unittest.main()