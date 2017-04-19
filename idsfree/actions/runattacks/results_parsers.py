from collections import defaultdict, Counter

try:
    import ujson as json
except ImportError:
    import json

from typing import List, Dict
from xml.sax.saxutils import escape
from libnmap.parser import NmapParser

from .model import SecurityResult


# --------------------------------------------------------------------------
# Parser functions of results depending of tool executed
# --------------------------------------------------------------------------
def _nmap_results_parser(results: str) -> List[SecurityResult]:
    nmap_report = NmapParser.parse_fromstring(results)

    PLUGINS_VULN_CATEGORY = [
        "afp-path-vuln",
        "broadcast-avahi-dos",
        "clamav-exec",
        "distcc-cve2004-2687",
        "dns-update",
        "firewall-bypass",
        "ftp-libopie",
        "ftp-proftpd-backdoor",
        "ftp-vsftpd-backdoor",
        "ftp-vuln-cve2010-4221",
        "http-adobe-coldfusion-apsa1301",
        "http-aspnet-debug",
        "http-avaya-ipoffice-users",
        "http-awstatstotals-exec",
        "http-axis2-dir-traversal",
        "http-cookie-flags",
        "http-cross-domain-policy",
        "http-csrf",
        "http-dlink-backdoor",
        "http-dombased-xss",
        "http-enum",
        "http-fileupload-exploiter",
        "http-frontpage-login",
        "http-git",
        "http-huawei-hg5xx-vuln",
        "http-iis-webdav-vuln",
        "http-internal-ip-disclosure",
        "http-litespeed-sourcecode-download",
        "http-majordomo2-dir-traversal",
        "http-method-tamper",
        "http-passwd",
        "http-phpmyadmin-dir-traversal",
        "http-phpself-xss",
        "http-shellshock",
        "http-slowloris-check",
        "http-sql-injection",
        "http-stored-xss",
        "http-tplink-dir-traversal",
        "http-trace",
        "http-vmware-path-vuln",
        "http-vuln-cve2006-3392",
        "http-vuln-cve2010-0738",
        "http-vuln-cve2010-2861",
        "http-vuln-cve2011-3192",
        "http-vuln-cve2011-3368",
        "http-vuln-cve2012-1823",
        "http-vuln-cve2013-0156",
        "http-vuln-cve2013-6786",
        "http-vuln-cve2013-7091",
        "http-vuln-cve2014-2126",
        "http-vuln-cve2014-2127",
        "http-vuln-cve2014-2128",
        "http-vuln-cve2014-2129",
        "http-vuln-cve2014-3704",
        "http-vuln-cve2014-8877",
        "http-vuln-cve2015-1427",
        "http-vuln-cve2015-1635",
        "http-vuln-cve2017-5638",
        "http-vuln-misfortune-cookie",
        "http-vuln-wnr1000-creds",
        "http-wordpress-users",
        "ipmi-cipher-zero",
        "irc-botnet-channels",
        "irc-unrealircd-backdoor",
        "mysql-vuln-cve2012-2122",
        "netbus-auth-bypass",
        "qconn-exec",
        "rdp-vuln-ms12-020",
        "realvnc-auth-bypass",
        "rmi-vuln-classloader",
        "samba-vuln-cve-2012-1182",
        "smb-vuln-conficker",
        "smb-vuln-cve2009-3103",
        "smb-vuln-ms06-025",
        "smb-vuln-ms07-029",
        "smb-vuln-ms08-067",
        "smb-vuln-ms10-054",
        "smb-vuln-ms10-061",
        "smb-vuln-regsvc-dos",
        "smtp-vuln-cve2010-4344",
        "smtp-vuln-cve2011-1720",
        "smtp-vuln-cve2011-1764",
        "ssl-ccs-injection",
        "ssl-cert-intaddr",
        "ssl-dh-params",
        "ssl-heartbleed",
        "ssl-known-key",
        "ssl-poodle",
        "sslv2-drown",
        "supermicro-ipmi-conf",
        "tls-ticketbleed",
        "wdb-version"
    ]

    results = []

    for scanned_hosts in nmap_report.hosts:

        for service in scanned_hosts.services:

            if service.scripts_results:
                for script in service.scripts_results:

                    #
                    # Determinate the level
                    #

                    # Search for 'vuln' category or any similar keywork
                    if script.get("id") in PLUGINS_VULN_CATEGORY:
                        level = "critical"
                    else:
                        level = "informational"

                    results.append(SecurityResult(
                        'nmap',
                        service.port,
                        tool_plugin_name=script.get('id'),
                        tool_version=nmap_report.version,
                        level=level,
                        log=script.get('output'),
                        vulnerability_type='net',
                        port_proto=service.protocol))

            else:
                results.append(SecurityResult(
                    'nmap',
                    service.port,
                    tool_version=nmap_report.version,
                    level="none",
                    log=service.banner,
                    vulnerability_type='net',
                    port_proto=service.protocol))

        return results

