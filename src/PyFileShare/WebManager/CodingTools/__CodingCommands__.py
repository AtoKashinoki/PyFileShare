"""
    Coding commands

This file contains the CodingCommand-relate tools used for developing in Python.
"""


""" imports """


from os import path, mkdir
from abc import ABC
from typing import Any, Callable

from .Wrapper import initialize
from .Command import CommandSkeleton


"""  commands """


class CodingToolsCommandSkeleton(CommandSkeleton, ABC):
    """ CodingTools commands skeleton """

    """ options """
    __options: dict[tuple[str, ...], Callable[[tuple[str, ...]], None]] = None

    def add_options(
            self,
            _options: dict[tuple[str, ...], Callable[[tuple[str, ...]], None]],
    ) -> None:
        if self.__options is None: self.__options = {}
        for key, value in _options.items():
            self.__options[key] = value
            ...
        return

    """ command process """
    def __command__(self, argv: tuple[str, ...]) -> Any | None:
        """ toml command process """
        command_argv = argv[1:]
        if len(command_argv) == 0 or command_argv[0] in self.help.names:
            self.help()
            return None

        for option in self.__options:
            if command_argv[0] not in option:
                continue

            result = self.__options[option](command_argv)
            if result is not None: print(result)

            break

        else:
            print(f"Option '{command_argv[0]}' is not found.")
            self.help()
            ...

        return None

    ...


@initialize()
class Toml(CodingToolsCommandSkeleton):
    """ Management toml file command """

    """ Settings """
    __help_message__: str = (
        "toml command help\n"
        "   toml [options]\n"
        "\n"
        "   options\n"
        "       [-h] or [--help]\n"
        "       Print toml command help\n"
        "\n"
        "       [create] or [-c]\n"
        "       Create toml file\n"
    )
    __names__: tuple[str, ...] = ("toml", )

    __toml_file__: str = "pyproject.toml"
    __toml_text__: str = (
        "[build-system]\n"
        "requires = ['setuptools']\n"
        "build-backend = 'setuptools.build_meta'\n"
        "\n"
        "\n"
        "[project]\n"
        "name = '<name>'\n"
        "version = '0.0.0'\n"
        "description = '<description>'\n"
        "\n"
        "readme = 'README.md'\n"
        "license = {file='LICENSE'}\n"
        "\n"
        "requires-python = '>=<python_version>'\n"
        "dependencies = [\n"
        "]\n"
        "\n"
        "authors = [\n"
        "   {name='<your_name>', email='<EMAIL>'}\n"
        "]\n"
        "classifiers = [\n"
        "   'Development Status :: 3 - Alpha',\n"
        "   'Intended Audience :: Developers',\n"
        "   'License :: OSI Approved :: MIT License',\n"
        "   'Natural Language :: English',\n"
        "   'Operating System :: OS Independent',\n"
        "   'Programming Language :: Python :: 3.7',\n"
        "   'Programming Language :: Python :: 3.8',\n"
        "   'Programming Language :: Python :: 3.9',\n"
        "   'Programming Language :: Python :: 3.10',\n"
        "   'Programming Language :: Python :: 3.11',\n"
        "   'Programming Language :: Python :: 3.12',\n"
        "   'Programming Language :: Python :: 3.13',\n"
        "   'Programming Language :: Python :: Implementation :: CPython',\n"
        "   'Topic :: Software Development :: Libraries :: Python Modules',\n"
        "   'Topic :: Utilities',\n"
        "]\n"
        "\n"
        "\n"
        "[project.urls]\n"
        "'Homepage' = '<url>'\n"
        "'Bug Traker' = '<url>'\n"
        "'Documentation' = '<url>'\n"
        "'Source' = '<url>'\n"
        "\n"
        "\n"
        "[project.scripts]\n"
    )

    """ Initializer """
    def __init__(self):
        """ Initialize self """
        super().__init__(
            help_message=self.__help_message__,
            names=self.__names__,
        )

        self.add_options({
            ("create", "-c"): self.__create__,
        })
        return

    """ options """

    def __create__(self, argv: tuple[str, ...]) -> None:
        """ Create toml file """
        print("Create toml file...")

        if path.isfile(self.__toml_file__):
            print("File already exists.")
            next_keys: tuple[str, ...] = ("Y", "Yes")
            reply = input(f"Reset toml file? [{'|'.join(next_keys)}|n] -> ")
            if reply not in next_keys:
                print("Cancelled to create toml file...")
                return None
            ...

        with open(f"./{self.__toml_file__}", "w") as toml_file:
            toml_file.write(self.__toml_text__)
            ...

        print("Successfully created toml file.")
        return None

    ...

@initialize()
class Library(CodingToolsCommandSkeleton):
    """ Management about library command """

    """ Settings """
    __help_message__: str = (
        "Library command help\n"
        "   library [options]\n"
        "\n"
        "   options\n"
        "       [create] or [-c]\n"
        "       Create directory and toml of library.\n"
    )

    __names__: tuple[str, ...] = ("library", )

    __dirs__: tuple[str, ...] = ("./src", "./src/None")
    __files__: tuple[str, ...] = ("./src/None/__init__.py", )

    """ Initializer """
    def __init__(self):
        """ Initialize self """
        super().__init__(
            help_message=self.__help_message__,
            names=self.__names__,
        )

        self.add_options({
            ("create", "-c"): self.__create__,
        })
        return

    """ options """

    def __create__(self, argv: tuple[str, ...]) -> None:
        """ Create Library process """
        print("Create directory of library...")

        """ create library directories """
        for directory in self.__dirs__:
            if path.isdir(directory): continue
            mkdir(directory)
            continue

        """ create library files """
        for file in self.__files__:
            if path.isfile(file): continue
            with open(file, "w"): ...
            continue

        """ add toml file """
        Toml(("toml", "create"))

        print("Successfully created library.")
        return None

    ...


""" CodingTools command """


@initialize(
    (
        Toml,
        Library,
    )
)
class CodingTools(CommandSkeleton):
    """ CodingTools command """

    __help_massage__: str = (
        "CodingTools command help\n"
        "   CodingTools [Command] [options]\n"
        "\n"
        "   Command\n"
        "       [Help] or [-h]\n"
        "       Print help of CodingTools command\n"
        "\n"
        "       [toml]\n"
        "       Create toml file\n"
        "\n"
        "       [library]\n"
        "       Create directory and toml of library.\n"
    )

    """ Initialize """
    def __init__(self, commands: tuple[CommandSkeleton, ...]):
        """ Initialize command list """
        super().__init__(self.__help_massage__)
        self.__commands = commands
        return

    """ command list """
    __commands: tuple[CommandSkeleton, ...]
    @property
    def commands(self) -> tuple[CommandSkeleton, ...]:
        return self.__commands

    """ command process """
    def __command__(self, argv: tuple[str, ...]) -> Any | None:
        """ Access process """
        command_argv = argv[1:]
        if len(command_argv) == 0:
            self.help()
            return None

        """ validate and run command """
        for command in (*self.__commands, self.help):
            if not command_argv[0] in command.names:
                continue

            result = command(command_argv)
            if result is not None: print(result)

            break

        else:
            print(f"Command '{command_argv[0]}' is not found.")
            self.help()
            ...

        return None

    ...
