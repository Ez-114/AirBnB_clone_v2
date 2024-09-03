#!/usr/bin/env python3
"""
models.State model class.
"""


from models.base_model import BaseModel


class State(BaseModel):
    """State model class."""

    name = ""

    def __init__(self, *args, **kwargs):
        """initializes"""
        super().__init__(*args, **kwargs)
