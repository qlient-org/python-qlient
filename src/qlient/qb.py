""" This file contains the query builder and fields

:author: Daniel Seifert
:created: 13.01.2022
"""
from typing import Optional, List, Dict, Any, Tuple

from qlient.schema.models import Input, Type
from qlient.settings import Settings


class Fields:
    @classmethod
    def parse_args(
            cls,
            args: Tuple[Any],
            fields: List[str] = None,
            sub_fields: Dict[str, "Fields"] = None
    ) -> Tuple[List[str], Dict[str, "Fields"]]:
        fields = fields or []
        sub_fields = sub_fields or {}
        for arg in args:
            if isinstance(arg, cls):
                fields += arg.fields  # noqa
                sub_fields.update(arg.sub_fields)  # noqa
                continue
            if isinstance(arg, str):
                arg = arg.strip()
                if not arg:
                    continue
                fields.append(arg)
                continue
            if isinstance(arg, list):
                fields += cls(*arg).fields  # noqa
                continue
            if isinstance(arg, dict):
                sub_fields.update(cls(**arg).sub_fields)  # noqa
                continue
            raise TypeError(f"Can't handle type `{type(arg).__name__}`")

        fields = list(dict.fromkeys(fields))  # drop duplicates but preserve order
        return fields, sub_fields

    @classmethod
    def parse_kwargs(
            cls,
            kwargs: Dict[Any, Any],
            fields: List[str] = None,
            sub_fields: Dict[str, "Fields"] = None
    ) -> Tuple[List[str], Dict[str, "Fields"]]:
        fields = fields or []
        sub_fields = sub_fields or {}
        for key, value in kwargs.items():
            if isinstance(value, str):
                value = Fields(value)
            if isinstance(value, list):
                value = cls(*value)
            if isinstance(value, dict):
                value = cls(**value)
            if isinstance(value, cls):
                sub_fields[key] = value
                continue
            raise TypeError(f"Can't handle type `{type(value).__name__}`")
        return fields, sub_fields

    def __init__(self, *args, **kwargs):
        _fields: List[str] = []
        _sub_fields: Dict[str, "Fields"] = {}

        _fields, _sub_fields = self.parse_args(args, _fields, _sub_fields)
        _fields, _sub_fields = self.parse_kwargs(kwargs, _fields, _sub_fields)

        self.fields: List[str] = _fields
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
        if other is None:
            return self.__class__(*self.fields, **self.sub_fields)
        if isinstance(other, str):
            other = Fields(other)
        if isinstance(other, (list, tuple)):
            other = Fields(*other)
        if isinstance(other, dict):
            other = Fields(**other)
        if isinstance(other, self.__class__):
            args = self.fields + other.fields
            kwargs = {**self.sub_fields}
            for key, value in other.sub_fields.items():
                if key not in kwargs:
                    kwargs[key] = self.__class__()
                kwargs[key] += value
            return self.__class__(*args, **kwargs)

    def __sub__(self, other) -> "Fields":
        """ Subtract another object from this fields

        :param other: holds the object to subtract
        :return: a new instance of this class with subtracted fields
        """
        if other is None:
            return self.__class__(*self.fields, **self.sub_fields)
        if isinstance(other, dict):
            other = Fields(**other)
        if isinstance(other, (list, tuple)):
            other = Fields(*other)
        if isinstance(other, str):
            other = Fields(other)
        if isinstance(other, self.__class__):
            args = [field for field in self.fields if field not in other.fields]
            kwargs = {**self.sub_fields}
            for key, value in other.sub_fields.items():
                if key not in kwargs:
                    continue
                kwargs[key] -= value

                # if the key is empty after subtraction, delete it
                if not kwargs[key]:
                    del kwargs[key]
            return self.__class__(*args, **kwargs)

    def __bool__(self) -> bool:
        return bool(self.fields) or bool(self.sub_fields)

    def __str__(self) -> str:
        builder = list(self.fields)
        for name, fields in self.sub_fields.items():
            builder.append(f"{name} {{ {str(fields)} }}")
        return " ".join(builder)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name}(gql='{str(self)}')>"

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

    def __init__(
            self,
            operation_type: str,
            operation_name: str,
            operation_inputs: Dict[str, Input],
            operation_output: Optional[Type],
            settings: Settings,
    ):
        self.settings: Settings = settings
        self.op_type: str = operation_type
        self.op_name: str = operation_name
        self.op_inputs: Dict[str, Input] = operation_inputs
        self.op_output: Optional[Type] = operation_output
        self.builder: GQLQueryBuilder = GQLQueryBuilder()
        self.builder.operation(self.op_type, self.op_name)
        self.builder.action(self.op_name)

    def fields(self, *args, **kwargs):
        if self.settings.validate_fields and self.op_output is not None:
            # do input field validation
            pass
        self.builder.fields(*args, **kwargs)

    def variables(self, **kwargs) -> Dict:
        operation_variables = {}
        action_variables = {}

        for key, value in kwargs.items():
            if self.settings.validate_variables:
                if key not in self.op_inputs:
                    raise KeyError(f"Input `{key}` not supported for {self.op_type} operation `{self.op_name}`")
            _input: Input = self.op_inputs[key]
            prefixed_key = f"{self.KEY_PREFIX}{key}"
            operation_variables[prefixed_key] = _input.type.graphql_representation
            action_variables[key] = prefixed_key

        self.builder.operation(self.op_type, self.op_name, operation_variables)
        self.builder.action(self.op_name, action_variables)
        return kwargs

    def build(self) -> str:
        return self.builder.build()
