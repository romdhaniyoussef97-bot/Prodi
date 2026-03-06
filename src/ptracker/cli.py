from datetime import datetime

from tracker_core.storage import (
    add_task,
    get_ongoing_tasks,
    pause_task,
    resume_task,
    finish_task
)
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

    while True:
        choice = input("\nEnter task ID to manage it, or 0 to return: ").strip()

        if choice == "0":
            return

        try:
            task_id = int(choice)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            continue

        selected_task = None

        for task in tasks:
            if task["id"] == task_id:
                selected_task = task
                break

        if selected_task is None:
            print("Task not found. Please try again.")
            continue

        manage_ongoing_task(selected_task)
        return

    
def get_task_duration_minutes(task):
    total_minutes = 0

    for session in task["sessions"]:
        start = datetime.fromisoformat(session["start"])

        if session["end"] is not None:
            end = datetime.fromisoformat(session["end"])
        else:
            end = datetime.now()

        total_minutes += int((end - start).total_seconds() / 60)

    return total_minutes


def show_task_status(task):
    duration = get_task_duration_minutes(task)

    print("\nTask Status")
    print("--------------------------------")
    print(f"ID: {task['id']}")
    print(f"Category: {task['category']}")
    print(f"Name: {task['name']}")
    print(f"Status: {task['status']}")
    print(f"Current tracked time: {duration} minutes")


def ask_finish_time():
    print("\nIs this the actual time you finished?")
    print("1. Yes")
    print("2. No")

    choice = input("> ").strip()

    if choice == "1":
        return None

    if choice == "2":
        user_time = input("Enter the approximate finish time (HH:MM): ").strip()

        try:
            hours, minutes = user_time.split(":")
            now = datetime.now()
            custom_time = now.replace(
                hour=int(hours),
                minute=int(minutes),
                second=0,
                microsecond=0
            )
            return custom_time.isoformat()
        except ValueError:
            print("Invalid time format. Current time will be used.")
            return None

    print("Invalid choice. Current time will be used.")
    return None


def ask_completion_percentage():
    print("\nDid you achieve your goal for this task?")
    print("1. Yes")
    print("2. No")

    choice = input("> ").strip()

    if choice == "1":
        return 100

    if choice == "2":
        while True:
            percent = input("Enter completion percentage (0-99): ").strip()

            try:
                percent = int(percent)
                if 0 <= percent <= 99:
                    return percent
            except ValueError:
                pass

            print("Invalid percentage. Please enter a number between 0 and 99.")

    print("Invalid choice. Defaulting to 100%.")
    return 100


def manage_ongoing_task(task):
    while True:
        print("\nTask Actions")
        print("--------------------------------")
        print("1. Pause task")
        print("2. Resume task")
        print("3. Finish task")
        print("4. Show status")
        print("0. Return")

        choice = input("> ").strip()

        if choice == "0":
            return

        elif choice == "1":
            updated_task = pause_task(task["id"])

            if updated_task is None:
                print("This task cannot be paused.")
            else:
                log_info(f"Task paused: {task['id']}")
                print("Task paused successfully.")
                task = updated_task

        elif choice == "2":
            updated_task = resume_task(task["id"])

            if updated_task is None:
                print("This task cannot be resumed.")
            else:
                log_info(f"Task resumed: {task['id']}")
                print("Task resumed successfully.")
                task = updated_task

        elif choice == "3":
            end_time = ask_finish_time()
            completion_percent = ask_completion_percentage()

            updated_task = finish_task(task["id"], completion_percent, end_time)

            if updated_task is None:
                print("This task cannot be finished.")
            else:
                log_info(f"Task finished: {task['id']}")
                print("Task finished successfully.")
                return

        elif choice == "4":
            show_task_status(task)

        else:
            log_warning("Invalid task action selected.")
            print("Invalid choice. Please try again.")


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