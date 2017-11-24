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

log = logging.getLogger('idsfree')


def launch_idsfree_shell_create_in_console(config: IdsFreeRunShellCreateModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting attacks of remote host...")

        stack_name, app_name, remote_port, remote_ip = run_shell_create_idsfree(config)

        #
        # Show results
        #
        print("\n ", "-" * 60)
        print("  #\n  # Your stack ID is: {}\n  #".format(
            stack_name,
        ))
        print(" ", "-" * 60)
        print("\n   Your kali instance is ready. To connect you should type:")
        print("\n    > ssh -p {port} root@{host}".format(
            port=remote_port,
            host=remote_ip
        ))
        print("\n        >> SSH PASSWORD: root <<")
        print("\n   Your kali instance is ready. To connect you should type:")
        msg = "\n   To reach attacked app you should use the name: '{app}'. " \
              "For example: \n" \
              "  \n    > ping {app}" \
              "  \n    > nmap -sS -p 80,8080 {app}".format(app=app_name)

        print(msg)
        print("\n\n ", "-" * 60)
        print("\n Notes:")
        print("\n   - If you want to launch 'nmap' be sure to add the option "
              "'--send-eth' to make the scan successfully")


__all__ = ("launch_idsfree_shell_create_in_console",)
