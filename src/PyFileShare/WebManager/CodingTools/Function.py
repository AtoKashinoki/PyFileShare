"""
    Function tools

This file contains the Function-relate tools used for developing in Python.
"""


""" imports """


from typing import Callable, Any


"""
    Functions
"""


""" Caveat functions """


class ConsoleCaveat:
    """ Functions about caveat """

    class Message:
        """ Caveatting message """
        ALREADY_EXISTS: str ="'{path}' already exists.\nOverwrite it?"
        ...

    @staticmethod
    def create(
            message: str = "Are you sure?",
            choices: dict = {"Y": True, "n": False}
    ) -> Callable[[dict], bool]:
        """ Create function that caveat in console. """

        def caveat(formats: dict = {}) -> bool:
            """
                Caveat function
            :return bool: True if the user was approved.
            """
            user_reply = input(
                f"{message.format(**formats)} "
                f"[{'|'.join(choices.keys())}]: ")
            if not user_reply in choices:
                return False
            return choices[user_reply]

        return caveat

    ...
