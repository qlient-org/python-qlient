""" This file contains the loader functions for the graphql schema

:author: Daniel Seifert
:created: 10.09.2021
"""
import logging
from typing import Dict, Optional

from qlient.cache import Cache
from qlient.schema.providers import SchemaProvider

logger = logging.getLogger("qlient")


def load_schema(
        provider: SchemaProvider,
        cache: Optional[Cache]
) -> Dict:
    """ Load the schema from the given provider

    :param provider: holds either None or the schema provider
    :param cache: holds the cache that contains the schema
    :return: the schema
    """
    schema: Optional[Dict] = cache.get(provider.cache_key) if cache is not None else None
    if schema is not None:
        # if schema is not None, this means that the cache is also not None.
        # Therefore, it is safe to access to cache properties
        logger.debug(f"Returning schema `{provider.cache_key}` from cache `{cache.__class__.__name__}`")
        return schema

    logger.debug(f"Using schema from provider `{provider}`")
    schema = provider.load_schema()

    if cache is not None:
        logger.debug(f"Caching schema in `{cache.__class__.__name__}` for future usage with key `{provider.cache_key}`")
        cache[provider.cache_key] = schema

    return schema
