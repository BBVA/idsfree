import asyncio
import logging

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from aiohttp import web


from .model import *
from .server import app
from ...core.model import SharedWithSSHRemove
from ..helpers import check_remote_requisites

log = logging.getLogger("idsfree")


def config_to_dict(config) -> dict:
    raw_value = {}
    for x in config._fields.keys():

        if x in SharedWithSSHRemove._fields.keys():
            raw_value[x] = getattr(config, str(x))

    return raw_value


def run_server_idsfree(config: IdsFreeRunServeRemoveModel):
    """
    This functions does:
    
    - Check that remote host has required software and versions
    - Build the environment and launch the attacks
    - Load raw results, transform it and return in selected format as string
    
    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreeRunServeRemoveModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    if not config.skip_check_requisites:
        loop.run_until_complete(check_remote_requisites(config))

    app['IDSFREE_CONFIG'] = config
    app['GLOBAL_CONFIG'] = config_to_dict(config)

    # Launch attacks
    web.run_app(app,
                host=config.listen_addr,
                port=int(config.listen_port))

__all__ = ("run_server_idsfree",)
