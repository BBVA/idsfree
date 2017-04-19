import re
import logging
import asyncio
import logging

from typing import Tuple

from asyncssh import connect, SSHClientConnection

from ..core.model import SharedConfig


log = logging.getLogger("idsfree")


def get_remote_ssh_connection(config: SharedConfig,
                              loop=None) -> SSHClientConnection:

    loop = loop or asyncio.get_event_loop()

    return connect(host=config.remote_host,
                   port=config.remote_port,
                   username=config.remote_user,
                   password=config.remote_password,
                   loop=loop)


def check_console_input_config(config: SharedConfig,
                               log: logging.Logger = None) -> bool:

    log = log or logging.getLogger(__package__.split(".", maxsplit=1)[0])

    # Check if config is valid
    if not config.is_valid:
        for prop, msg in config.validation_errors:

            log.critical("[!] '%s' property %s" % (prop, msg))
        return False

    return True


async def check_remote_docker_version(connection: SSHClientConnection,
                                      loop=None) -> str:
    """
    Checks remote Docker version and return it.
    
    >>> check_remote_docker_version(connection)
    '1.12'
    """
    result = await connection.run('docker -v', check=True)

    raw_result = result.stdout

    return re.search(
        r"""(Docker version )([\.\-\w\d]+)(.*)""", raw_result).group(2)


async def check_remote_linux_distribution_and_kernel(
        connection: SSHClientConnection,
        loop=None) -> Tuple[str, str]:
    """
    Checks remote Docker version and return it.
    
    Supported linux distributions: {kali | debian | ubuntu | centos | unknown} 
    
    >>> check_remote_linux_distribution_and_kernel(connection)
    ('kali', '4.10.0')
    
    :return: tuple as format: (distribution name, kernel version) 
    :rtype: tuple(str, str)
    
    """
    distributions = ("kali", "debian", "ubuntu", "centos")

    result = await connection.run('uname -a', check=True)
    raw_results = result.stdout.lower()

    # Get remote distribution
    remote_distribution = 'unknown'
    for dist in distributions:
        if dist in raw_results:
            remote_distribution = dist
            break

    # Get remote kernel version
    _, _, kernel_version, *_ = raw_results.split(" ")
    remote_kernel, *_ = kernel_version.split("-")

    return remote_distribution, remote_kernel


async def check_remote_requisites(config: SharedConfig):

    async with get_remote_ssh_connection(config) as con:
        log.info("Checking remote Docker version")
        remote_docker_version = await check_remote_docker_version(con)

        log.info("Checking remote Linux distribution and kernel")
        remote_distribution, remote_kernel = \
            await check_remote_linux_distribution_and_kernel(con)


__all__ = ("check_console_input_config",
           "check_remote_docker_version",
           "get_remote_ssh_connection",
           "check_remote_linux_distribution_and_kernel",
           "check_remote_requisites")
