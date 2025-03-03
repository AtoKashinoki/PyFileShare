"""
    Type error tools

This file contains the TypeError-relate tools used for developing in Python.
"""


""" imports """


from typing import Any

from .Skeleton import gen_skeleton, ErrorSkeleton


""" error """


TypeError = gen_skeleton(TypeError)


class ValidError(TypeError, ErrorSkeleton):
    """ Valid to set value """

    __message__ = "Value {value}[{value_type}] is not a valid type."

    def __init__(self, value: Any) -> None:
        super().__init__(value=value, value_type=type(value))
        return

    ...



