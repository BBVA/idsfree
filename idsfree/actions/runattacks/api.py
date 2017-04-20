
import asyncio
import logging
import tempfile

from typing import Tuple, Dict, Union

from .model import *
from .helpers import *
from .results_parsers import *
from ...core.exceptions import IdsFreeInsecureData
from ..helpers import check_remote_requisites, get_remote_ssh_connection

log = logging.getLogger("idsfree")


def build_attack_command(attack_type: str,
                         results_file_name: str,
                         network_name: str,
                         attacker_app: str,
                         ports_to_attack: str,
                         attacked_app: str,
                         service_name: str = "") -> Dict[str, Tuple[str, str]]:
    """
    This functions build and returns the command for attack and the result 
    file path
    
    :return: tuple as format: (command string, results file path) 
    :rtype: tuple(str, str)
    """
    port_to_scan = expand_ports(ports_to_attack)
    NMAP_SCRIPTS_WEB = "--script \"http* and not *brute* and not *enum* and " \
                       "not " \
                       "external and not intrusive and not discovery and " \
                       "not malware\""

    if service_name:
        NMAP_SCRIPTS_NET = "--script \"default or *{service}*\"".format(
            service=service_name.lower()
        )
    else:
        NMAP_SCRIPTS_NET = "-sC"

    BASE_NMAP_COMMAND = \
        "docker run --rm --network={netname} --name {attacker_app}" \
        " -v /tmp:/tmp k0st/nmap -v -p {scan_ports} -oX /tmp/" \
        "{results_file}.xml {attacked_app_addr}". \
            format(results_file=results_file_name,
                   scan_ports=",".join(port_to_scan),
                   netname=network_name,
                   attacker_app=attacker_app,
                   attacked_app_addr=attacked_app)

    commands = {}

    if attack_type == "net":
        command_file_results = "/tmp/{}.xml".format(results_file_name)
        command = "{} {}".format(BASE_NMAP_COMMAND,
                                 NMAP_SCRIPTS_NET)

        commands["nmap"] = (command, command_file_results)
    elif attack_type == "web":
        command_file_results = "/tmp/{}.xml".format(results_file_name)
        command = "{} {}".format(BASE_NMAP_COMMAND,
                                 NMAP_SCRIPTS_WEB)

        commands["nmap"] = (command, command_file_results)

    return commands


async def launch_attacks(config: IdsFreeRunAttacksModel,
                         console_queue: asyncio.Queue = None) \
        -> Union[Dict[str,
                      str],
                 IdsFreeInsecureData]:

    #
    # Check if inputs are secure
    #
    if check_sanitized_input_for_command(config.service_name) is False:
        raise IdsFreeInsecureData('Service name: "{}" contains not allowed '
                                  'character values'.
                                  format(config.service_name))
    if check_sanitized_input_for_command(config.docker_image) is False:
        raise IdsFreeInsecureData('Docker image: "{}" contains not allowed '
                                  'character values'.
                                  format(config.docker_image))

    async with get_remote_ssh_connection(config) as connection:

        async with SwamNetwork(config, connection) as network_name:

            # Built temporal result name
            results_file_name = generate_random_name()
            attacked_app = "attacked_app_{}".format(generate_random_name(
                4, 10))
            attacker_app = "attacker_app_{}".format(generate_random_name(
                4, 10))

            # Launch app to attack
            log.warning("Launching attacked app with name: {}".format(
                attacked_app))
            attacked_app_raw = await connection.run(
                "docker run --rm -d --network={netname} --name {attacked_app} "
                "{docker_image}".format(
                    netname=network_name,
                    attacked_app=attacked_app,
                    docker_image=config.docker_image
                ))

            # Remove the en '\n'
            attacked_app_id = attacked_app_raw.stdout[:-1]

            try:
                # Launch attacks
                log.warning("Launching attacked app with name: {}".format(
                    attacker_app))

                scan_results = {}

                for tool_name, params in build_attack_command(
                        config.attacks_type,
                        results_file_name,
                        network_name,
                        attacker_app,
                        config.port_to_check,
                        attacked_app,
                        config.service_name).items():

                    command, results_path = params

                    log.info("Launching tool: '{}'. Command: {}".format(
                        tool_name,
                        command
                    ))

                    async with await connection.create_process(command) as rproc:

                        # Wait until attacker container ends
                        while True:
                            scan_line = await rproc.stdout.readline()

                            if scan_line == "":
                                break

                            if console_queue:
                                await console_queue.put(scan_line)

                            log.debug(scan_line)

                    # Download results
                    with tempfile.NamedTemporaryFile() as local_results_file:
                        async with connection.start_sftp_client() as sftp:
                            await sftp.get(results_path,
                                           localpath=local_results_file.name)

                        local_results_content = open(
                            local_results_file.name).read()

                    # Remove temporal result file
                    await connection.run("rm -rf {}".format(results_path))

                    scan_results[tool_name] = local_results_content

                #
                # Return the results of the all commands
                #
                return scan_results

            finally:
                # Destroy attacked app container
                log.warning("Destroying attacked app with name: {}".format(
                    attacked_app))
                await connection.run("docker rm -f {attacked_app_id}".format(
                    attacked_app_id=attacked_app_id
                ))


def run_runattasks_idsfree(config: IdsFreeRunAttacksModel) \
        -> Union[str,
                 IdsFreeInsecureData]:
    """
    This functions does:
    
    - Check that remote host has required software and versions
    - Build the environment and launch the attacks
    - Load raw results, transform it and return in selected format as string
    
    It returns the name of cyphered network created.
    """
    assert isinstance(config, IdsFreeRunAttacksModel)

    loop = asyncio.get_event_loop()

    # Check remote Docker version
    loop.run_until_complete(check_remote_requisites(config))

    # Launch attacks
    results = loop.run_until_complete(launch_attacks(config))

    # Parse results

    log.error("Generating results as '{}' format, in file: '{}'".format(
        config.output_results_format,
        config.output_results_path
    ))

    return parse_results(results,
                         config.attacks_type,
                         config.output_results_format)


__all__ = ("run_runattasks_idsfree",)
