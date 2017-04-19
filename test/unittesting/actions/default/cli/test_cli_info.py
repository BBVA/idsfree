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
