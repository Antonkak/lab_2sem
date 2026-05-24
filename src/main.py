from src.dispatcher import TaskDispatcher
from src.sources import FileSource, GeneratorSource, APISource
from src.queue import TaskQueue
import asyncio
from src.executor import TaskExecutor
from src.handler import Handler

async def main():
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

    await queue.load_tasks_to_queue()
    handler = Handler()
    async with TaskExecutor(queue, handler):
        while len(queue) > 0:
            await asyncio.sleep(0.1)
            
    filtered_queue = queue.filter_by_priority(4)
    async with TaskExecutor(filtered_queue, handler):
        while len(filtered_queue) > 0:
            await asyncio.sleep(0.1)
if __name__ == "__main__":
    asyncio.run(main())
