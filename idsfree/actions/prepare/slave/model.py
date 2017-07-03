
from idsfree import SharedWithSSHRemove, String


class IdsFreePrepareSlaveModel(SharedWithSSHRemove):
    cluster_id = String()
    master_addr = String()

__all__ = ("IdsFreePrepareSlaveModel",)
