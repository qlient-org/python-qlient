""" This file contains the query builder and fields

:author: Daniel Seifert
:created: 13.01.2022
"""
from typing import Optional, List, Dict, Any, Tuple

from qlient.schema.schema import Schema
from qlient.schema.types import (
    Input as SchemaInput,
    Type as SchemaType,
    Directive as SchemaDirective,
    Field as SchemaField,
    TypeRef as SchemaTypeRef,
)
from qlient.settings import Settings


class Directive:
    def __init__(
            self,
            _name: str,
            **directive_variables
    ):
        self.name: str = _name
        self.variables = directive_variables

    def prepare(self, schema: Schema) -> "PreparedDirective":
        p = PreparedDirective()
        p.prepare(
            schema=schema,
            name=self.name,
            variables=self.variables,
        )
        return p

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can not compare other classes than {self.__class__.__name__}")
        return hash(self) == hash(other)


class PreparedDirective:
    def __init__(self):
        # the graphql schema directive type
        self.schema_directive: Optional[SchemaDirective] = None
        # the name of the directive
        self.name: Optional[str] = None
        # a dictionary with the variable name mapped to the variable reference
        self.var_name_to_var_ref: Optional[Dict[str, str]] = None
        # a dictionary with the variable reference mapped to the variable value
        self.var_ref_to_var_value: Optional[Dict[str, Any]] = None
        # a dictionary with the variable reference mapped to the variable type
        self.var_ref_to_var_input: Optional[Dict[str, SchemaTypeRef]] = None

    def prepare(
            self,
            schema: Schema,
            name: Optional[str] = None,
            variables: Optional[Dict[str, Any]] = None,
    ):
        self.prepare_name(name)
        self.prepare_type_checking(schema)
        self.prepare_input(variables)

    def prepare_type_checking(self, schema: Schema):
        if not self.name:
            raise ValueError(f"Name must be set before calling `{self.prepare_type_checking.__name__}`")
        schema_directive = schema.directives_registry.get(self.name)
        if schema_directive is None:
            raise ValueError(f"No directive found with name `{self.name}` in schema.")
        self.schema_directive = schema_directive

    def prepare_name(self, name: Optional[str]):
        if not name:
            raise ValueError("Directive name must have a value.")
        self.name = name

    def prepare_input(self, variables: Optional[Dict[str, Any]]):
        if not self.name:
            raise ValueError(f"Name must be set before calling `{self.prepare_input.__name__}`")
        if self.schema_directive is None:
            raise ValueError(f"Directive must be set before calling `{self.prepare_input.__name__}`")
        ref_prefix = f"{self.name}_{id(self)}"
        var_to_ref = {}
        ref_to_val = {}
        ref_to_type = {}
        for key, value in variables.items():
            input_type: Optional[SchemaInput] = self.schema_directive.arg_name_to_arg.get(key)
            if input_type is None:
                raise ValueError(f"Input `{key}` not supported for directive {self.name}")
            ref_key = f"{ref_prefix}_{key}"
            var_to_ref[key] = ref_key
            ref_to_val[ref_key] = value
            ref_to_type[ref_key] = input_type.type

        self.var_name_to_var_ref = var_to_ref
        self.var_ref_to_var_value = ref_to_val
        self.var_ref_to_var_input = ref_to_type

    def __gql__(self) -> str:
        builder = f"@{self.name}"
        if self.var_name_to_var_ref:
            builder += "("
            builder += " ".join(map(
                lambda name_to_ref: f"{name_to_ref[0]}: ${name_to_ref[1]}",
                self.var_name_to_var_ref.items()
            ))
            builder += ")"
        return builder

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can not compare other classes than {self.__class__.__name__}")
        return hash(self) == hash(other)


