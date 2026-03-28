import pytest
import uuid
from datetime import datetime
from models import Task
from protocols import TaskSource
from sources import FileSource, GeneratorSource, APISource
from dispatcher import TaskDispatcher
from exeptions.task_exeption import TaskCheckError

class TestTask:
    """Тесты модели задачи и дескрипторов"""
    def test_task_creation(self):
        """Проверка создания задачи"""
        task = Task(payload={"data": "test"}, priority=7)
        assert isinstance(task.id, str)
        assert len(task.id) > 0
        assert task.payload == {"data": "test"}
        assert task.priority == 7
    def test_priority_validation(self):
        """Проверка валидации приоритета"""
        task = Task(payload={})
        task.priority = 0
        assert task.priority == 0
        task.priority = 10
        assert task.priority == 10
        with pytest.raises(TaskCheckError):
            task.priority = 11
        with pytest.raises(TaskCheckError):
            task.priority = -1
    def test_priority_types(self):
        """Проверка типов данных для приоритета"""
        task = Task(payload={})
        with pytest.raises(TaskCheckError):
            task.priority = "5"
        with pytest.raises(TaskCheckError):
            task.priority = 5.5
    def test_id_is_readonly(self):
        """Проверка что id и дата неизменяемы"""
        task = Task(payload={})
        with pytest.raises(AttributeError):
            task.id = "new_id"
        with pytest.raises(AttributeError):
            task.created_at = datetime.now()
    def test_default_priority(self):
        """Проверка значения приоритета по умолчанию"""
        task = Task(payload={})
        assert task.priority == 5
    def test_unique_uuids(self):
        """Проверка уникальности id для разных объектов"""
        task1 = Task(payload={})
        task2 = Task(payload={})
        assert task1.id != task2.id
        assert isinstance(uuid.UUID(task1.id), uuid.UUID)
    def test_task_created_cover(self):
        task = Task(payload={"data": 123})
        assert task.payload == {"data": 123}
        assert isinstance(task.created_at, datetime)
class TestTaskSourceProtocol:
    """Тесты протокола источников"""
    def test_runtime_checkable(self):
        assert hasattr(TaskSource, '_is_runtime_protocol')
    def test_valid_source_isinstance(self):
        """Проверка isinstance для валидного источника"""
        source = GeneratorSource(5)
        assert isinstance(source, TaskSource)
    def test_invalid_source_isinstance(self):
        """Проверка isinstance для невалидного объекта"""
        class InvalidSource:
            pass
        invalid = InvalidSource()
        assert not isinstance(invalid, TaskSource)
    def test_source_has_get_tasks_method(self):
        """Проверка наличия метода get_tasks у источников"""
        sources = [
            FileSource("test.json"),
            GeneratorSource(5),
            APISource()
        ]
        for source in sources:
            assert hasattr(source, 'get_tasks')
            assert callable(getattr(source, 'get_tasks'))
class TestFileSource:
    """Тесты источника из файла"""
    def test_file_source_handles_missing_file(self):
        """Проверка обработки отсутствующего файла"""
        source = FileSource("stupid_file.json")
        tasks = source.get_tasks()
        assert isinstance(tasks, list)
    def test_file_source_creation(self):
        """Проверка создания источника"""
        source = FileSource("src/data/data.json")
        assert source.filepath == "src/data/data.json"
    def test_file_source_get_tasks(self):
        """Проверка что get_tasks возвращает список"""
        source = FileSource("src/data/data.json")
        tasks = source.get_tasks()
        assert isinstance(tasks, list)
    def test_file_source_get_tasks_(self):
        """Проверка что get_tasks возвращает объекты Task"""
        source = FileSource("src/data/data.json")
        tasks = source.get_tasks()
        if len(tasks) > 0:
            assert all(isinstance(task, Task) for task in tasks)
    def test_file_source_protocol_compliance(self):
        """Проверка соответствия протоколу"""
        source = FileSource("src/data/data.json")
        assert isinstance(source, TaskSource)
