def test_simple_client():
    from qlient.client import Client
    from qlient import HTTPBackend
    from qlient.schema.schema import Schema
    from qlient.schema.providers import StaticSchemaProvider
    from __base__ import raw_schema
    client = Client(
        "https://swapi-graphql.netlify.app/.netlify/functions/index",
        schema=Schema(StaticSchemaProvider(raw_schema["data"]["__schema"], "Test"))
    )

    assert isinstance(client.backend, HTTPBackend)
    assert client.backend.endpoint == "https://swapi-graphql.netlify.app/.netlify/functions/index"
    assert "allPeople" in client.query
