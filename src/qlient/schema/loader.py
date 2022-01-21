""" This file contains the loader functions for the graphql schema

:author: Daniel Seifert
:created: 10.09.2021
"""
import logging
from typing import Dict, Optional

from qlient.cache import Cache
from qlient.schema.providers import SchemaProvider

LOGGER = logging.getLogger("qlient")


def load_schema(
        provider: SchemaProvider,
        cache_key: str,
        cache: Optional[Cache]
) -> Dict:
    """ Load the schema either from cache, disk or api

    :param provider: holds either None or the schema provider
    :param cache_key: holds the location of the schema
    :param cache: holds the cache that contains the schema
    :return: the schema
    """
    schema: Optional[Dict] = cache.get(cache_key) if cache else None
    if schema is not None:
        LOGGER.debug(f"Returning schema `{cache_key}` from cache")
        return schema

    schema = provider.load_schema()

    if cache:
        cache[cache_key] = schema

    return schema
