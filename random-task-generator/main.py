"""Точка входа в приложение."""
from services.task_manager import TaskManager
from ui.cli import ConsoleUI


def main():
    manager = TaskManager()
    ui = ConsoleUI(manager)
    ui.run()


if __name__ == "__main__":
    main()