""" This file contains the graphql schema

:author: Daniel Seifert
:created: 16.09.2021
"""
import logging
from typing import Optional, Dict

from qlient.cache import Cache
from qlient.schema.models import Type, Directive
from qlient.schema.providers import SchemaProvider, detect_schema_provider
from qlient.settings import Settings
from qlient.transport import Transport


class Schema:
    """ Represents a graphql schema """

    logger = logging.getLogger("qlient")

    def __init__(
            self,
            location: Optional[str] = None,
            transport: Optional[Transport] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None,
            provider: Optional[SchemaProvider] = None,
    ):
        self.location: str = str(location)
        self.transport: Transport = transport or Transport()
        self.settings: Settings = settings or Settings()
        self.cache: Optional[Cache] = cache
        self.schema_provider: SchemaProvider = provider or detect_schema_provider(location, transport)

        self.schema: Optional[Dict] = None

        self.query_type: Optional[Type] = None
        self.mutation_type: Optional[Type] = None
        self.subscription_type: Optional[Type] = None
        self.types_registry: Optional[Dict[str, Type]] = None
        self.directives_registry: Optional[Dict[str, Directive]] = None

        self.introspect()  # prepare the schema for further usage

    def introspect(self):
        """ Load the schema definition """
        self.logger.debug("Schema introspection started")
        from qlient.schema.loader import load_schema
        self.schema: Dict = load_schema(self.schema_provider, self.location, self.cache)
        self.logger.debug("Schema loaded")

        from qlient.schema.parser import parse_schema, ParseResult
        parse_result: ParseResult = parse_schema(self.schema)
        self.logger.debug("Schema parsed")

        self.query_type = parse_result.query_type
        self.mutation_type = parse_result.mutation_type
        self.subscription_type = parse_result.subscription_type
        self.types_registry = parse_result.types
        self.directives_registry = parse_result.directives
        self.logger.debug("Schema successfully introspected")

    def __str__(self) -> str:
        """ Return a simple string representation of the schema instance """
        return repr(self)

    def __repr__(self) -> str:
        """ Return a more detailed string representation of the schema instance """
        class_name = self.__class__.__name__
        return f"<{class_name}(query_type={self.query_type}, mutation_type={self.mutation_type}, subscription_type={self.subscription_type})>"
