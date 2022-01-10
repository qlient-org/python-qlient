# Schema Providers

There are two built in schema providers. The first is the `LocalSchemaProvider` which reads the graphql schema from a
local file, the other is the `RemoteSchemaProvider` which sends an introspection query to the graphql server and gets
the schema from there.

**Remote Introspection only works when allowed by the graphql server.**

