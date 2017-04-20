import logging

from .api import *
from .model import *
from ...core.helpers import *
from ...core.exceptions import *

log = logging.getLogger('idsfree')


def launch_idsfree_prepare_in_console(config: IdsFreeDefaultModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting preparation of remote host...")

        try:
            run_prepare_idsfree(config)
        except IdsFreeInvalidRequisitesError as e:
            log.console(e)


__all__ = ("launch_idsFree_in_console",)
