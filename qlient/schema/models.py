""" This file contains the graphql schema class

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
import logging
from typing import Optional, Dict, List, Any

from qlient import __about__
from qlient.cache import Cache
from qlient.settings import Settings
from qlient.transport import Transport


class TypeRef:
    """ Represents a basic graphql Type Reference """

    def __init__(
            self,
            kind: Optional[str] = None,
            name: Optional[str] = None,
            of_type: Optional["TypeRef"] = None
    ):
        pass


class Input:
    """ Represents a basic graphql Input """

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            type: Optional[TypeRef] = None,
            default_value: Optional[Any] = None
    ):
        pass


class Directive:
    """ Represents a basic graphql Directive """

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            locations: Optional[List[str]] = None,
            args: Optional[List[Input]] = None
    ):
        pass


class Field:
    """ Represents a basic graphql Field """

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            args: Optional[List[Input]] = None,
            type: Optional[TypeRef] = None,
            is_deprecated: Optional[bool] = None,
            deprecation_reason: Optional[str] = None
    ):
        pass


class EnumValue:
    """ Represents a basic graphql enum value """

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            is_deprecated: Optional[bool] = None,
            deprecation_reason: Optional[str] = None
    ):
        pass


class Type:
    """ Represents a basic graphql Type """

    def __init__(
            self,
            kind: Optional[str] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            fields: Optional[List[Field]] = None,
            input_fields: Optional[List[Input]] = None,
            interfaces: Optional[List[TypeRef]] = None,
            enum_values: Optional[List[EnumValue]] = None,
            possible_types: Optional[List[TypeRef]] = None
    ):
        pass


class Schema:
    """ Represents a graphql schema """

    logger = logging.getLogger(__about__.__title__)

    def __init__(self, location: str, transport: Transport, settings: Settings, cache: Optional[Cache]):
        self.location: str = location
        self.transport: Transport = transport
        self.settings: Settings = settings
        self.cache: Optional[Cache] = cache

        self.schema: Optional[Dict] = None

        self.query_type: Optional[Type] = None
        self.mutation_type: Optional[Type] = None
        self.subscription_type: Optional[Type] = None
        self.types: Optional[List[Type]] = None
        self.directives: Optional[List[Directive]] = None

        self.introspect()  # prepare the schema for further usage

    def introspect(self):
        """ Load the schema definition """
        self.logger.debug("Schema introspection started")
        from qlient.schema.loader import load_schema
        self.schema: Dict = load_schema(self.location, self.transport, self.cache)
        self.logger.debug("Schema loaded")

        from qlient.schema.parser import parse_schema, ParseResult
        parse_result: ParseResult = parse_schema(self.schema)
        self.logger.debug("Schema parsed")

        self.query_type = parse_result.query_type
        self.mutation_type = parse_result.mutation_type
        self.subscription_type = parse_result.subscription_type
        self.types = parse_result.types
        self.directives = parse_result.directives
        self.logger.debug("Schema successfully introspected")
