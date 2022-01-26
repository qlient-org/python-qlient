def test_simple_client():
    from qlient.client import Client
    from qlient import HTTPBackend
    from __base__ import make_test_schema
    client = Client(
        "https://swapi-graphql.netlify.app/.netlify/functions/index",
        schema=make_test_schema()
    )

    assert isinstance(client.backend, HTTPBackend)
    assert client.backend.endpoint == "https://swapi-graphql.netlify.app/.netlify/functions/index"
    assert "allPeople" in client.query
