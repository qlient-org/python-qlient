# skipcq: PY-D0003
def test_default_settings():
    from qlient.settings import Settings
    settings = Settings()
    assert settings.introspect is True
    assert settings.validate_variables is True
    assert settings.validate_fields is True


# skipcq: PY-D0003
def test_settings_introspect():
    from qlient.settings import Settings
    settings = Settings(introspect=False)
    assert settings.introspect is False


# skipcq: PY-D0003
def test_settings_validate_variables():
    from qlient.settings import Settings
    settings = Settings(validate_variables=False)
    assert settings.validate_variables is False


# skipcq: PY-D0003
def test_settings_validate_fields():
    from qlient.settings import Settings
    settings = Settings(validate_fields=False)
    assert settings.validate_fields is False
