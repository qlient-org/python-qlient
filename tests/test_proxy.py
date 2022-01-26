def test_query_service():
    from qlient.client import Client
    from qlient.proxy import QueryService, Query
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = QueryService(client)
    assert service.operations != {}
    assert "allPeople" in service
    assert isinstance(service["allPeople"], Query)


def test_mutation_service():
    from qlient.client import Client
    from qlient.proxy import MutationService
    from __base__ import make_test_schema
    client = Client("https://...", schema=make_test_schema())
    service = MutationService(client)
    assert service.operations == {}
