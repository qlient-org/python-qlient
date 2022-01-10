# Schema

The schema is a core part of graphql.

## Custom Schema

In some cases, for example when the introspection has been disabled on the graphql api, you'd want to manually create
the schema. This can be for example from a local file or a custom endpoint.

### Schema from local path

Below shows an example that reads the schema from a local path on the file system.

````python
from pathlib import Path

from qlient import Client, Schema

path_to_schema = Path("./path/to/my/schema.json")

local_schema = Schema(location=path_to_schema)

client = Client(endpoint="https://...", schema=local_schema)
````

### Schema from custom remote

Maybe you got a replica of the graphql api that allows for introspection. In that case can get the schema from the
replica like so:

````python
from qlient import Client, Schema

remote_schema = Schema(location="https://my-schema-provider.com")

client = Client(endpoint="https://my-graphql-api.com", schema=remote_schema)
````