class Field:

    def __init__(
            self,
            _name: str,
            _alias: Optional[str] = None,
            _directive: Optional[Directive] = None,
            _sub_fields: Optional[Any] = None,
            **field_variables
    ):
        self.name: str = _name
        self.alias: Optional[str] = _alias
        self.directive: Optional[Directive] = _directive
        self.sub_fields: Optional["Fields"] = Fields(_sub_fields) if _sub_fields is not None else None
        self.variables: Dict[str, Any] = field_variables

    def __and__(self, other) -> "Fields":
        return self.__add__(other)

    def __add__(self, other) -> "Fields":
        if isinstance(other, (str, self.__class__)):
            other = Fields(other)
        if isinstance(other, (list, tuple, set)):
            other = Fields(*other)
        if isinstance(other, dict):
            other = Fields(**other)
        if isinstance(other, Fields):
            return Fields(self) + other
        raise TypeError(f"Can not handle type `{type(other)}`")

    def prepare(self, parent: SchemaType, schema: Schema) -> "PreparedField":
        p = PreparedField()
        p.prepare(
            parent=parent,
            schema=schema,
            name=self.name,
            alias=self.alias,
            directive=self.directive,
            sub_fields=self.sub_fields,
            variables=self.variables
        )
        return p

    def __hash__(self) -> int:
        return hash((self.alias, self.name, self.directive, self.sub_fields))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can not compare other classes than {self.__class__.__name__}")
        return hash(self) == hash(other)


class PreparedField:
    def __init__(self):
        # the graphql schema field type
        self.schema_field: Optional[SchemaField] = None
        # the name of the field
        self.name: Optional[str] = None
        # the alias of the field
        self.alias: Optional[str] = None
        # the directive of the field
        self.directive: Optional[PreparedDirective] = None
        # a sub selection of fields of this type
        self.sub_fields: Optional[PreparedFields] = None
        # a dictionary with the variable name mapped to the variable reference
        self.var_name_to_var_ref: Optional[Dict[str, str]] = None
        # a dictionary with the variable reference mapped to the variable value
        self.var_ref_to_var_value: Optional[Dict[str, Any]] = None
        # a dictionary with the variable reference mapped to the variable type
        self.var_ref_to_var_input: Optional[Dict[str, SchemaTypeRef]] = None

    def prepare(
            self,
            parent: SchemaType,
            schema: Schema,
            name: Optional[str] = None,
            alias: Optional[str] = None,
            directive: Optional[Directive] = None,
            sub_fields: Optional[Any] = None,
            variables: Optional[Dict[str, Any]] = None,
    ):
        self.prepare_name(name, alias)
        self.prepare_type_checking(parent)
        self.prepare_directive(schema, directive)
        self.prepare_input(variables)
        self.prepare_sub_fields(schema, sub_fields)

    def prepare_name(self, name: Optional[str], alias: Optional[str]):
        if not name:
            raise ValueError("Directive name must have a value.")
        self.name = name
        self.alias = alias

    def prepare_type_checking(self, parent: SchemaType):
        if not self.name:
            raise ValueError(f"Name must be set before calling `{self.prepare_type_checking.__name__}`")
        schema_field_type = parent.field_name_to_field.get(self.name)
        if schema_field_type is None:
            raise ValueError(f"No Field found with name `{self.name}` in schema.")
        self.schema_field = schema_field_type

    def prepare_directive(self, schema: Schema, directive: Optional[Directive]):
        if directive is None:
            return
        self.directive = directive.prepare(schema)

    def prepare_sub_fields(self, schema: Schema, sub_fields: Optional["Fields"]):
        if sub_fields is None:
            return
        new_parent = self.schema_field.type.leaf_type
        self.sub_fields = sub_fields.prepare(new_parent, schema)

    def prepare_input(self, variables: Optional[Dict[str, Any]]):
        if not self.name:
            raise ValueError(f"Name must be set before calling `{self.prepare_input.__name__}`")
        if self.schema_field is None:
            raise ValueError(f"Field must be set before calling `{self.prepare_input.__name__}`")
        ref_prefix = f"{f'{self.alias}_' if self.alias else ''}{self.name}_{id(self)}"
        var_to_ref = {}
        ref_to_val = {}
        ref_to_type = {}
        for key, value in variables.items():
            input_type: Optional[SchemaInput] = self.schema_field.arg_name_to_arg.get(key)
            if input_type is None:
                raise ValueError(f"Input `{key}` not supported for field {self.name}")
            ref_key = f"{ref_prefix}_{key}"
            var_to_ref[key] = ref_key
            ref_to_val[ref_key] = value
            ref_to_type[ref_key] = input_type.type

        self.var_name_to_var_ref = var_to_ref
        self.var_ref_to_var_value = ref_to_val
        self.var_ref_to_var_input = ref_to_type

    @property
    def rec_var_ref_to_var_input_type_ref(self) -> Dict[str, SchemaTypeRef]:
        ref_to_input_type_ref = self.var_ref_to_var_input.copy()
        if self.sub_fields is not None:
            ref_to_input_type_ref.update(self.sub_fields.var_ref_to_var_type)
        return ref_to_input_type_ref

    @property
    def rec_var_ref_to_var_value(self) -> Dict[str, Any]:
        ref_to_value = self.var_ref_to_var_value.copy()
        if self.sub_fields is not None:
            ref_to_value.update(self.sub_fields.var_ref_to_var_value)
        return ref_to_value

    def __gql__(self) -> str:
        builder = f"{f'{self.alias}: ' if self.alias else ''}{self.name}"
        if self.var_name_to_var_ref:
            builder += "("
            builder += " ".join(map(
                lambda name_to_ref: f"{name_to_ref[0]}: ${name_to_ref[1]}",
                self.var_name_to_var_ref.items()
            ))
            builder += ")"
        if self.directive is not None:
            builder += f" {self.directive.__gql__()}"
        if self.sub_fields is not None:
            builder += f" {{ {self.sub_fields.__gql__()} }}"
        return builder

    def __hash__(self) -> int:
        return hash((self.alias, self.name, self.directive, self.sub_fields))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can not compare other classes than {self.__class__.__name__}")
        return hash(self) == hash(other)


