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

from booby import *


class SharedConfig(Model):
    verbosity = Integer(default=0)
    debug = Boolean(default=False)
    config_file = String(default="")
    skip_check_requisites = Boolean(default=False)


class SharedWithSSHRemove(SharedConfig):
    timeout = Integer(default=10)
    remote_host = String(default="127.0.0.1")
    remote_port = Integer(default=22)
    remote_user = String(default="root")
    remote_password = String(default="toor")
    cert_path = String(default="")
