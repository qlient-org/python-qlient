# Schema Providers

**What if my schema is neither located on my filesystem, nor is it on any backend?**

Do not fear, solution is near. Under the hood, the schema uses `SchemaProvider`s. This package comes with three built in
providers:

* The `StaticSchemaProvider` in case you have a static dictionary with the schema
* The `FilepathSchemaProvider` in case your schema is on your disk
* The `BackendSchemaProvider` in case your schema can be obtained from the backend (**Backend Introspection only works
  when allowed by the graphql backend.**)

If neither of these two built in providers suit your needs, you can create your own schema provider like so:

```python 
{% include "../examples/custom_schema_provider.py" %}
```
