""" This file contains the graphql schema

:author: Daniel Seifert
:created: 16.09.2021
"""
import logging
from typing import Optional, Dict

from qlient.cache import Cache
from qlient.schema.providers import SchemaProvider
from qlient.schema.types import Type, Directive
from qlient.settings import Settings

logger = logging.getLogger("qlient")


class Schema:
    """ Represents a graphql schema """

    def __init__(
            self,
            provider: SchemaProvider,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None,
    ):
        self.schema_provider: SchemaProvider = provider
        self.settings: Settings = settings or Settings()
        self.cache: Optional[Cache] = cache

        logger.debug("Schema introspection started")
        from qlient.schema.loader import load_schema
        self.raw: Dict = load_schema(self.schema_provider, self.cache)
        logger.debug("Schema loaded")

        from qlient.schema.parser import parse_schema, ParseResult
        parse_result: ParseResult = parse_schema(self.raw)
        logger.debug("Schema parsed")

        self.query_type: Optional[Type] = parse_result.query_type
        self.mutation_type: Optional[Type] = parse_result.mutation_type
        self.subscription_type: Optional[Type] = parse_result.subscription_type
        self.types_registry: Dict[str, Type] = parse_result.types
        self.directives_registry: Dict[str, Directive] = parse_result.directives
        logger.debug("Schema successfully introspected")

    def __str__(self) -> str:
        """ Return a simple string representation of the schema instance """
        return repr(self)

    def __repr__(self) -> str:
        """ Return a more detailed string representation of the schema instance """
        class_name = self.__class__.__name__
        return f"<{class_name}(query_type={self.query_type}, mutation_type={self.mutation_type}, subscription_type={self.subscription_type})>"
