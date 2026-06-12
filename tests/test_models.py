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

    def test_user_email_validation(self):
        with self.assertRaises(ValueError):
            User(name="Bad", email="no-at-symbol")

    def test_task_contributors_and_complete(self):
        t = Task(title="C")
        t.add_contributor(5)
        self.assertIn(5, t.assigned_to)
        t.mark_done()
        self.assertEqual(t.status, "done")


if __name__ == "__main__":
    unittest.main()
