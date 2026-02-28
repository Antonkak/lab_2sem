from protocols import TaskSource
from models import Task

class TaskDispatcher:
    """Принимает источники проверяет и обрабатывает"""
    def __init__(self, sources: list[TaskSource]):
        self.sources: list[TaskSource] = []
        for source in sources:
            if not isinstance(source, TaskSource):
                raise TypeError(f"Object {type(source)} does not implement TaskSource protocol")
            self.sources.append(source)
    def process_all(self) -> None:
        """задачи из всех источников и их обработка"""
        for source in self.sources:
            tasks = source.get_tasks()
            for task in tasks:
                self._out_task(task)
    def _out_task(self, task: Task) -> None:
        print(f"Processing task: {task.id} | Payload: {task.payload}")
