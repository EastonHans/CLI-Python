from .user import User
from data.storage import DataStore


class Admin(User):
    """Administrator user with extra management actions."""

    def delete_project(self, project_id: int, ds: DataStore) -> bool:
        """Delete a project by id from the given DataStore."""
        proj = ds.find_project_by_id(project_id)
        if not proj:
            return False
        ds.projects = [p for p in ds.projects if p.id != project_id]
        # remove from users' project lists
        for u in ds.users:
            if hasattr(u, "_project_ids") and project_id in u._project_ids:
                u._project_ids.remove(project_id)
        ds.save()
        return True
