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
import asyncio
import logging

from typing import Tuple, Union

from .model import *
from ....core.exceptions import IdsFreeInsecureData
from ...helpers import check_remote_requisites, get_remote_ssh_connection, \
    wait_for_service, generate_random_name, run_service_or_stack, \
    SwamNetwork, ConfigLaunchService, ConfigLaunchSwarmCompose

log = logging.getLogger("idsfree")


async def create_remote_environment(config: IdsFreeRunShellCreateModel) \
        -> Union[Tuple[str, str, str],
                 IdsFreeInsecureData]:
    async with get_remote_ssh_connection(config) as connection:

        stack_prefix = "SHELL_{}".format(generate_random_name(5, 5))

        async with SwamNetwork(connection,
                               prefix=stack_prefix,
                               autoremove_network=False) as network_name:

            _attacked_app = generate_random_name(5, 5)
            _kali_app = generate_random_name(5, 5)

            if not config.swarm_compose:
                command_or_compose = ConfigLaunchService(_attacked_app,
                                                         config.target_docker_image)
            else:
                command_or_compose = ConfigLaunchSwarmCompose(
                    config.swarm_compose,
                    network_name
                )

            attacked_service_id = await run_service_or_stack(
                stack_prefix,
                connection,
                network_name,
                command_or_compose)

            #
            # Get free ports in remote machine
            #
            used_ports_raw = await connection.run(
                'sudo docker ps --format "{{ .Ports }}"')
            used_ports = set([x.split("/")[0]
                              for x
                              in used_ports_raw.stdout.splitlines()])
            while True:
                ssh_port = random.randint(1025, 65535)
                if ssh_port not in used_ports:
                    break

            #
            # Launch the kali with remote SSH
            #
            _kali_service_config = ConfigLaunchService(
                _kali_app,
                "rastasheep/ubuntu-sshd:16.04",
                publish_ports={str(ssh_port): "22"})

            log.error("Building remote Kali access")
            kali_service_id = await run_service_or_stack(stack_prefix,
                                                         connection,
                                                         network_name,
                                                         _kali_service_config)

            #
            # wait until the service is available
            #
            log.error("Waiting until the environment is ready")
            await wait_for_service(connection,
                                   network_name,
                                   kali_service_id,
                                   ssh_port)

        return stack_prefix, attacked_service_id, ssh_port


def run_shell_create_idsfree(config: IdsFreeRunShellCreateModel) \
        -> Union[Tuple[str, str, str, str],
                 IdsFreeInsecureData]:
    """
    This functions does:

    - Check that remote host has required software and versions
    - Build the environment and launch the attacks
    - Load raw results, transform it and return in selected format as string

    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreeRunShellCreateModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    if not config.skip_check_requisites:
        loop.run_until_complete(check_remote_requisites(config))

    # Launch attacks
    stack_prefix, app_target_name, remote_port = \
        loop.run_until_complete(create_remote_environment(config))

    return stack_prefix, app_target_name, remote_port, config.remote_host


__all__ = ("run_shell_create_idsfree",)
