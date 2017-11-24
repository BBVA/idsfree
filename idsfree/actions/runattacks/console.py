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
from ...core.helpers import *

log = logging.getLogger('idsfree')


def launch_idsfree_runattasks_in_console(config: IdsFreeRunAttacksModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting attacks of remote host...")

        results = run_runattasks_idsfree(config)

        # Export results
        with open(config.output_results_path, "w") as f:
            f.write(results)


__all__ = ("launch_idsFree_in_console",)
