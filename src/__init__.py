"""Package initialization for Project Copier."""

from .project_copier import ProjectCopier
from .state_manager import StateManager
from .vscode_controller import VSCodeController

__version__ = "1.0.0"
__all__ = ["ProjectCopier", "StateManager", "VSCodeController"]
