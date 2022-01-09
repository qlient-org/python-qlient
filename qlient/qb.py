from typing import Optional, List, Dict


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
        return self + other

    def __add__(self, other) -> "Fields":
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


class GQLQueryBuilder:

    def __init__(self):
        self.action_field: str = ""
        self.operation_field: str = ""
        self.fields_field: Optional[Fields] = None

    def fields(self, *args, **kwargs):
        self.fields_field = Fields(*args, **kwargs)

    def action(self, action: str):
        self.action_field = action

    def query(self):
        self.action("query")

    def mutation(self):
        self.action("mutation")

    def build(self) -> str:
        pass
