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


def generate_random_name(mininum: int = 10, maximum: int = 40):
    return "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(mininum, maximum)))


class SwamNetwork:
    """Context manager that creates a new docker Swarm cyphered network and
    delete at exit"""

    def __init__(self,
                 config: IdsFreeRunAttacksModel,
                 con: SSHClientConnection):
        self.con = con
        self.config = config

        # Generates network name
        self.remote_cyphered_network = generate_random_name()

    async def __aenter__(self):

        log.error("Creating temporal encrypted network: {}".format(
            self.remote_cyphered_network))

        await self.con.run("docker network create --opt encrypted {net_name}"
                           .format(net_name=self.remote_cyphered_network))

        return self.remote_cyphered_network

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        log.error("Removing temporal encrypted network: {}".format(
            self.remote_cyphered_network))

        await self.con.run("docker network rm {net_name}"
                           .format(net_name=self.remote_cyphered_network))

ALLOWED_VALUES_FOR_COMMAND = re.compile(r'^[\d\w\_\/\\\.\-\:]*$')


def check_sanitized_input_for_command(message: str) -> bool:
    if not message:
        return True

    if ALLOWED_VALUES_FOR_COMMAND.match(message):
        return True
    else:
        return False


__all__ = ("expand_ports", "generate_random_name", "SwamNetwork",
           "check_sanitized_input_for_command")
