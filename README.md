# Лабораторная работа №1, семестр 2: Источники задач и контракты
## Описание
Модуль приёма задач для платформы обработки заданий. Реализует контрактное программирование на основе typing.Protocol с поддержкой Duck Typing. Система позволяет подключать различные источники задач без изменения существующего кода.
Ключевые особенности
* Duck Typing  источники совместимы структурно, а не через наследование
* Protocol + @runtime_checkable  проверка контрактов во время выполнения
* Расширяемость  новые источники добавляются без модификации ядра
* Использование дескрипторов — валидация приоритета $0 \le x \le 10$ и добавление readonly полей
* Тесты  покрытие 90%
##Структура проекта
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
from models import Task
from protocols import TaskSource
from sources import FileSource, GeneratorSource, APISource
from dispatcher import TaskDispatcher

# Создаём источники задач
sources = [
    FileSource("src/data/data.json"),
    GeneratorSource(count=5),
    APISource()
]
```
### Вывод
```
Processing task: 5fe0880c-5aa4-4336-851e-2765ecea3dc4 | Payload: {'source': 'file', 'type': 'order', 'data': 'Process order #12345'} | Priority: 2
Processing task: e329da19-76d7-4415-a0e5-23ecc9e7a0e0 | Payload: {'source': 'file', 'type': 'notification', 'data': 'Send email to user@example.com'} | Priority: 5
Processing task: d934ac20-dc72-49e3-a9c7-89e2c91e9a87 | Payload: {'source': 'file', 'type': 'analytics', 'data': 'Recalculate statistics for 2024'} | Priority: 3
Processing task: f9ff8d27-346d-43a7-8d4a-13cc1150b624 | Payload: {'source': 'generator'} | Priority: 0
Processing task: b610f2c8-ae79-4dc2-a0f7-cca2a7d19672 | Payload: {'source': 'generator'} | Priority: 1
Processing task: ca36b4a5-19b0-4bba-90be-1370e82747be | Payload: {'source': 'generator'} | Priority: 2
Processing task: 60d4242d-cee3-4177-98d7-c844480e557f | Payload: {'source': 'generator'} | Priority: 3
Processing task: eadb9082-ffa2-423f-b106-e15662159154 | Payload: {'source': 'generator'} | Priority: 4
Processing task: 45a52737-6c07-4967-9862-c15515aefd20 | Payload: {'source': 'api'} | Priority: 4
...
```
## Тестирование
Покрытие кода
```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
src\__init__.py                      0      0   100%
src\dispatcher.py                   16      0   100%
src\exeptions\task_exeption.py       2      0   100%
src\main.py                          8      8     0%   1-14
src\models.py                       39      1    97%   52
src\protocols.py                     5      0   100%
src\sources.py                      21      0   100%
--------------------------------------------------------------
TOTAL                               91      9    90%
```
