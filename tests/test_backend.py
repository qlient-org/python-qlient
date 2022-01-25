def test_http_backend():
    from qlient.backend import HTTPBackend
    from requests.sessions import Session

    backend = HTTPBackend("https://test.test")
    assert isinstance(backend.session, Session)
    assert backend.session is not Session()
    assert backend.endpoint == "https://test.test"
