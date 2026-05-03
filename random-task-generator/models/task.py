"""Модуль с базовым классом Task и конкретными типами задач."""
from abc import ABC


class Task(ABC):
    """Абстрактный базовый класс для всех задач."""
    VALID_TYPES = {"work", "sport", "study"}
    VALID_DIFFICULTIES = {"easy", "medium", "hard"}

    def __init__(self, description: str, diff: str):
        self.description = description
        self.difficulty = diff
        self._type = None  # будет установлен в подклассах

    @property
    def type(self) -> str:
        return self._type

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return (self.description, self.type, self.difficulty) == (
            other.description, other.type, other.difficulty)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description!r}, {self.difficulty!r})"


class WorkTask(Task):
    """Рабочая задача."""
    def __init__(self, description: str, diff: str):
        super().__init__(description, diff)
        self._type = "work"


class SportTask(Task):
    """Спортивная задача."""
    def __init__(self, description: str, diff: str):
        super().__init__(description, diff)
        self._type = "sport"


class StudyTask(Task):
    """Учебная задача."""
    def __init__(self, description: str, diff: str):
        super().__init__(description, diff)
        self._type = "study"