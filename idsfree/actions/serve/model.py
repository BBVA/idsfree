
from idsfree import SharedWithSSHRemove, String


class IdsFreeRunServeRemoveModel(SharedWithSSHRemove):
    listen_addr = String(default="127.0.0.1")
    listen_port = String(default="8000")


__all__ = ("IdsFreeRunServeRemoveModel",)
