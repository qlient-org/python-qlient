""" This file contains the loader functions for the graphql schema

:author: Daniel Seifert
:created: 10.09.2021
:copyright: Swisscom
"""
import json
import logging
import pathlib
from typing import Dict, Optional

from qlient import __about__
from qlient.cache import Cache
from qlient.transport import Transport

LOGGER = logging.getLogger(__about__.__title__)

INTROSPECTION_OPERATION_NAME = "IntrospectionQuery"
INTROSPECTION_QUERY = """
        query IntrospectionQuery {
          __schema {
            queryType { name }
            mutationType { name }
            subscriptionType { name }
            types {
              ...FullType
            }
            directives {
              name
              description
              locations
              args {
                ...InputValue
              }
            }
          }
        }
        fragment FullType on __Type {
          kind
          name
          description
          fields(includeDeprecated: true) {
            name
            description
            args {
              ...InputValue
            }
            type {
              ...TypeRef
            }
            isDeprecated
            deprecationReason
          }
          inputFields {
            ...InputValue
          }
          interfaces {
            ...TypeRef
          }
          enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
          }
          possibleTypes {
            ...TypeRef
          }
        }
        fragment InputValue on __InputValue {
          name
          description
          type { ...TypeRef }
          defaultValue
        }
        fragment TypeRef on __Type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """


def is_local_path(location: str) -> bool:
    """ Check if the given location is a local path

    :param location: holds the location of the schema definition
    :return: True if the schema is a local path
    """
    try:
        return pathlib.Path(location).exists()
    except OSError:
        # when something goes wrong, the location is most likely not a local file
        return False


def read_local_schema(location: str) -> Dict:
    """ Read the schema from a local location for instance a file

    :param location: holds the location of the schema
    :return: the schema as a dictionary
    """
    with open(location, "r") as schema_file:
        LOGGER.debug(f"Reading local schema from `{location}`")
        return json.load(schema_file)


def load_remote_schema(transport: Transport) -> Dict:
    """ Load the schema remotely from the graphql api

    :param transport: holds the transport to use for querying the graphql api
    :return:
    """
    LOGGER.debug(f"Loading remote schema from `{transport.endpoint}`")
    return transport.send_query(
        operation_name=INTROSPECTION_OPERATION_NAME,
        query=INTROSPECTION_QUERY,
        variables={}
    )


def load_schema(location: str, transport: Transport, cache: Optional[Cache]) -> Dict:
    """ Load the schema either from cache, disk or api

    :param location: holds the location of the schema
    :param transport: holds the transport instance, used for getting it from the api
    :param cache: holds the cache that contains the schema
    :return: the schema
    """
    schema: Optional[Dict] = cache.get(location) if cache else None
    if schema is not None:
        LOGGER.debug(f"Returning schema `{location}` from cache")
        return schema

    if is_local_path(location):
        schema = read_local_schema(location)
    else:
        schema = load_remote_schema(transport)
        schema = schema.get("data", {}).get("__schema", {})
    if cache:
        cache.put(location, schema)
    return schema
