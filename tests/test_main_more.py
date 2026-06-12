from main import build_parser, handle_command
from data.storage import DataStore
from models.user import User
from models.project import Project


def test_list_users_and_projects(tmp_path):
    p = tmp_path / "data.json"
    ds = DataStore(path=str(p))
    ds._create_empty()
    u = User(name="ListUser", email="l@e.com")
    ds.add_user(u)
    proj = Project(title="LP", owner_id=u.id)
    ds.add_project(proj)
    parser = build_parser()
    # list-users
    args = parser.parse_args(["list-users"])
    ok, msg = handle_command(args, ds)
    assert ok
    # list-projects without user
    args = parser.parse_args(["list-projects"])
    ok, msg = handle_command(args, ds)
    assert ok
    # list-tasks project missing
    args = parser.parse_args(["list-tasks", "--project", "Nope"])
    ok, msg = handle_command(args, ds)
    assert not ok and msg == "Project not found"