class Fields:
    @classmethod
    def parse_args(
            cls,
            args: Tuple[Any],
            fields: Dict[int, Field] = None,
    ) -> Dict[int, Field]:
        fields = fields or {}
        for arg in args:
            if isinstance(arg, str):
                arg = arg.strip()
                if not arg:
                    continue
                arg = Field(arg)
            if isinstance(arg, Field):
                fields[hash(arg)] = arg
                continue
            if isinstance(arg, (list, tuple, set)):
                arg = cls(*arg)
            if isinstance(arg, dict):
                arg = cls(**arg)
            if isinstance(arg, cls):
                for field in arg.selected_fields:
                    fields[hash(field)] = field
                continue
            raise TypeError(f"Can't handle type `{type(arg).__name__}`")

        return fields

    @classmethod
    def parse_kwargs(
            cls,
            kwargs: Dict[Any, Any],
            fields: Dict[int, Field] = None,
    ) -> Dict[int, Field]:
        fields = fields or {}
        for key, value in kwargs.items():
            field = Field(key, _sub_fields=cls(value))
            fields[hash(field)] = field
        return fields

    def __init__(self, *args, **kwargs):
        _fields: Dict[int, Field] = {}

        _fields = self.parse_args(args, _fields)
        _fields = self.parse_kwargs(kwargs, _fields)

        self.selected_fields: List[Field] = list(_fields.values())

    def __contains__(self, item) -> bool:
        return item in self.selected_fields

    def __and__(self, other) -> "Fields":
        """ Synthetic sugar method which essentially just does the __add__

        :param other: holds the other instance to add to this instance
        :return: a new Fields instance with the added properties
        """
        return self.__add__(other)

    def __add__(self, other) -> "Fields":
        """ Add another object to this fields

        :param other: the object to add
        :return: a new instance of this class with the added fields
        """
        cls = self.__class__
        if other is None:
            return cls(*self.selected_fields)
        if isinstance(other, (str, Field)):
            other = cls(other)
        if isinstance(other, (list, tuple, set)):
            other = cls(*other)
        if isinstance(other, dict):
            other = cls(**other)
        if isinstance(other, cls):
            args = [*self.selected_fields, *other.selected_fields]
            return cls(*args)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can not compare other classes than {self.__class__.__name__}")
        return hash(self) == hash(other)

    def __bool__(self) -> bool:
        return bool(self.selected_fields)

    def __hash__(self) -> int:
        return hash(tuple(self.selected_fields))

    def prepare(self, parent: SchemaType, schema: Schema) -> "PreparedFields":
        p = PreparedFields()
        p.prepare(
            parent=parent,
            schema=schema,
            fields=self.selected_fields,
        )
        return p


