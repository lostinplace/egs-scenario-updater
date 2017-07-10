import unittest

from playfield_manager import get_playfield

from utils.mission_builder import extract_poi_names, generate_conquer_task, get_pois, construct_playfield_chapter


class TestMissionBuilding(unittest.TestCase):

    def test_basic(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        self.assertTrue(True)

    def test_get_poi_names(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        pois = get_pois(playfield)
        actual = extract_poi_names(pois)

        self.assertEqual(('DroneBaseNingues', 'Drone Base Ningues '), actual[0])

    def test_task_builder(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")
        pois = get_pois(playfield)
        actual = extract_poi_names(pois)
        poi = actual[0]
        actual = generate_conquer_task(poi)

        self.assertEqual(1, 1)

    def test_chapter_builder(self):
        playfield = get_playfield("assets/Playfields/Mato/playfield.yaml")

        chapter, messagedict = construct_playfield_chapter("testing", playfield)

        self.assertEqual(chapter["ChapterTitle"], "chaptertesting")
        self.assertEqual(len(chapter["Tasks"]), 5)






if __name__ == '__main__':
    unittest.main()