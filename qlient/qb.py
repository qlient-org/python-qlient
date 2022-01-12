from typing import Optional, List, Dict, Any

from qlient.schema.models import Field, Input


class Fields:
    """
    Fields(a, b, c) -> Fields(a, b, c)
    Fields(a, b, c=Fields(d, e, f)) -> Fields(a, b, c=Fields(d, e, f))
    Fields(Fields(a, b), Fields(c, d, e=f)) -> Fields(a, b, c, d, e=f)
    foo = Fields(a, b) & Fields(c, d) -> Fields(a, b, c, d)
    """

    def __init__(self, *args, **kwargs):
        _fields: List[str] = []
        _sub_fields: Dict[str, "Fields"] = {}

        for arg in args:
            if isinstance(arg, self.__class__):
                _fields += arg.fields  # noqa
                _sub_fields.update(arg.sub_fields)  # noqa
                continue
            if isinstance(arg, str):
                _fields.append(arg)
                continue
            if isinstance(arg, list):
                _fields += self.__class__(*arg).fields  # noqa
                continue
            if isinstance(arg, dict):
                _sub_fields.update(self.__class__(**arg).sub_fields)  # noqa
                continue
            raise TypeError(f"Can't handle type `{type(arg).__name__}`")

        for key, value in kwargs.items():
            if isinstance(value, str):
                value = Fields(value)
            if isinstance(value, list):
                value = self.__class__(*value)
            if isinstance(value, self.__class__):
                _sub_fields[key] = value
                continue
            raise TypeError(f"Can't handle type `{type(value).__name__}`")

        self.fields: List[str] = list(set(_fields))
        self.sub_fields: Dict[str, "Fields"] = _sub_fields

    def __and__(self, other) -> "Fields":
        """ Synthetic sugar method which essentially just does the __add__

        :param other: holds the other instance to add to this instance
        :return: a new Fields instance with the added properties
        """
        return self + other

    def __add__(self, other) -> "Fields":
        """ Add another object to this fields

        :param other: the object to add
        :return: a new instance of this class with the added fields
        """
        if isinstance(other, self.__class__):
            args = list(set(self.fields + other.fields))
            kwargs = {**self.sub_fields, **other.sub_fields}
            return self.__class__(*args, **kwargs)
        if isinstance(other, str):
            return self.__class__(*list(self.fields + [other]), **self.sub_fields)
        if isinstance(other, list):
            return self.__class__(*list(self.fields + other), **self.sub_fields)
        if isinstance(other, dict):
            return self.__class__(*self.fields, **{**self.sub_fields, **other})

    def __sub__(self, other) -> "Fields":
        """ Subtract another object from this fields

        :param other: holds the object to subtract
        :return: a new instance of this class with subtracted fields
        """
        if isinstance(other, self.__class__):
            args = list(set(self.fields) - set(other.fields))
            kwargs = {**self.sub_fields}
            for key in other.sub_fields:
                if key not in kwargs:
                    continue
                del kwargs[key]
            return self.__class__(*args, **kwargs)
        if isinstance(other, str):
            return self.__class__(*list(set(self.fields) - set(other)), **self.sub_fields)
        if isinstance(other, list):
            return self.__class__(*list(set(self.fields) - set(other)), **self.sub_fields)
        if isinstance(other, dict):
            kwargs = {**self.sub_fields}
            for key in other:
                if key not in kwargs:
                    continue
                del kwargs[key]
            return self.__class__(*self.fields, **kwargs)

    def __str__(self) -> str:
        builder = list(self.fields)
        for name, fields in self.sub_fields.items():
            builder.append(f"{name} {{ {str(fields)} }}")
        return " ".join(builder)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.fields == other.fields and self.sub_fields == other.sub_fields


class GQLQueryBuilder:

    @staticmethod
    def remove_duplicate_spaces(query: str) -> str:
        return " ".join(query.split())

    @staticmethod
    def build_input(variables: Dict[str, Any], initial_str: str) -> str:
        inputs: List[str] = []

        final_str = initial_str

        if variables:
            key = list(variables.keys())[0]
            nested_keys = list()

            while isinstance(variables[key], dict):
                nested_keys.append(key)
                variables: Dict = variables[key]
                key = list(variables.keys())[0]

            for key, value in variables.items():
                if nested_keys:
                    inputs.append(f'{key}: "{value}"')  # Nested input won't have double quotes

                else:
                    inputs.append(f"{key}: {value}")

            final_str += "("

            for key in nested_keys:
                final_str = final_str + key + ": {"

            final_str = final_str + ", ".join(inputs)

            for _ in nested_keys:
                final_str += "}"

            final_str += ")"

        return final_str

    def __init__(self):
        self.operation_field: str = ""
        self.action_field: str = ""
        self.fields_field: Optional[Fields] = None

    def fields(self, *args, **kwargs) -> "GQLQueryBuilder":
        self.fields_field = Fields(*args, **kwargs)
        return self

    def action(self, action: str, variables: Dict[str, Any] = None) -> "GQLQueryBuilder":
        action = self.build_input(variables, action)
        self.action_field = action
        return self

    def operation(
            self,
            operation: str,
            name: str = "",
            variables: Dict[str, Any] = None
    ) -> "GQLQueryBuilder":
        if name:
            operation = f"{operation} {name}"
            operation = self.build_input(variables, operation)
        self.operation_field = operation
        return self

    def query(self, **kwargs) -> "GQLQueryBuilder":
        return self.operation("query", **kwargs)

    def mutation(self, **kwargs) -> "GQLQueryBuilder":
        return self.operation("mutation", **kwargs)

    def build(self) -> str:
        query_parts = []
        query_parts.append(self.operation_field)
        query_parts.append("{")
        query_parts.append(self.action_field)
        if self.fields_field:
            query_parts.append("{")
            query_parts.append(str(self.fields_field))
            query_parts.append("}")
        query_parts.append("}")
        final_query = " ".join(query_parts)
        return self.remove_duplicate_spaces(final_query)


class TypedGQLQueryBuilder:
    KEY_PREFIX = "$"

    def __init__(self, operation_type: str, operation_field: Field):
        self.op_type: str = operation_type
        self.op_field: Field = operation_field
        self.op_inputs: Dict[str, Input] = {_input.name: _input for _input in self.op_field.args}
        self.builder: GQLQueryBuilder = GQLQueryBuilder()
        self.builder.operation(self.op_type, self.op_field.name)
        self.builder.action(self.op_field.name)

    def fields(self, *args, **kwargs):
        self.builder.fields(*args, **kwargs)

    def variables(self, **kwargs) -> Dict:
        operation_variables = {}
        action_variables = {}

        for key, value in kwargs.items():
            if key not in self.op_inputs:
                raise KeyError(f"Input `{key}` not supported for {self.op_type} operation `{self.op_field.name}`")
            _input: Input = self.op_inputs[key]
            prefixed_key = f"{self.KEY_PREFIX}{key}"
            operation_variables[prefixed_key] = _input.type.graphql_representation
            action_variables[key] = prefixed_key

        self.builder.operation(self.op_type, self.op_field.name, operation_variables)
        self.builder.action(self.op_field.name, action_variables)
        return kwargs

    def build(self) -> str:
        return self.builder.build()
