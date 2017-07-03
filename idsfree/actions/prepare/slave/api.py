import asyncio
import logging

from .model import *
from ...helpers import check_remote_requisites, get_remote_ssh_connection

log = logging.getLogger("idsfree")


async def join_swarm(config: IdsFreePrepareSlaveModel):
    """
    Configures and return remote Swarm and encrypted network
    
    :return: tuple as format: (Swam listen add, cyphered network name)
    :rtype: tuple(str, str)
    """
    async with get_remote_ssh_connection(config) as con:
        log.error("Joining to Swarm cluster at IP: {}".format(
            config.remote_host))

        await con.run("docker swarm join --token {token} {addr}:2377"
                      .format(token=config.cluster_id,
                              addr=config.master_addr))


def run_prepare_slave_idsfree(config: IdsFreePrepareSlaveModel) -> str:
    """
    Check and prepare a remote host to run Swarm with and encrypted network.
    
    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreePrepareSlaveModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    loop.run_until_complete(check_remote_requisites(config))

    # Install Swarm
    loop.run_until_complete(join_swarm(config))


__all__ = ("run_prepare_slave_idsfree",)
