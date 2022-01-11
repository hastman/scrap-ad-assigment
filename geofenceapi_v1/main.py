from fastapi import FastAPI,  Response, status, HTTPException, Security
from fastapi.security import APIKeyHeader
from adapters.adapters import adapt_model_point_to_shapely, adapt_model_polygon_to_shapely

from models.models_in import Point, Polygon
from repository.folderRepository import FolderRepository
import os

X_API_KEY = APIKeyHeader(name="X-API-KEY", auto_error=True)


def is_authenticated(x_api_key: str = Security(X_API_KEY)):
    if (x_api_key != os.getenv("API_KEY")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No api key found in header")


app = FastAPI(openapi_prefix=os.getenv('ROOT_PATH_V1', ''))


@app.get("/health", status_code=status.HTTP_200_OK)
def healthcheck(response: Response):
    try:
        if not os.path.isfile(os.getenv("STORAGE_LOCATION")):
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    except:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {}


@app.post("/geofence/point", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Security(is_authenticated)])
def point_in_polygon(point: Point, response: Response):

    repository = FolderRepository()
    if not repository.find_point_in_fence(adapt_model_point_to_shapely(point)):
        response.status_code = status.HTTP_404_NOT_FOUND
    return {}


@app.put("/geofence", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Security(is_authenticated)])
def modify_geofence(polygon: Polygon, response: Response):
    if not polygon.is_valid():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "msg": "Invalid polygon, minimun three points"}
    adapted_polygon = adapt_model_polygon_to_shapely(polygon)
    if not adapted_polygon.is_valid:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "msg": "Invalid polygon, coordenates must be closed"}
    repository = FolderRepository()
    repository.update_fence(adapted_polygon)
    return {}
