import random
import string
import asyncio
import logging

from typing import Tuple

from .model import *
from ..helpers import check_remote_requisites, get_remote_ssh_connection

log = logging.getLogger("idsfree")


async def setup_remote_swarm(config: IdsFreeDefaultModel) -> Tuple[str, str]:
    """
    Configures and return remote Swarm and encrypted network
    
    :return: tuple as format: (Swam listen add, cyphered network name)
    :rtype: tuple(str, str)
    """
    remote_cyphered_network = "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(10, 40)))

    async with get_remote_ssh_connection(config) as con:
        log.error("Initialization Swarm at IP: {}".format(config.remote_host))
        await con.run("docker swarm init --advertise-addr {listen_addr}"
                      .format(listen_addr=config.remote_host))

        log.error("Creating new encrypted network: {}".format(
            remote_cyphered_network))
        await con.run("docker network create --opt encrypted {net_name}"
                      .format(net_name=remote_cyphered_network))

        return config.remote_host, remote_cyphered_network


def run_prepare_idsfree(config: IdsFreeDefaultModel) -> str:
    """
    Check and prepare a remote host to run Swarm with and encrypted network.
    
    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreeDefaultModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    loop.run_until_complete(check_remote_requisites(config))

    # Install Swarm
    swarm_addr, net_name = loop.run_until_complete(setup_remote_swarm(config))

    return net_name


__all__ = ("run_prepare_idsfree",)
