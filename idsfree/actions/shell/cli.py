import click
import getpass
import logging

from ..helpers import check_console_input_config

from .create.model import IdsFreeRunShellCreateModel
from .remove.model import IdsFreeRunShellRemoveModel

from .create.console import launch_idsfree_shell_create_in_console
from .remove.console import launch_idsfree_shell_remove_in_console

log = logging.getLogger('idsfree')


@click.group(help="Connect a Kali linux shell to an application")
@click.pass_context
def shell(ctx, **kwargs):
    pass


@shell.command(help="Create a remote environment with a shell")
@click.pass_context
@click.option('-s',
              '--swarm-compose',
              'swarm_compose',
              help="Swarm compose file for complex environments")
@click.argument('target_docker_image')
def create(ctx, **kwargs):

    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)
    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreeRunShellCreateModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_shell_create_in_console(config)


@shell.command(help="remove remove environment")
@click.pass_context
@click.argument("stack_id")
def remove(ctx, **kwargs):
    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)
    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreeRunShellRemoveModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_shell_remove_in_console(config)


__all__ = ("shell", )
