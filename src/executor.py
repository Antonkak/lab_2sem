import asyncio
from src.queue import TaskQueue
from src.protocols import TaskHandler

class TaskExecutor:
    """Асинхронный исполнитель задач"""
    def __init__(self, queue: TaskQueue, handler: TaskHandler):
        self.queue = queue
        self.handler = handler
        self._runner_task: asyncio.Task | None = None
    async def _run(self) -> None:
        """Цикл обработки задач"""
        while True:
            task = await self.queue.get_task() # type: ignore
            await self.handler.handle(task)
    async def __aenter__(self):
        """Запуск цикла"""
        self._runner_task = asyncio.create_task(self._run())
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Остановка цикла"""
        if self._runner_task:
            self._runner_task.cancel()
            try:
                await self._runner_task
            except asyncio.CancelledError:
                pass
