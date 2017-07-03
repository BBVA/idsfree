import click
import logging

from idsfree import global_options, load_idsfree_config, SharedWithSSHRemove

from .prepare.cli import prepare
from .runattacks.cli import run_attacks
from .shell.cli import shell
from .serve.cli import serve

log = logging.getLogger('idsfree')


@global_options()
@click.pass_context
def cli(ctx, **kwargs):
    config = load_idsfree_config(kwargs.get('config_file', None))

    # Load config from file
    for k, v in config.items():
        if k in SharedWithSSHRemove._fields and kwargs.get(k, None) is None:
            # Fix value type
            if SharedWithSSHRemove._fields[k].field_type[0] is int:
                v = int(v)
            if SharedWithSSHRemove._fields[k].field_type[0] is float:
                v = float(v)

            kwargs[k] = v

    ctx.obj = kwargs

cli.add_command(prepare)
cli.add_command(run_attacks)
cli.add_command(shell)
cli.add_command(serve)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli()
