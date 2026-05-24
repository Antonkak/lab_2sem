from src.models import Task
from src.protocols import TaskSource
import asyncio
from typing import AsyncGenerator

class TaskQueue:
    """Асинхронная чередь задач"""
    def __init__(self) -> None:
        self._sources: list[TaskSource] = []
        self.async_queue: asyncio.Queue[Task] = asyncio.Queue()
    def add_source(self, source: TaskSource) -> None:
        """Добавить источник задач"""
        self._sources.append(source)
    def __len__(self) -> int:
        """Количество задач"""
        return self.async_queue.qsize()
    def __aiter__(self):
        """Асинхронный итератор"""
        return self
    async def __anext__(self) -> Task:
        """Получение следующей задачи"""
        if self.async_queue.empty():
            raise StopAsyncIteration
        return await self.async_queue.get()
    async def filter_by_priority(self, priority: int) -> AsyncGenerator[Task, None]:
        """Асинхронный фильтр по приоритету"""
        while not self.async_queue.empty():
            task = await self.async_queue.get()
            if task.priority == priority:
                yield task
    async def load_tasks_to_queue(self) -> None:
        """Получение задач"""
        for source in self._sources:
            tasks = source.get_tasks()
            for task in tasks:
                await self.async_queue.put(task)
