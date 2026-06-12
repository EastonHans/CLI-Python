import unittest
from models.user import User
from models.project import Project
from models.task import Task


class ModelTests(unittest.TestCase):
    def test_user_project_task_relations(self):
        u = User(name="TestUser", email="t@example.com")
        p = Project(title="P1", owner_id=u.id)
        t = Task(title="T1")
        p.add_task(t)
        self.assertEqual(p.owner_id, u.id)
        self.assertEqual(len(p.tasks), 1)
        d = p.to_dict()
        p2 = Project.from_dict(d)
        self.assertEqual(p2.title, p.title)


if __name__ == "__main__":
    unittest.main()
