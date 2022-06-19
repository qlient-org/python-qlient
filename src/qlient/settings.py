"""This file contains the settings that can be overwritten in the qlient Client"""
import json


class Settings:
    """Class that represents the settings that can be adjusted to your liking"""

    def __init__(
        self,
        introspect: bool = True,
        validate_variables: bool = True,
        validate_fields: bool = True,
        json_loads=json.loads,
        json_dumps=json.dumps,
    ):
        self.introspect: bool = introspect
        self.validate_variables: bool = validate_variables
        self.validate_fields: bool = validate_fields
        self.json_loads = json_loads
        self.json_dumps = json_dumps

    def __str__(self) -> str:
        """Return a simple string representation of the settings"""
        return repr(self)

    def __repr__(self) -> str:
        """Return a detailed string representation of the settings"""
        class_name = self.__class__.__name__
        return f"{class_name}()"
