from models.admin import Admin
from data.storage import DataStore
from models.project import Project
from models.user import User


def test_admin_delete(tmp_path):
    p = tmp_path / "data.json"
    ds = DataStore(path=str(p))
    ds._create_empty()
    u = User(name="Owner", email="o@e.com")
    ds.add_user(u)
    proj = Project(title="ToDelete", owner_id=u.id)
    ds.add_project(proj)
    admin = Admin(name="Root", email="r@e.com")
    ds.add_user(admin)
    ds.save()
    assert ds.find_project_by_title("ToDelete") is not None
    ok = admin.delete_project(proj.id, ds)
    assert ok
    assert ds.find_project_by_title("ToDelete") is None
