# bjorn-skills

Cross-tool **AI agent skills** ([SKILL.md format](https://agentskills.io)) by Björn Vingedal.

An [Agent Skill](https://agentskills.io) is a folder with a `SKILL.md` file (YAML frontmatter +
Markdown instructions, plus optional reference docs). The same skill folder is read — natively or
by copying it into a skills directory — by **Claude Code, OpenAI Codex CLI, Google Gemini CLI,
Cursor, and GitHub Copilot**. No conversion needed.

## Skills

| Skill | What it does |
|---|---|
| [`tsqlt-testing`](plugins/tsqlt-testing/skills/tsqlt-testing/SKILL.md) | Author, run, and debug [tSQLt](https://tsqlt.org) unit tests for SQL Server — structure tests as Assemble/Act/Assert, fake or spy out dependencies (tables, functions, procedures), assert on query results, expect exceptions, and run suites. |

## Install

### Claude Code

Add this repo as a [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces), then
install the skill:

```text
/plugin marketplace add Vingedal/bjorn-skills
/plugin install tsqlt-testing@bjorn-skills
```

To update later: `/plugin marketplace update bjorn-skills`.

### Other agents (Codex CLI, Gemini CLI, Cursor, Copilot)

These tools read Agent Skills from a `skills/` directory. Copy the skill folder
`plugins/tsqlt-testing/skills/tsqlt-testing/` into your tool's skills directory (paths vary by
tool and version — check each tool's current docs):

| Tool | Copy the skill folder to | Docs |
|---|---|---|
| OpenAI Codex CLI | `~/.codex/skills/tsqlt-testing/` | [Codex skills](https://developers.openai.com/codex/skills) |
| Google Gemini CLI | `~/.gemini/skills/tsqlt-testing/` | [Gemini CLI skills](https://geminicli.com/docs/cli/skills/) |
| Cursor | `~/.cursor/skills/tsqlt-testing/` | [Cursor skills](https://cursor.com/docs) |
| GitHub Copilot | per the VS Code agent-skills location | [Copilot customization](https://docs.github.com/copilot) |
| Claude Code (manual) | `~/.claude/skills/tsqlt-testing/` | [Claude Code skills](https://code.claude.com/docs) |

For example, with Git:

```bash
git clone https://github.com/Vingedal/bjorn-skills
cp -r bjorn-skills/plugins/tsqlt-testing/skills/tsqlt-testing ~/.codex/skills/
```

The folder you copy is always `plugins/tsqlt-testing/skills/tsqlt-testing/`, regardless of tool.

## Repository layout

```
bjorn-skills/
├─ .claude-plugin/
│  └─ marketplace.json                 # lists the plugins in this marketplace
└─ plugins/
   └─ tsqlt-testing/
      ├─ .claude-plugin/plugin.json     # plugin manifest
      └─ skills/
         └─ tsqlt-testing/
            ├─ SKILL.md                 # the skill (entry point)
            └─ reference/               # progressive-disclosure docs, loaded on demand
```

Each skill is packaged as its own plugin so it can be installed independently in Claude Code, while
the `skills/<name>/` folder stays a portable unit any agent can copy.

## Add a skill

1. Create `plugins/<skill>/skills/<skill>/SKILL.md` (YAML frontmatter with `name` + `description`,
   then Markdown instructions; add a `reference/` folder for details loaded on demand).
2. Add `plugins/<skill>/.claude-plugin/plugin.json` (`name`, `description`, `version`).
3. Add a plugin entry to `.claude-plugin/marketplace.json`.
4. Run the validator below.

## Validate

```bash
python3 .github/scripts/validate_skills.py
```

Checks that every `SKILL.md` has frontmatter with a `description`, and that all `marketplace.json` /
`plugin.json` files are valid JSON. CI runs this on every push and pull request. To validate the
Claude Code manifests specifically, run `claude plugin validate .` from the repo root.

## License

[MIT](LICENSE) © 2026 Björn Vingedal. Free to use, modify, and redistribute.

> **Note:** tSQLt is a development/test tool. Never install it on a production database.
