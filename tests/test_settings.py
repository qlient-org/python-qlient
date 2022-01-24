def test_default_settings():
    from qlient.settings import Settings
    settings = Settings()
    assert settings.validate_url is True


def test_settings_introspect():
    from qlient.settings import Settings
    settings = Settings(introspect=False)
    assert settings.introspect is False


def test_settings_validate_url():
    from qlient.settings import Settings
    settings = Settings(validate_url=False)
    assert settings.validate_url is False


def test_settings_validate_variables():
    from qlient.settings import Settings
    settings = Settings(validate_variables=False)
    assert settings.validate_variables is False


def test_settings_validate_fields():
    from qlient.settings import Settings
    settings = Settings(validate_fields=False)
    assert settings.validate_fields is False


def test_settings_response_type():
    from qlient.response import BaseResponse
    class TestResponse(BaseResponse):
        def __init__(self, response):
            super(TestResponse, self).__init__(response)

    from qlient.settings import Settings
    settings = Settings(response_type=TestResponse)
    assert settings.response_type == TestResponse
