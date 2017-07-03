import re
import random
import string
import logging

from typing import Set, Union
from asyncssh import SSHClientConnection

from .model import *

log = logging.getLogger("idsfree")


def expand_ports(raw_ports: str) -> Set[int]:

    total_ports = set()

    for port_element in raw_ports.split(","):

        if "-" in port_element:
            _p = port_element.split("-", maxsplit=1)

            if len(_p) == 2 and all(x for x in _p):
                sorted(_p)
                port_start = int(_p[0])
                port_end = int(_p[1])

                ports_ranges = range(port_start, port_end)

            else:

                # If more than 2 elements of less than 1, only get the first
                # port at start port and the end port
                ports_ranges = [_p[0]]

        else:
            ports_ranges = [port_element]

        total_ports.update(ports_ranges)

    return total_ports


ALLOWED_VALUES_FOR_COMMAND = re.compile(r'^[\d\w\_\/\\\.\-\:]*$')


def check_sanitized_input_for_command(message: str) -> bool:
    if not message:
        return True

    if ALLOWED_VALUES_FOR_COMMAND.match(message):
        return True
    else:
        return False


__all__ = ("expand_ports",
           "check_sanitized_input_for_command")