#
# Parser mapper
#
TOOLS_PARSERS = {
    'net': _nmap_results_parser
}


# --------------------------------------------------------------------------
# Output transform
# --------------------------------------------------------------------------
def _json_export(data: List[SecurityResult]) -> str:
    return json.dumps([
        x.json for x in data
    ])


def _junit_export(data: List[SecurityResult]) -> str:
    base_xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
{scans_results}
</testsuites>    
"""

    tool_report_template = """    <testsuite name="idsFree.{tool_name}.scanReport" errors="{total_issues}" tests="{total_scans}" failures="{total_issues}" timestamp="2013-05-24T10:23:58">
        <properties>
            <property name="scanner.{tool_name}" value="Scanned with Nmap {tool_version}" />
        </properties>

{issues}
    
    </testsuite>"""

    issue_template = """        <testcase classname="{tool_name}" name="{title}" time="0.001">
             <failure message="test failure">{scan_description}
             </failure>
        </testcase>"""

    issue_with_no_errortemplate = """        <testcase classname="{tool_name}" name="{scan_description}" time="0.001" />"""

    results_by_tool = defaultdict(list)
    issues_by_tool = Counter()

    # Generate the partial result for each tool
    for partial_result in data:

        complete_tool_name = "{tool_name}{tool_plugin}".format(
            tool_name=partial_result.tool_name,
            tool_plugin="-{}".format(partial_result.tool_plugin_name) if
                        partial_result.tool_plugin_name else ""
        )

        if partial_result.level == "none":
            test_case_result = issue_with_no_errortemplate.format(
                tool_name=complete_tool_name,
                scan_description=escape(partial_result.log)
            )

        else:
            test_case_result = issue_template.format(
                tool_name=complete_tool_name,
                title="Scan was found a issue with level: "
                      "{}".format(partial_result.level),
                scan_description=escape(partial_result.log)

            )

            issues_by_tool['issues'] += 1

        results_by_tool[partial_result.tool_name].append(
            (
                partial_result.tool_version,
                test_case_result
            )
        )

    # Test suites
    tests_suites = []
    for tool_name, data in results_by_tool.items():

        total_issues = []
        for tool_version, reports in data:
            total_issues.append(reports)

        tests_suites.append(
            tool_report_template.format(
                tool_version=data[0][0],
                total_issues=issues_by_tool['nmap'],
                total_scans=len(total_issues),
                tool_name=tool_name,
                issues="\n".join(total_issues)
            )
        )

    return base_xml_template.format(scans_results="\n".join(tests_suites))


FORMAT_TRANSFORMS = {
    'json': _json_export,
    'junit': _junit_export
}


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def parse_results(results: Dict[str, str],
                  attack_type: str,
                  results_format: str) -> str:

    parsed_results = []

    for tool, result in results.items():
        # Transform raw input data from scan tool
        parsed_results.extend(TOOLS_PARSERS[attack_type](result))

    # Transform to the correct output format
    return FORMAT_TRANSFORMS[results_format](parsed_results)


__all__ = ("parse_results",)
