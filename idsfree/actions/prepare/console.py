import logging

from .api import *
from .model import *
from ...core.helpers import *

log = logging.getLogger('idsfree')


def launch_idsfree_prepare_in_console(config: IdsFreeDefaultModel):
    """Launch in console mode"""

    log.setLevel(config.verbosity)

    with run_in_console(config.debug):
        log.console("Starting preparation of remote host...")

        run_prepare_idsfree(config)


__all__ = ("launch_idsFree_in_console",)
