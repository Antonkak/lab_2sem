from src.dispatcher import TaskDispatcher
from src.sources import FileSource, GeneratorSource, APISource
from src.queue import TaskQueue


def main():
    sources = [
        FileSource("src/data/data.json"),
        GeneratorSource(5),
        APISource()
    ]
    dispatcher = TaskDispatcher(sources)
    dispatcher.process_all()
    queue = TaskQueue()
    for source in sources:
        queue.add_source(source)
    print("Все задачи:")
    for i, task in enumerate(queue, 1):
        print(f"  {i}. [{task.id[:8]}] приоритет={task.priority}, статус={task._status}")
    print("Задачи с приоритетом 2:")
    for task in queue.filter_by_priority(2):
        print(f"  - [{task.id[:8]}] приоритет={task.priority}, статус={task._status}")

if __name__ == "__main__":
    main()
