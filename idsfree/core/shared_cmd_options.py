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
import re
import os
import click
import codecs

#
# Get version software version
#
version_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '__init__.py')
with codecs.open(version_file, 'r', 'latin1') as fp:  # pragma no cover
    try:
        version = re.findall(r"^__version__ = ['\"]([^']+)['\"]\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

# --------------------------------------------------------------------------
# Common options for command line interface
# --------------------------------------------------------------------------
global_options_list = (
    # General
    click.option('-v', 'verbosity', count=True, type=int, default=1,
                 help='Verbose output'),
    click.option('-y', 'skip_check_requisites', is_flag=True, default=False,
                 help='skip remote checks requisites to run idsFRee'),
    click.option('-d', 'debug', is_flag=True, default=False,
                 help='enable debug'),
    click.option('-c', 'config_file', help='configuration file path'),
    click.option('--quiet', '-q', 'verbosity', flag_value=0,
                 help='Minimal output'),
    click.option('--remote-host', "-H", 'remote_host',
                 help='Remote host addr. Default: localhost'),
    click.option('--remote-port', "-R", 'remote_port', type=int,
                 help='Remote port. Default: 22'),
    click.option('--remote-user', "-U", 'remote_user',
                 help='Remote user for SSH service'),
    click.option('--remote-password', "-P", 'remote_password',
                 help='Remote password for SSH service'),
    click.option('-A', 'ask_remote_password', is_flag=True, default=False,
                 help='Ask for remote SSH password'),
    click.option('--cert-path', "-i", 'cert_path',
                 help='Certificate file for remote SSH service'),
    click.version_option(version=version)
)


class global_options(object):
    def __init__(self, invoke_without_command=False):
        assert isinstance(invoke_without_command, bool)

        self.invoke_without_command = invoke_without_command

    def __call__(self, f):
        def wrapped_f(*args):
            fn = f
            for option in reversed(global_options_list):
                fn = option(f)

            fn = click.group(context_settings={'help_option_names': ['-h', '--help']},
                             invoke_without_command=self.invoke_without_command)(fn)

            return fn

        return wrapped_f()


#
# HERE MORE EXAMPLES OF CMD OPTIONS
#
# --------------------------------------------------------------------------
# Options for "auto" command
# --------------------------------------------------------------------------
#
# auto_options_list = (
#     click.option('-T', '--timeout', 'timeout', type=int, default=60,
#                  help="max time to wait until actions are available"),
# )
#
#
# class auto_options(object):
#     def __call__(self, f):
#         def wrapped_f(*args):
#             fn = f
#             for option in reversed(auto_options_list):
#                 fn = option(f)
#
#             return fn
#
#         return wrapped_f()


__all__ = ("global_options",)  # "auto_options")
