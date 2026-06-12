class Task:
    _id_counter = 1

    def __init__(self, title: str, status: str = "open", assigned_to: int | None = None, id: int | None = None):
        """Initialize a Task with optional status and assignee.

        New tasks get an auto-incremented id unless `id` is provided.
        """
        if id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = id
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    def to_dict(self):
        """Serialize the task for JSON storage."""
        return {"id": self.id, "title": self.title, "status": self.status, "assigned_to": self.assigned_to}

    @classmethod
    def from_dict(cls, d):
        """Recreate a Task from its dictionary form and adjust id counter."""
        t = cls(title=d.get("title"), status=d.get("status", "open"), assigned_to=d.get("assigned_to"), id=d.get("id"))
        if d.get("id") and d.get("id") >= cls._id_counter:
            cls._id_counter = d.get("id") + 1
        return t

    def __repr__(self):
        """Readable representation used in CLI messages."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status})"
