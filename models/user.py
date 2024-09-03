#!/usr/bin/env python3
"""
models.User model class.
"""


from models.base_model import BaseModel


class User(BaseModel):
    """User model class."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes"""
        super().__init__(*args, **kwargs)
