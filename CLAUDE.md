# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`bjorn-skills` is a collection of cross-tool **Agent Skills** (the `SKILL.md` format). The same
`skills/<name>/` folder is consumed three ways from one source, with no conversion:

- copied directly into any agent's skills directory (Codex CLI, Gemini CLI, Cursor, Copilot, or Claude
  Code manual),
- installed via skills.sh (`npx skills add Vingedal/bjorn-skills --skill <name>`), and
- installed as a standalone Claude Code plugin (`<name>@bjorn-skills`).

There is no application to build or run. The only executable code is the CI validator; everything else is
skill content (Markdown) and plugin manifests (JSON). Work here means authoring/maintaining skill docs and
keeping the manifests in sync.

## Commands

```bash
# The repo's "test": validates every SKILL.md frontmatter + all JSON manifests. Runs in CI on push/PR.
python3 .github/scripts/validate_skills.py     # `python` also works on the Windows dev host

# Validate the Claude Code marketplace + plugin manifests (needs the claude CLI; not run in CI)
claude plugin validate .
```

There are no build/lint/unit-test steps — `validate_skills.py` is the only check.

## Architecture: how one skill is wired in three places

A skill must stay consistent across three files:

1. **`skills/<name>/SKILL.md`** — the skill itself: YAML frontmatter (`name`, `description`) + Markdown
   instructions. The `description` is deliberately trigger-rich ("Use when the user asks to …") because
   that text is what causes the skill to be selected. Keep SKILL.md lean and push specifics into
   **`skills/<name>/reference/*.md`**, which SKILL.md links and the agent loads on demand (progressive
   disclosure).
2. **`skills/<name>/.claude-plugin/plugin.json`** — makes the skill an installable Claude Code plugin.
   The skill folder *is* the plugin root: SKILL.md sits at the root (not under a nested `skills/` subdir),
   which is the supported single-skill plugin layout.
3. **`.claude-plugin/marketplace.json`** — one entry per skill in `plugins[]`, each with
   `"source": "./skills/<name>"`. Every skill is its own plugin, so users install only what they want.

**Invariant:** the plugin `name` in `marketplace.json` must equal the `name` in that skill's `plugin.json`
(and conventionally the folder name). `claude plugin validate` enforces this; the Python validator does not.

Skills live at the **top level** (`skills/`, not nested inside a plugin) on purpose: any tool can copy
`skills/<name>/` directly, and skills.sh discovers them in a standard location. The `.claude-plugin/`
folders are ignored by every tool except Claude Code.

### Adding a skill
1. Create `skills/<name>/SKILL.md` (+ optional `reference/`).
2. Add `skills/<name>/.claude-plugin/plugin.json` (`name`, `description`, `version`).
3. Add a `plugins[]` entry to `.claude-plugin/marketplace.json` with `"source": "./skills/<name>"`.
4. **Update `README.md`**: add a row to the Skills table and the skill's per-skill install commands —
   the skills.sh `npx skills add Vingedal/bjorn-skills --skill <name>` line and the Claude Code
   `/plugin install <name>@bjorn-skills` line.
5. Run the validator, then commit.

(The cross-tool copy and skills.sh flows need only step 1 — the SKILL.md.)

**`README.md` is the canonical, per-skill install reference.** There is intentionally no "install all
skills" command — the skills are unrelated, so nobody installs the whole set. Enumerate each skill's
install commands explicitly and keep that list in sync as skills are added (step 4 above).

## Gotchas

- **`validate_skills.py` uses `pathlib.rglob`, not `glob.glob`.** `glob.glob("**/…")` silently skips
  dot-directories, so it never sees the manifests under `.claude-plugin/` — making the JSON check a no-op
  while still printing success. Do not "simplify" it back to `glob`.
- **Verify tSQLt API claims against upstream, never from memory.** When editing `skills/tsqlt-testing/`,
  the source of truth is the tSQLt repo (`tSQLt-org/tSQLt`, files under `Source/`, e.g.
  `Source/tSQLt.FakeTable.ssp.sql`). The reference docs publish exact procedure signatures — an invented
  parameter produces broken SQL for users.
- JSON manifests are UTF-8 without BOM; non-ASCII (e.g. `Björn`) is fine.