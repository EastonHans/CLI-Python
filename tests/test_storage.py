import json
import tempfile
import os
import sys

from data.storage import DataStore
from models.user import User
from models.project import Project
from models.task import Task


def test_save_load_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    ds = DataStore(path=str(path))
    # start empty
    ds._create_empty()
    u = User(name="Alice", email="a@example.com")
    ds.add_user(u)
    p = Project(title="Proj", owner_id=u.id)
    ds.add_project(p)
    t = Task(title="Do it")
    ds.add_task(p.id, t)
    ds.save()

    # Load into fresh store
    ds2 = DataStore(path=str(path))
    ds2.load()
    assert len(ds2.users) == 1
    assert len(ds2.projects) == 1
    assert ds2.projects[0].tasks[0].title == "Do it"


def test_validation_backups(tmp_path):
    path = tmp_path / "data.json"
    # write invalid content
    with open(path, "w", encoding="utf-8") as f:
        f.write("not-a-json")
    ds = DataStore(path=str(path))
    ds.load()
    # should create a data.json and not crash
    assert os.path.exists(str(path))
