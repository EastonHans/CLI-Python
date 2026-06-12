from main import build_parser, handle_command
from data.storage import DataStore
from models.user import User


def test_handle_add_user_and_project(tmp_path):
    p = tmp_path / "data.json"
    ds = DataStore(path=str(p))
    ds._create_empty()
    parser = build_parser()
    # add user
    args = parser.parse_args(["add-user", "--name", "TM", "--email", "tm@example.com"])
    ok, msg = handle_command(args, ds)
    assert ok and "Added user" in msg
    # add project
    args = parser.parse_args(["add-project", "--user", "TM", "--title", "ProjX"])
    ok, msg = handle_command(args, ds)
    assert ok and "Added project" in msg
    # add task
    args = parser.parse_args(["add-task", "--project", "ProjX", "--title", "Task1"])
    ok, msg = handle_command(args, ds)
    assert ok and "Added task" in msg
    # list projects for user
    args = parser.parse_args(["list-projects", "--user", "TM"])
    ok, msg = handle_command(args, ds)
    assert ok


def test_complete_and_assign(tmp_path):
    p = tmp_path / "data.json"
    ds = DataStore(path=str(p))
    ds._create_empty()
    # prepare data
    u = User(name="A", email="a@e.com")
    ds.add_user(u)
    from models.project import Project
    from models.task import Task
    proj = Project(title="P1", owner_id=u.id)
    ds.add_project(proj)
    t = Task(title="T1")
    ds.add_task(proj.id, t)
    ds.save()
    parser = build_parser()
    # assign contributor
    args = parser.parse_args(["assign-contributor", "--project", "P1", "--task-id", str(t.id), "--assigned", "A"])
    ok, msg = handle_command(args, ds)
    assert ok and msg == "Contributor assigned"
    # complete task
    args = parser.parse_args(["complete-task", "--project", "P1", "--task-id", str(t.id)])
    ok, msg = handle_command(args, ds)
    assert ok and msg == "Task marked complete"
