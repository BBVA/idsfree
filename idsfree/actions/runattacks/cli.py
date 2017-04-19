import click
import getpass
import logging

from .model import IdsFreeRunAttacksModel
from .console import launch_idsfree_runattasks_in_console
from ..helpers import check_console_input_config


log = logging.getLogger('idsfree')


@click.command(help="Run attacks using a remote host")
@click.pass_context
@click.argument('docker_image')
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
@click.option('-s',
              '--service-name',
              'service_name',
              help="service name to test. I.e: redis")
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
