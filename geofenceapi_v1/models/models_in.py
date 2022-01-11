

from typing import List

from pydantic.main import BaseModel


class Point(BaseModel):
    x: float
    y: float


class Polygon(BaseModel):
    points: List[Point]

    def is_valid(self):
        return len(self.points) >= 3
