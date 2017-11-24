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
from ....core.exceptions import IdsFreeNotFoundError
from ...helpers import check_remote_requisites, get_remote_ssh_connection, \
    remove_service_or_stack

log = logging.getLogger("idsfree")


async def remove_remote_environment(config: IdsFreeRunShellRemoveModel) \
        -> IdsFreeNotFoundError:

    async with get_remote_ssh_connection(config) as connection:

        await remove_service_or_stack(connection,
                                      config.stack_id,
                                      auto_remove_network=True)


def run_shell_remove_idsfree(config: IdsFreeRunShellRemoveModel) \
        -> IdsFreeNotFoundError:
    """
    This functions does:

    - Check that remote host has required software and versions
    - Build the environment and launch the attacks
    - Load raw results, transform it and return in selected format as string

    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreeRunShellRemoveModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    if not config.skip_check_requisites:
        loop.run_until_complete(check_remote_requisites(config))

    # Launch attacks
    loop.run_until_complete(remove_remote_environment(config))


__all__ = ("run_shell_remove_idsfree",)
