from pathlib import Path

from qlient import Client, Schema
from qlient.schema.providers import FileSchemaProvider

path_to_schema = Path("./path/to/my/schema.json")

local_schema = Schema(provider=FileSchemaProvider(path_to_schema))

client = Client("https://...", schema=local_schema)
