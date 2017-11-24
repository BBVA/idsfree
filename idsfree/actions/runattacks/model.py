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

from idsfree import SharedWithSSHRemove, String


class IdsFreeRunAttacksModel(SharedWithSSHRemove):
    output_results_path = String(default="")
    output_results_format = String(default="json")
    attacks_type = String(default="net")
    port_to_check = String(default="80")
    service_name = String(default="")
    target_docker_image = String()
    swarm_compose = String()

    ATTACKS_TYPES = ('net', "web")
    RESULTS_FORMATS = ('json', 'junit')


class SecurityResult:

    SECURITY_LEVELS = ("none", "informational", "low", "middle", "high",
                       "critical")
    PORT_PROTOCOLS = ("TCP", "UDP")

    __slots__ = ("tool_name", "port_number", "port_proto",
                 "vulnerability_type", "log", "payload", "extra_info",
                 "level", "tool_plugin_name", "tool_version")

    def __init__(self,
                 tool_name: str,
                 port_number: int,
                 *,
                 tool_version: str = "",
                 tool_plugin_name: str = "",
                 level: str = "low",
                 extra_info: str = None,
                 payload: str = None,
                 log: str = None,
                 vulnerability_type: str = "net",
                 port_proto: str = "TCP"):
        assert port_proto.upper() in SecurityResult.PORT_PROTOCOLS
        assert level in SecurityResult.SECURITY_LEVELS

        self.tool_name = tool_name
        self.tool_version = tool_version
        self.tool_plugin_name = tool_plugin_name
        self.port_number = port_number
        self.port_proto = port_proto.upper()

        #: "net|xss|..."
        self.vulnerability_type = vulnerability_type
        self.log = log
        self.payload = payload
        self.extra_info = extra_info
        self.level = level

    @property
    def json(self):
        return dict(
            toolName=self.tool_name,
            portNumber=self.port_number,
            portProto=self.port_proto,
            vulnerabilityType=self.vulnerability_type,
            log=self.log,
            payload=self.payload,
            extraInfo=self.extra_info,
            level=self.level
        )

__all__ = ("IdsFreeRunAttacksModel", "SecurityResult")
