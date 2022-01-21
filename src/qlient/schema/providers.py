""" This file contains the different schema providers

:author: Daniel Seifert
:created: 13.01.2022
"""
import abc
import logging
import pathlib
from typing import Union

from qlient.schema.models import RawSchema
from qlient.transport import Transport

LOGGER = logging.getLogger("qlient")


class SchemaProvider(abc.ABC):

    @abc.abstractmethod
    def load_schema(self) -> RawSchema:
        raise NotImplementedError


class LocalSchemaProvider(SchemaProvider):

    def __init__(self, filepath: Union[str, pathlib.Path]):
        self.filepath: pathlib.Path = pathlib.Path(filepath)

    def load_schema(self) -> RawSchema:
        LOGGER.debug(f"Reading local schema from `{self.filepath}`")
        import json
        with self.filepath.open("r") as schema_file_buffer:
            return json.load(schema_file_buffer)


class RemoteSchemaProvider(SchemaProvider):
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

    def __init__(self, endpoint: str, transport: Transport, introspect: bool = True):
        self.should_introspect: bool = introspect
        self.endpoint: str = endpoint
        self.transport: Transport = transport

    def load_schema(self) -> RawSchema:
        if not self.should_introspect:
            LOGGER.warning("Schema introspection was disabled by user.")
            return {}

        LOGGER.debug(f"Loading remote schema from `{self.endpoint}`")
        schema_response = self.transport.send_query(
            endpoint=self.endpoint,
            operation_name=self.INTROSPECTION_OPERATION_NAME,
            query=self.INTROSPECTION_QUERY,
            variables={}
        )
        return schema_response["data"]["__schema"]
