# Fields

The `Fields` class is a powerful class for making nested or pre-configured field selections.

## Nested Fields selection

```python
from qlient import Fields

nested_fields = Fields(
    "first_name",
    "last_name",
    hobby="name"
)

print(nested_fields)
```

```text
last_name first_name hobby { name }
```

The `hobby` selection can be changed from a single item to a `list`:

```python
from qlient import Fields

nested_fields = Fields(
    "first_name",
    "last_name",
    hobby=["name", "description"]
)

print(nested_fields)
```

```text
last_name first_name hobby { name description }
```

or even another `Fields` instance for even deeper selection.

```python
from qlient import Fields

nested_fields = Fields(
    "first_name",
    "last_name",
    hobby=Fields(
        "name",
        club="name"
    )
)

print(nested_fields)
```

```text
last_name first_name hobby { name club { name } }
```

## Supported Operators

The `Fields` class supports multiple operators.

### Addition

```python
from qlient import Fields

name = Fields("first_name", "last_name")
age = Fields("age")

added = name + age

print(added)
```

```text
first_name last_name age
```

### Subtraction

```python
from qlient import Fields

full_name = Fields("first_name", "last_name")
last_name = Fields("last_name")

subtracted = full_name - last_name

print(subtracted)
```

```text
first_name
```