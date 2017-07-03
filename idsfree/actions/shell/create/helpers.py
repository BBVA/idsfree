import logging

from asyncssh import SSHClientConnection

from .model import *
from ..helpers import generate_random_name

log = logging.getLogger("idsfree")


class SwamNetwork:
    """Context manager that creates a new docker Swarm cyphered network and
    delete at exit"""

    def __init__(self,
                 config: IdsFreeRunShellCreateModel,
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


__all__ = ("SwamNetwork", )
