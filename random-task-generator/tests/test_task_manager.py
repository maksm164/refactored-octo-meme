from models.task_factory import TaskFactory
from services.task_manager import TaskManager


class TestTaskManager:
    def setup_method(self):
        self.manager = TaskManager()
        self.t1 = TaskFactory.create_task("work", "Write report", "easy")
        self.t2 = TaskFactory.create_task("sport", "Run 5km", "hard")
        self.t3 = TaskFactory.create_task("study", "Read chapter 5", "medium")
        for t in [self.t1, self.t2, self.t3]:
            self.manager.add_to_pool(t)

    def test_generate_random_returns_task(self):
        task = self.manager.generate_random()
        assert task is not None
        assert task in [self.t1, self.t2, self.t3]

    def test_generate_filtered_by_type(self):
        task = self.manager.generate_random(filter_type="sport")
        assert task is not None
        assert task.type == "sport"

    def test_generate_filtered_no_match(self):
        self.manager._pool = [self.t1]  # only work
        task = self.manager.generate_random(filter_type="study")
        assert task is None

    def test_history_is_fifo(self):
        # generate three tasks
        tasks = []
        for _ in range(3):
            t = self.manager.generate_random()
            if t: tasks.append(t)
        hist = self.manager.get_history_list()
        assert len(hist) == 3
        assert hist == tasks  # same order

    def test_clear_history(self):
        self.manager.generate_random()
        self.manager.clear_history()
        assert len(self.manager.get_history_list()) == 0

    def test_set_history(self):
        tasks = [self.t1, self.t2]
        self.manager.set_history(tasks)
        assert list(self.manager.history) == tasks