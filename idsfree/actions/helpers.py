import re
import os
import copy

import yaml
import random
import string
import asyncio
import logging
import tempfile
import asyncssh

from typing import Tuple, Union, List
from asyncssh import connect, SSHClientConnection, import_private_key

from ..core.model import SharedConfig
from ..core.exceptions import IdsFreeInvalidRequisitesError, IdsFreeError, \
    IdsFreeNotFoundError

log = logging.getLogger("idsfree")

MINIMUM_LINUX_KERNEL_DEBIAN = (4, 4)
MINIMUM_LINUX_KERNEL_CENTOS = (3, 10)
MINIMUM_DOCKER_VERSION = ((17, 0), (1, 13))


def generate_random_name(mininum: int = 10, maximum: int = 40):
    return "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(mininum, maximum)))


class SwamNetwork:
    """Context manager that creates a new docker Swarm cyphered network and
    delete at exit"""

    def __init__(self,
                 con: SSHClientConnection,
                 prefix: str = "",
                 autoremove_network: bool = True):
        self.con = con
        self.autoremove_network = autoremove_network

        # Generates network name
        self.remote_cyphered_network = "IDSFREE_{prefix}{net_id}".format(
            prefix="%s_" % prefix if prefix else "",
            net_id=generate_random_name(5, 5))

    async def __aenter__(self):
        log.error("Creating temporal encrypted network: {}".format(
            self.remote_cyphered_network))

        ret = await self.con.run("sudo docker network create --driver overlay "
                                 "--opt encrypted {net_name} "
                                 "--attachable --internal".
                                 format(net_name=self.remote_cyphered_network))

        # Wail until network are created
        while True:
            ret_net = await self.con.run("sudo docker network ls | grep -i {}"
                                         " | awk '{{print $1}}'".
                                     format(self.remote_cyphered_network))
            if ret_net.stdout == "":
                await asyncio.sleep(1)
            else:
                break

        return self.remote_cyphered_network

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.autoremove_network:
            log.error("Removing temporal encrypted network: {}".format(
                self.remote_cyphered_network))

            await self.con.run("sudo docker network rm {net_name}"
                               .format(net_name=self.remote_cyphered_network))


class ConfigLaunchService:
    def __init__(self,
                 app_name: str,
                 target_docker_image: str,
                 publish_ports: dict = None):
        """
        :param publish_ports: in format: {EXTERNAL_PORT: INTERNAL_PORT} 
        :type publish_ports: dict(str, str)
        """
        self.app_name = app_name
        self.target_docker_image = target_docker_image
        self.publish_ports = publish_ports


class ConfigLaunchSwarmCompose:
    def __init__(self,
                 compose_path: str,
                 network_name: str,
                 main_service: str = None):
        self.main_service = main_service
        self.network_name = network_name
        self.compose_path = compose_path

        try:
            self._compose_content_json = yaml.safe_load(
                    open(self.compose_path).read()
                )
        except Exception as e:
            raise IdsFreeError("Invalid Swarm compose format: {}".format(
                e
            ))

    def transform(self) -> str:
        return _swarm_compose_parser(
            self._compose_content_json,
            self.network_name)

    def contains_service(self, service_name: str) -> bool:
        # """Check if `service_name` is listed as a service in Compose file"""
        # if not service_name:
        #     return False
        services = self._compose_content_json.get("services", None)

        if services:
            return service_name in services.keys()
        else:
            return False


class ConfigLaunchCustom:
    def __init__(self,
                 command: str):
        self.command = command


