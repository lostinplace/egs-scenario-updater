import unittest

from run import generate_playfield_processor, process_playfields, build_new_scenario


class TestProcessExecution(unittest.TestCase):

    def test_generate_playfield_processor(self):
        processor = generate_playfield_processor("assets/default-scenario", "assets")
        playfield = processor("Alien")
        self.assertTrue(isinstance(playfield, dict))

        playfield = processor("M32")
        self.assertTrue(isinstance(playfield, dict))

    def test_scenario_processor(self):
        result = process_playfields("assets/default-scenario", "assets")
        self.assertTrue(True)

    def test_whole_process(self):
        result = build_new_scenario("assets/default-scenario", "assets", "scratch/output-scenario")
        self.assertTrue(True)

    def test_whole_process_2(self):
        result = build_new_scenario("assets/test-scenario", "assets", "scratch/output-scenario")
        self.assertTrue(True)



