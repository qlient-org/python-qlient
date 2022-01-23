""" This file contains the graphql schema

:author: Daniel Seifert
:created: 16.09.2021
"""
import logging
from typing import Optional, Dict

from qlient.cache import Cache
from qlient.schema.models import Type, Directive
from qlient.schema.providers import SchemaProvider
from qlient.settings import Settings


class Schema:
    """ Represents a graphql schema """

    logger = logging.getLogger("qlient")

    def __init__(
            self,
            provider: SchemaProvider,
            endpoint: Optional[str] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None,
    ):
        self.schema_provider: SchemaProvider = provider
        self.endpoint: str = endpoint
        self.settings: Settings = settings or Settings()
        self.cache: Optional[Cache] = cache

        self.logger.debug("Schema introspection started")
        from qlient.schema.loader import load_schema
        self.schema: Dict = load_schema(self.schema_provider, self.endpoint, self.cache)
        self.logger.debug("Schema loaded")

        from qlient.schema.parser import parse_schema, ParseResult
        parse_result: ParseResult = parse_schema(self.schema)
        self.logger.debug("Schema parsed")

        self.query_type: Optional[Type] = parse_result.query_type
        self.mutation_type: Optional[Type] = parse_result.mutation_type
        self.subscription_type: Optional[Type] = parse_result.subscription_type
        self.types_registry: Dict[str, Type] = parse_result.types
        self.directives_registry: Dict[str, Directive] = parse_result.directives
        self.logger.debug("Schema successfully introspected")

    def __str__(self) -> str:
        """ Return a simple string representation of the schema instance """
        return repr(self)

    def __repr__(self) -> str:
        """ Return a more detailed string representation of the schema instance """
        class_name = self.__class__.__name__
        return f"<{class_name}(query_type={self.query_type}, mutation_type={self.mutation_type}, subscription_type={self.subscription_type})>"
