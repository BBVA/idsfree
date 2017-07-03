import logging

from .api import *
from .model import *
from ....core.helpers import *
from ....core.exceptions import IdsFreeNotFoundError

log = logging.getLogger('idsfree')


def launch_idsfree_shell_remove_in_console(config: IdsFreeRunShellRemoveModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting removing process of remote stack..")

        try:
            run_shell_remove_idsfree(config)

            log.console("Stack '{}' removed correctly".format(config.stack_id))

        except IdsFreeNotFoundError as e:
            log.console(e)


__all__ = ("launch_idsfree_shell_remove_in_console",)
