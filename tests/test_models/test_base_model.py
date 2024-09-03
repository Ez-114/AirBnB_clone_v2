#!/usr/bin/python3
"""
test_base_model.py

This module define tests that will help validate the BaseModel class
methods as it is intended to.

The module achives this by the help of the unittest module.
"""
from models.base_model import BaseModel
import unittest
import datetime
import json
import os


class test_basemodel(unittest.TestCase):
    """
    TestBaseModel class.

    This class contain all possible test cases that ensure
    the BaseModel class is working correctly.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes the test case and sets up attributes for the test,
        including self.name (the class name) and self.value (the class itself).
        """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """
        called before each test method is executed. Currently, it does nothing.
        """
        pass

    def tearDown(self):
        """
        called after each test method.

        It attempts to remove the file.json file,
        which is likely created during tests to ensure
        a clean state for subsequent tests.
        """
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """
        Tests that an instance of BaseModel can be created
        and that its type is correct.
        """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """
        Tests that a new BaseModel instance can be created
        from a dictionary representation of another instance
        and that the new instance is not the same object as the original.
        """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """
        Tests that passing a dictionary with an integer key to
        BaseModel raises a TypeError.
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """
        Tests that the save method correctly serializes the instance
        to a JSON file and that the file contains the correct data.
        """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """
        Tests the __str__ method of BaseModel,
        ensuring it returns the expected string representation.
        """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """
        Tests the to_dict method,
        ensuring it returns a correct dictionary representation
        of the instance.
        """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """
        Tests that passing a dictionary with None as a key
        raises a TypeError.
        """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """
        Tests that the id attribute of a new instance is a string.
        """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """
        Tests that the created_at attribute of a new instance
        is a datetime object.
        """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """
        Tests that the updated_at attribute is a datetime object
        and that when reloading an instance from its dictionary representation,
        created_at and updated_at are not the same.
        """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        new.save()
        self.assertFalse(new.created_at == new.updated_at)
