def test_fields_simple_single():
    from qlient.builder import Fields
    a = Fields("a")
    assert a.fields == ["a"]


def test_fields_simple_multiple():
    from qlient.builder import Fields
    a = Fields("a", "b", "c")
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.fields


def test_fields_simple_multiple_duplicates():
    from qlient.builder import Fields
    a = Fields("a", "b", "c", "c", "c")
    assert len(a.fields) == 3
    assert a.fields.count("c") == 1


def test_fields_simple_list():
    from qlient.builder import Fields
    a = Fields(["a", "b", "c"])
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.fields


def test_fields_simple_list_duplicates():
    from qlient.builder import Fields
    fields = ["a", "b", "c", "c", "c"]
    a = Fields(fields)
    assert len(a.fields) == 3
    assert a.fields.count("c") == 1


def test_fields_complex_simple():
    from qlient.builder import Fields
    a = Fields("a", "b", c="d")
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.sub_fields
    assert a.sub_fields["c"].fields == ["d"]


def test_fields_complex_simple_list():
    from qlient.builder import Fields
    a = Fields("a", "b", c=["a", "b"])
    assert "a" in a.fields
    assert "b" in a.fields
    assert "c" in a.sub_fields
    assert len(a.sub_fields["c"].fields) == 2


def test_fields_complex_nested_fields():
    from qlient.builder import Fields
    a = Fields(a=Fields("a"), b=Fields("b"))
    assert "a" in a.sub_fields
    assert a.sub_fields["a"].fields == ["a"]

    assert "b" in a.sub_fields
    assert a.sub_fields["b"].fields == ["b"]


def test_fields_simple_eq_operator():
    from qlient.builder import Fields
    a = Fields("a")
    b = Fields("a")
    assert a == b


def test_fields_simple_eq_operator_not():
    from qlient.builder import Fields
    a = Fields("a")
    b = Fields("b")
    assert a != b


def test_fields_complex_eq_operator():
    from qlient.builder import Fields
    a = Fields("a", b="c")
    b = Fields("a", b="c")
    assert a == b


def test_fields_complex_eq_operator_not():
    from qlient.builder import Fields
    a = Fields("a", b="c")
    b = Fields("a", b="d")
    assert a != b


def test_fields_simple_add_operator_simple():
    from qlient.builder import Fields
    a = Fields("a")
    expected = Fields("a", "b")
    actual = a + "b"
    assert expected == actual


def test_fields_simple_add_operator_list():
    from qlient.builder import Fields
    a = Fields("a")
    expected = Fields("a", "b", "c")
    actual = a + ["b", "c"]
    assert expected == actual


def test_fields_simple_add_operator_dict():
    from qlient.builder import Fields
    a = Fields("a")
    expected = Fields("a", b="c")
    actual = a + {"b": "c"}
    assert expected == actual


def test_fields_simple_add_operator_fields():
    from qlient.builder import Fields
    a = Fields("a")
    b = Fields("a", "b", c="d")
    expected = Fields("a", "b", c="d")
    actual = a + b
    assert expected == actual


def test_fields_complex_add_operator_simple():
    from qlient.builder import Fields
    a = Fields("a", b="b")
    expected = Fields("a", "c", b="b")
    actual = a + "c"
    assert expected == actual


def test_fields_complex_add_operator_list():
    from qlient.builder import Fields
    a = Fields("a", b="b")
    expected = Fields("a", "c", "z", b="b")
    actual = a + ["a", "c", "z"]
    assert expected == actual


def test_fields_complex_add_operator_dict():
    from qlient.builder import Fields
    a = Fields("a", b="b")
    expected = Fields("a", b=["b", "c", "e"])
    actual = a + {"b": ["c", "e"]}
    assert expected == actual


def test_fields_complex_add_operator_fields():
    from qlient.builder import Fields
    a = Fields("a", b="b")
    b = Fields("a", "c")
    expected = Fields("a", "c", b="b")
    actual = a + b
    assert expected == actual


def test_fields_simple_sub_operator_simple():
    from qlient.builder import Fields
    a = Fields("a", "b")
    expected = Fields("a")
    actual = a - "b"
    assert expected == actual


def test_fields_simple_sub_operator_list():
    from qlient.builder import Fields
    a = Fields("a", "b", "c")
    expected = Fields("a")
    actual = a - ["b", "c"]
    assert expected == actual


def test_fields_simple_sub_operator_fields():
    from qlient.builder import Fields
    a = Fields("a", "b", "c")
    expected = Fields("a")
    actual = a - Fields("b", "c", "z")
    assert expected == actual


def test_fields_complex_sub_operator_simple():
    from qlient.builder import Fields
    a = Fields("a", "b", c="c")
    expected = Fields("a", c="c")
    actual = a - "b"
    assert expected == actual


def test_fields_complex_sub_operator_list():
    from qlient.builder import Fields
    a = Fields("a", "b", "z", c="c")
    expected = Fields("a", c="c")
    actual = a - ["b", "z"]
    assert expected == actual


def test_fields_complex_sub_operator_dict():
    from qlient.builder import Fields
    a = Fields("a", "b", "z", c=["a", "b", "c"])
    expected = Fields("a", "b", "z", c=["a"])
    actual = a - {"c": ["b", "c"]}
    assert expected == actual


def test_fields_complex_sub_operator_fields():
    from qlient.builder import Fields
    a = Fields("a", "b", "z", c="c")
    expected = Fields("a")
    actual = a - Fields("b", "z", c="c")
    assert expected == actual
