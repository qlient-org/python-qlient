"""This file contains the different schema providers

:author: Daniel Seifert
:created: 13.01.2022
"""
import abc
import io
import logging
import pathlib
from typing import Union, IO

from qlient.backend import Backend
from qlient.schema.types import RawSchema

logger = logging.getLogger("qlient")


class SchemaProvider(abc.ABC):
    """Super class for all schema providers

    This makes it easy to create your own schema provider anytime.
    See the implementations below for a quick overview.
    """

    @abc.abstractmethod
    def load_schema(self) -> RawSchema:
        """Abstract method to load the schema.

        This function gets called in order to load the schema from the source.
        Note that this function is not called with any arguments.

        :return: The raw schema in it's json form
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache_key(self) -> str:
        """A key that uniquely identifies the schema for a specific backend

        For example this can be a unique url or hostname.
        Or even a static key if the schema remains the same for the backend.

        :return: a string that uniquely identifies the schema
        """
        raise NotImplementedError


class StaticSchemaProvider(SchemaProvider):
    """Simple schema provider that returns a previously declared schema."""

    def __init__(self, raw_schema: RawSchema, cache_key: str):
        self.raw_schema = raw_schema
        self._cache_key = cache_key

    def load_schema(self) -> RawSchema:
        """Method that returns the schema that was passed by in the __init__ function.

        :return: The schema that was passed by in the __init__ function.
        """
        return self.raw_schema

    @property
    def cache_key(self) -> str:
        """Property to return the cache key for this schema.

        To uniquely identify a schema in the cache it needs a unique key.
        Caching does not make sense for this provider, matter of fact, it's actually slower to use caching
        when you have a static schema provider because there are more calls being made.

        :return: the unique cache key of this schema.
        """
        return self._cache_key


class FileSchemaProvider(SchemaProvider):
    """Schema provider to read the schema from the file."""

    def __init__(self, file: Union[str, pathlib.Path, IO, io.IOBase]):
        filepath = None
        if isinstance(file, str):
            file = pathlib.Path(file)
        if isinstance(file, pathlib.Path):
            filepath = str(file.resolve())
            file = file.open("r")
        self.filepath: str = filepath or file.name
        self.file = file

    def load_schema(self) -> RawSchema:
        """Method to load the schema from the local file

        :return: the schema from the file
        """
        logger.debug(f"Reading local schema from `{self.file}`")
        import json
        return json.load(self.file)

    @property
    def cache_key(self) -> str:
        """Property to return the cache key that uniquely identifies this schema.

        This uses the absolute filepath as cache key.

        :return: the absolute filepath
        """
        return self.filepath


class BackendSchemaProvider(SchemaProvider):
    """Schema provider to read the schema using the backend.

    This provider uses an introspection query to load the schema directly from the backend.

    NOTE! This only works when the graphql backend has allowed introspection.
    """

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

    def __init__(self, backend: Backend, introspect: bool = True):
        self.backend: Backend = backend
        self.should_introspect: bool = introspect

    def load_schema(self) -> RawSchema:
        """Send the introspection query to the backend and return the given schema

        :return: the given schema from the backend.
        """
        if not self.should_introspect:
            logger.warning("Schema introspection was disabled by user.")
            return {}

        logger.debug(f"Loading remote schema using `{self.backend}`")
        schema_content = self.backend.execute_query(
            query=self.INTROSPECTION_QUERY,
            operation_name=self.INTROSPECTION_OPERATION_NAME,
            variables={}
        )
        return schema_content["data"]["__schema"]

    @property
    def cache_key(self) -> str:
        """Property to return the cache key that uniquely identifies this schema in the cache.

        This uses the backends cache key property as cache key.
        See ref:`Backend.cache_key` for more information.

        :return: the cache key as defined by the backend.
        """
        return self.backend.cache_key