async def remove_service_or_stack(
        connection,
        service_or_stack_id: Union[str, set, list] = None,
        auto_remove_network: bool = False):

    if isinstance(service_or_stack_id, (set, tuple, list)):
        services_to_remove = set(service_or_stack_id)
    else:
        services_to_remove = {service_or_stack_id}

    for service_or_stack in services_to_remove:

        #
        # Try to find services with this id
        #
        _services_raw = await connection.run(
            "sudo docker service ls  2> /dev/null | grep -v NAME | "
            "awk '{print $2}'")

        _services_raw_set = set(_services_raw.stdout.splitlines())

        services_to_remove = set()
        for x in _services_raw_set:
            if service_or_stack in x and "STACK" not in x:
                services_to_remove.add(x)

        #
        # Try to find stacks with this id
        #
        _stacks_raw = await connection.run(
            "sudo docker stack ls 2> /dev/null | grep -v NAME  | "
            "awk '{print $1}'")

        _stacks_raw_set = set(_stacks_raw.stdout.splitlines())

        stacks_to_remove = set()
        for x in _stacks_raw_set:
            if service_or_stack in x:
                stacks_to_remove.add(x)

        stacks_and_services_to_remove = set()
        stacks_and_services_to_remove.update(services_to_remove)
        stacks_and_services_to_remove.update(stacks_to_remove)

        if not stacks_and_services_to_remove:
            log.info("Stack ID '{}' not found".format(
                service_or_stack
            ))

        #
        # Remove the service or stack
        #
        for service_or_stack_to_remove in stacks_and_services_to_remove:
            if "STACK" in service_or_stack_to_remove:
                # Is a Stack
                await connection.run(
                    "sudo docker stack rm {stack_id}".format(
                        stack_id=service_or_stack_to_remove))
            else:
                # Is a service
                await connection.run(
                    "sudo docker service rm {app_id}".format(
                        app_id=service_or_stack_to_remove))

        #
        # Try to find and remote associated network/s to the service
        #
        if auto_remove_network:
            networks_raw = await connection.run(
                'sudo docker network ls --format "{{.Name}}"')

            networks_raw_set = set(networks_raw.stdout.splitlines())

            for x in networks_raw_set:
                if service_or_stack in x and "STACK" not in x:
                    network = x
                    break
            else:
                log.info(
                    "No network found for stack ID '{}' not found".format(
                        service_or_stack
                    ))

            # Remove the network
            await connection.run("sudo docker network rm {}".format(network))


