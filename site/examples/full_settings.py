from qlient import Settings, Client

my_settings = Settings(
    introspect=True,  # default, enable backend schema introspection
    validate_fields=True,  # default, enable query field selection validation
    validate_variables=True  # default, enable query variable validation
)

my_client = Client("https://...", settings=my_settings)
