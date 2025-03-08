"""
    PyFileShare

This file contains PyFileShare-relate tools used for share py files.
"""


""" imports """


import os
from datetime import datetime

from typing import Callable

from flask import Flask
from .WebManager import WebpageManager

import qrcode
from qrcode.image.pil import PilImage
from PIL import Image


"""
    processes 
"""


""" share process """


def share_pages(
        _pages: dict,
        host: str = "127.0.0.1",
        port: int = 5000,
        web_page_dist_path: str = os.path.join("", "dist"),
) -> None:
    """ Share the page on your webpage. """

    """ setup """
    app = Flask(__name__)
    webpage = WebpageManager(app, web_page_dist_path, False)

    """ add pages """
    name: str
    source: str
    for name, source in _pages.items():
        webpage.add_page(name, source.replace("\n", "<br>"))
        continue

    """ qrcode """
    qr_path = os.path.join(web_page_dist_path, "host_qrcode.png")
    qr_img: PilImage = qrcode.make(f"http://{host}:{port}")
    qr_img.save(qr_path)

    qr_img: Image.Image = Image.open(qr_path)
    qr_img.show()

    """ running """
    webpage.run(host, port)
    return


""" share directory """


def read_file(_path: str) -> str:
    """ Read and return file contents """
    contents = f"<h5># {_path.split(os.sep)[-1]}</h5>"
    with open(_path, "r") as f:
        contents += f.read()
        ...
    return contents


def get_directory_datas(
        _directory_path: str,
        target_extension: str = "py",
) -> dict:
    """ Return contents in directory """

    datas: dict = {}

    """ get contents """
    contents: list = os.listdir(_directory_path)

    """ add index """

    """ get datas """
    content: str
    for content in contents:
        content_path = os.path.join(_directory_path, content)

        if os.path.isfile(content_path):
            """ content is file """

            if content[-len(target_extension):] == target_extension:
                """ content extension is target """
                datas[content] = (
                    read_file(content_path),
                    datetime.fromtimestamp(os.path.getmtime(content_path)),
                )
                ...

            continue

        else:
            """ content is directory """
            datas[content] = get_directory_datas(
                content_path, target_extension
            )
            ...

        continue

    return datas


def pages_from(
        _dir_datas: dict,
        index_generator: Callable[[str, dict], str]
) -> dict:
    """ Reform and return _dir_datas """

    def reform(_datas: dict, route: str = ".") -> dict:
        """ Reform datas """
        pages: dict = {}
        contents: dict = {}

        """  Reform """
        for name, content in _datas.items():
            content_route = f"{route}/{name}"
            contents[content_route] = (
                name, content,
            )

            if isinstance(content, tuple):
                pages[content_route] = content[0]
                ...

            else:
                pages = {
                    **pages,
                    **reform(content, content_route)
                }
                ...

            continue

        pages[f"{route}/index"] = index_generator(route, contents)
        return pages

    return reform(_dir_datas)


def gen_index_page(name: str, contents: dict) -> str:
    """ Generate index page """
    content: str = f"<h3>{name}<br>directory content links</h3>"
    for link, content_ in contents.items():
        name_ = content_[0]
        date = ""
        if isinstance(content_[1], tuple):
            date = "["+str(content_[1][1]).split(".")[0]+"]"
            ...
        content += f"<a href='{link[1:]}'>{name_}{date}</a><br>"
        continue
    return content


def share_directory(
        _directory_path: str,
        host: str = "127.0.0.1",
        port: int = 5000,
        index_generator: Callable[[str, dict], str] = gen_index_page
) -> None:
    """ Share the directory on your webpage."""

    """ get share dates """
    datas: dict = get_directory_datas(_directory_path)

    """ Reform datas """
    pages = pages_from(datas, index_generator)

    """ share """
    share_pages(pages, host, port,)

    return

