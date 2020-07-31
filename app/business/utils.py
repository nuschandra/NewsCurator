import json
from enum import Enum

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name

        return json.JSONEncoder.default(self, obj)

    # def as_enum(d):
    #     if "__enum__" in d:
    #         name, member = d["__enum__"].split(".")
    #         return getattr(PUBLIC_ENUMS[name], member)
    #     else:
    #         return d