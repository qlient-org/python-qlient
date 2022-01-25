from qlient.types import GraphQLQuery, GraphQLVariables, GraphQLOperation, GraphQLContext, GraphQLRoot, \
    GraphQLReturnType


def test_http_backend():
    from qlient.backend import HTTPBackend
    from requests.sessions import Session

    backend = HTTPBackend("https://test.test")
    assert isinstance(backend.session, Session)
    assert backend.session is not Session()
    assert backend.endpoint == "https://test.test"


def test_custom_backend():
    from qlient.backend import Backend

    class MyBackend(Backend):
        def execute_query(
                self,
                query: GraphQLQuery,
                variables: GraphQLVariables = None,
                operation_name: GraphQLOperation = None,
                context: GraphQLContext = None,
                root: GraphQLRoot = None
        ) -> GraphQLReturnType:
            return {}

        @property
        def cache_key(self) -> str:
            return "ABC"

    my_backend = MyBackend()

    assert my_backend.cache_key == "ABC"
    assert my_backend.execute_query("foo") == {}
