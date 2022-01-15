def test_type_ref_empty():
    from qlient.schema.models import TypeRef
    type_ref = TypeRef()
    assert type_ref.kind is None
    assert type_ref.name is None
    assert type_ref.of_type is None
    assert type_ref.graphql_representation is None


def test_type_ref_values():
    from qlient.schema.models import TypeRef
    type_ref = TypeRef(kind="NON_NULL", name="String")
    assert type_ref.kind == "NON_NULL"
    assert type_ref.name == "String"
    assert type_ref.of_type is None
    assert type_ref.graphql_representation == "String!"
    assert type_ref.final_type_name == "String"


def test_type_ref_nested():
    from qlient.schema.models import TypeRef
    type_ref = TypeRef(kind="NON_NULL", name=None, ofType=TypeRef(kind="LIST", name="String"))
    assert type_ref.kind == "NON_NULL"
    assert type_ref.name is None
    assert isinstance(type_ref.of_type, TypeRef)
    assert type_ref.graphql_representation == "[String]!"
    assert type_ref.final_type_name == "String"


def test_type_ref_parse():
    from qlient.schema.models import TypeRef
    type_ref = TypeRef.parse({"kind": "NON_NULL", "name": "String"})
    assert type_ref.kind == "NON_NULL"
    assert type_ref.name == "String"
    assert type_ref.of_type is None
    assert type_ref.graphql_representation == "String!"
    assert type_ref.final_type_name == "String"


def test_input_empty():
    from qlient.schema.models import Input
    input_type = Input()
    assert input_type.name is None
    assert input_type.description is None
    assert input_type.type is None
    assert input_type.default_value is None


def test_input_values():
    from qlient.schema.models import Input
    input_type = Input(name="first_name")
    assert input_type.name == "first_name"
