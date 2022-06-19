# skipcq: PY-D0003
def test_query_service(swapi_schema):
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy, QueryProxy
    client = Client("https://...", schema=swapi_schema)
    service = QueryServiceProxy(client)
    assert service.operations != {}
    assert "allPeople" in service
    assert isinstance(service["allPeople"], QueryProxy)


# skipcq: PY-D0003
def test_query_query_select(swapi_schema):
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy
    client = Client("https://...", schema=swapi_schema)
    service = QueryServiceProxy(client)
    expected = "query film { film { id title episodeID } }"
    actual = service.film.select("id", "title", "episodeID").__gql__()
    assert actual == expected


# skipcq: PY-D0003
def test_query_query_variables(swapi_schema):
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy
    client = Client("https://...", schema=swapi_schema)
    service = QueryServiceProxy(client)
    expected = "query film($id: ID) { film(id: $id) { id title episodeID } }"
    actual = service.film.variables(id="ZmlsbXM6MQ==").select("id", "title", "episodeID").__gql__()
    assert actual == expected


# skipcq: PY-D0003
def test_mutation_service(swapi_schema):
    from qlient.client import Client
    from qlient.proxy import MutationServiceProxy
    client = Client("https://...", schema=swapi_schema)
    service = MutationServiceProxy(client)
    assert service.operations == {}
