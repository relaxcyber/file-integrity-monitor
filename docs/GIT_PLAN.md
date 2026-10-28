# Git plan

The idea is to show real work over several days, not one big upload.
Suggested order for the commits, the dates are just a guide.

## Day 1: project setup (Donald, directly on main)

1. `Initial commit with project skeleton and gitignore`
2. `Add shared data models`
3. `Add README draft and license`
4. `Add CI workflow and PR template`

Then add the teammate as a collaborator (Settings > Collaborators).

## Day 2 to 3: first modules (in parallel)

| Donald | Colleague |
|--------|-----------|
| `feature/hasher` | `feature/config` |
| `feature/scanner` | `feature/logger` |

Each branch: 3 to 6 small commits, then a Pull Request, reviewed by the other person.

## Day 4 to 5

| Donald | Colleague |
|--------|-----------|
| `feature/baseline` | `feature/report` |
| `feature/comparer` | `feature/monitor` |

## Day 6

- Donald: `feature/cli` (connects everything)
- Both: `fix/...` branches for bugs found while testing by hand (these are good material for the defence)
- Colleague: `docs/readme-team` with his name in README and LICENSE

## Day 7

- final README check, screenshots or sample output
- tag a release: `git tag v1.0.0 && git push --tags`

## Example commit sequence for one branch (hasher)

```
Add function that hashes a file with sha256
Read the file in 64KB chunks
Raise a clear error when the file cannot be read
Add unit tests for hasher
Add test for empty file and big file
```

## Useful commands

```bash
git log --oneline --graph --all     # nice picture of branches, show it at the defence
git status
git diff
git branch -a
```
