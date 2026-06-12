# CLI Project Management Tool

Simple command-line project management tool with users, projects, and tasks.

Setup

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Usage

Run the CLI via:

```bash
python main.py add-user --name "Alex" --email alex@example.com
python main.py add-project --user "Alex" --title "CLI Tool" --due 2026-12-31
python main.py add-task --project "CLI Tool" --title "Implement add-task"
python main.py list-projects --user "Alex"
```

Persistence

Data is saved in `data/data.json`.

Tests

Run unit tests with:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=. tests/
```

## All Commands

| Command | Description |
|---|---|
| `add-user` | Create a new user |
| `add-project` | Create a project for a user |
| `add-task` | Add a task to a project |
| `list-users` | List all users |
| `list-projects` | List all or filtered projects |
| `list-tasks` | List tasks for a project |
| `complete-task` | Mark a task as done |
| `assign-contributor` | Assign a user to a task |
| `search-projects` | Search projects by user |
