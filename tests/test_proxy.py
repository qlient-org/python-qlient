# skipcq: PY-D0003
def test_query_service():
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy, QueryProxy
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = QueryServiceProxy(client)
    assert service.operations != {}
    assert "allPeople" in service
    assert isinstance(service["allPeople"], QueryProxy)


# skipcq: PY-D0003
def test_query_query_select():
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = QueryServiceProxy(client)
    expected = "query film { film { id title episodeID } }"
    actual = service.film.select("id", "title", "episodeID").__gql__()
    assert actual == expected


# skipcq: PY-D0003
def test_query_query_variables():
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = QueryServiceProxy(client)
    expected = "query film($id: ID) { film(id: $id) { id title episodeID } }"
    actual = service.film.variables(id="ZmlsbXM6MQ==").select("id", "title", "episodeID").__gql__()
    assert actual == expected


# skipcq: PY-D0003
def test_mutation_service():
    from qlient.client import Client
    from qlient.proxy import MutationServiceProxy
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = MutationServiceProxy(client)
    assert service.operations == {}
