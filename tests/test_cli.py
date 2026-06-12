import subprocess
import sys
import os
import tempfile


def run(cmd_args, cwd=None):
    proc = subprocess.run([sys.executable] + cmd_args, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def test_cli_add_user_and_project(tmp_path):
    cwd = os.getcwd()
    # use a temp copy of the project to avoid clobbering data
    proj = tmp_path / "proj"
    subprocess.run(["git", "clone", cwd, str(proj)])
    # add user
    code, out, err = run(["main.py", "add-user", "--name", "CliUser", "--email", "cli@example.com"], cwd=str(proj))
    assert code == 0
    # add project
    code, out, err = run(["main.py", "add-project", "--user", "CliUser", "--title", "Proj1"], cwd=str(proj))
    assert code == 0
