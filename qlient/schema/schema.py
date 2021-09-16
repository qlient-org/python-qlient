""" This file contains the graphql schema

:author: Daniel Seifert
:created: 16.09.2021
:copyright: Swisscom
"""
import logging
from typing import Optional, Dict, List

from qlient import __about__
from qlient.cache import Cache
from qlient.schema.models import Type, Directive
from qlient.settings import Settings
from qlient.transport import Transport


class Schema:
    """ Represents a graphql schema """

    logger = logging.getLogger(__about__.__title__)

    def __init__(
            self,
            location: str,
            transport: Optional[Transport] = None,
            settings: Optional[Settings] = None,
            cache: Optional[Cache] = None
    ):
        self.location: str = str(location)
        self.transport: Transport = transport or Transport()
        self.settings: Settings = settings or Settings()
        self.cache: Optional[Cache] = cache

        self.schema: Optional[Dict] = None

        self.query_type: Optional[Type] = None
        self.mutation_type: Optional[Type] = None
        self.subscription_type: Optional[Type] = None
        self.types: Optional[Dict[str, Type]] = None
        self.directives: Optional[Dict[str, Directive]] = None

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
