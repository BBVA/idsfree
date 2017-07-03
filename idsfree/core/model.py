# -*- coding: utf-8 -*-

from booby import *


class SharedConfig(Model):
    verbosity = Integer(default=0)
    debug = Boolean(default=False)
    config_file = String(default="")
    skip_check_requisites = Boolean(default=False)


class SharedWithSSHRemove(SharedConfig):
    timeout = Integer(default=10)
    remote_host = String(default="127.0.0.1")
    remote_port = Integer(default=22)
    remote_user = String(default="root")
    remote_password = String(default="toor")
    cert_path = String(default="")
