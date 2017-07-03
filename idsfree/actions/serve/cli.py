import click
import getpass
import logging

from .model import IdsFreeRunServeRemoveModel
from ..helpers import check_console_input_config
from .console import launch_idsfree_serve_in_console

log = logging.getLogger('idsfree')


@click.command(help="Launch REST api")
@click.pass_context
def serve(ctx, **kwargs):

    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)
    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreeRunServeRemoveModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_serve_in_console(config)


__all__ = ("serve", )
