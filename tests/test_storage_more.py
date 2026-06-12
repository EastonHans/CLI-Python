from data.storage import DataStore
from models.user import User
from models.project import Project
from models.task import Task


def test_storage_helpers(tmp_path):
    p = tmp_path / "d" / "data.json"
    ds = DataStore(path=str(p))
    ds._create_empty()
    u = User(name="Z", email="z@e.com")
    ds.add_user(u)
    proj = Project(title="Alpha", owner_id=u.id)
    ds.add_project(proj)
    t = Task(title="T")
    ds.add_task(proj.id, t)
    ds.save()
    assert ds.find_user_by_id(u.id) is not None
    assert ds.find_project_by_title("Alpha") is not None
    assert ds.get_projects_for_user(u.id)
    assert ds.complete_task(proj.id, "999") is False
    # completing existing
    assert ds.complete_task(proj.id, str(t.id)) is True

