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
import random
import string
import asyncio
import logging

from typing import Tuple

from .model import *
from ...helpers import check_remote_requisites, get_remote_ssh_connection

log = logging.getLogger("idsfree")


async def setup_remote_swarm(config: IdsFreePrepareMasterModel) -> Tuple[str, str]:
    """
    Configures and return remote Swarm and encrypted network

    :return: tuple as format: (Swam listen add, cyphered network name)
    :rtype: tuple(str, str)
    """

    async with get_remote_ssh_connection(config) as con:
        log.error("Initialization Swarm at IP: {}".format(config.remote_host))
        cluster_id = await con.run("sudo docker swarm init "
                                   "--advertise-addr {listen_addr}"
                      .format(listen_addr=config.remote_host))

        if "This node is already part of a swarm" in cluster_id.stderr:
            cluster_id = await con.run("sudo docker swarm join-token manager")

        start = cluster_id.stdout.find("--token ") + len("--token ")
        cluster_id = \
            cluster_id.stdout[start: cluster_id.stdout.find(" ", start)]

        return config.remote_host, cluster_id


def run_prepare_master_idsfree(config: IdsFreePrepareMasterModel) -> Tuple[str, str]:
    """
    Check and prepare a remote host to run Swarm with and encrypted network.

    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreePrepareMasterModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    loop.run_until_complete(check_remote_requisites(config))

    # Install Swarm
    swarm_addr, cluster_id = loop.run_until_complete(
        setup_remote_swarm(config))

    return swarm_addr, cluster_id


__all__ = ("run_prepare_master_idsfree",)
