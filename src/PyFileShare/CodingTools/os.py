"""
    os tools

This file contains the os-relate tools for used for developing in python.
"""


""" imports """


import os
import shutil

from typing import Callable, Any

from .Function import ConsoleCaveat


""" os processes """

""" directory """


def mkdir(_path: str) -> bool:
    """
        Make directory
    :return bool: True if the directory was created.
    """
    if os.path.exists(_path): return False
    os.mkdir(_path)
    return True


caveat_rmtree = ConsoleCaveat.create(
    "Are you sure you want to delete '{path}'?",
)


def mk_rote(
        _start_path: str,
        _dir_names: tuple[str, ...],
) -> bool:
    """
    Make directory rote
    :return: True if the directory rote was created.
    """
    path = _start_path
    for dir_name in _dir_names:
        path = os.path.join(path, dir_name)
        mkdir(path)
        continue
    return True


def rmtree(
        _path: str,
        caveat_process: Callable[[dict[str, Any]], bool] = caveat_rmtree
) -> bool:
    """
        Remove a directory and its contents

    :return bool: True if the directory and its contents were removed.
    """
    if not os.path.isdir(_path): return False
    if not caveat_process({"path": _path}): return False
    shutil.rmtree(_path)
    return True
