import logging

from .api import *
from .model import *
from ...core.helpers import *

log = logging.getLogger('idsfree')


def launch_idsfree_runattasks_in_console(config: IdsFreeRunAttacksModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):
        log.console("Starting attacks of remote host...")

        results = run_runattasks_idsfree(config)

        # Export results
        with open(config.output_results_path, "w") as f:
            f.write(results)


__all__ = ("launch_idsFree_in_console",)
