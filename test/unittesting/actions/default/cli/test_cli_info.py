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

from click.testing import CliRunner

from idsfree.actions.default.cli import info

import idsfree.actions.default.console


def _launch_idsfree_in_console(blah, **kwargs):
    click.echo("ok")


def test_cli_info_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(info)

    assert 'Usage: info [OPTIONS] ' in result.output


def test_cli_info_runs_ok():
    # Patch the launch of: launch_idsfree_info_in_console
    idsfree.actions.default.cli.launch_idsfree_in_console = _launch_idsfree_in_console

    runner = CliRunner()
    result = runner.invoke(info, ["aaaa"])

    assert 'ok' in result.output