class TestGeneratorSource:
    """Тесты генератора задач"""
    def test_generator_source_creation(self):
        """Проверка создания генератора"""
        source = GeneratorSource(10)
        assert source.count == 10
    def test_generator_source_count(self):
        """Проверка количества генерируемых задач"""
        source = GeneratorSource(7)
        tasks = source.get_tasks()
        assert len(tasks) == 7
    def test_generator_source_ids(self):
        """Проверка уникальности ID задач"""
        source = GeneratorSource(5)
        tasks = source.get_tasks()
        ids = [task.id for task in tasks]
        assert len(ids) == len(set(ids))
    def test_generator_source_protocol(self):
        """Проверка соответствия протоколу"""
        source = GeneratorSource(5)
        assert isinstance(source, TaskSource)
class TestAPISource:
    """Тесты API заглушки"""
    def test_api_source_creation(self):
        """Проверка создания API источника"""
        source = APISource()
        assert source is not None
    def test_api_source_get_tasks(self):
        """Проверка, что get_tasks возвращает список"""
        source = APISource()
        tasks = source.get_tasks()
        assert isinstance(tasks, list)
    def test_api_source_get_tasks_(self):
        """Проверка что get_tasks возвращает объекты Task"""
        source = APISource()
        tasks = source.get_tasks()
        assert len(tasks) > 0
        assert all(isinstance(task, Task) for task in tasks)
    def test_api_source_protocol(self):
        """Проверка соответствия протоколу"""
        source = APISource()
        assert isinstance(source, TaskSource)
class TestTaskDispatcher:
    """Тесты диспетчера задач"""
    def test_dispatcher_creation(self):
        """Проверка создания диспетчера с валидными источниками"""
        sources = [GeneratorSource(5), APISource()]
        dispatcher = TaskDispatcher(sources)
        assert len(dispatcher.sources) == 2
    def test_dispatcher_reject(self):
        """Проверка отклонения невалидного источника"""
        class InvalidSource:
            pass
        with pytest.raises(TypeError) as exc_info:
            TaskDispatcher([InvalidSource()])
        assert "does not implement TaskSource" in str(exc_info.value)
    def test_dispatcher_process(self):
        """Проверка что process_all вызывает get_tasks у всех источников"""
        source1 = GeneratorSource(3)
        source2 = APISource()
        dispatcher = TaskDispatcher([source1, source2])
        dispatcher.process_all()
    def test_dispatcher_empty_s(self):
        """Проверка работы с пустым списком источников"""
        dispatcher = TaskDispatcher([])
        assert len(dispatcher.sources) == 0
        dispatcher.process_all()
class TestRuntimeContractCheck:
    def test_isinstance_check_invalid(self):
        """Проверка isinstance с объектом где нет метода get_tasks"""
        class FakeSource:
            pass
        fake = FakeSource()
        assert isinstance(fake, TaskSource) is False
    def test_isinstance_check(self):
        class CompatibleSource:
            def get_tasks(self):
                return []
        compatible = CompatibleSource()
        assert isinstance(compatible, TaskSource) is True
    def test_issubclass(self):
        """Проверка issubclass для классов источников"""
        assert issubclass(GeneratorSource, TaskSource) is True
        assert issubclass(FileSource, TaskSource) is True
        assert issubclass(APISource, TaskSource) is True
class TestIntegration:
    """Интеграционные тесты всей системы"""
    def test_full_pipeline(self):
        """Проверка полного цикла обработки задач"""
        sources = [GeneratorSource(3), APISource()]
        dispatcher = TaskDispatcher(sources)
        dispatcher.process_all()
    def test_source_independence(self):
        """Проверка независимости источников (уникальность ID)"""
        source1 = GeneratorSource(5)
        source2 = GeneratorSource(5)
        tasks1 = source1.get_tasks()
        tasks2 = source2.get_tasks()
        ids1 = set(t.id for t in tasks1)
        ids2 = set(t.id for t in tasks2)
        assert ids1.isdisjoint(ids2)
