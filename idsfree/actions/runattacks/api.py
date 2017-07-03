import os
import asyncio
import logging
import tempfile

from typing import Dict, Union

from .model import *
from .attacks import *
from .helpers import *
from .results_parsers import *
from ...core.exceptions import IdsFreeInsecureData, IdsFreeError
from ..helpers import check_remote_requisites, get_remote_ssh_connection, \
    wait_for_service, SwamNetwork, generate_random_name, ConfigLaunchService, \
    ConfigLaunchSwarmCompose, run_service_or_stack, ConfigLaunchCustom, \
    remove_service_or_stack

log = logging.getLogger("idsfree")

BASE_REMOTE_SHARED_PATH = "/swarm/volumes/"


async def coro_run_runallattacks_idsfree(config: IdsFreeRunAttacksModel) \
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
    if check_sanitized_input_for_command(config.target_docker_image) is False:
        raise IdsFreeInsecureData('Docker image: "{}" contains not allowed '
                                  'character values'.
                                  format(config.target_docker_image))

    async with get_remote_ssh_connection(config) as connection:

        stack_prefix = "SCAN_{}".format(generate_random_name(5, 5))

        async with SwamNetwork(connection,
                               prefix=stack_prefix) as network_name:

            # Built temporal result name
            _target_app = generate_random_name(5, 5)

            # Launch app to attack
            log.debug("Launching attacked app with name: {}".format(
                _target_app))
            log.error("Launching application to analyze")

            if config.swarm_compose:
                command_or_compose = ConfigLaunchSwarmCompose(
                    config.swarm_compose,
                    network_name,
                    main_service=config.target_docker_image
                )

            else:
                command_or_compose = ConfigLaunchService(
                    _target_app,
                    config.target_docker_image)

            target_service_id = await run_service_or_stack(
                stack_prefix,
                connection,
                network_name,
                command_or_compose)

            # extract ports to test
            ports_to_scan = expand_ports(config.port_to_check)

            # Wait until all ports of service are up
            log.error("Waiting for the application is ready ... ")
            for port in ports_to_scan:
                await wait_for_service(connection,
                                       network_name,
                                       target_service_id,
                                       port)

            # scans_id = set()
            scan_results = {}
            try:
                # Launch attacks
                log.debug("Launching target app with name: {}".format(
                    target_service_id))
                log.error("Launching hacking tests... (this could take some "
                          "time)")

                for tool_name, params in build_attack_command(
                        config.attacks_type,
                        network_name,
                        ports_to_scan,
                        target_service_id,
                        config.service_name).items():

                    command, results_path = params

                    log.error("Launching tool: '{}'.".format(tool_name))
                    log.error("Scan info: '{}'. Command: '{}'".format(
                        tool_name,
                        command
                    ))

                    #
                    # Launch attack
                    #
                    _custom_service_config = ConfigLaunchCustom(command)

                    scan_tool_name = await run_service_or_stack(
                        stack_prefix,
                        connection,
                        network_name,
                        _custom_service_config)

                    # Wait until execution ends
                    _check_retry_counter = 0
                    while True:
                        try:
                            log.debug("Checking remote service status: '{}' "
                                      .format(scan_tool_name))
                            _cr = connection.run(
                                'sudo docker service ps {app} | grep -i {app}'.
                                    format(app=scan_tool_name)
                            )

                            c = await asyncio.wait_for(_cr, timeout=5)

                        except TimeoutError:

                            log.info("Timeout reached while checking service "
                                     "'{}' status".format(scan_tool_name))

                            _check_retry_counter += 1

                            if _check_retry_counter >= 4:
                                raise IdsFreeError("Timeout when try to check "
                                                   "the remote service status")

                            await asyncio.sleep(1)

                        # Check if container has not replicas -> execution was
                        # finished
                        if "Shutdown" in c.stdout:
                            break

                        log.debug("Service '{}' is still running. Waiting... "
                                  .format(scan_tool_name))

                        await asyncio.sleep(0.5)

                    complete_remote_results_file_path = os.path.join(
                        BASE_REMOTE_SHARED_PATH,
                        results_path)

                    # Download results
                    log.info("trying to download result file from: {}".format(
                        complete_remote_results_file_path
                    ))
                    with tempfile.NamedTemporaryFile() as local_results_file:
                        async with connection.start_sftp_client() as sftp:

                            #
                            # Try to download generated report.
                            #
                            # The report will be stored in shared location,
                            # managed by a GlusterFS. Sometimes, Glustedfs
                            # could be not synchronised and remote file
                            # could be not found. So we'll wait until the
                            # file are available. These checks will be done
                            # until 5 times. If in these checks the file not
                            #  found, try to check if glusterFs is nos sync
                            #
                            for i in range(6):
                                try:
                                    await sftp.get(
                                        complete_remote_results_file_path,
                                        localpath=local_results_file.name)

                                    break
                                except Exception as e:
                                    await asyncio.sleep(1)

                                    if i == 5:
                                        res = await connection.run(
                                            "sudo mount | grep -i gluster"
                                        )

                                        if res.stdout != "":
                                            raise IdsFreeError(
                                                "File not found in shared "
                                                "gluster "
                                                "volume. Maybe you should "
                                                "re-mount your "
                                                "partition. Try type: '> "
                                                "mount.glusterfs "
                                                "localhost:/swarm-vols "
                                                "/swarm/volumes'")

                                    continue

                            local_results_content = open(
                                local_results_file.name).read()

                            # Remove remote temporal result file
                            await connection.run("sudo rm -rf {}".format(
                                complete_remote_results_file_path))

                            scan_results[tool_name] = local_results_content

                #
                # Return the results of the all commands
                #
                return scan_results

            finally:
                await remove_service_or_stack(connection,
                                              stack_prefix,
                                              auto_remove_network=False)


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
    if not config.skip_check_requisites:
        loop.run_until_complete(check_remote_requisites(config))

    # Launch attacks
    results = loop.run_until_complete(coro_run_runallattacks_idsfree(config))

    # Parse results

    log.error("Generating results as '{}' format, in file: '{}'".format(
        config.output_results_format,
        config.output_results_path
    ))

    return runallattacks_parse_results(results,
                                       config.attacks_type,
                                       config.output_results_format)


__all__ = ("run_runattasks_idsfree", "coro_run_runallattacks_idsfree")
