import json
import os
import tempfile
from services.json_service import TaskJSONService
from models.task_factory import TaskFactory


class TestJSONService:
    def setup_method(self):
        self.tasks = [
            TaskFactory.create_task("work", "Write report", "easy"),
            TaskFactory.create_task("sport", "Run 5km", "hard"),
            TaskFactory.create_task("study", "Learn Python", "medium"),
        ]
        self.tmpfile = tempfile.mktemp(suffix=".json")

    def teardown_method(self):
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)

    def test_roundtrip(self):
        TaskJSONService.save_history(self.tmpfile, self.tasks)
        loaded = TaskJSONService.load_history(self.tmpfile)
        assert len(loaded) == len(self.tasks)
        for orig, loaded_task in zip(self.tasks, loaded):
            assert orig == loaded_task

    def test_load_nonexistent_returns_empty(self):
        loaded = TaskJSONService.load_history("i_dont_exist.json")
        assert loaded == []

    def test_save_creates_valid_json(self):
        TaskJSONService.save_history(self.tmpfile, self.tasks)
        with open(self.tmpfile, 'r') as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["description"] == "Write report"