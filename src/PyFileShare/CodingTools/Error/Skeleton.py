"""
    Error class skeleton

This file contains the ErrorClass-relate skeleton used for developing in Python.
"""


""" imports """


from abc import ABC, abstractmethod


""" skeleton """


class ErrorSkeleton(ABC):
    """ Error class skeleton """

    """ message """
    __message__: str

    ...


def gen_skeleton(
        _super_error_class: type = Exception,
) -> type:
    """ Generate error class skeleton """

    class Skeleton(_super_error_class, ErrorSkeleton):
        """ Error class skeleton """

        def __init__(self, **kwargs):
            """ Initialize message """
            super().__init__(
                self.__message__.format(
                    **kwargs,
                )
            )
            return

        ...

    return Skeleton
