

import unittest

from shapely.geometry import Point, Polygon
from models.models_in import Point as ModelPoint, Polygon as ModelPolygon
from adapters.adapters import adapt_model_point_to_shapely, adapt_model_polygon_to_shapely


class AdapterTest(unittest.TestCase):

    def test_when_adapt_model_point_should_return_shapely_point(self):

        expected_point = adapt_model_point_to_shapely(ModelPoint(x=1.0, y=0.0))
        self.assertIsInstance(expected_point, Point)
        self.assertEqual(expected_point.x, 1.0)
        self.assertEqual(expected_point.y, 0.0)

    def test_when_adapt_model_polygon_should_return_shapely_poin(self):
        list_points = [ModelPoint(x=0, y=0), ModelPoint(x=1, y=0), ModelPoint(
            x=0, y=1), ModelPoint(x=1, y=1), ModelPoint(x=0, y=0)]
        expected_polygon = adapt_model_polygon_to_shapely(
            ModelPolygon(points=list_points))
        self.assertIsInstance(expected_polygon, Polygon)
