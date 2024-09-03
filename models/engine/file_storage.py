#!/usr/bin/env python3
"""
models.engine.file_storage.py Module.

This module implements the FileStorage class that helps in storing
a persistent JSON file containing all data about the pre-defined objects
from their classes.
"""

import os
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class FileStorage:
    """
    FileStorage class.

    Serializes instances to a JSON file and
    deserializes JSON file to instances.

    Attributes:
        - __file_path (str): Path to the JSON file (ex: file.json)
        - __objects (dict): Stores all created objects by <class name>.id

    Methods:
        - all(): Returns the dictionary __objects
        - new(obj): Sets in __objects the obj with key <obj class name>.id
        - save(): Serializes __objects to the JSON file (path: __file_path)
        - reload(): Deserializes the JSON file to __objects
                (only if the JSON file (__file_path) exists;
                        otherwise, do nothing.)
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        FileStorage.new() Instance method.

        Sets in __objects the obj with key <obj class name>.id
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        FileStorage.save() Instance method.

        Serializes __objects to the JSON file (path: __file_path)
        """
        json_objects = FileStorage.__objects.copy()
        for obj_id, obj in json_objects.items():
            json_objects[obj_id] = obj.to_dict()

        # Open the file that will save our objects data
        with open(FileStorage.__file_path, mode='w', encoding='utf-8') \
                as storage_file:

            json.dump(json_objects, storage_file)

    def reload(self):
        """
        FileStorage.reload() Instance method.

        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists ; otherwise, do nothing.)
        """
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, mode='r', encoding='utf-8') \
                    as storage_file:

                loaded_objs = json.load(storage_file)

            # Now fill in the __objects dict with loaded objects
            for obj_id, obj_data in loaded_objs.items():
                FileStorage.__objects.update({
                        obj_id: classes[obj_data['__class__']](**obj_data)
                    })

    def delete(self, obj=None):
        """delete obj from __objects if it's inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
