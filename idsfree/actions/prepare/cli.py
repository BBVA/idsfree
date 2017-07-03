import click
import getpass
import logging

from .slave.console import *
from .master.console import *

from .slave.model import *
from .master.model import *

from ..helpers import check_console_input_config


log = logging.getLogger('idsfree')


@click.group(help="Check and prepare remote host for idsFree")
@click.pass_context
def prepare(ctx, **kwargs):
    pass


@prepare.command(help="Start new master server for build a cluster")
@click.pass_context
def master(ctx, **kwargs):
    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)

    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreePrepareMasterModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_prepare_master_in_console(config)


@prepare.command(help="Start new master server for build a cluster")
@click.pass_context
@click.argument('cluster_id')
@click.argument('master_addr')
def slave(ctx, **kwargs):
    if ctx.obj.get("ask_remote_password") is True:
        ctx.obj["remote_password"] = getpass.getpass("Remote SSH password: ",
                                                     stream=None)

    # Remote form the model
    ctx.obj.pop("ask_remote_password")

    config = IdsFreePrepareSlaveModel(**ctx.obj, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_idsfree_prepare_slave_in_console(config)


__all__ = ("prepare", )
