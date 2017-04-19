import click
import logging

from idsfree import global_options

from .prepare.cli import prepare
from .runattacks.cli import run_attacks

log = logging.getLogger('idsfree')


@global_options()
@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = kwargs

cli.add_command(prepare)
cli.add_command(run_attacks)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli()
