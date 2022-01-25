from typing import Dict

from qlient import Client, Schema
from qlient.schema.providers import SchemaProvider


class MySchemaProvider(SchemaProvider):

    def load_schema(self) -> Dict:
        # do some logic that loads your schema
        return {...}


my_schema = Schema(provider=MySchemaProvider())

client = Client("https://...", schema=my_schema)
