
from idsfree import SharedWithSSHRemove, String


class IdsFreeRunShellRemoveModel(SharedWithSSHRemove):
    stack_id = String()


__all__ = ("IdsFreeRunShellRemoveModel",)
