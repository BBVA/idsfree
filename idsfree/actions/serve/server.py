import os

from aiohttp import web

from idsfree import coro_run_runallattacks_idsfree, IdsFreeRunAttacksModel, \
    runallattacks_parse_results


async def scan_create(request):

    # image = request.args.get("image")

    return web.Response(body=EXAMPLE_RESPONSE,
                        content_type="application/xml")

    # scan_config = dict(
    #     port_to_check="6379",
    #     service_name="redis",
    #     target_docker_image="redis"
    # )
    #
    # raw_value = request.app['GLOBAL_CONFIG']
    # raw_value.update(scan_config)
    #
    # config = IdsFreeRunAttacksModel(**raw_value)
    #
    # results = await coro_run_runallattacks_idsfree(config)
    #
    # parsed_results = runallattacks_parse_results(results,
    #                                              config.attacks_type,
    #                                              config.output_results_format)
    #
    # return web.json_response({
    #     'message': "scan created"
    # })

async def shell_create(request):
    return web.Response(text=u"Scan created")

async def shell_remove(request):
    return web.Response(text=u"Scan created")

EXAMPLE_RESPONSE = '''<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
    <testsuite name="idsFree.nmap.scanReport" errors="0" tests="2" failures="0" timestamp="2013-05-24T10:23:58">
        <properties>
            <property name="scanner.nmap" value="Scanned with Nmap 6.47" />
        </properties>

        <testcase classname="nmap-redis-brute" name="Scan was found a issue with level: informational" time="0.001">
             <failure message="test failure">
  ERROR: Server does not require authentication
             </failure>
        </testcase>
        <testcase classname="nmap-redis-info" name="Scan was found a issue with level: informational" time="0.001">
             <failure message="test failure">
  Version            3.2.8
  Operating System   Linux 4.4.0-1016-aws x86_64
  Architecture       64 bits
  Process ID         1
  Used CPU (sys)     0.01
  Used CPU (user)    0.04
  Connected clients  1
  Connected slaves   0
  Used memory        802.97K
  Role               master

             </failure>
        </testcase>
    
    </testsuite>
</testsuites>    
'''
API_PREFIX = "/api/v1/{}"

app = web.Application()
#
# /api/v1/scan
#
app.router.add_get(API_PREFIX.format("scan"), scan_create)
app.router.add_get(API_PREFIX.format("scan"), scan_create)
app.router.add_get(API_PREFIX.format("scan/download/<id>"), scan_create)

#
# /api/v1/shell
#
app.router.add_post(API_PREFIX.format("shell"), shell_create)
app.router.add_delete(API_PREFIX.format("shell"), shell_remove)

__all__ = ('app', )