class PreparedFields:
    def __init__(self):
        # the prepared fields
        self.fields: Optional[List[PreparedField]] = None

    def prepare(
            self,
            parent: SchemaType,
            schema: Schema,
            fields: Optional[List[Field]] = None
    ):
        self.prepare_fields(parent, schema, fields)

    def prepare_fields(self, parent: SchemaType, schema: Schema, fields: Optional[List[Fields]]):
        self.fields = [
            field.prepare(parent, schema)
            for field in fields
        ]

    @property
    def var_ref_to_var_type(self) -> Dict[str, SchemaTypeRef]:
        ref_to_type = {}
        for field in self.fields:
            ref_to_type.update(field.rec_var_ref_to_var_input_type_ref)
        return ref_to_type

    @property
    def var_ref_to_var_value(self) -> Dict[str, Any]:
        ref_to_value = {}
        for field in self.fields:
            ref_to_value.update(field.rec_var_ref_to_var_value)
        return ref_to_value

    def __gql__(self) -> str:
        return " ".join(
            field.__gql__()
            for field in self.fields
        )

    def __hash__(self) -> int:
        return hash(tuple(self.fields))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can not compare other classes than {self.__class__.__name__}")
        return hash(self) == hash(other)


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
            nested_keys = []

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
        self.fields_field: Optional[str] = None

    def fields(self, fields: str) -> "GQLQueryBuilder":
        self.fields_field = fields
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
        query_parts = [self.operation_field, "{", self.action_field]
        if self.fields_field:
            query_parts.append("{")
            query_parts.append(self.fields_field)
            query_parts.append("}")
        query_parts.append("}")
        final_query = " ".join(query_parts)
        return self.remove_duplicate_spaces(final_query)

    def __gql__(self) -> str:
        return self.build()


class TypedGQLQueryBuilder:

    def __init__(
            self,
            operation_type: str,
            operation_field: SchemaField,
            schema: Schema,
            settings: Settings,
    ):
        self.settings: Settings = settings
        self.op_type: str = operation_type
        self.op_field: SchemaField = operation_field
        self.op_name: str = self.op_field.name
        self.op_inputs: Dict[str, SchemaInput] = self.op_field.arg_name_to_arg
        self.op_output: Optional[SchemaType] = schema.types_registry.get(self.op_field.output_type_name)
        self.schema: Schema = schema
        self.builder: GQLQueryBuilder = GQLQueryBuilder()
        self.builder.operation(self.op_type, self.op_name)
        self.builder.action(self.op_name)

        self._fields: Optional[PreparedFields] = None
        self._operation_variables: Optional[Dict[str, Any]] = {}
        self._action_variables: Optional[Dict[str, Any]] = {}

    def fields(self, *args, **kwargs) -> Dict[str, Any]:
        self._fields = Fields(*args, **kwargs).prepare(self.op_output, self.schema)
        for var_ref, var_type_ref in self._fields.var_ref_to_var_type.items():
            prefixed_key = f"${var_ref}"
            self._operation_variables[prefixed_key] = var_type_ref.__gql__()

        return self._fields.var_ref_to_var_value

    def variables(self, **kwargs) -> Dict[str, Any]:
        for key in kwargs.keys():
            if self.settings.validate_variables:
                if key not in self.op_inputs:
                    raise KeyError(f"Input `{key}` not supported for {self.op_type} operation `{self.op_name}`")
            _input: SchemaInput = self.op_inputs[key]
            prefixed_key = f"${key}"
            self._operation_variables[prefixed_key] = _input.type.__gql__()
            self._action_variables[key] = prefixed_key

        return kwargs

    def build(self) -> str:
        if self._fields is not None:
            self.builder.fields(self._fields.__gql__())
        if self._operation_variables is not None:
            self.builder.operation(self.op_type, self.op_name, self._operation_variables)
        if self._action_variables is not None:
            self.builder.action(self.op_name, self._action_variables)
        return self.builder.build()

    def __gql__(self) -> str:
        return self.build()
