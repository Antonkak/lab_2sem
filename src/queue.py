from typing import Generator
from src.models import Task
from src.protocols import TaskSource

class TaskQueue:
    """Очередь задач"""
    def __init__(self) -> None:
        self._sources: list[TaskSource] = []
    def add_source(self, source: TaskSource) -> None:
        """Добавить источник задач"""
        self._sources.append(source)
    def __len__(self) -> int:
        """Количество задач"""
        return sum(1 for _ in self)
    def __iter__(self) -> Generator[Task, None, None]:
        """Итератор по всем задачам из всех источников"""
        for source in self._sources:
            yield from source.get_tasks()
    def filter_by_status(self, status: str) -> Generator[Task, None, None]:
        """Фильтр по статусу"""
        for task in self:
            if task._status == status:
                yield task
    def filter_by_priority(self, priority: int) -> Generator[Task, None, None]:
        """Фильтр по приоритету задачи"""
        for task in self:
            if task.priority == priority:
                yield task
    def get_all(self) -> list[Task]:
        """Получить все задачи как список"""
        return list(self)
