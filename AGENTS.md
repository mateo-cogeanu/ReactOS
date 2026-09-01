# Repository Working Agreement

These instructions apply to the entire repository. They exist to keep this
experimental ReactOS fork understandable, reproducible, and properly
attributed.

## Before changing anything

1. Read this file, `README.md`, and `CHANGELOG.md`.
2. Inspect `git status`, the current branch, configured remotes, and relevant
   recent history before editing.
3. Treat every pre-existing modification and untracked file as user work.
   Preserve it and do not stage, overwrite, discard, or reformat it unless the
   task explicitly includes it.
4. Keep the fork focused on native AMD64 ReactOS. Changes to i386/i686 are only
   in scope when they are required for the subordinate SysWOW64 payload or the
   user explicitly requests them.

## Keep the changelog current

Every material source, build-system, configuration, test, packaging, or
documentation change must update the root `CHANGELOG.md` in the same work
session. Do not postpone the entry until a later task.

Each entry must state, as applicable:

- the exact local date and time, including timezone;
- the affected subsystem and files;
- what changed and why;
- its honest status: WIP, compiled, booted, tested, verified, or unverified;
- the build/test commands and useful evidence, including artifact checksums;
- known limitations, regressions, and the next unresolved step; and
- the relevant commit hash once it is known.

Never describe an experiment as working merely because it compiles. Keep
unverified and failed attempts visible and clearly labeled. A commit hash may
be added in one follow-up documentation commit; that follow-up does not require
another self-referential changelog entry.

## Commit completed milestones

- Commit each coherent, completed milestone promptly. Do not leave validated
  work available only as uncommitted files.
- Update `CHANGELOG.md` in the same commit as the material change whenever
  possible.
- Do not include unrelated files or known-broken work in a completed milestone.
  If a checkpoint commit is genuinely necessary, label it `WIP` in both the
  commit subject and changelog and document exactly what remains unverified.
- Use concise, subsystem-oriented commit subjects. Preserve authorship and
  trailers when incorporating work from others.
- Before every commit, inspect the staged diff, run `git diff --check`, and run
  the relevant build or tests in proportion to the change. Record the result
  in `CHANGELOG.md`.
- Do not commit generated build trees, VM disks, ISOs, logs, credentials,
  private keys, passwords, or other secrets unless the user explicitly asks
  for an appropriate artifact and repository policy permits it.

## Push and verify

After verification, push completed commits to the configured GitHub fork
(`github-user`, branch `master`) unless the user explicitly asks not to push.
Never force-push or rewrite published history without explicit authorization.
After pushing, verify that the remote tip matches the intended local commit and
report the commit hash to the user.

## Attribution and licensing

This remains a fork of the ReactOS Project. Preserve the complete upstream Git
history, copyright notices, licenses, `CREDITS`, author identities, and commit
metadata. Never present upstream or third-party work as original fork work.
Clearly distinguish local experimental changes from upstream ReactOS and give
prominent credit to the original ReactOS contributors and any named feature
authors in documentation and release notes.

## Definition of done

A task is complete only when the requested change is implemented, its relevant
validation has been performed (or the lack of validation is explicit), the
changelog is accurate, the intended files are committed, and the remote push is
verified. Any intentionally retained local WIP must remain unstaged and be
called out in the handoff.
