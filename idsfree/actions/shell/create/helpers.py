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
