"""Управление пулом задач и историей (очередь)."""
import random
from collections import deque

from models.task import Task
from models.task_factory import TaskFactory


class TaskManager:
    """Хранит пул всех возможных задач и историю сгенерированных (FIFO)."""

    def __init__(self):
        self._pool: list[Task] = []
        self._history = deque()  # очередь сгенерированных задач

    @property
    def pool(self) -> list[Task]:
        return self._pool

    @property
    def history(self) -> deque:
        return self._history

    def add_to_pool(self, task: Task) -> None:
        """Добавление задачи в общий пул."""
        self._pool.append(task)

    def generate_random(self,
                        filter_type: str | None = None,
                        filter_difficulty: str | None = None) -> Task | None:
        """
        Случайная задача из пула с опциональными фильтрами.
        Если фильтры заданы, выбирает из задач, удовлетворяющих условиям.
        Возвращает None, если подходящих задач нет.
        Сгенерированная задача добавляется в историю (очередь).
        """
        candidates = self._pool[:]

        if filter_type:
            candidates = [t for t in candidates if t.type == filter_type]
        if filter_difficulty:
            candidates = [t for t in candidates
                          if t.difficulty == filter_difficulty]

        if not candidates:
            return None

        chosen = random.choice(candidates)
        self._history.append(chosen)
        return chosen

    def get_history_list(self) -> list[Task]:
        """История в виде списка (от старых к новым)."""
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()

    def set_history(self, tasks: list[Task]) -> None:
        """Замена всей истории новым списком задач (для загрузки)."""
        self._history = deque(tasks)