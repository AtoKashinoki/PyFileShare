"""
    Coordinate definitions

This file contains coordinate definitions used for developing in Python.
"""


""" imports """


from .Inheritance import DataClass


""" Definitions """


class Coordinate(DataClass):
    """ Coordinate definitions """

    class IDX(DataClass):
        """ Coordinate list index definitions """
        X, Y, Z = range(3)
        ...

    ...
