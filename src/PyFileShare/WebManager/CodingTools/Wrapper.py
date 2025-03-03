"""
    Wrapper tools

This file contains wrapper-related tools used for developing in Python.
"""


""" imports """


from typing import Callable, Any
from functools import wraps

from .Inheritance import InheritanceSkeleton, abstractmethod


""" Wrapper skeleton """


class WrapperSkeleton(InheritanceSkeleton):
    """ Wrapper skeleton """

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any: ...

    ...


""" Wrapper class """


class Wrapper(WrapperSkeleton):
    """ Wrapper class """

    """ Generate wrapper """
    wrapper: Callable[[Any], Any]

    def __init__(self, _wrapper: Callable[[Any], Any]) -> None:
        """ Setting wrapper process """
        self.wrapper = _wrapper
        return

    """ Wrapping """
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """ Wrapp and return target """
        return self.wrapper(*args, **kwargs)

    ...


""" classtools wraps """


functools_wraps = wraps

@Wrapper
def classtools_wraps(
        _wrapped,
        _assigned = ("__module__", "__doc__"),
):
    """ wraps function about class """

    def wrapper(_target: Any):

        for attr in _assigned:
            setattr(_target, attr, getattr(_wrapped, attr))
            continue

        return _target

    return wrapper


""" initializer """


@Wrapper
def initialize(*args, **kwargs) -> Callable[[Any], Any]:
    """ Initialize target class """

    def wrapper(_target: Any) -> Any:
        return _target(*args, **kwargs)

    return wrapper
