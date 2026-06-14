# bjorn-skills

Cross-tool **AI agent skills** ([SKILL.md format](https://agentskills.io)) by Björn Vingedal.

An [Agent Skill](https://agentskills.io) is a folder with a `SKILL.md` file (YAML frontmatter +
Markdown instructions, plus optional reference docs). The same skill folder is read — natively or
by copying it into a skills directory — by **Claude Code, OpenAI Codex CLI, Google Gemini CLI,
Cursor, and GitHub Copilot**. No conversion needed.

## Skills

| Skill | What it does |
|---|---|
| [`tsqlt-testing`](skills/tsqlt-testing/SKILL.md) | Author, run, and debug [tSQLt](https://tsqlt.org) unit tests for SQL Server — structure tests as Assemble/Act/Assert, fake or spy out dependencies (tables, functions, procedures), assert on query results, expect exceptions, and run suites. |

## Install

### skills.sh (any supported agent)

[skills.sh](https://skills.sh) is a package manager for Agent Skills. From your project directory:

```bash
npx skills add Vingedal/bjorn-skills
```

### Claude Code

Add this repo as a [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces), then
install the skill you want — **each skill is its own plugin**, so you get only what you ask for:

```text
/plugin marketplace add Vingedal/bjorn-skills
/plugin install tsqlt-testing@bjorn-skills
```

Update later with `/plugin marketplace update bjorn-skills`.

### Other agents (Codex CLI, Gemini CLI, Cursor, Copilot)

These tools read Agent Skills from a `skills/` directory. Copy the `skills/tsqlt-testing/` folder
into your tool's skills directory (paths vary by tool and version — check each tool's current docs):

| Tool | Copy `skills/tsqlt-testing/` to | Docs |
|---|---|---|
| OpenAI Codex CLI | `~/.codex/skills/tsqlt-testing/` | [Codex skills](https://developers.openai.com/codex/skills) |
| Google Gemini CLI | `~/.gemini/skills/tsqlt-testing/` | [Gemini CLI skills](https://geminicli.com/docs/cli/skills/) |
| Cursor | `~/.cursor/skills/tsqlt-testing/` | [Cursor skills](https://cursor.com/docs) |
| GitHub Copilot | per the VS Code agent-skills location | [Copilot customization](https://docs.github.com/copilot) |
| Claude Code (manual) | `~/.claude/skills/tsqlt-testing/` | [Claude Code skills](https://code.claude.com/docs) |

For example, with Git:

```bash
git clone https://github.com/Vingedal/bjorn-skills
cp -r bjorn-skills/skills/tsqlt-testing ~/.codex/skills/
```

(The `.claude-plugin/` folder inside a skill is only used by Claude Code's marketplace; other tools ignore it.)

## Repository layout

```
bjorn-skills/
├─ skills/
│  └─ tsqlt-testing/
│     ├─ SKILL.md                  # the skill (entry point)
│     ├─ reference/                # progressive-disclosure docs, loaded on demand
│     └─ .claude-plugin/
│        └─ plugin.json            # makes this skill an installable Claude Code plugin
└─ .claude-plugin/
   └─ marketplace.json             # lists each skill as its own plugin
```

Skills live at the top level so any agent can copy a `skills/<name>/` folder directly and skills.sh
finds them in a standard location. Each skill is exposed as its **own** Claude Code plugin
(`<name>@bjorn-skills`), so you install only the skills you want.

## Add a skill

1. Create `skills/<name>/SKILL.md` — YAML frontmatter with `name` + `description`, then Markdown
   instructions; add a `reference/` folder for details loaded on demand.
2. Add `skills/<name>/.claude-plugin/plugin.json` (`name`, `description`, `version`) so Claude Code
   can install it as a standalone plugin.
3. Add a plugin entry to `.claude-plugin/marketplace.json` with `"source": "./skills/<name>"`.
4. Run the validator below, then commit.

(skills.sh and the copy-to-any-tool flow only need step 1 — the `SKILL.md`.)

## Validate

```bash
python3 .github/scripts/validate_skills.py    # frontmatter + JSON checks (also runs in CI)
claude plugin validate .                       # validate the Claude Code marketplace manifest
```

## License

[MIT](LICENSE) © 2026 Björn Vingedal. Free to use, modify, and redistribute.

> **Note:** tSQLt is a development/test tool. Never install it on a production database.