async def run_service_or_stack(stack_prefix: str,
                               connection,
                               network_name: str,
                               service_or_stack: Union[
                                   ConfigLaunchService,
                                   ConfigLaunchSwarmCompose,
                                   ConfigLaunchCustom]) -> \
        Union[str, IdsFreeNotFoundError]:
    """Deploy a service and return service ID or Swarm stack name"""
    #
    # Determinate if command to launch is a command or a Swarm compose
    #
    if isinstance(service_or_stack, ConfigLaunchSwarmCompose):
        action = "compose"
    elif isinstance(service_or_stack, ConfigLaunchService):
        action = "service"
    elif isinstance(service_or_stack, ConfigLaunchCustom):
        action = "custom"
    else:
        raise IdsFreeError("Invalid service or stack action")

    # -------------------------------------------------------------------------
    # Deploy using Swarm Compose
    # -------------------------------------------------------------------------
    if action == "compose":
        log.error("Building and deploying environment from Swarm Compose")

        # Check that compose file contains the service to check
        if not service_or_stack.contains_service(
                service_or_stack.main_service):
            raise IdsFreeNotFoundError(
                "Main service '{}' is not listed in Swarm Compose file".format(
                    service_or_stack.main_service
                ))

        # Transform compose add add the new features
        prepared_compose_file = service_or_stack.transform()

        with tempfile.NamedTemporaryFile() as modified_compose:
            # Dump modified Swarm compose
            open(modified_compose.name, "w").write(prepared_compose_file)

            # Get random filename for remote Swarm compose
            remote_swarm_file_name = "/tmp/{}.yml".format(
                generate_random_name(20)
            )

            async with connection.start_sftp_client() as sftp:
                c = await sftp.put(modified_compose.name,
                               remote_swarm_file_name)

                # Build stack name
                stack_name = "IDSFREE_STACK_{prefix}_{id}".format(
                    prefix=stack_prefix,
                    id=generate_random_name(5, 5)
                )

                # Deploy using swarm
                _deploy = await connection.run(
                    "sudo docker stack deploy -c {compose_path} {stack_name}".format(
                        compose_path=remote_swarm_file_name,
                        stack_name=stack_name
                    )
                )

                # Resolve the name of main application in the stack
                while True:
                    _resolve = await connection.run(
                        "sudo docker service ls | grep -i {main_service} | "
                        "grep -i {prefix} | "
                        "awk '{{print $2}}'".format(
                            main_service=service_or_stack.main_service,
                            prefix=stack_name
                        )
                    )

                    if not _resolve.stdout:
                        await asyncio.sleep(0.5)
                    else:
                        ret = _resolve.stdout.replace("\n", "")
                        break

                # Remove temporal compose
                await sftp.remove(remote_swarm_file_name)

    # -------------------------------------------------------------------------
    # Deploy without Compose
    # -------------------------------------------------------------------------
    elif action == "service":
        log.error("Building and deploying service")

        service_name = "IDSFREE_SERVICE_{prefix}_{app_name}".format(
            prefix=stack_prefix,
            app_name=service_or_stack.app_name)

        _published_ports = ""
        if service_or_stack.publish_ports:
            _published_ports = " ".join(
                "--publish {external}:{internal}".format(
                    external=x,
                    internal=y)
                for x, y in service_or_stack.publish_ports.items()
            )

        service_command = \
            "sudo docker service create --network={network_name} " \
            "{ports} --replicas 1 " \
            "--name {attacked_app} {target_docker_image}".format(
                network_name=network_name,
                ports=_published_ports,
                attacked_app=service_name,
                target_docker_image=service_or_stack.target_docker_image
            )

        _remote_response = await connection.run(service_command)
        ret = service_name

    elif action == "custom":
        log.error("Building and deploying custom command")

        service_name = "IDSFREE_SERVICE_{prefix}_{app_name}".format(
            prefix=stack_prefix,
            app_name=generate_random_name(5, 10))

        # Add service name
        command = service_or_stack.command.replace(
            "##SERVICE_NAME##", service_name)

        _remote_response = await connection.run(command)
        ret = service_name

    return ret


def _swarm_compose_parser(content: Union[str, dict],
                          overlay_network_name: str,
                          return_format: str = "yaml") -> str:
    """
    This function parse and fix a Swarm compose file. The adjust that the
    function does is:
    
    - Convert all networks in internal
    - Remove host mount points: 'bind'
    - Add a new network for each service to connect to the apps.
    """

    if isinstance(content, str):
        parsed_yaml = yaml.safe_load(content)
    else:
        parsed_yaml = content

    # Check the version
    if parsed_yaml.get("version") != '3':
        raise IdsFreeError("Invalid version of Swarm Compose file. "
                           "Version must be '3'")

    # Get all services:
    _services = copy.deepcopy(parsed_yaml.get("services"))
    for service_name, service_prop in _services.items():
        #
        # Check host mount points for insecure mounts
        #

        #
        # Add the testing overlay network
        #
        service_networks = service_prop.get("networks", None)
        if service_networks:
            parsed_yaml['services'][service_name].get("networks").append(
                overlay_network_name)
        else:
            parsed_yaml['services'][service_name]["networks"] = \
                [overlay_network_name]

    #
    # Networks:
    #   1 - Make all networks private
    _networks = copy.deepcopy(parsed_yaml.get("networks"))
    for network_name, network_prop in _networks.items():

        if network_prop:
            parsed_yaml.get("networks")[network_name].pop("external")

            parsed_yaml.get("networks")[network_name]['internal'] = True
        else:
            parsed_yaml["networks"][network_name] = {}
            parsed_yaml["networks"][network_name]['internal'] = True

    # 2 - Add a new overlay and cyphered network to perform the tests
    parsed_yaml.get("networks")[overlay_network_name] = {
        'external': True
    }

    if return_format == "json":
        return parsed_yaml
    else:
        return yaml.dump(parsed_yaml)


