#!/usr/bin/env python3
"""
models.City model class.
"""


from models.base_model import BaseModel


class City(BaseModel):
    """City model class."""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """initializes"""
        super().__init__(*args, **kwargs)
