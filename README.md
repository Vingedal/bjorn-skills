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
install the bundle:

```text
/plugin marketplace add Vingedal/bjorn-skills
/plugin install bjorn-skills@bjorn-skills
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

## Repository layout

```
bjorn-skills/
├─ skills/
│  └─ tsqlt-testing/
│     ├─ SKILL.md            # the skill (entry point)
│     └─ reference/          # progressive-disclosure docs, loaded on demand
└─ .claude-plugin/
   └─ marketplace.json       # exposes skills/ as a Claude Code plugin
```

Skills live at the top level so any agent can copy a `skills/<name>/` folder directly and skills.sh
finds them in a standard location. `marketplace.json` bundles everything under `skills/` into one
installable Claude Code plugin.

## Add a skill

Create `skills/<name>/SKILL.md` — YAML frontmatter with `name` + `description`, then Markdown
instructions; add a `reference/` folder for details loaded on demand. That's it: it's picked up by
skills.sh and the copy-to-any-tool flow, and auto-included in the Claude Code bundle (no
`marketplace.json` change needed). Run the validator below, then commit.

## Validate

```bash
python3 .github/scripts/validate_skills.py    # frontmatter + JSON checks (also runs in CI)
claude plugin validate .                       # validate the Claude Code marketplace manifest
```

## License

[MIT](LICENSE) © 2026 Björn Vingedal. Free to use, modify, and redistribute.

> **Note:** tSQLt is a development/test tool. Never install it on a production database.
