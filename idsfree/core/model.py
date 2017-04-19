# -*- coding: utf-8 -*-

from booby import *


class SharedConfig(Model):
    verbosity = Integer(default=0)
    timeout = Integer(default=10)
    debug = Boolean(default=False)
    remote_host = String(default="127.0.0.1")
    remote_port = Integer(default=22)
    remote_user = String(default="root")
    remote_password = String(default="toor")
    remote_cert_path = String(default="")
