# Лабораторная работа №1, семестр 2: Источники задач и контракты
## Описание
Модуль приёма задач для платформы обработки заданий. Реализует контрактное программирование на основе typing.Protocol с поддержкой Duck Typing. Система позволяет подключать различные источники задач без изменения существующего кода.
Ключевые особенности
* Duck Typing  источники совместимы структурно, а не через наследование
* Protocol + @runtime_checkable  проверка контрактов во время выполнения
* Расширяемость  новые источники добавляются без модификации ядра
* Тесты  покрытие 86%
##Структура проекта
```
lab_2sem_1/
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── protocols.py
│   ├── sources.py
│   ├── dispatcher.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py
│   └──
├── src/data/
│   └── data.json
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
    FileTaskSource("src/data/data.json"),
    GeneratorTaskSource(count=5),
    APIMockSource()
]
```
### Вывод
```
Processing task: file_1 | Payload: {'source': 'file'}
Processing task: file_2 | Payload: {'source': 'file'}
Processing task: gen_0 | Payload: {'source': 'generator'}
Processing task: gen_1 | Payload: {'source': 'generator'}
...
```
## Тестирование
Покрытие кода
```
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src\__init__.py         0      0   100%
src\dispatcher.py      16      0   100%
src\main.py             8      8     0%   1-14
src\models.py           6      0   100%
src\protocols.py        5      0   100%
src\sources.py         21      0   100%
-------------------------------------------------
TOTAL                  56      8    86%
```
