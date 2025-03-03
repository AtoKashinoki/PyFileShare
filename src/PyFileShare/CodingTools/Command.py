"""
    Command tools

This file contains the command-related tools used for developing in Python.
"""


""" imports """


import sys
from abc import abstractmethod
from typing import Any

from .Inheritance import InheritanceSkeleton


""" Command Skeleton """


class CommandSkeleton(InheritanceSkeleton):
    """ Command class skeleton """

    """ Initialize  """
    def __init__(
            self,
            help_message: str = None,
            names: tuple = None,
            help_names: tuple = ("-h", "--help"),
    ):
        """ Initialize method """
        """ set name """
        if names is None:
            self.__names = (self.__class__.__name__, )
            ...
        else:
            self.__names = names
            ...

        """ set help """
        self.__help: Help = (
            Help(help_message, help_names)
            if help_message is not None else
            None
        )

        return

    """ name """
    __names: tuple
    @property
    def names(self) -> tuple: return self.__names

    """ help command """
    @property
    def help(self): return self.__help

    """ Command process """
    @abstractmethod
    def __command__(self, argv: tuple) -> Any or None: ...

    """ Call command """
    def __call__(self, argv: tuple = tuple(sys.argv)) -> Any or None:
        """ Call command """
        return self.__command__(tuple(argv))

    """ debug """

    ...


class Help(CommandSkeleton):
    """ Help command """

    """ Initializer """
    def __init__(self, message: str, names: tuple=None):
        super().__init__(names=("-h", "--help") if names is None else names)
        self.__message = message
        return

    """ message """
    __message: str
    @property
    def message(self) -> str: return self.__message

    """ command """
    def __command__(self, argv: tuple) -> Any or None:
        """ Display help message """
        print(self.__message)
        return None

    """ debug """
    def __repr__(self) -> str:
        return self.__message

    ...
