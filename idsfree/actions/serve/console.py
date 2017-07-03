import logging

from .api import *
from .model import *
from ...core.helpers import *

log = logging.getLogger('idsfree')


def launch_idsfree_serve_in_console(config: IdsFreeRunServeRemoveModel):
    """Launch in console mode"""

    log.setLevel(get_log_level(config.verbosity))

    run_server_idsfree(config)


__all__ = ("launch_idsfree_serve_in_console",)
