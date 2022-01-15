def test_settings():
    from qlient.settings import Settings
    settings = Settings()
    assert settings.validate_url is True


def test_settings_validate_url():
    from qlient.settings import Settings
    settings = Settings(validate_url=False)
    assert settings.validate_url is False
