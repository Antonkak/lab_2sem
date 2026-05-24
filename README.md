# Лабораторная работа, семестр 2: Источники задач и контракты
## Описание
Модуль приёма задач для платформы обработки заданий. Реализует контрактное программирование на основе typing.Protocol с поддержкой Duck Typing. Система позволяет подключать различные источники задач без изменения существующего кода.
Ключевые особенности
* Duck Typing  источники совместимы структурно, а не через наследование
* Protocol + @runtime_checkable  проверка контрактов во время выполнения
* Расширяемость  новые источники добавляются без модификации ядра
* Использование дескрипторов — валидация приоритета $0 \le x \le 10$ и добавление readonly полей
* Тесты  покрытие 83%
* Асинхронность — обработка задач выполняется с использованием asyncio и контекстным менеджера
## Структура проекта
```
lab_2sem_1/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── data.json
│   ├── exeptions/
│   │   ├── task_exeption.py
│   ├── models.py
│   ├── protocols.py
│   ├── sources.py
│   ├── dispatcher.py
│   ├── executor.py
│   ├── handler.py
│   ├── queue.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_app.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```
## Установка и запуск
### Установка зависимостей
```
pip install -r requirements.txt
```
### Запуск демонстрации
```
python src/main.py
```
### Запуск тестов
```
pytest --cov=src -v
```
### Пример использования
```
python
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
        while len(filtered_queue) > 0:  # Проверяем длину именно отфильтрованной очереди
            await asyncio.sleep(0.1)
if __name__ == "__main__":
    asyncio.run(main())
```
### Вывод
```
Processing task: 8c556858-c586-4825-a028-acd8a154e9d6 | Payload: {'source': 'file', 'type': 'order', 'data': 'Process order #12345'} | Priority: 2
Processing task: 83877017-94bc-4057-a47c-afcf8b6061d4 | Payload: {'source': 'file', 'type': 'notification', 'data': 'Send email to user@example.com'} | Priority: 5
Processing task: 507383c0-a719-4894-8966-cc7b950a15fe | Payload: {'source': 'file', 'type': 'analytics', 'data': 'Recalculate statistics for 2024'} | Priority: 3
Processing task: 67d6cf51-fee5-4516-8181-0d5715a84ac8 | Payload: {'source': 'generator'} | Priority: 0
Processing task: b53eca12-b4af-4717-8f7f-dc8c96e9ac14 | Payload: {'source': 'generator'} | Priority: 1
Processing task: 587f2dc1-2e2e-43e6-a044-5c6c9ec31aec | Payload: {'source': 'generator'} | Priority: 2
Processing task: 59b2b8f3-417d-4ade-a212-f063bf39dc80 | Payload: {'source': 'generator'} | Priority: 3
Processing task: 9f2e0d01-3b54-4626-a5e0-6174bddfa292 | Payload: {'source': 'generator'} | Priority: 4
Processing task: 8cdcf5b9-def9-4f2d-9420-2cdbe24b2154 | Payload: {'source': 'api'} | Priority: 4
...
```
## Тестирование
Покрытие кода
```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
src\__init__.py                      0      0   100%
src\dispatcher.py                   16      0   100%
src\executor.py                     22      0   100%
src\exeptions\task_exeption.py       2      0   100%
src\handler.py                       7      0   100%
src\main.py                         23     23     0%   1-30
src\models.py                       39      1    97%   52
src\protocols.py                     8      0   100%
src\queue.py                        28      4    86%   33-36
src\sources.py                      21      0   100%
--------------------------------------------------------------
TOTAL                              166     28    83%
```
