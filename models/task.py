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
        # Support single id or list of contributor ids
        if assigned_to is None:
            self.assigned_to: list[int] = []
        elif isinstance(assigned_to, list):
            self.assigned_to = assigned_to
        else:
            self.assigned_to = [assigned_to]

    def to_dict(self):
        """Serialize the task for JSON storage."""
        return {"id": self.id, "title": self.title, "status": self.status, "assigned_to": self.assigned_to}

    @classmethod
    def from_dict(cls, d):
        """Recreate a Task from its dictionary form and adjust id counter."""
        assigned = d.get("assigned_to")
        # Ensure assigned is a list for backward compatibility
        if isinstance(assigned, int):
            assigned = [assigned]
        t = cls(title=d.get("title"), status=d.get("status", "open"), assigned_to=assigned, id=d.get("id"))
        if d.get("id") and d.get("id") >= cls._id_counter:
            cls._id_counter = d.get("id") + 1
        return t

    def __repr__(self):
        """Readable representation used in CLI messages."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status})"

    def add_contributor(self, user_id: int):
        """Add a contributor user id to this task."""
        if user_id not in self.assigned_to:
            self.assigned_to.append(user_id)

    def mark_done(self):
        """Mark task status as done."""
        self.status = "done"
