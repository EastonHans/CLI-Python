from utils.helpers import parse_date, pretty_print
from models.user import User
from rich.console import Console
import io


def test_parse_date():
    assert parse_date("2026-01-02") == "2026-01-02"
    assert parse_date("Jan 2 2026") == "2026-01-02"
    assert parse_date("not a date") is None


def test_pretty_print_empty(capsys):
    pretty_print([])
    captured = capsys.readouterr()
    assert "No items found" in captured.out


def test_pretty_print_models(capsys):
    u = User(name="PTest", email="p@example.com")
    pretty_print([u])
    captured = capsys.readouterr()
    assert "PTest" in captured.out
