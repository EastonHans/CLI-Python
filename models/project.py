from typing import List
from .task import Task


class Project:
    _id_counter = 1

    def __init__(self, title: str, description: str = "", due_date: str | None = None, owner_id: int | None = None, tasks: List[Task] | None = None, id: int | None = None):
        """Create a Project instance.

        `due_date` should be an ISO date string (YYYY-MM-DD) or None.
        """
        if id is None:
            self.id = Project._id_counter
            Project._id_counter += 1
        else:
            self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.tasks = tasks or []

    def assign_contributor(self, task_id: int, user_id: int) -> bool:
        """Assign a contributor (user id) to a task within this project.

        Returns True if task found and user added, False otherwise.
        """
        for t in self.tasks:
            if t.id == task_id:
                t.add_contributor(user_id)
                return True
        return False

    def get_task(self, task_id: int) -> Task | None:
        """Return the Task with the given id or None."""
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def add_task(self, task: Task):
        """Attach a Task instance to this project."""
        self.tasks.append(task)

    def to_dict(self):
        """Serialize the project including nested tasks."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_id": self.owner_id,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, d):
        """Recreate a Project from its dict representation.

        Restores Task objects for nested tasks and adjusts id counters.
        """
        tasks = [Task.from_dict(td) for td in d.get("tasks", [])]
        p = cls(title=d.get("title"), description=d.get("description", ""), due_date=d.get("due_date"), owner_id=d.get("owner_id"), tasks=tasks, id=d.get("id"))
        if d.get("id") and d.get("id") >= cls._id_counter:
            cls._id_counter = d.get("id") + 1
        return p

    def __repr__(self):
        """Short representation for CLI messages."""
        return f"Project(id={self.id}, title={self.title!r})"
