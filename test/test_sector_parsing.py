import unittest

from utils.sector_processing import parse_sectors


class TestSectorParsing(unittest.TestCase):

    def test_basic(self):
        actual_g = parse_sectors("assets/Sectors.yaml")

        names, types = zip(*actual_g)
        self.assertTrue('Nex Orbit' in names)


if __name__ == '__main__':
    unittest.main()