# Defence notes (20 points)

Two parts: 1) PowerPoint with problems, bugs and how it works, 2) show the code.
Each person presents his own part, about 5 minutes each.

## 1. PowerPoint outline (8 to 10 slides)

1. **Title.** Project name, names of both authors
2. **The problem.** What is file integrity monitoring and why it matters (config tampering, malware, audit)
3. **Our solution.** One sentence plus the four types of change we detect
4. **How it works.** The diagram from the README (scan, baseline, compare, report)
5. **Architecture.** The module list and who wrote which one
6. **Demo.** Live: `init`, change a file, `check`. Keep a screenshot as backup in case the live demo fails
7. **Problems we had and bugs we fixed.** See the list below, use the real ones
8. **Testing.** Number of tests, coverage number, one example of a good test
9. **Git workflow.** Screenshot of `git log --graph`, branches, pull requests, reviews
10. **Limitations and future work.** Unprotected baseline, polling instead of events, ideas

## Problems and bugs (replace this list with the ones you really hit)

These are the usual problems in this kind of project, so you will probably meet some of them.
Write down every real bug while you work, with the commit that fixed it. It makes slide 7 easy.

- a file disappears between listing and hashing, the tool crashed with FileNotFoundError
- permission denied on some files, one error stopped the whole scan
- symlinks pointing in a loop or outside the folder
- big files loaded fully into memory, fixed with chunked reading
- on Windows paths use backslashes, so the same baseline did not match, fixed by storing paths with `/`
- the first version compared only mtime, a file with the same mtime but other content was missed, so we compare hashes
- the log handlers were added twice and every line was printed twice

## 2. Show the code (what to open and what to say)

Prepare these files in the editor before you start, in this order:

| File | What to say |
|------|-------------|
| `models.py` | The two small data classes everything else uses |
| `hasher.py` | Why chunks, why SHA-256 |
| `scanner.py` | How the walk works, ignore patterns, error handling |
| `comparer.py` | The core idea: compare two dictionaries by path, 4 cases |
| `cli.py` | How the commands are wired together, exit codes |
| `report.py`, `monitor.py` | Output formats, functions passed as arguments so it is testable |
| `tests/` | Run `pytest` live, show the coverage line |

## Questions the teacher may ask

- Why SHA-256 and not MD5? (MD5 has known collisions, SHA-256 does not)
- What if the attacker edits the baseline too? (known limitation, store it safely, could sign it)
- Why polling in watch mode? (simple, works everywhere, no extra libraries, events could be future work)
- How do you test code that depends on the file system? (pytest `tmp_path`, fake functions)
- Who wrote what? (answer from the Team table, and show the commits)
