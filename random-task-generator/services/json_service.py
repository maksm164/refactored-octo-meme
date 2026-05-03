"""Сохранение и загрузка истории задач в JSON."""
import json
import os
from typing import List

from models.task import Task
from models.task_factory import TaskFactory


class TaskJSONService:
    """Сериализация и десериализация списка задач (истории)."""

    @staticmethod
    def tasks_to_dicts(tasks: List[Task]) -> List[dict]:
        return [
            {
                "description": t.description,
                "type": t.type,
                "difficulty": t.difficulty,
            }
            for t in tasks
        ]

    @staticmethod
    def dicts_to_tasks(dicts: List[dict]) -> List[Task]:
        tasks = []
        for d in dicts:
            tasks.append(
                TaskFactory.create_task(
                    task_type=d["type"],
                    description=d["description"],
                    difficulty=d["difficulty"]
                )
            )
        return tasks

    @staticmethod
    def save_history(filename: str, tasks: List[Task]) -> None:
        """Сохраняет список задач в JSON-файл."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(TaskJSONService.tasks_to_dicts(tasks), f,
                      ensure_ascii=False, indent=2)

    @staticmethod
    def load_history(filename: str) -> List[Task]:
        """
        Загружает список задач из JSON-файла.
        Если файла нет, возвращает пустой список.
        """
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return TaskJSONService.dicts_to_tasks(data)