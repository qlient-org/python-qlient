def test_query_service():
    from qlient.client import Client
    from qlient.proxy import QueryServiceProxy, QueryProxy
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = QueryServiceProxy(client)
    assert service.operations != {}
    assert "allPeople" in service
    assert isinstance(service["allPeople"], QueryProxy)


def test_mutation_service():
    from qlient.client import Client
    from qlient.proxy import MutationServiceProxy
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = MutationServiceProxy(client)
    assert service.operations == {}
