import json

from qlient import Settings, Client

my_settings = Settings(
    introspect=True,  # default, enable backend schema introspection
    validate_fields=True,  # default, enable query field selection validation
    validate_variables=True,  # default, enable query variable validation,
    json_dumps=json.dumps,  # default, use python's builtin json.dumps for internal dumping
    json_loads=json.loads,  # default, use python's builtin json.loads for internal loading
)

my_client = Client("https://...", settings=my_settings)
