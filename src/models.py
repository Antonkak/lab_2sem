from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
    """Модель задачи"""
    id: str
    payload: Any
