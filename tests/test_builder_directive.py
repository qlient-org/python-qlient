# skipcq: PY-D0003
def test_directive():
    from qlient.builder import Directive
    actual = Directive("my_directive")
    assert actual.name == "my_directive"


# skipcq: PY-D0003
def test_directive_with_variables():
    from qlient.builder import Directive
    my_directive = Directive("my_directive", foo="5")
    assert "foo" in my_directive.variables
    assert my_directive.variables["foo"] == "5"
    assert "my_directive" == my_directive.name


# skipcq: PY-D0003
def test_prepared_directive(swapi_schema):
    from qlient.builder import Directive, PreparedDirective
    my_directive = Directive("include")
    prepared_directive = my_directive.prepare(swapi_schema)
    assert isinstance(prepared_directive, PreparedDirective)


# skipcq: PY-D0003
def test_prepared_directive_with_variables(swapi_schema):
    from qlient.builder import Directive, PreparedDirective
    my_directive = Directive("include", **{"if": True})
    prepared_directive = my_directive.prepare(swapi_schema)
    assert isinstance(prepared_directive, PreparedDirective)
    assert prepared_directive.name == "include"
    assert "if" in prepared_directive.var_name_to_var_ref


# skipcq: PY-D0003
def test_prepared_directive_gql(swapi_schema):
    from qlient.builder import Directive
    my_directive = Directive("include")
    prepared_directive = my_directive.prepare(swapi_schema)
    assert prepared_directive.__gql__() == "@include"


# skipcq: PY-D0003
def test_prepared_directive_with_variables_gql(swapi_schema):
    from qlient.builder import Directive
    my_directive = Directive("include", **{"if": True})
    prepared_directive = my_directive.prepare(swapi_schema)
    assert prepared_directive.__gql__() == f"@include(if: $include_{id(prepared_directive)}_if)"
