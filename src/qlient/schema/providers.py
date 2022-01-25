""" This file contains the different schema providers

:author: Daniel Seifert
:created: 13.01.2022
"""
import abc
import logging
import pathlib
from typing import Union

from qlient.backend import Backend
from qlient.schema.types import RawSchema

logger = logging.getLogger("qlient")


class SchemaProvider(abc.ABC):

    @abc.abstractmethod
    def load_schema(self) -> RawSchema:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache_key(self) -> str:
        """ A key that uniquely identifies the schema for a specific backend

        For example this can be a unique url or hostname.
        Or even a static key if the schema remains the same for the backend.

        :return: a string that uniquely identifies the schema
        """
        raise NotImplementedError


class StaticSchemaProvider(SchemaProvider):

    def __init__(self, raw_schema: RawSchema, cache_key: str):
        self.raw_schema = raw_schema
        self._cache_key = cache_key

    def load_schema(self) -> RawSchema:
        return self.raw_schema

    @property
    def cache_key(self) -> str:
        return self._cache_key


class FilepathSchemaProvider(SchemaProvider):

    def __init__(self, filepath: Union[str, pathlib.Path]):
        self.filepath: pathlib.Path = pathlib.Path(filepath)

    def load_schema(self) -> RawSchema:
        logger.debug(f"Reading local schema from `{self.filepath}`")
        import json
        with self.filepath.open("r") as schema_file_buffer:
            return json.load(schema_file_buffer)

    @property
    def cache_key(self) -> str:
        return str(self.filepath.resolve())


class BackendSchemaProvider(SchemaProvider):
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
        return self.backend.cache_key
