""" This file contains the loader functions for the graphql schema

:author: Daniel Seifert
:created: 10.09.2021
:copyright: Swisscom
"""
import logging
from typing import Dict, Optional

from qlient import __about__
from qlient.cache import Cache
from qlient.exceptions import SchemaDetectionException
from qlient.schema.providers import SchemaProvider, LocalSchemaProvider, RemoteSchemaProvider
from qlient.transport import Transport
from qlient.validators import is_url, is_local_path

LOGGER = logging.getLogger(__about__.__title__)


def detect_schema_provider(location: str, transport: Transport) -> SchemaProvider:
    if is_local_path(location):
        return LocalSchemaProvider(location)
    if is_url(location):
        return RemoteSchemaProvider(location, transport)
    raise SchemaDetectionException(location=location)


def load_schema(
        provider: Optional[SchemaProvider],
        location: str,
        transport: Transport,
        cache: Optional[Cache]
) -> Dict:
    """ Load the schema either from cache, disk or api

    :param provider: holds either None or the schema provider
    :param location: holds the location of the schema
    :param transport: holds the transport instance, used for getting it from the api
    :param cache: holds the cache that contains the schema
    :return: the schema
    """
    schema: Optional[Dict] = cache.get(location) if cache else None
    if schema is not None:
        LOGGER.debug(f"Returning schema `{location}` from cache")
        return schema

    provider = provider or detect_schema_provider(location, transport)
    schema = provider.load_schema()

    if cache:
        cache.put(location, schema)

    return schema
