
from models.models_in import Point as ModelPoint
from shapely.geometry import Point


def adapt_model_point_to_shapely(
    modelPoint: ModelPoint): return Point(modelPoint.x, modelPoint.y)
