"""Фабрика для создания задач нужного типа."""
from .task import Task, WorkTask, SportTask, StudyTask


class TaskFactory:
    """Создаёт экземпляр подходящего подкласса Task."""

    TYPE_CLASS_MAP = {
        "work": WorkTask,
        "sport": SportTask,
        "study": StudyTask,
    }

    @staticmethod
    def create_task(task_type: str, description: str, difficulty: str) -> Task:
        """
        Args:
            task_type: допустимое значение из Task.VALID_TYPES.
            description: непустая строка.
            difficulty: допустимое значение из Task.VALID_DIFFICULTIES.

        Returns:
            Подкласс Task.

        Raises:
            ValueError: если параметры невалидны.
        """
        task_type = task_type.strip().lower()
        if task_type not in Task.VALID_TYPES:
            raise ValueError(f"Invalid task type: '{task_type}'. "
                             f"Choose from {Task.VALID_TYPES}")

        if not description or not description.strip():
            raise ValueError("Description cannot be empty.")

        difficulty = difficulty.strip().lower()
        if difficulty not in Task.VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: '{difficulty}'. "
                             f"Choose from {Task.VALID_DIFFICULTIES}")

        task_class = TaskFactory.TYPE_CLASS_MAP[task_type]
        return task_class(description.strip(), difficulty)