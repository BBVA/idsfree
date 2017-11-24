# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This file contains utils and reusable functions
"""

import os
import logging
import configparser

from os.path import exists
from collections import namedtuple
from contextlib import contextmanager


log = logging.getLogger('idsfree')


def load_idsfree_config(config_path: str = None) -> dict:
    """
    This function try load config from 'config_path'.

    If no info provided try to load from a file called .idsfree from:
    1 - Current path
    2 - User home and load

    """

    try:
        config = configparser.ConfigParser()

        if config_path and exists(config_path):
            config_path = os.path.abspath(config_path)

            config.read(config_path)

        curr_path = os.path.join(os.getcwd(), '.idsfreerc')  # Current path
        if not config.sections() and exists(curr_path):
            config.read(curr_path)

        user_home = os.path.expanduser('~/.idsfreerc')  # User home
        if not config.sections() and exists(user_home):
            config.read(user_home)

        return dict(config.items('DEFAULT'))

    except configparser.NoSectionError as e:
        log.error('Error parsing configuration file: {}'.format(
            e
        ))

        return {}


def dict_to_obj(data):
    """
    Transform an input dict into a object.

    >>> data = dict(hello="world", bye="see you")
    >>> obj = dict_to_obj(data)
    >>> obj.hello
    'world'

    :param data: input dictionary data
    :type data: dict
    """
    assert isinstance(data, dict)

    if not data:
        return namedtuple("OBJ", [])

    obj = namedtuple("OBJ", list(data.keys()))

    return obj(**data)


def get_log_level(verbosity: int) -> int:
    verbosity *= 10

    if verbosity > logging.CRITICAL:
        verbosity = logging.CRITICAL

    if verbosity < logging.DEBUG:
        verbosity = logging.DEBUG

    return logging.CRITICAL - verbosity


@contextmanager
def run_in_console(debug=False):
    try:
        yield
    except Exception as e:
        log.critical(" !! {}".format(e))

        if debug:
            log.critical(e, exc_info=True)
    finally:
        log.debug("Shutdown...")


__all__ = ("dict_to_obj", "get_log_level", "run_in_console",
           "load_idsfree_config")
