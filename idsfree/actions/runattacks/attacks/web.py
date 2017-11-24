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
from typing import Dict, Tuple

from ...helpers import generate_random_name

BASE_NMAP = (
    "k0st/nmap --open -p {scan_ports} "
    "-oX /tmp/{results_file}.xml {attacked_app_addr}/24")


def _nmap_command_with_plugins(ports_to_scan: str,
                               attacked_app: str,
                               *,
                               service_or_app_name: str = None) -> \
        Tuple[str, str]:

    NMAP_SCRIPTS_WEB = (
        '--script "http* {app} and not *brute* and not *enum* and '
        'not external and not intrusive and not discovery and '
        'not malware"')

    results_file_name = "{name}.xml".format(
        name=generate_random_name(10, 15)
    )

    if service_or_app_name:
        SCRIPTS = NMAP_SCRIPTS_WEB.format(app="or *%s*" % service_or_app_name)
    else:
        SCRIPTS = NMAP_SCRIPTS_WEB.format(app="")

    COMMAND = "{base} {scripts}".format(
        base=BASE_NMAP,
        scripts=SCRIPTS
    ).format(results_file=results_file_name,
             scan_ports=",".join(ports_to_scan),
             attacked_app_addr=attacked_app)

    return COMMAND, results_file_name


def run_all_web(ports_to_scan: str,
                attacked_app: str,
                *,
                service_or_app_name: str = None) -> Dict[str, Tuple[str, str]]:
    return {
        'nmap-web': _nmap_command_with_plugins(
            ports_to_scan,
            attacked_app,
            service_or_app_name=service_or_app_name
        )
    }


__all__ = ("run_all_web", )
