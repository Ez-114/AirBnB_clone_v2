#!/usr/bin/env python3
"""
models.State model class.
"""


from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel):
    """State model class."""

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        """initializes"""
        super().__init__(*args, **kwargs)
