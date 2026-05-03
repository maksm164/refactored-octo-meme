"""Консольный интерфейс с проверкой ввода."""
from models.task_factory import TaskFactory
from services.task_manager import TaskManager
from services.json_service import TaskJSONService


class ConsoleUI:
    def __init__(self, manager: TaskManager):
        self.manager = manager

    @staticmethod
    def input_nonempty(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Error: input cannot be empty.")

    @staticmethod
    def input_choice(prompt: str, variants: set) -> str:
        while True:
            value = input(prompt).strip().lower()
            if value in variants:
                return value
            print(f"Error: choose from {variants}.")

    def add_task(self):
        print("\n--- Add new task to pool ---")
        desc = self.input_nonempty("Description: ")
        ttype = self.input_choice("Type (work/sport/study): ",
                                  {"work", "sport", "study"})
        diff = self.input_choice("Difficulty (easy/medium/hard): ",
                                 {"easy", "medium", "hard"})
        try:
            task = TaskFactory.create_task(ttype, desc, diff)
            self.manager.add_to_pool(task)
            print(f"Task added: {task}")
        except ValueError as e:
            print(f"Error: {e}")

    def generate_random(self):
        print("\n--- Generate random task ---")
        filter_type = input("Filter by type (work/sport/study) or press Enter to skip: ").strip().lower()
        if filter_type and filter_type not in {"work", "sport", "study"}:
            print("Invalid type. Filter will be ignored.")
            filter_type = None
        filter_diff = input("Filter by difficulty (easy/medium/hard) or press Enter to skip: ").strip().lower()
        if filter_diff and filter_diff not in {"easy", "medium", "hard"}:
            print("Invalid difficulty. Filter will be ignored.")
            filter_diff = None

        task = self.manager.generate_random(
            filter_type=filter_type or None,
            filter_difficulty=filter_diff or None
        )
        if task:
            print(f"Generated: {task}")
        else:
            print("No tasks matching the criteria. Add more tasks to the pool.")

    def view_history(self):
        history = self.manager.get_history_list()
        print("\n--- History (old → new) ---")
        if not history:
            print("History is empty.")
            return
        for i, task in enumerate(history, 1):
            print(f"{i}. {task}")

    def save_history(self):
        filename = input("Filename to save history (e.g. history.json): ").strip()
        if not filename:
            print("Filename cannot be empty.")
            return
        tasks = self.manager.get_history_list()
        try:
            TaskJSONService.save_history(filename, tasks)
            print(f"History saved to {filename}")
        except Exception as e:
            print(f"Save failed: {e}")

    def load_history(self):
        filename = input("Filename to load history (e.g. history.json): ").strip()
        if not filename:
            print("Filename cannot be empty.")
            return
        try:
            tasks = TaskJSONService.load_history(filename)
            self.manager.set_history(tasks)
            print(f"Loaded {len(tasks)} tasks into history.")
        except Exception as e:
            print(f"Load failed: {e}")

    def run(self):
        menu = """
Choose an action:
1. Add new task to pool
2. Generate random task
3. View generation history
4. Save history to JSON
5. Load history from JSON
6. Exit
"""
        while True:
            print(menu)
            choice = input("Your choice: ").strip()
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.generate_random()
            elif choice == "3":
                self.view_history()
            elif choice == "4":
                self.save_history()
            elif choice == "5":
                self.load_history()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Wrong input. Try again.")