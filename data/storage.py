import json
import os
from typing import List
from models.user import User
from models.project import Project
from models.task import Task
from models.schemas import DataSchema
from pydantic import ValidationError


class DataStore:
    def __init__(self, path: str | None = None):
        self.path = path or os.path.join(os.path.dirname(__file__), "data.json")
        self.users: List[User] = []
        self.projects: List[Project] = []
        import logging
        self.logger = logging.getLogger(__name__)

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
        # Validate structure with pydantic schema; if invalid, back up file and reset
        try:
            DataSchema.parse_obj(d)
        except ValidationError:
            # backup bad file
            bak = self.path + ".bak"
            try:
                os.replace(self.path, bak)
            except Exception:
                pass
            self._create_empty()
            return
        self.users = [User.from_dict(u) for u in d.get("users", [])]
        self.projects = [Project.from_dict(p) for p in d.get("projects", [])]

    def save(self):
        """Persist current in-memory users and projects to the JSON file using atomic replace."""
        out = {"version": 1, "users": [u.to_dict() for u in self.users], "projects": [p.to_dict() for p in self.projects]}
        dirpath = os.path.dirname(self.path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        # Write to a temp file then atomically replace
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, self.path)

    def _create_empty(self):
        """Create an empty data file and initialize in-memory lists."""
        self.users = []
        self.projects = []
        self.save()

    def add_user(self, user: User):
        """Add a User instance to the store."""
        self.users.append(user)

    def add_project(self, project: Project):
        """Add a Project instance to the store and register it with owner user."""
        self.projects.append(project)
        # Update owner's project list if user exists
        if project.owner_id is not None:
            owner = self.find_user_by_id(project.owner_id)
            if owner:
                owner.add_project(project.id)

    def find_user_by_id(self, id: int) -> User | None:
        """Return a User by numeric id or None."""
        for u in self.users:
            if u.id == id:
                return u
        return None

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
