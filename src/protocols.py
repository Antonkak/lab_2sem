from typing import Protocol, runtime_checkable
from src.models import Task

@runtime_checkable
class TaskSource(Protocol):
    """Протокол источника задач"""
    def get_tasks(self) -> list[Task]:
        """Список задач"""
        ...
