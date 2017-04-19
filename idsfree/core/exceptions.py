class IdsFreeError(Exception):
    pass


class IdsFreeValueError(ValueError):
    pass


class IdsFreeInsecureData(ValueError):
    pass


class IdsFreeTypeError(TypeError):
    pass


__all__ = ("IdsFreeError", "IdsFreeValueError", "IdsFreeTypeError",
           "IdsFreeInsecureData")