async def wait_for_service(connection,
                           network_name: str,
                           attacked_app: str,
                           port: int,
                           *,
                           sleep_time: int = 5,
                           max_retries: int = 3):
    for _ in range(max_retries):

        res = await connection.run(
            'sudo docker run --rm --network={network_name} '
            '--entrypoint /bin/sh gophernet/netcat '
            '-c "nc -v {attacked_app} {port} -w 0"'.format(
                network_name=network_name,
                attacked_app=attacked_app,
                port=port
            ))

        msg = res.stdout

        if "Connection refused" in msg:
            await asyncio.sleep(sleep_time)

        else:
            return


def get_remote_ssh_connection(config: SharedConfig,
                              loop=None) -> SSHClientConnection:
    loop = loop or asyncio.get_event_loop()

    if config.cert_path.endswith("pem"):
        c = open(
            os.path.abspath(
                os.path.expanduser(config.cert_path)
            ),
            "r").read()
        cert = import_private_key(c)
    else:
        cert = ()

    return connect(host=config.remote_host,
                   port=config.remote_port,
                   username=config.remote_user,
                   password=config.remote_password,
                   client_keys=cert,
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


async def check_remote_gluster(connection: SSHClientConnection,
                               loop=None) -> bool:
    result = await connection.run('sudo glusterd -V', check=True)

    raw_result = result.stdout

    return "glusterfs 3" in raw_result


async def check_mounted_gluster(connection: SSHClientConnection,
                                loop=None) -> bool:
    try:
        result = await connection.run('mount | grep -i gluster', check=True)

        raw_result = result.stdout
    except asyncssh.process.ProcessError:
        return False

    return any('/swarm-vols on /swarm/volumes type fuse.glusterfs' in x
               for x in
               raw_result.splitlines())


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
        await connection.run('sudo docker ps', check=True)

        has_remote_perms = True
    except asyncssh.process.ProcessError as e:
        has_remote_perms = False

    return remote_distribution, remote_kernel, has_remote_perms


async def check_remote_requisites(config: SharedConfig,
                                  disable_check_volumes=False):
    log.error("Checking remote machine for minimum requisites")

    async with get_remote_ssh_connection(config) as con:
        # --------------------------------------------------------------------------
        # Check remote docker version
        # --------------------------------------------------------------------------
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

        # --------------------------------------------------------------------------
        # Check remote kernel
        # --------------------------------------------------------------------------
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

        elif remote_distribution in ('centos',) and \
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

        # ---------------------------------------------------------------------
        # Check remote shared data
        # ---------------------------------------------------------------------
        remote_gluster = await check_remote_gluster(con)

        if not remote_gluster:
            raise IdsFreeInvalidRequisitesError(
                "You need to install GlusterFS ans share remote volumes "
                "calling them 'swarm-vols' and mounting in '/swarm/volumes'. "
                "You need to do that in each host. You can read a howto at: "
                "http://embaby.com/blog/using-glusterfs-docker-swarm-cluster/")

        remote_gluster_mounted = await check_mounted_gluster(con)

        if not disable_check_volumes:
            if not remote_gluster_mounted:
                raise IdsFreeInvalidRequisitesError(
                    "You need to install GlusterFS ans share remote volumes "
                    "calling them 'swarm-vols' and mounting in "
                    "'/swarm/volumes'. You need to do that in each host. "
                    "Maybe you should run: "
                    "'sudo mount.glusterfs localhost:/swarm-vols "
                    "/swarm/volumes'. For more info you can read a howto at: "
                    "http://embaby.com/blog/using-glusterfs-docker-swarm"
                    "-cluster/")


__all__ = ("check_console_input_config",
           "check_remote_docker_version",
           "get_remote_ssh_connection",
           "check_remote_linux_distribution_and_kernel",
           "check_remote_requisites",
           "generate_random_name",
           "remove_service_or_stack",
           "run_service_or_stack",
           "SwamNetwork")
