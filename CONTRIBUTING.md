# How we work in this repo

Two people, one repo. To keep `main` working and the history readable we follow a few simple rules.

## Branches

- `main` always works and its tests pass. Nobody commits straight to it.
- One branch per feature, named `feature/<name>`, for example `feature/report`.
- Tests for a module go into the same branch as the module (or `test/<name>` if separate).
- Small fixes: `fix/<name>`. Docs only: `docs/<name>`.

## Workflow

```bash
git checkout main
git pull
git checkout -b feature/report

# work, then commit often in small steps
git add fim/report.py
git commit -m "Add text report formatter"

git push -u origin feature/report
```

Then open a Pull Request on GitHub into `main`. The other person looks at it,
leaves at least one comment or review, and then merges it.

## Commit messages

Short, in the imperative, one change per commit.

Good:
- `Add chunked sha256 hashing`
- `Fix crash when a file disappears during scan`
- `Add tests for comparer`

Bad:
- `update`
- `final version`
- `fix stuff and add things`

## Before you open a PR

- `pytest` passes on your machine
- every new function has a short docstring or comment explaining why it exists
- no leftover debug prints, no `baseline.json` or log files committed

## Pull request review

The reviewer checks that the code is readable, the tests make sense and the branch
does what the PR text says. Leave comments directly on the lines. Yes, even small ones.
It counts as visible teamwork.
