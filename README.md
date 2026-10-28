# File Integrity Monitor

A small command line tool written in Python that tells you when files in a folder
were changed. It takes a snapshot of the folder (called a baseline), and later
compares the folder with that snapshot. Anything that was added, modified, deleted
or had its permissions changed is reported.

This is a university project made by two people. See the [Team](#team) section.

## Why this exists

If someone (or some malware) quietly edits a config file or a script, you usually
do not notice. File integrity monitoring is a standard security control: you store a
fingerprint (hash) of every important file, and if the fingerprint changes later,
something touched the file. Tools like Tripwire and AIDE do the same thing on a bigger scale.

## Features

- SHA-256 hash for every file, read in chunks so big files are fine
- Stores size, modification time and permissions together with the hash
- Detects four kinds of changes: added, modified, deleted, permissions changed
- Ignore patterns (for example `*.log`, `__pycache__`)
- Reports as plain text, JSON or CSV
- Watch mode that re-checks the folder every N seconds
- Log file with everything the tool did
- No third party libraries, only the Python standard library

## Requirements

- Python 3.9 or newer

## Installation

```bash
git clone https://github.com/<your-username>/file-integrity-monitor.git
cd file-integrity-monitor
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -e .
```

For running the tests you also need the dev requirements:

```bash
pip install -r requirements-dev.txt
```

## Usage

The same commands work as `fim ...` or as `python -m fim ...`.

```bash
# 1. create a baseline for a folder
fim init ./my_folder --baseline baseline.json

# 2. later, check if anything changed
fim check ./my_folder --baseline baseline.json

# 3. get the result as JSON or CSV
fim check ./my_folder --baseline baseline.json --format json

# 4. skip some files
fim check ./my_folder --ignore "*.log" --ignore "__pycache__"

# 5. you changed things on purpose, accept the new state
fim update ./my_folder --baseline baseline.json

# 6. keep watching, check every 10 seconds
fim watch ./my_folder --interval 10
```

Example output:

```
[MODIFIED]    config/settings.ini
[ADDED]       scripts/new_tool.py
[DELETED]     notes/old.txt
[PERMISSIONS] run.sh   (0o644 -> 0o777)

4 change(s) found
```

Exit codes: `0` nothing changed, `1` changes found, `2` error (bad path, broken baseline and so on).
This makes it easy to use the tool inside scripts.

## How it works

```
 folder --> scanner --> list of FileRecord --> baseline.json     (init / update)
                                   |
                                   +--> comparer <-- baseline.json   (check)
                                            |
                                            v
                                     list of Change --> report (text / json / csv)
```

1. `scanner` walks the folder and asks `hasher` for the SHA-256 of each file.
2. `baseline` saves those records to a JSON file.
3. On `check`, the folder is scanned again and `comparer` compares both sides by path.
4. `report` prints the differences. `monitor` repeats steps 3 and 4 in a loop.

## Project structure

```
file-integrity-monitor/
├── fim/
│   ├── __init__.py
│   ├── __main__.py     # python -m fim
│   ├── cli.py          # argparse commands
│   ├── config.py       # defaults and ignore patterns
│   ├── hasher.py       # SHA-256 of a file
│   ├── scanner.py      # walks the folder, builds FileRecord objects
│   ├── baseline.py     # save and load the baseline json
│   ├── comparer.py     # baseline vs current state -> Change list
│   ├── monitor.py      # watch mode
│   ├── report.py       # text / json / csv output
│   ├── logger.py       # logging setup
│   └── models.py       # FileRecord, Change, ChangeType
├── tests/              # unit tests (pytest)
├── docs/               # defence notes
├── .github/            # CI and pull request template
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Running the tests

```bash
pytest
pytest --cov=fim --cov-report=term-missing    # with coverage
```

The tests create their own temporary folders (pytest `tmp_path`), so they never touch real files.

## Known limitations

- The baseline file itself is not protected. If an attacker can edit it, they can hide changes.
  Keep it somewhere safe or on read only media.
- Watch mode is polling, not instant. A change is noticed at the next interval.
- A very fast change and change back between two checks will not be seen.

## Team

| Person | Modules |
|--------|---------|
| Donald | hasher, scanner, baseline, comparer, cli |
| Colleague | config, logger, report, monitor |

Work is done on feature branches and merged into `main` with pull requests.
Rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).
