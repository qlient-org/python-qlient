""" This file contains the graphql schema class

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
import logging
from typing import Optional, Dict, List, Any, Union

from qlient import __about__
from qlient.cache import Cache
from qlient.settings import Settings
from qlient.transport import Transport


class TypeRef:
    """ Represents a basic graphql Type Reference """

    kind: Optional[str]
    name: Optional[str]
    of_type: Optional["TypeRef"]

    @classmethod
    def parse(cls, type_ref: Union["TypeRef", Dict]) -> "TypeRef":
        """ Parse a single type reference

        :param type_ref: holds the type reference to parse
        :return: the parsed type ref
        """
        if isinstance(type_ref, dict):
            type_ref = cls(**type_ref)
        if not isinstance(type_ref, cls):
            raise TypeError(f"Expected dict, {cls.__name__} got {type(type_ref)}")
        return type_ref

    @classmethod
    def parse_list(cls, type_refs: Optional[List[Union["TypeRef", Dict]]]) -> List["TypeRef"]:
        """ Parse a list of type_refs

        :param type_refs: holds the type_ref list to parse
        :return: a list of type_refs
        """
        return [
            cls.parse(type_ref)
            for type_ref in type_refs
            if type_ref
        ] if type_refs else []

    def __init__(
            self,
            kind: Optional[str] = None,
            name: Optional[str] = None,
            ofType: Optional["TypeRef"] = None
    ):
        self.kind = kind
        self.name = name
        self.of_type = self.parse(ofType) if ofType else None


class Input:
    """ Represents a basic graphql Input """

    name: Optional[str]
    description: Optional[str]
    type: Optional[TypeRef]
    default_value: Optional[Any]

    @classmethod
    def parse(cls, input_value: Union["Input", Dict]) -> "Input":
        """ Parse a single input value

        :param input_value: holds the input value to parse
        :return: the parsed input
        """
        if isinstance(input_value, dict):
            input_value = cls(**input_value)
        if not isinstance(input_value, cls):
            raise TypeError(f"Expected dict, {cls.__name__} got {type(input_value)}")
        return input_value

    @classmethod
    def parse_list(cls, inputs: Optional[List[Union["Input", Dict]]]) -> List["Input"]:
        """ Parse a list of inputs

        :param inputs: holds the input list to parse
        :return: a list of inputs
        """
        return [
            cls.parse(input_value)
            for input_value in inputs
            if input_value
        ] if inputs else []

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            type: Optional[TypeRef] = None,
            defaultValue: Optional[Any] = None
    ):
        self.name = name
        self.description = description
        self.type = TypeRef.parse(type) if type else None
        self.default_value = defaultValue


class Directive:
    """ Represents a basic graphql Directive """
    name: Optional[str]
    description: Optional[str]
    locations: Optional[List[str]]
    args: Optional[List[Input]]

    @classmethod
    def parse(cls, directive: Union["Directive", Dict]) -> "Directive":
        """ Parse a single directive

        :param directive: holds the directive to parse
        :return: the parsed directive
        """
        if isinstance(directive, dict):
            directive = cls(**directive)
        if not isinstance(directive, cls):
            raise TypeError(f"Expected dict, {cls.__name__} got {type(directive)}")
        return directive

    @classmethod
    def parse_list(cls, directives: Optional[List[Union["Directive", Dict]]]) -> List["Directive"]:
        """ Parse a list of directives

        :param directives: holds the directive list to parse
        :return: a list of directives
        """
        return [
            cls.parse(directive)
            for directive in directives
            if directive
        ] if directives else []

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            locations: Optional[List[str]] = None,
            args: Optional[List[Input]] = None
    ):
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self.locations: Optional[List[str]] = locations
        self.args: List[Input] = Input.parse_list(args)


class Field:
    """ Represents a basic graphql Field """
    name: Optional[str]
    description: Optional[str]
    args: Optional[List[Input]]
    type: Optional[TypeRef]
    is_deprecated: Optional[bool]
    deprecation_reason: Optional[str]

    @classmethod
    def parse(cls, field: Union["Field", Dict]) -> "Field":
        """ Parse a single field

        :param field: holds the field to parse
        :return: the parsed field
        """
        if isinstance(field, dict):
            field = cls(**field)
        if not isinstance(field, cls):
            raise TypeError(f"Expected dict, {cls.__name__} got {type(field)}")
        return field

    @classmethod
    def parse_list(cls, fields: Optional[List[Union["Field", Dict]]]) -> List["Field"]:
        """ Parse a list of fields

        :param fields: holds the field list to parse
        :return: a list of fields
        """
        return [
            cls.parse(field)
            for field in fields
            if field
        ] if fields else []

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            args: Optional[List[Input]] = None,
            type: Optional[TypeRef] = None,
            isDeprecated: Optional[bool] = None,
            deprecationReason: Optional[str] = None
    ):
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self.args: List[Input] = Input.parse_list(args)
        self.type: Optional[TypeRef] = TypeRef.parse(type) if type else None
        self.is_deprecated: Optional[bool] = isDeprecated
        self.deprecation_reason: Optional[str] = deprecationReason


class EnumValue:
    """ Represents a basic graphql enum value """

    @classmethod
    def parse(cls, enum_value: Union["EnumValue", Dict]) -> "EnumValue":
        """ Parse a single field

        :param enum_value: holds the field to parse
        :return: the parsed field
        """
        if isinstance(enum_value, dict):
            enum_value = cls(**enum_value)
        if not isinstance(enum_value, cls):
            raise TypeError(f"Expected dict, {cls.__name__} got {type(enum_value)}")
        return enum_value

    @classmethod
    def parse_list(cls, enum_values: Optional[List[Union["EnumValue", Dict]]]) -> List["EnumValue"]:
        """ Parse a list of enum values

        :param enum_values: holds the list of enum values to parse
        :return: a list of enum values
        """
        return [
            cls.parse(enum_value)
            for enum_value in enum_values
            if enum_value
        ] if enum_values else []

    def __init__(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            isDeprecated: Optional[bool] = None,
            deprecationReason: Optional[str] = None
    ):
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self.is_deprecated: Optional[bool] = isDeprecated
        self.deprecation_reason: Optional[str] = deprecationReason


class Type:
    """ Represents a basic graphql Type """

    kind: Optional[str]
    name: Optional[str]
    description: Optional[str]
    fields: Optional[List[Field]]
    input_fields: Optional[List[Input]]
    interfaces: Optional[List[TypeRef]]
    enum_values: Optional[List[EnumValue]]
    possible_types: Optional[List[TypeRef]]

    @classmethod
    def parse(cls, type_value: Union["Type", Dict]) -> "Type":
        """ Parse a single field

        :param type_value: holds the field to parse
        :return: the parsed field
        """
        if isinstance(type_value, dict):
            type_value = cls(**type_value)
        if not isinstance(type_value, cls):
            raise TypeError(f"Expected dict, {cls.__name__} got {type(type_value)}")
        return type_value

    def __init__(
            self,
            kind: Optional[str] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            fields: Optional[List[Union[Field, Dict]]] = None,
            inputFields: Optional[List[Union[Input, Dict]]] = None,
            interfaces: Optional[List[Union[TypeRef, Dict]]] = None,
            enumValues: Optional[List[Union[EnumValue, Dict]]] = None,
            possibleTypes: Optional[List[Union[TypeRef, Dict]]] = None
    ):
        self.kind: Optional[str] = kind
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self.fields: List[Field] = Field.parse_list(fields)
        self.input_fields: List[Input] = Input.parse_list(inputFields)
        self.interfaces: List[TypeRef] = TypeRef.parse_list(interfaces)
        self.enum_values: List[EnumValue] = EnumValue.parse_list(enumValues)
        self.possible_types: List[TypeRef] = TypeRef.parse_list(possibleTypes)


class Schema:
    """ Represents a graphql schema """

    logger = logging.getLogger(__about__.__title__)

    def __init__(self, location: str, transport: Transport, settings: Settings, cache: Optional[Cache]):
        self.location: str = location
        self.transport: Transport = transport
        self.settings: Settings = settings
        self.cache: Optional[Cache] = cache

        self.schema: Optional[Dict] = None

        self.query_type: Optional[Type] = None
        self.mutation_type: Optional[Type] = None
        self.subscription_type: Optional[Type] = None
        self.types: Optional[List[Type]] = None
        self.directives: Optional[List[Directive]] = None

        self.introspect()  # prepare the schema for further usage

    def introspect(self):
        """ Load the schema definition """
        self.logger.debug("Schema introspection started")
        from qlient.schema.loader import load_schema
        self.schema: Dict = load_schema(self.location, self.transport, self.cache)
        self.logger.debug("Schema loaded")

        from qlient.schema.parser import parse_schema, ParseResult
        parse_result: ParseResult = parse_schema(self.schema)
        self.logger.debug("Schema parsed")

        self.query_type = parse_result.query_type
        self.mutation_type = parse_result.mutation_type
        self.subscription_type = parse_result.subscription_type
        self.types = parse_result.types
        self.directives = parse_result.directives
        self.logger.debug("Schema successfully introspected")
