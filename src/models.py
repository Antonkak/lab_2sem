from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime
from exeptions.task_exeption import TaskCheckError

class PriorCheck:
    def __init__(self, default=5):
        self._default = default

    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name, self._default)

    def __set__(self, instance, value):
        if isinstance(value, PriorCheck):
            value = self._default

        if not isinstance(value, int):
            raise TaskCheckError("Priority must be an integer")
        if not (0 <= value <= 10):
            raise TaskCheckError("Priority must be between 0 and 10")

        setattr(instance, self._name, value)

@dataclass
class Task:
    """Модель задачи"""
    payload: Any
    priority: int = 5

    priority = PriorCheck(default=5) # type: ignore

    _id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    _created_at: datetime = field(default_factory=datetime.now, init=False)
    _status: str = field(default="New", init=False)

    @property
    def id(self) -> str:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_ready(self) -> bool:
        return self._status == "Completed"
