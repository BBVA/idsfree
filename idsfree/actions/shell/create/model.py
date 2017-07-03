
from idsfree import SharedWithSSHRemove, String


class IdsFreeRunShellCreateModel(SharedWithSSHRemove):
    output_results_path = String(default="")
    output_results_format = String(default="json")
    attacks_type = String(default="net")
    port_to_check = String(default="80")
    target_docker_image = String()
    swarm_compose = String()


__all__ = ("IdsFreeRunShellCreateModel",)
