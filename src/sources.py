import json
from models import Task

class FileSource:
    """Задачи из файла"""
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath
    def get_tasks(self) -> list[Task]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task(id=item['id'], payload=item['payload']) for item in data]
        except FileNotFoundError as e:
            print(f"Failed to open file: {e}")
            return []
class GeneratorSource:
    """Задачи программно"""
    def __init__(self, count: int):
        self.count = count
    def get_tasks(self) -> list[Task]:
        return [Task(id=f"gen_{i}", payload={"source": "generator"}) for i in range(self.count)]
class APISource:
    """Имитация внешнего API"""
    def get_tasks(self) -> list[Task]:
        return [Task(id="api_1", payload={"source": "api"})]
