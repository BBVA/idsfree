import logging

from .api import *
from .model import *
from ....core.helpers import *
from ....core.exceptions import *

log = logging.getLogger('idsfree')


def launch_idsfree_prepare_master_in_console(config: IdsFreePrepareMasterModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting preparation of Master...")

        try:
            master_addr, slave_info = run_prepare_master_idsfree(config)
            log.console("Master initialized...")

            #
            # Show results
            #
            print("-" * len(master_addr))
            print("#")
            print("# Your Cluster ID is: ")
            print("#")
            print("#   ", slave_info)
            print("#")
            print("# Your Master Address is: {}".format(master_addr))
            print("#")
            print("-" * len(master_addr))
        except IdsFreeInvalidRequisitesError as e:
            log.console(e)


__all__ = ("launch_idsfree_prepare_master_in_console",)
