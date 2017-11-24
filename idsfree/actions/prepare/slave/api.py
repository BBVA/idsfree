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
