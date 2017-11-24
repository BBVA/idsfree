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

from .api import *
from .model import *
from ....core.helpers import *
from ....core.exceptions import IdsFreeNotFoundError

log = logging.getLogger('idsfree')


def launch_idsfree_shell_remove_in_console(config: IdsFreeRunShellRemoveModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting removing process of remote stack..")

        try:
            run_shell_remove_idsfree(config)

            log.console("Stack '{}' removed correctly".format(config.stack_id))

        except IdsFreeNotFoundError as e:
            log.console(e)


__all__ = ("launch_idsfree_shell_remove_in_console",)
