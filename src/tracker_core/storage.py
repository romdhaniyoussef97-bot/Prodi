import json
from pathlib import Path

from ptracker.config import DATA_FILE
from tracker_core.models import Task


def ensure_data_file():
    """
    Create the data file with an initial structure if it does not exist
    or if it is empty.
    """
    data_path = Path(DATA_FILE)
    data_path.parent.mkdir(parents=True, exist_ok=True)

    if not data_path.exists() or data_path.stat().st_size == 0:
        initial_data = {
            "tasks": [],
            "notes": []
        }
        with open(data_path, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)


def load_data():
    """
    Load and return all data from the JSON file.
    """
    ensure_data_file()

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    """
    Save all data to the JSON file.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_next_task_id(data):
    """
    Return the next available task ID.
    """
    tasks = data["tasks"]

    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def add_task(category, name=None, expected_minutes=None):
    """
    Create a new task, start it immediately, save it, and return it.
    """
    data = load_data()
    task_id = get_next_task_id(data)

    task = Task(task_id, category, name, expected_minutes)
    task.start()

    data["tasks"].append(task.to_dict())
    save_data(data)

    return task.to_dict()


def get_ongoing_tasks():
    """
    Return all tasks that are currently running or paused.
    """
    data = load_data()

    ongoing_tasks = [
        task for task in data["tasks"]
        if task["status"] in ["running", "paused"]
    ]

    return ongoing_tasks


def get_task_by_id(task_id):
    """
    Return a task dictionary by its ID, or None if not found.
    """
    data = load_data()

    for task in data["tasks"]:
        if task["id"] == task_id:
            return task

    return None


def update_task(updated_task):
    """
    Replace an existing task in the JSON file with updated task data.
    """
    data = load_data()

    for index, task in enumerate(data["tasks"]):
        if task["id"] == updated_task["id"]:
            data["tasks"][index] = updated_task
            save_data(data)
            return True

    return False