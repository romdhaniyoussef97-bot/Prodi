from datetime import datetime

from tracker_core.storage import add_task, get_ongoing_tasks
from ptracker.logger import log_info, log_warning


CATEGORIES = {
    "1": "Work",
    "2": "Study",
    "3": "Workout"
}


def show_main_menu():
    print("\nWelcome to PRODI")
    print("Productivity Tracker")

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Today's date: {today}")

    print("\nMain Menu")
    print("--------------------------------")
    print("1. Start a new task")
    print("2. View ongoing tasks")
    print("3. View reports")
    print("4. Exit")


def choose_category():
    while True:
        print("\nChoose a category:")
        print("1. Work")
        print("2. Study")
        print("3. Workout")
        print("0. Return")

        choice = input("> ").strip()

        if choice == "0":
            return None

        if choice in CATEGORIES:
            return CATEGORIES[choice]

        log_warning("Invalid category choice.")
        print("Invalid choice. Please try again.")


def start_task_flow():
    category = choose_category()

    if category is None:
        return

    name = input("\nEnter task name (optional): ").strip()
    if name == "":
        name = None

    expected = input("\nExpected time to finish (HH:MM) or press ENTER to skip: ").strip()

    expected_minutes = None

    if expected:
        try:
            hours, minutes = expected.split(":")
            expected_minutes = int(hours) * 60 + int(minutes)
        except ValueError:
            log_warning("Invalid time format entered.")
            print("Invalid time format. Skipping expected time.")

    task = add_task(category, name, expected_minutes)

    log_info(f"Task started: {task['id']}")

    print("\nTask started successfully!")
    print(f"Task ID: {task['id']}")
    print(f"Category: {task['category']}")
    print(f"Name: {task['name']}")


def view_ongoing_tasks():
    tasks = get_ongoing_tasks()

    if not tasks:
        print("\nNo ongoing tasks.")
        return

    print("\nOngoing Tasks")
    print("--------------------------------")

    for task in tasks:
        print(f"ID: {task['id']} | {task['category']} | {task['name']} | Status: {task['status']}")


def run_cli():
    while True:
        show_main_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            start_task_flow()

        elif choice == "2":
            view_ongoing_tasks()

        elif choice == "3":
            print("\nReports feature coming soon.")

        elif choice == "4":
            print("\nGoodbye.")
            break

        else:
            log_warning("Invalid menu selection.")
            print("Invalid choice. Please try again.")