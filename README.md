# Лабораторная работа, семестр 2: Источники задач и контракты
## Описание
Модуль приёма задач для платформы обработки заданий. Реализует контрактное программирование на основе typing.Protocol с поддержкой Duck Typing. Система позволяет подключать различные источники задач без изменения существующего кода.
Ключевые особенности
* Duck Typing  источники совместимы структурно, а не через наследование
* Protocol + @runtime_checkable  проверка контрактов во время выполнения
* Расширяемость  новые источники добавляются без модификации ядра
* Использование дескрипторов — валидация приоритета $0 \le x \le 10$ и добавление readonly полей
* Тесты  покрытие 82%
* Реализация очереди и ленивые вычисления
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
python -m src/main.py
```
### Запуск тестов
```
pytest --cov=src -v
```
### Пример использования
```python
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

```
### Вывод
```bash
Processing task: 8a92104b-2a24-443e-8ef0-a5295a31756b | Payload: {'source': 'file', 'type': 'order', 'data': 'Process order #12345'} | Priority: 2
Processing task: 88b87cbc-bb22-4204-9ab0-482fb20d8dd2 | Payload: {'source': 'file', 'type': 'notification', 'data': 'Send email to user@example.com'} | Priority: 5
Processing task: e1360d21-2a56-4e36-b484-419d9b6ab7f5 | Payload: {'source': 'file', 'type': 'analytics', 'data': 'Recalculate statistics for 2024'} | Priority: 3
Processing task: 03be6b32-8b96-42ec-880c-b4a4634018a7 | Payload: {'source': 'generator'} | Priority: 0
Processing task: f4647de1-4b9e-4d35-a0b7-3164a9752567 | Payload: {'source': 'generator'} | Priority: 1
Processing task: 8d12b4bc-23cc-4a0e-981f-18c20c96d371 | Payload: {'source': 'generator'} | Priority: 2
Processing task: e585583d-297f-49fe-9c36-db7109386263 | Payload: {'source': 'generator'} | Priority: 3
Processing task: 28533426-fcd6-4736-833c-a936b496a6b6 | Payload: {'source': 'generator'} | Priority: 4
Processing task: 9f2242ec-ed0b-4318-925f-9d73ee4da03c | Payload: {'source': 'api'} | Priority: 4
Все задачи:
  1. [a461b9ec] приоритет=2, статус=New
  2. [822e97f2] приоритет=5, статус=New
  3. [04a050f6] приоритет=3, статус=New
  4. [09bea5aa] приоритет=0, статус=New
  5. [09e5f8a6] приоритет=1, статус=New
  6. [d6bf71d4] приоритет=2, статус=New
  7. [9ae32327] приоритет=3, статус=New
  8. [1c12815f] приоритет=4, статус=New
  9. [b917f4b0] приоритет=4, статус=New
Задачи с приоритетом 2:
  - [51afab25] приоритет=2, статус=New
  - [ff8b08d9] приоритет=2, статус=New
...
```
## Тестирование
Покрытие кода
```bash
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
src\__init__.py                      0      0   100%
src\dispatcher.py                   16      0   100%
src\exeptions\task_exeption.py       2      0   100%
src\main.py                         18     18     0%   1-25
src\models.py                       39      3    92%   24, 26, 52
src\protocols.py                     5      0   100%
src\queue.py                        23      1    96%   31
src\sources.py                      21      0   100%
--------------------------------------------------------------
TOTAL                              124     22    82%
```
