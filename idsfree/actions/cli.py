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
