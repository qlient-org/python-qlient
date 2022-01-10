# Schema Providers

**What if my schema is neither located on my filesystem, nor is it on any remote?**

Do not fear, solution is near. Under the hood, the schema uses `SchemaProviders`. This package comes with two built in
providers:

* The `LocalSchemaProvider` in case your schema is on your disk
* The `RemoteSchemaProvider` in case your schema can be obtained from the remote (**Remote Introspection only works when
  allowed by the graphql server.**)

If neither of these two built in providers suit your needs, you can create your own schema provider like so:

```python
from typing import Dict

from qlient import Client, Schema
from qlient.schema.providers import SchemaProvider


class MySchemaProvider(SchemaProvider):

  def load_schema(self) -> Dict:
    # do some logic that loads your schema
    return {...}


my_schema = Schema(provider=MySchemaProvider())

client = Client(endpoint="https://...", schema=my_schema)
```

