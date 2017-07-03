import asyncio
import logging


from .model import *
from ....core.exceptions import IdsFreeNotFoundError
from ...helpers import check_remote_requisites, get_remote_ssh_connection, \
    remove_service_or_stack

log = logging.getLogger("idsfree")


async def remove_remote_environment(config: IdsFreeRunShellRemoveModel) \
        -> IdsFreeNotFoundError:

    async with get_remote_ssh_connection(config) as connection:

        await remove_service_or_stack(connection,
                                      config.stack_id,
                                      auto_remove_network=True)


def run_shell_remove_idsfree(config: IdsFreeRunShellRemoveModel) \
        -> IdsFreeNotFoundError:
    """
    This functions does:
    
    - Check that remote host has required software and versions
    - Build the environment and launch the attacks
    - Load raw results, transform it and return in selected format as string
    
    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreeRunShellRemoveModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    if not config.skip_check_requisites:
        loop.run_until_complete(check_remote_requisites(config))

    # Launch attacks
    loop.run_until_complete(remove_remote_environment(config))


__all__ = ("run_shell_remove_idsfree",)
