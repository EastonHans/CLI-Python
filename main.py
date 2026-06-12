#!/usr/bin/env python3
import argparse
from data.storage import DataStore
from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import pretty_print, parse_date


def build_parser():
    parser = argparse.ArgumentParser(description="CLI Project Management Tool")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list-users", help="List all users")

    p = sub.add_parser("add-user", help="Add a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=False)

    p2 = sub.add_parser("add-project", help="Add project for a user")
    p2.add_argument("--user", required=True)
    p2.add_argument("--title", required=True)
    p2.add_argument("--description", required=False, default="")
    p2.add_argument("--due", required=False, help="Due date (YYYY-MM-DD)")

    p3 = sub.add_parser("list-projects", help="List projects (optionally for a user)")
    p3.add_argument("--user", required=False)

    t1 = sub.add_parser("add-task", help="Add task to a project")
    t1.add_argument("--project", required=True)
    t1.add_argument("--title", required=True)
    t1.add_argument("--assigned", required=False, help="Assigned user name")

    t2 = sub.add_parser("list-tasks", help="List tasks for a project")
    t2.add_argument("--project", required=True)

    c = sub.add_parser("complete-task", help="Mark a task complete")
    c.add_argument("--project", required=True)
    c.add_argument("--task-id", required=True)

    s = sub.add_parser("search-projects", help="Search projects by user")
    s.add_argument("--user", required=True)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    ds = DataStore()
    ds.load()

    if args.command == "list-users":
        pretty_print(ds.users)

    elif args.command == "add-user":
        u = User(name=args.name, email=args.email)
        ds.add_user(u)
        ds.save()
        print(f"Added user: {u}")

    elif args.command == "add-project":
        user = ds.find_user_by_name(args.user)
        if not user:
            print("User not found")
            return
        due = parse_date(args.due) if args.due else None
        p = Project(title=args.title, description=args.description, due_date=due, owner_id=user.id)
        ds.add_project(p)
        ds.save()
        print(f"Added project: {p}")

    elif args.command == "list-projects":
        if args.user:
            user = ds.find_user_by_name(args.user)
            if not user:
                print("User not found")
                return
            projects = ds.get_projects_for_user(user.id)
            pretty_print(projects)
        else:
            pretty_print(ds.projects)

    elif args.command == "add-task":
        project = ds.find_project_by_title(args.project)
        if not project:
            print("Project not found")
            return
        assigned = None
        if args.assigned:
            assigned_user = ds.find_user_by_name(args.assigned)
            assigned = assigned_user.id if assigned_user else None
        t = Task(title=args.title, assigned_to=assigned)
        ds.add_task(project.id, t)
        ds.save()
        print(f"Added task: {t}")

    elif args.command == "list-tasks":
        project = ds.find_project_by_title(args.project)
        if not project:
            print("Project not found")
            return
        pretty_print(project.tasks)

    elif args.command == "complete-task":
        project = ds.find_project_by_title(args.project)
        if not project:
            print("Project not found")
            return
        updated = ds.complete_task(project.id, args.task_id)
        if updated:
            ds.save()
            print("Task marked complete")
        else:
            print("Task not found")

    elif args.command == "search-projects":
        user = ds.find_user_by_name(args.user)
        if not user:
            print("User not found")
            return
        projects = ds.get_projects_for_user(user.id)
        pretty_print(projects)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
