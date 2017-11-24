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
import click
import getpass
import logging

from .model import IdsFreeRunAttacksModel
from .console import launch_idsfree_runattasks_in_console
from ..helpers import check_console_input_config


log = logging.getLogger('idsfree')


@click.command(help="Run attacks using a remote host")
@click.pass_context
@click.argument('target_docker_image')
@click.option('-p',
              '--check-ports',
              'port_to_check',
              help="remote ports to check. Default: 80",
              default="80")
@click.option('-t',
              '--attacks-type',
              'attacks_type',
              help="attacks to performs. Default: 'net'",
              default="net",
              type=click.Choice(IdsFreeRunAttacksModel.ATTACKS_TYPES))
@click.option('-e',
              '--export-format',
              'output_results_format',
              help="format for output results. Default: json",
              default="json",
              type=click.Choice(IdsFreeRunAttacksModel.RESULTS_FORMATS))
@click.option('-o',
              '--results-file',
              'output_results_path',
              help="output results file path",
              default="idsfree-results.json")
@click.option('-n',
              '--service-name',
              'service_name',
              help="extra information about the service name to test. "
                   "I.e: redis")
@click.option('-s',
              '--swarm-compose',
              'swarm_compose',
              help="Swarm compose file for complex environments")
def run_attacks(ctx, **kwargs):
    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)
    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreeRunAttacksModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_runattasks_in_console(config)


__all__ = ("run_attacks", )
