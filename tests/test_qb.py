def test_fields_simple_single():
    from qlient.qb import Fields
    a = Fields("a")
    assert a.fields == ["a"]


def test_fields_simple_multiple():
    from qlient.qb import Fields
    a = Fields("a", "b", "c")
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.fields


def test_fields_simple_multiple_duplicates():
    from qlient.qb import Fields
    a = Fields("a", "b", "c", "c", "c")
    assert len(a.fields) == 3
    assert a.fields.count("c") == 1


def test_fields_simple_list():
    from qlient.qb import Fields
    a = Fields(["a", "b", "c"])
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.fields


def test_fields_simple_list_duplicates():
    from qlient.qb import Fields
    fields = ["a", "b", "c", "c", "c"]
    a = Fields(fields)
    assert len(a.fields) == 3
    assert a.fields.count("c") == 1


def test_fields_deep_simple():
    from qlient.qb import Fields
    a = Fields("a", "b", c="d")
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.sub_fields
    assert a.sub_fields["c"].fields == ["d"]


def test_fields_deep_simple_list():
    from qlient.qb import Fields
    a = Fields("a", "b", c=["a", "b"])
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.sub_fields
    assert len(a.sub_fields["c"].fields) == 2


def test_fields_deep_nested_fields():
    from qlient.qb import Fields
    a = Fields(a=Fields("a"), b=Fields("b"))
    assert "a" in a.sub_fields
    assert a.sub_fields["a"].fields == ["a"]

    assert "b" in a.sub_fields
    assert a.sub_fields["b"].fields == ["b"]


def test_fields_eq_operator():
    from qlient.qb import Fields
    a = Fields()
    b = Fields()
    pass


def test_fields_add_operator():
    from qlient.qb import Fields
    a = Fields()
    b = Fields()
    pass


def test_fields_sub_operator():
    from qlient.qb import Fields
    a = Fields()
    b = Fields()
    pass


def test_fields_and_operator():
    from qlient.qb import Fields
    a = Fields()
    b = Fields()
    pass
