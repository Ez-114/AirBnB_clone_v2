#!/usr/bin/env python3
"""DBStorage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv

from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """DBStorage"""

    __engine = None
    __session = None
    __classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    def __init__(self):
        """__init__"""

        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB
            )
        )

        if HBNB_ENV == "test":
            Base.metadata.dropall(self.__engine)

    def all(self, cls=None):
        """all method"""

        objs_dict = {}

        if cls and cls in self.__classes.keys():
            objects = self.__session.query(self.__classes[cls]).all()

            for obj in objects:
                obj_key = f'{obj.__class__.__name__}.{obj.id}'
                objs_dict[obj_key] = obj

        elif cls is None:

            for item in self.__classes.keys():
                objects = self.__session.query(self.__classes[item]).all()

                for obj in objects:
                    obj_key = f'{obj.__class__.__name__}.{obj.id}'
                    objs_dict[obj_key] = obj

        return objs_dict

    def new(self, obj):
        """add new obj"""

        self.__session.add(obj)

    def save(self):
        """save objs"""

        self.__session.commit()

    def delete(self, obj=None):
        """deletes a given object"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload"""

        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()
