---
description: Group changes into semantic commits and push
---

Group all current changes into meaningful semantic commits and push the current branch.

Optional context for commit messages: `$ARGUMENTS`

Rules:

- First inspect the full repository state:
  - `git status --short`
  - `git diff --stat`
  - `git log --oneline -10`
  - `git diff -- "-*lock.json" "-*.svg"` (Avoid printing massive auto-generated files to save context).
- Identify related file groups by intent: feature, fix, refactor, tests, docs, chore, release, or config.
- Create multiple commits when there are independent changes. Do not mix unrelated changes in the same commit.
- If `$ARGUMENTS` is not empty, use it as context to adjust commit messages, but do not force that text if it does not accurately describe the changes.
- Use clear, semantic, concise commit messages that follow the repo's recent style (e.g., Conventional Commits).
- CRITICAL SECURITY CHECK: Before committing, check for sensitive or suspicious files (`.env`, tokens, credentials, keys, secrets, `sqlite` DBs). If any appear, STOP AND ASK.
- Include new, modified, and deleted files that belong to each group.
- Do not revert existing changes.
- Do not use `--no-verify`, `--amend`, or force push.
- If a commit fails due to a pre-commit hook (linter/formatter), read the error, attempt to fix the code automatically if trivial, or stop and ask for guidance.
- If `git push` fails because there is no upstream branch, automatically use `git push -u origin HEAD`.

Flow:

1. Show the proposed commit plan with the files included in each commit.
2. If the grouping is clear, continue. If there is real ambiguity, ask before committing.
3. For each group:
  - Add only the files for that group using `git add <files>`.
  - Create the commit with a semantic message.
4. Once all commits have been created, run `git push`.
5. When finished, summarize the commits created and the branch that was pushed.