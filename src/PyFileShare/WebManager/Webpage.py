"""
    Webpage processes

This file contains the Webpage-relate processes used for manage webpages.
"""


""" imports """


import os
from CodingTools import mkdir, rmtree, mk_rote

from typing import Any, Callable

from flask import Flask

from .WebpageMeta import (
    WebpageMetaKeys,
    create_webpage_meta,
    META_NAME,
    read_webpage_meta, access_webpage_meta, META_FORMAT,
)

from CodingTools.Function import ConsoleCaveat


""" rename """


WMK: WebpageMetaKeys = WebpageMetaKeys


"""
    Webpage manager
"""


""" Constants """


WEB_DATA: str = "webpage data"
WEB_META: str = "webpage meta"


""" Functions """


def get_webpage_meta(
        _meta_path: str
) -> dict[str, Any]:
    """
    Return webpage meta.
    :return: Webpage meta data.
    """
    create_webpage_meta(_meta_path)
    webpage_meta = read_webpage_meta(_meta_path)
    return webpage_meta


def gen_webpage_directory(
        _dist_path: str,
        _webpage_meta: dict[str, Any],
) -> str:
    """
        Generate webpage directory.
    :return: path to webpage directory.
    """
    rmtree_conf_access_keys: tuple[str, ...] = (
        WMK.CONFIG, WMK.RMTREE_SELF
    )
    webpage_rmtree_conf: bool = access_webpage_meta(
        _webpage_meta,
        rmtree_conf_access_keys
    )

    name_access_keys: tuple[str, ...] = (WMK.WEBPAGE, WMK.NAME)
    webpage_name: str = access_webpage_meta(
        _webpage_meta,
        name_access_keys,
    )

    webpage_data_path = os.path.join(_dist_path, webpage_name)
    if webpage_rmtree_conf:
        rmtree(webpage_data_path)
    mkdir(webpage_data_path)

    return webpage_data_path


def recognition_web_datas(
        _path: str,
        use_meta_file: bool = True,
) -> dict[str, str]:
    """"""

    """ create dist """
    mkdir(_path)

    """ gen meta file """
    webpage_meta_path = os.path.join(_path, META_NAME)

    webpage_meta: dict[str: Any] = None
    if use_meta_file:
        webpage_meta = get_webpage_meta(webpage_meta_path)
        ...

    if webpage_meta is None:
        webpage_meta = META_FORMAT
        ...

    """ gen webpage data file """
    webpage_data_path =\
        gen_webpage_directory(_path, webpage_meta)

    """ gen path dict """
    path_dict: dict[str, str] = {
        WEB_META: webpage_meta_path,
        WEB_DATA: webpage_data_path,
    }

    return path_dict


caveat_exist = ConsoleCaveat.create(
    ConsoleCaveat.Message.ALREADY_EXISTS
)


def add_webpage(
        _web_dir_path: str,
        _file_path_in_web_dir: str,
        _page_source: str,
        caveat_process: Callable[[dict[str, str]], bool] = caveat_exist,
) -> bool:
    """
    Add page source in web datas.
    :return: True if the file was created.
    """
    _file_path_in_web_dir =\
        _file_path_in_web_dir.replace("/", "\\")

    mk_rote(_web_dir_path, os.path.split(_file_path_in_web_dir)[:-1])

    page_path = os.path.join(_web_dir_path, _file_path_in_web_dir)

    print(page_path)

    if os.path.isfile(page_path):
        if not caveat_process({"path": page_path}):
            return False
        ...

    with open(page_path, "w") as page_file:
        page_file.write(_page_source)
        ...

    return True


def read_file(
        _path: str,
        encoding: str = "utf-8"
) -> str:
    """
    Read file from path.
    :return:  file content text.
    """
    with open(_path, "r", encoding=encoding) as file:
        text = file.read()
    return text


def read_dir(
        _target_dir_path: str,
) -> dict[str, str | dict]:
    """
    Read directory from path.
    :return: readed directory contents.
    """

    """ init data """
    datas: dict[str, str | dict] = {}

    """ get contents """
    contents: list[str] = os.listdir(_target_dir_path)

    """ read process """
    for content in contents:
        content_path = os.path.join(_target_dir_path, content)

        if os.path.isdir(content_path):
            data = read_dir(content_path)
            ...
        else:
            data = read_file(content_path)
            ...

        datas[content.split(".")[0]] = data
        continue

    return datas


""" Manager """


class WebpageManager:
    """ Management webpages """

    """ Initializer """
    def __init__(
            self,
            app: Flask = Flask(__name__),
            webpage_dist_path: str = os.path.join("", "dist"),
    ) -> None:
        """ Initialize self settings """

        """ flask """
        self.__app = app
        self.__top_page = "index"

        """ recognition webpage data """
        self.__dist_path = webpage_dist_path

        path_dict = recognition_web_datas(self.dist_path)
        self.__meta_path = path_dict[WEB_META]
        self.__data_path = path_dict[WEB_DATA]

        return

    """ flask """
    __app: Flask
    @property
    def app(self) -> Flask: return self.__app

    __route: str
    @property
    def route(self) -> str: return self.__route

    __top_page: str
    @property
    def top_page(self) -> str: return self.__top_page

    class PageFuncs:
        ...

    def __flask_create_page(
            self,
            _route: str,
            _page_source: str,
    ) -> None:
        """ Add page source in web datas """
        _route_hash: int = abs(hash(_route))
        code: str =(
            f"def create_page(app, route, page_source):\n"
            f"  @app.route(route)\n"
            f"  def webpage_{_route_hash}():\n"
            f"      return page_source\n"
            f"  return None\n"
            f"\n"
            f"create_page(app, route, page_source)\n"
        )
        app = self.__app
        route = _route
        page_source = _page_source
        exec(code, globals(), locals())
        return

    def __flask_create_pages(
            self,
            _web_datas: dict[str, str | dict],
            top_page: str = "index",
            target_route: str = ".",
    ) -> None:
        """ Create pages from web datas """

        """ create pages """
        for name, content in _web_datas.items():
            route = target_route + "/" + name

            if isinstance(content, dict):
                self.__flask_create_pages(
                    _web_datas[name], top_page, route,
                )
                ...
            else:
                self.__flask_create_page(
                    target_route[1:]+"/" if name == top_page else route[1:],
                    content,
                )
                ...

            continue

        return

    def run(
            self,
            host: str = '127.0.0.1',
            port: int = 5000,
            debug: bool = False,
    ) -> None:
        """ Run webpage """

        web_datas: dict[str, str | dict] =\
            read_dir(self.__data_path)

        self.__flask_create_pages(web_datas, self.__top_page)

        self.__app.run(
            host=host,
            port=port,
            debug=debug,
        )
        return

    """ web datas """
    __dist_path: str
    @property
    def dist_path(self) -> str: return self.__dist_path

    __meta_path: str
    @property
    def meta_path(self) -> str: return self.__meta_path

    __data_path: str
    @property
    def data_path(self) -> str: return self.__data_path

    """ web page manage functions """

    def add_page(
            self,
            _path_in_web_dir: str,
            _page_source: str,
            caveat_process: Callable[[dict[str, str]], bool] = caveat_exist,
    ) -> bool:
        """
        Add page source in web datas.
        :return: True if the file was created.
        """
        return add_webpage(
            self.__data_path,
            _path_in_web_dir,
            _page_source,
            caveat_process
        )

    ...
