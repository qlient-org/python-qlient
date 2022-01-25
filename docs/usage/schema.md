# Schema

The schema describes what operations can be made, which inputs can be given and which return values are expected.

By default, the schema will be introspected using the `BackendSchemaProvider`.

The `BackendSchemaProvider` takes the in the client specified backend and uses an introspection query to load the schema
from the backend.

## Custom Schema

In some cases, for example when the introspection has been disabled on the graphql backend, you'd want to read the
schema from a different location. This can be for example from a local file.

Thanks to the `SchemaProvider` base class, this can quite easily be achieved.

### Schema from local path

Below shows an example that reads the schema from a local path on the file system.

````python 
{% include "../examples/read_schema_from_local_path.py" %}
````

### My schema is neither on my filesystem, nor on any remote

Do not fear, solution is near. have a look at the [documentation for schema providers](schema_providers.md)
