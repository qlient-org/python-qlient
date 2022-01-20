""" This file contains the settings that can be overwritten in the qlient Client

:author: Daniel Seifert
:created: 09.09.2021
"""


class Settings:
    """ Class that represents the settings that can be adjusted to your liking """

    def __init__(
            self,
            validate_url: bool = True,
            validate_variables: bool = True,
            validate_fields: bool = True
    ):
        self.validate_url: bool = validate_url
        self.validate_variables: bool = validate_variables
        self.validate_fields: bool = validate_fields

    def __str__(self) -> str:
        """ Return a simple string representation of the settings """
        return repr(self)

    def __repr__(self) -> str:
        """ Return a detailed string representation of the settings """
        class_name = self.__class__.__name__
        return f"{class_name}()"
