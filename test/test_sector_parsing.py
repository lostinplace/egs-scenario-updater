import unittest

from utils.sector_processing import get_playfields_from_sector_file


class TestSectorParsing(unittest.TestCase):

    def test_basic(self):
        actual_g = get_playfields_from_sector_file("assets/Sectors.yaml")

        names, types = zip(*actual_g)
        self.assertTrue('Nex Orbit' in names)


if __name__ == '__main__':
    unittest.main()