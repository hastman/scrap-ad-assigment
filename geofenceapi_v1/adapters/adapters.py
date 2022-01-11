
from models.models_in import Point as ModelPoint, Polygon as ModelPolygon
from shapely.geometry import Point, Polygon


def adapt_model_point_to_shapely(
    modelPoint: ModelPoint): return Point(modelPoint.x, modelPoint.y)


def adapt_model_polygon_to_shapely(modelPolygon: ModelPolygon):

    list_points = [
        adapt_model_point_to_shapely(point) for point in modelPolygon.points]
    return Polygon(list_points)
