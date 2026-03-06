from datetime import datetime


class Task:
    def __init__(self, task_id, category, name=None, expected_minutes=None):
        self.id = task_id
        self.category = category
        self.name = name
        self.expected_minutes = expected_minutes

        self.start_time = None
        self.end_time = None
        self.status = "created"

        self.completion_percent = None

        # sessions are used for pause/resume
        self.sessions = []

    def start(self):
        now = datetime.now().isoformat()

        self.start_time = now
        self.status = "running"

        self.sessions.append({
            "start": now,
            "end": None
        })

    def pause(self):
        if self.status != "running":
            return

        now = datetime.now().isoformat()

        self.sessions[-1]["end"] = now
        self.status = "paused"

    def resume(self):
        if self.status != "paused":
            return

        now = datetime.now().isoformat()

        self.sessions.append({
            "start": now,
            "end": None
        })

        self.status = "running"

    def finish(self, completion_percent, end_time=None):
        if end_time is None:
            end_time = datetime.now().isoformat()

        # close current session
        if self.sessions and self.sessions[-1]["end"] is None:
            self.sessions[-1]["end"] = end_time

        self.end_time = end_time
        self.completion_percent = completion_percent
        self.status = "completed"

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "expected_minutes": self.expected_minutes,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "completion_percent": self.completion_percent,
            "sessions": self.sessions
        }