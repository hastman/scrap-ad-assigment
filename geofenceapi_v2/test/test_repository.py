import unittest
from unittest import mock

from shapely.geometry import Point
from repositoy.folderRepository import FolderRepository
import os


class RepositoryTest(unittest.TestCase):

    os_mock = None
    repositorySUT: FolderRepository = None

    def setUp(self):
        self.os_mock = mock.patch.dict(
            os.environ, {"STORAGE_LOCATION": './test/fixture/mock_fence.json'})
        self.os_mock.start()
        self.repositorySUT = FolderRepository()
        self.repositorySUT.__refresh__()

    def tearDown(self):
        self.os_mock.stop()

    def test_when_instanciate_repository_one_time_should_return_the_instance_with_the_data(self):

        self.assertIsNotNone(self.repositorySUT._data)

    def test_when_instanciate_repository_twice_should_return_the_same_instance(self):
        repository2 = FolderRepository()
        self.assertEqual(self.repositorySUT, repository2)

    def test_when_check_point_and_not_belongs_to_base_polygon_should_return_false(self):
        point_outside = Point(0, 0)
        distance = self.repositorySUT.find_point_in_fence(point_outside)
        self.assertEqual(distance, -1)

    def test_when_check_point_and_belongs_to_base_polygon_should_return_true(self):
        point_inside = Point(68.2473, 4.1272)
        distance = self.repositorySUT.find_point_in_fence(point_inside)
        self.assertGreater(distance, -1)
