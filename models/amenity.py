#!/usr/bin/env python3
"""
models.Amenity model class.
"""


from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model class."""

    name = ""

    def __init__(self, *args, **kwargs):
        """initializes"""
        super().__init__(*args, **kwargs)
