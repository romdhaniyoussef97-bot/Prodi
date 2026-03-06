from datetime import datetime, timedelta


def calculate_task_duration_minutes(task):
    total_minutes = 0

    for session in task["sessions"]:
        start = datetime.fromisoformat(session["start"])

        if session["end"] is None:
            end = datetime.now()
        else:
            end = datetime.fromisoformat(session["end"])

        total_minutes += int((end - start).total_seconds() / 60)

    return total_minutes


def format_minutes(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"


def filter_tasks_by_date(tasks, target_date):
    filtered_tasks = []

    for task in tasks:
        if task["start_time"] is None:
            continue

        task_date = datetime.fromisoformat(task["start_time"]).date()

        if task_date == target_date:
            filtered_tasks.append(task)

    return filtered_tasks


def filter_tasks_by_date_range(tasks, start_date, end_date):
    filtered_tasks = []

    for task in tasks:
        if task["start_time"] is None:
            continue

        task_date = datetime.fromisoformat(task["start_time"]).date()

        if start_date <= task_date <= end_date:
            filtered_tasks.append(task)

    return filtered_tasks


def build_report(tasks, title):
    total_minutes = 0
    category_totals = {
        "Work": 0,
        "Study": 0,
        "Workout": 0
    }

    completed_count = 0
    incomplete_count = 0

    for task in tasks:
        task_minutes = calculate_task_duration_minutes(task)
        total_minutes += task_minutes

        category = task["category"]
        if category in category_totals:
            category_totals[category] += task_minutes

        if task["status"] == "completed":
            if task["completion_percent"] == 100:
                completed_count += 1
            else:
                incomplete_count += 1

    lines = []
    lines.append(f"\n{title}")
    lines.append("--------------------------------")
    lines.append(f"Total productive time: {format_minutes(total_minutes)}")
    lines.append("")
    lines.append("Time by category:")
    lines.append(f"Work: {format_minutes(category_totals['Work'])}")
    lines.append(f"Study: {format_minutes(category_totals['Study'])}")
    lines.append(f"Workout: {format_minutes(category_totals['Workout'])}")
    lines.append("")
    lines.append(f"Completed tasks: {completed_count}")
    lines.append(f"Incomplete tasks: {incomplete_count}")
    lines.append(f"Total tasks in report: {len(tasks)}")

    return "\n".join(lines)


def generate_daily_report(data, target_date=None):
    if target_date is None:
        target_date = datetime.now().date()

    tasks = filter_tasks_by_date(data["tasks"], target_date)
    title = f"Daily Report — {target_date}"

    return build_report(tasks, title)


def generate_weekly_report(data, target_date=None):
    if target_date is None:
        target_date = datetime.now().date()

    start_of_week = target_date - timedelta(days=target_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    tasks = filter_tasks_by_date_range(data["tasks"], start_of_week, end_of_week)
    title = f"Weekly Report — {start_of_week} to {end_of_week}"

    return build_report(tasks, title)


def generate_monthly_report(data, target_date=None):
    if target_date is None:
        target_date = datetime.now().date()

    year = target_date.year
    month = target_date.month

    tasks = []

    for task in data["tasks"]:
        if task["start_time"] is None:
            continue

        task_date = datetime.fromisoformat(task["start_time"]).date()

        if task_date.year == year and task_date.month == month:
            tasks.append(task)

    title = f"Monthly Report — {year}-{month:02d}"

    return build_report(tasks, title)