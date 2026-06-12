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
python -m unittest discover -s tests -p "test_*.py"
```
