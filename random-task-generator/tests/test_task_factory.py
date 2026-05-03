import pytest
from models.task_factory import TaskFactory
from models.task import WorkTask, SportTask, StudyTask


class TestTaskFactory:
    def test_create_work_task(self):
        t = TaskFactory.create_task("work", "Write report", "hard")
        assert isinstance(t, WorkTask)
        assert t.type == "work"
        assert t.description == "Write report"
        assert t.difficulty == "hard"

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError, match="Invalid task type"):
            TaskFactory.create_task("flying", "desc", "easy")

    def test_empty_description_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskFactory.create_task("work", "", "easy")

    def test_invalid_difficulty_raises(self):
        with pytest.raises(ValueError, match="Invalid difficulty"):
            TaskFactory.create_task("sport", "run", "impossible")

    def test_case_insensitive_type_and_difficulty(self):
        t = TaskFactory.create_task("STUDY", "Learn OOP", "MEDIUM")
        assert isinstance(t, StudyTask)
        assert t.difficulty == "medium"