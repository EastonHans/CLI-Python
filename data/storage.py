import json
import os
from typing import List
from models.user import User
from models.project import Project
from models.task import Task


class DataStore:
    def __init__(self, path: str | None = None):
        self.path = path or os.path.join(os.path.dirname(__file__), "data.json")
        self.users: List[User] = []
        self.projects: List[Project] = []

    def load(self):
        """Load data from JSON file into memory, creating an empty store if needed."""
        if not os.path.exists(self.path):
            self._create_empty()
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            self._create_empty()
            return
        self.users = [User.from_dict(u) for u in d.get("users", [])]
        self.projects = [Project.from_dict(p) for p in d.get("projects", [])]

    def save(self):
        """Persist current in-memory users and projects to the JSON file."""
        out = {"users": [u.to_dict() for u in self.users], "projects": [p.to_dict() for p in self.projects]}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)

    def _create_empty(self):
        """Create an empty data file and initialize in-memory lists."""
        self.users = []
        self.projects = []
        self.save()

    def add_user(self, user: User):
        """Add a User instance to the store."""
        self.users.append(user)

    def add_project(self, project: Project):
        """Add a Project instance to the store."""
        self.projects.append(project)

    def add_task(self, project_id: int, task: Task):
        """Attach a Task to the given project by id."""
        proj = self.find_project_by_id(project_id)
        if proj:
            proj.add_task(task)

    def find_user_by_name(self, name: str) -> User | None:
        """Return a User matching `name` or None if not found."""
        for u in self.users:
            if u.name == name:
                return u
        return None

    def find_project_by_title(self, title: str) -> Project | None:
        """Return a Project matching `title` or None if not found."""
        for p in self.projects:
            if p.title == title:
                return p
        return None

    def find_project_by_id(self, id: int) -> Project | None:
        """Return a Project by its numeric id or None."""
        for p in self.projects:
            if p.id == id:
                return p
        return None

    def get_projects_for_user(self, user_id: int) -> List[Project]:
        """Get all projects owned by the given user id."""
        return [p for p in self.projects if p.owner_id == user_id]

    def complete_task(self, project_id: int, task_id: str) -> bool:
        """Mark a task as complete by id within a project. Returns True if updated."""
        p = self.find_project_by_id(project_id)
        if not p:
            return False
        for t in p.tasks:
            if str(t.id) == str(task_id):
                t.status = "done"
                return True
        return False
