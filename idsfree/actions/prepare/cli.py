import click
import getpass
import logging

from .model import IdsFreeDefaultModel
from .console import launch_idsfree_prepare_in_console
from ..helpers import check_console_input_config


log = logging.getLogger('idsfree')


@click.command(help="Install required software in remote host")
@click.pass_context
def prepare(ctx, **kwargs):
    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)

    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreeDefaultModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_prepare_in_console(config)


__all__ = ("prepare", )
