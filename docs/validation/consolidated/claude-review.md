They'll need to make the fixes below. All of this comes from static reading only. I couldn't run the scripts in this environment, so the pass counts, hashes and bundle matches are unverified. I didn't evaluate the new business test, which is still in progress.

## Findings that need fixing

**1. Medium: the run records and `verify_samples.py` don't bind the files that hold the skills' business rules (②③)**
- **Evidence:** `verify_samples.py:112-116` builds the expected run configuration from `structure['configuration_sha256']`. In `verify_employee_workspace.py`, only AGENTS, CLAUDE and SKILL.md are marked as configuration. Supporting files under the skill are read by `tree()`, which doesn't mark them.
- **Effect:** none of the three `run-manifest.json` files contain `references/`. So `sales/.claude/skills/work-001/references/sales-rules.md` and `input-schema.md`, and `minutes/.../references/input-contract.md`, are not tied to the outputs. If someone edits the business rules and regenerates `bundle-manifest.json`, `verify_samples` still passes.
- **Conflict:** this contradicts `docs/validation.md:36`, which says each run manifest binds the definition used. `test_samples.py` has no case for it.
- **Fix:** bind every file under the skill directory to the run, and add a regression case.

**2. Medium: the sales hearing record isn't complete inside the employee folder (①)**
- `sample/sales/interview.md` says the full hearing text "is stored once in the records below". But the only Q&A record it links, `records/runtime-v001/source-evidence.md:3`, says it is an excerpt, and that the 4 original files are kept in "the approved D's source-history", which is outside the employee folder.
- Minutes and reconciliation do include the originals. This contradicts spec 2.4 (`employee-format-spec.md:82`), `interview-qa.md:181` and the KIT `AGENTS.md:51`, which require the original record inside the folder.
- **Fix:** bundle the sales part of the originals, or state the limitation plainly in `interview.md`.

**3. Medium: skill links through the symlinked directory probably break on GitHub (①④)**
- `sample/README.md:7-9` and each employee README's "Codex-discovered business skill" row link to `.agents/skills/<slug>/SKILL.md`, which passes through the directory symlink.
- GitHub's file view generally doesn't follow directory symlinks, so these links probably fail on the published repo. I haven't confirmed this on GitHub.
- `verify_samples.py` resolves links on the local filesystem, so it reports them as passing.
- **Fix:** point these links at the canonical `.claude/skills/<slug>/SKILL.md` and describe `.agents` in text as the link.

**4. Low–Medium: two leftover scripts for the old layout (④)**
- `scripts/verify_substantial_samples.py` and `scripts/verify_reconciliation_sample.py` default to `sample/substantial/...`.
- They read files that no longer exist (`output/report.json`, `expected.json`, `provenance.json`, `validation/independent/*`) and fail if run. Nothing references them.
- **Fix:** delete them (they stay in Git history) or move them under a history location with a note.

**5. Low: the saved independent check isn't hash-bound (③)**
- The run manifest's `independent_verification` entry holds a path and a check count, but no SHA.
- `verify_samples.py:127-131` only reads `all_passed` and identity fields, and never compares the 6285 / 1224 / 5004 counts with `len(checks)`.
- **Fix:** add a SHA and compare the count.

**6. Low: who did the browser check is ambiguous (⑤)**
- `docs/validation.md:44` says the initial display of each report was checked in the user's Orca browser on their Mac, without saying who did it. It can be read as a human visual check.
- **Fix:** name who did it (AI operation or a person), and state that it isn't acceptance.

**7. Low: two docs give different test commands**
- `docs/compatibility.md:61-72` lists only `test_employee_workspace` and `test_prepare_sample_workspace`.
- `validation.md:25-30` also includes `verify_samples` and `test_samples`.
- **Fix:** list the same commands in both.

## Unverified
- Results of running each script and test, including the 126 / 24 / 13 pass counts and the actual bundle-manifest match.
- Report contents (I didn't read the large report.json/html), Codex discovery, the business re-run in progress, and human acceptance.