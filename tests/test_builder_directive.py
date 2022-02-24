def test_directive():
    from qlient.builder import Directive
    actual = Directive("my_directive")
    assert actual.name == "my_directive"


def test_directive_with_variables():
    from qlient.builder import Directive
    my_directive = Directive("my_directive", foo="5")
    assert "foo" in my_directive.variables
    assert my_directive.variables["foo"] == "5"
    assert "my_directive" == my_directive.name


def test_prepared_directive():
    from qlient.builder import Directive, PreparedDirective
    from __base__ import make_test_schema
    my_directive = Directive("include")
    prepared_directive = my_directive.prepare(make_test_schema())
    assert isinstance(prepared_directive, PreparedDirective)


def test_prepared_directive_with_variables():
    from qlient.builder import Directive, PreparedDirective
    from __base__ import make_test_schema
    my_directive = Directive("include", **{"if": True})
    prepared_directive = my_directive.prepare(make_test_schema())
    assert isinstance(prepared_directive, PreparedDirective)
    assert prepared_directive.name == "include"
    assert "if" in prepared_directive.var_name_to_var_ref


def test_prepared_directive_gql():
    from qlient.builder import Directive
    from __base__ import make_test_schema
    my_directive = Directive("include")
    prepared_directive = my_directive.prepare(make_test_schema())
    assert prepared_directive.__gql__() == f"@include"


def test_prepared_directive_with_variables_gql():
    from qlient.builder import Directive
    from __base__ import make_test_schema
    my_directive = Directive("include", **{"if": True})
    prepared_directive = my_directive.prepare(make_test_schema())
    assert prepared_directive.__gql__() == f"@include(if: $include_{id(prepared_directive)}_if)"
