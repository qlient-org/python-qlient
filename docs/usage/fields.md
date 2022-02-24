# Field and Fields

The `Fields` class is a powerful class for making nested or pre-configured field selections. In combination with
the `Field` class you can create every query you need.

## Using the Field Class

The Field class supports all major graphql features ranging from name, alias to directives and field inputs.

```python 
{% include "../examples/using_field_class.py" %}
```

{% include "../examples/script_legend.md" %}

## Using the Fields Class

```python 
{% include "../examples/using_fields_class.py" %}
```

{% include "../examples/script_legend.md" %}

## Supported Operators

Both, the `Field` and `Fields` class currently support the following operators:

### Addition

```python 
{% include "../examples/fields_addition_operator.py" %}
```

{% include "../examples/script_legend.md" %}

## Combination of Fields and Field

```python 
{% include "../examples/combination_of_fields_and_field.py" %}
```