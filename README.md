# bjorn-skills

Cross-tool **AI agent skills** ([SKILL.md format](https://agentskills.io)) by Björn Vingedal.

An [Agent Skill](https://agentskills.io) is a folder with a `SKILL.md` file (YAML frontmatter +
Markdown instructions, plus optional reference docs). The same skill folder is read - natively or
by copying it into a skills directory - by **Claude Code, OpenAI Codex CLI, Google Gemini CLI,
Cursor, and GitHub Copilot**. No conversion needed.

## Skills

| Skill | What it does |
|---|---|
| [`tsqlt-testing`](skills/tsqlt-testing/SKILL.md) | Author, run, and debug [tSQLt](https://tsqlt.org) unit tests for SQL Server - structure tests as Assemble/Act/Assert, fake or spy out dependencies (tables, functions, procedures), assert on query results, expect exceptions, and run suites. |
| [`xquik`](skills/xquik/SKILL.md) | Plan and implement Xquik X data extraction, automation, REST API, webhook, and MCP workflows. |

## See it in action

Load the [tSQLt example database](https://github.com/tSQLt-org/tSQLt/tree/main/Examples) without Tests.sql (let Claude make them instead), then give
Claude the tests you want by name and let the skill write them:

```text
can you create the following tsqlt tests for the database tSQLt_Example on my local ms sql server with windows authentication?

[AcceleratorTests].[test ready for experimentation if 2 particles]
[AcceleratorTests].[test we are not ready for experimentation if there is only 1 particle]
[AcceleratorTests].[test no particles are in a rectangle when there are no particles in the table]
[AcceleratorTests].[test a particle within the rectangle is returned]
[AcceleratorTests].[test a particle within the rectangle is returned with an Id, Point Location and Value]
[AcceleratorTests].[test a particle is included only if it fits inside the boundaries of the rectangle]
[AcceleratorTests].[test email is sent if we detected a higgs-boson]
[AcceleratorTests].[test email is not sent if we detected something other than higgs-boson]
[AcceleratorTests].[test status message includes the number of particles]
[AcceleratorTests].[test foreign key violated if Particle color is not in Color table]
[AcceleratorTests].[test foreign key is not violated if Particle color is in Color table]
```

From the test names alone, the skill scaffolds the full suite: faking tables, asserting on scalars and
result sets, spying on the email procedure so no mail is actually sent, checking the status message, and
verifying the foreign-key constraints. It then runs the class with `tSQLt.Run` and iterates until green.

Learn more about tSQLt at [tsqlt.org](https://tsqlt.org) or on [GitHub](https://github.com/tSQLt-org/tSQLt).

## Install

### skills.sh (any supported agent)

[skills.sh](https://skills.sh) is a package manager for Agent Skills. From your project directory, install
the skill you want by name (run `npx skills add Vingedal/bjorn-skills --list` to see all available skills):

```bash
npx skills add Vingedal/bjorn-skills --skill tsqlt-testing
```

### Claude Code

Add this repo as a [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces), then
install the skill you want - **each skill is its own plugin**, so you get only what you ask for:

```text
/plugin marketplace add Vingedal/bjorn-skills
/plugin install tsqlt-testing@bjorn-skills
```

Already installed? Pull the latest version and load it into your session:

```text
/plugin marketplace update bjorn-skills
/reload-plugins
```

(Third-party marketplaces don't auto-update, so updating is a manual two-step refresh:
`marketplace update` refreshes the catalog, `/reload-plugins` loads the new version.)

### Other agents (Codex CLI, Gemini CLI, Cursor, Copilot)

These tools read Agent Skills from a `skills/` directory. Copy the skill folder
into your tool's skills directory (paths vary by tool and version - check each tool's current docs):

| Tool | Copy a skill folder to | Docs |
|---|---|---|
| OpenAI Codex CLI | `~/.codex/skills/<skill-name>/` | [Codex skills](https://developers.openai.com/codex/skills) |
| Google Gemini CLI | `~/.gemini/skills/<skill-name>/` | [Gemini CLI skills](https://geminicli.com/docs/cli/skills/) |
| Cursor | `~/.cursor/skills/<skill-name>/` | [Cursor skills](https://cursor.com/docs) |
| GitHub Copilot | per the VS Code agent-skills location | [Copilot customization](https://docs.github.com/copilot) |
| Claude Code (manual) | `~/.claude/skills/<skill-name>/` | [Claude Code skills](https://code.claude.com/docs) |

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
│  ├─ tsqlt-testing/
│  │  ├─ SKILL.md                  # the skill (entry point)
│  │  ├─ reference/                # progressive-disclosure docs, loaded on demand
│  │  └─ .claude-plugin/
│  │     └─ plugin.json            # makes this skill an installable Claude Code plugin
│  └─ xquik/
│     ├─ SKILL.md                  # the skill (entry point)
│     └─ .claude-plugin/
│        └─ plugin.json            # makes this skill an installable Claude Code plugin
└─ .claude-plugin/
   └─ marketplace.json             # lists each skill as its own plugin
```

Skills live at the top level so any agent can copy a `skills/<name>/` folder directly and skills.sh
finds them in a standard location. Each skill is exposed as its **own** Claude Code plugin
(`<name>@bjorn-skills`), so you install only the skills you want.

## Add a skill

1. Create `skills/<name>/SKILL.md` - YAML frontmatter with `name` + `description`, then Markdown
   instructions; add a `reference/` folder for details loaded on demand.
2. Add `skills/<name>/.claude-plugin/plugin.json` (`name`, `description`, `version`) so Claude Code
   can install it as a standalone plugin.
3. Add a plugin entry to `.claude-plugin/marketplace.json` with `"source": "./skills/<name>"`.
4. Run the validator below, then commit.

(skills.sh and the copy-to-any-tool flow only need step 1 - the `SKILL.md`.)

## Validate

```bash
python3 .github/scripts/validate_skills.py    # frontmatter + JSON checks (also runs in CI)
claude plugin validate .                       # validate the Claude Code marketplace manifest
```

## License

[MIT](LICENSE) © 2026 Björn Vingedal. Free to use, modify, and redistribute.

> **Note:** tSQLt is a development/test tool. Never install it on a production database.
