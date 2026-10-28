# Tasks for the teammate

Hi! Here is your part of the project. Each task is its own branch, its own pull request,
and has its own tests. Please do them in this order, and push after every task, not
all at the end. The commits and PRs are part of our Git grade.

Everyone must be able to see who did what, so please commit with your own GitHub account.

## One time setup

```bash
git clone https://github.com/<donald-username>/file-integrity-monitor.git
cd file-integrity-monitor
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
pip install -r requirements-dev.txt
pytest                             # should show 3 passed
```

Check that you have write access (Donald adds you in Settings > Collaborators).

## The shared contract

Look at `fim/models.py` first. `FileRecord` is one file, `Change` is one difference.
Your modules only work with these, so you do not need Donald's code to start.
In your tests just create `Change` objects by hand.

## Task 1: `feature/config` (small, good to learn the flow)

File: `fim/config.py`, tests: `tests/test_config.py`

- constant `DEFAULT_IGNORE` with a list of patterns: `__pycache__`, `*.pyc`, `.git`, `*.log`
- function `load_config(path)` that reads an optional `fim.json` file and returns a dict
  merged with the defaults (missing file means just defaults)
- function `is_ignored(rel_path, patterns)` using `fnmatch`, checks every part of the path

Tests (at least 4): defaults used when no file, file overrides defaults, ignored file,
not ignored file, pattern matching a folder name inside a deeper path.

## Task 2: `feature/logger`

File: `fim/logger.py`, tests: `tests/test_logger.py`

- function `setup_logger(log_file="fim.log", verbose=False)` that returns a logger
  writing to the console and to the file
- verbose=True means DEBUG level, otherwise INFO
- calling it twice must not duplicate the handlers (this is a classic bug, test it)

## Task 3: `feature/report`

File: `fim/report.py`, tests: `tests/test_report.py`

- `format_text(changes)` produces the output shown in the README (one line per change,
  summary line at the end, a friendly message if there are no changes)
- `format_json(changes)` returns a JSON string with a list of objects
  (`path`, `type`, and old/new hash when available)
- `format_csv(changes)` returns CSV text with a header row
- `render(changes, fmt)` picks the right one, raises `ValueError` for unknown format
- sort the changes by path so the output is always the same order

Tests (at least 6): each format with an empty list, each format with one of every
change type, unknown format raises, sorting works.

## Task 4: `feature/monitor`

File: `fim/monitor.py`, tests: `tests/test_monitor.py`

- function `watch(check_once, interval, on_change, max_rounds=None)`
  - `check_once` is a function that returns a list of `Change`
  - call it every `interval` seconds with `time.sleep`
  - call `on_change(changes)` only when the list is not empty
  - stop after `max_rounds` (None means run until Ctrl+C), and handle `KeyboardInterrupt`
    cleanly without a traceback
- it takes functions as arguments on purpose, so you can test it with fake functions
  and `max_rounds=3` without needing real files or waiting

## Task 5: `docs` and review

- read Donald's pull requests and leave real comments (even a small suggestion counts)
- add your name to the license file and to the Team table in the README
- prepare your part of the defence, see `docs/DEFENCE.md`, you present report, monitor,
  logger and config

## Git checklist for every task

```bash
git checkout main
git pull
git checkout -b feature/<name>
# code + tests, commit in small steps (3 to 6 commits per branch is nice)
pytest
git push -u origin feature/<name>
# open a Pull Request on GitHub, fill in the template, ask Donald to review
```

Do not commit `fim.log`, `baseline.json` or `__pycache__`. They are in `.gitignore`.
If you get a merge conflict, do not panic, write to Donald and we fix it together.
