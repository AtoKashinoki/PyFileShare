"""
    Attribute error tools

This file contains AttributeError-related tools used for developing in Python.
"""


""" imports """


from .Skeleton import gen_skeleton


""" Error """


AttributeError = gen_skeleton(AttributeError)


class DefinedError(AttributeError):
    """ Attribute define error """

    """ message """
    message: str = (
        "name '{name}' is not defined."
    )

    def __init__(self, _name: str) -> None:
        """ Initialize message """
        super().__init__(name=_name)
        return

    ...
