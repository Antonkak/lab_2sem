import asyncio
from src.models import Task

class Handler:
    """Jбработчик"""
    async def handle(self, task: Task) -> None:
        print(f"[Handler] Началась обработка задачи {task.id[:8]}")
        await asyncio.sleep(1)
        print(f"[Handler] Задача {task.id[:8]} успешно выполнена")
