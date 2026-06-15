from main import build_parser, handle_command
from data.storage import DataStore


def test_cli_add_user_and_project(tmp_path):
    ds = DataStore(path=str(tmp_path / "data.json"))
    ds._create_empty()
    parser = build_parser()

    # add user
    args = parser.parse_args(["add-user", "--name", "CliUser", "--email", "cli@example.com"])
    ok, msg = handle_command(args, ds)
    assert ok and "CliUser" in msg

    # add project
    args = parser.parse_args(["add-project", "--user", "CliUser", "--title", "Proj1"])
    ok, msg = handle_command(args, ds)
    assert ok and "Proj1" in msg
