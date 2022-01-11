

import os
import json
from shapely.geometry.base import BaseMultipartGeometry
from shapely.geometry import shape, Point

import threading

from shapely.geometry.geo import mapping

lock = threading.Lock()

"""
Base Singleton Thread Safe implementation
"""


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FolderRepository(metaclass=Singleton):
    _data: BaseMultipartGeometry = None

    def __load__(self):
        with open(os.getenv('STORAGE_LOCATION')) as geofile:
            ori_json = json.load(geofile)
            self._data = shape(ori_json.get("geometry"))

    def __init__(self):
        self.__load__()

    def __refresh__(self):
        self.__load__()

    def find_point_in_fence(self, point: Point):
        if self._data.contains(point):
            return self._data.exterior.distance(point)
        return -1
