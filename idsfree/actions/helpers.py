import re
import asyncio
import logging

from typing import Tuple

import asyncssh
from asyncssh import connect, SSHClientConnection

from ..core.model import SharedConfig
from ..core.exceptions import IdsFreeInvalidRequisitesError


log = logging.getLogger("idsfree")

MINIMUM_LINUX_KERNEL_DEBIAN = (4, 8)
MINIMUM_LINUX_KERNEL_CENTOS = (3, 10)
MINIMUM_DOCKER_VERSION = ((17, 0), (1, 13))


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
        loop=None) -> Tuple[str, str, bool]:
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

    try:
        await connection.run('docker ps', check=True)

        has_remote_perms = True
    except asyncssh.process.ProcessError as e:
        has_remote_perms = False

    return remote_distribution, remote_kernel, has_remote_perms


async def check_remote_requisites(config: SharedConfig):

    log.error("Checking remote machine for minimum requisites")

    async with get_remote_ssh_connection(config) as con:
        log.info("Checking remote Docker version")
        remote_docker_version_raw = await check_remote_docker_version(con)

        remote_docker_version = tuple([int(x)
                                       for x in remote_docker_version_raw.
                                      split(".", maxsplit=2)[:2]])

        oks_remote_version = False
        for allowed_version in MINIMUM_DOCKER_VERSION:
            if remote_docker_version >= allowed_version:
                oks_remote_version = True

        if oks_remote_version is False:
            raise IdsFreeInvalidRequisitesError(
                "Invalid remote Docker version. Minimum needed are: 1.13 "
                "or 17.X.X-ce")

        log.info("Checking remote Linux distribution and kernel")
        remote_distribution, remote_kernel_raw, has_remote_perms = \
            await check_remote_linux_distribution_and_kernel(con)

        remote_kernel = tuple([int(x)
                               for x in remote_kernel_raw.
                              split(".", maxsplit=2)[:2]])

        if remote_distribution in ('debian', 'kali', 'ubuntu') and \
                not remote_kernel >= MINIMUM_LINUX_KERNEL_DEBIAN:
            raise IdsFreeInvalidRequisitesError(
                'remote linux distribution has invalid kernel. For Ubuntu / '
                'debian based system minimum kernel version is: "{}"'.format(
                    MINIMUM_LINUX_KERNEL_DEBIAN
                ))

        elif remote_distribution in ('centos', ) and \
                not remote_kernel >= MINIMUM_LINUX_KERNEL_CENTOS:
            raise IdsFreeInvalidRequisitesError(
                'remote linux distribution has invalid kernel. For Centos '
                'based system minimum kernel version is: "{}"'.format(
                    MINIMUM_LINUX_KERNEL_CENTOS
                ))

        if has_remote_perms is False:
            raise IdsFreeInvalidRequisitesError("User '{}' has not "
                                                "permissions to run docker "
                                                "in remote system".format(
                config.remote_user))


__all__ = ("check_console_input_config",
           "check_remote_docker_version",
           "get_remote_ssh_connection",
           "check_remote_linux_distribution_and_kernel",
           "check_remote_requisites")
