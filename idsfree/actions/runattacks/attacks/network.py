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
from typing import Dict, Tuple, List

from ...helpers import generate_random_name


BASE_NMAP = (
    "k0st/nmap --send-eth --open -p {scan_ports} "
    "-oX /tmp/{results_file} {attacked_app_addr}")


def _nmap_command_with_plugins(ports_to_scan: str,
                               attacked_app: str,
                               *,
                               service_or_app_name: str = None) -> \
        Tuple[str, str]:

    results_file_name = "{name}.xml".format(
        name=generate_random_name(10, 15)
    )

    if service_or_app_name:
        SCRIPTS = '--script "default or *{service}*"'.format(
            service=service_or_app_name
        )
    else:
        SCRIPTS = '-sC'

    COMMAND = "{base} {scripts}".format(
        base=BASE_NMAP,
        scripts=SCRIPTS
    ).format(results_file=results_file_name,
             scan_ports=",".join(ports_to_scan),
             attacked_app_addr=attacked_app)

    return COMMAND, results_file_name


def run_all_net(ports_to_scan: str,
                attacked_app: List[str],
                *,
                service_or_app_name: str = None) -> Dict[str, Tuple[str, str]]:

    return {
        'nmap-net': _nmap_command_with_plugins(
            ports_to_scan,
            attacked_app,
            service_or_app_name=service_or_app_name
        )
    }


__all__ = ("run_all_net", )
