from enum import Enum


class BaseEnum(Enum):
    def __init__(self, value, title):
        self.code = value
        self.title = title

    @classmethod
    def get_codes(cls):
        return [obj.code for obj in cls]

    @classmethod
    def get_choices(cls):
        return [(obj.code, obj.title) for obj in cls]
