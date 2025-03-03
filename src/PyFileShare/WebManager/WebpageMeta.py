"""
    Webpage meta tools

This file contains the WebpageMeta-relate tools used for recognizing webpage datas.
"""


""" imports """


import os

from CodingTools import Any, Callable

from CodingTools import DataClass
from CodingTools.Function import ConsoleCaveat
from CodingTools import initialize

from json import dumps, loads


"""
    Webpage meta
"""


""" Constants """


@initialize()
class WebpageMetaKeys(DataClass):
    """ Webpage meta key constants """
    WEBPAGE: str = "webpage"
    NAME: str = "name"
    DATA: str = "data"
    CONFIG: str = "config"
    RMTREE_SELF: str = "rmtree self"
    ...

WebpageMetaKeys: WebpageMetaKeys
WMK: WebpageMetaKeys = WebpageMetaKeys


META_NAME: str = "webpage_meta"
META_FORMAT: dict[str: str] = \
    {
        WMK.WEBPAGE: {
            WMK.NAME: "Webpage",
            WMK.DATA: "src",
        },
        WMK.CONFIG: {
            WMK.RMTREE_SELF: True,
        }
    }


""" Create meta file """


caveat_init_meta = ConsoleCaveat.create(
    ConsoleCaveat.Message.ALREADY_EXISTS
)



def create_webpage_meta(
        _path: str,
        caveat_process: Callable[[dict[str, Any]], bool] = caveat_init_meta,
) -> bool:
    """
    Create a webpage meta file.
    :return: True if the file was created.
    """
    if os.path.isfile(_path):
        if not caveat_process({"path": _path}): return False
        os.remove(_path)
        ...

    with open(_path, "w") as meta_file:
        meta_file.write(
            dumps(
                META_FORMAT,
                indent=4,
                separators=(",", ": ")
            )
        )
        ...

    return True


""" read metafile """


def read_webpage_meta(
        _path: str,
) -> dict[str, Any]:
    """
    Read a webpage meta file.
    :return: Webpage meta data.
    """
    with open(_path, "r") as meta_file:
        web_meta = loads(meta_file.read())
        ...
    return web_meta


""" Access meta datas """


def access_webpage_meta(
        _meta_data: dict[str, Any],
        _access_key: tuple[str, ...]
) -> Any:
    """
    Access webpage meta data.
    :return: Any data in webpage meta data.
    """
    _data = _meta_data

    for key in _access_key:
        _data = _data[key]
        continue

    return _data
