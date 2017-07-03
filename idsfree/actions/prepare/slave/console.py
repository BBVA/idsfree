import logging

from .api import *
from .model import *
from ....core.helpers import *
from ....core.exceptions import *

log = logging.getLogger('idsfree')


def launch_idsfree_prepare_slave_in_console(config: IdsFreePrepareSlaveModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting preparation of cluster slave...")

        try:
            run_prepare_slave_idsfree(config)

            log.console("Created new slave in cluster")
        except IdsFreeInvalidRequisitesError as e:
            log.console(e)


__all__ = ("launch_idsfree_prepare_slave_in_console",)
