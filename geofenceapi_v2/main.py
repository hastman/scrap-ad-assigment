import re
from fastapi import FastAPI,  status, HTTPException, Security, Response
from fastapi.security import APIKeyHeader
from models.models_in import Point
from repositoy.folderRepository import FolderRepository
from adapters.adapters import adapt_model_point_to_shapely
import os

X_API_KEY = APIKeyHeader(name="X-API-KEY", auto_error=True)


def is_authenticated(x_api_key: str = Security(X_API_KEY)):
    if (x_api_key != os.getenv("API_KEY")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No api key found in header")


app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
def healthcheck(response: Response):
    try:
        if not os.path.isfile(os.getenv("STORAGE_LOCATION")):
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    except:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {}


@app.post("/geofence/in_fence/{x}/{y}", status_code=status.HTTP_200_OK, dependencies=[Security(is_authenticated)])
def point_in_polygon(x: float, y: float, response: Response):
    repository = FolderRepository()
    distance = repository.find_point_in_fence(
        adapt_model_point_to_shapely(Point(x=x, y=y)))
    if distance == -1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}

    return {"threshold": distance}
