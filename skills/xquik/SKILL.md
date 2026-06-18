---
name: xquik
description: Plan and implement Xquik X data extraction, automation, REST API, webhook, and MCP workflows. Use when the user asks for Xquik, x-twitter-scraper, X/Twitter data extraction, social data automation, X account monitoring, X webhooks, or MCP access to X data.
---

# Xquik workflows

Xquik provides X data extraction, automation, REST API, webhooks, and MCP workflows through public product surfaces. Use this skill to keep implementation plans explicit and source-backed.

## The loop

1. **Classify the task.** Separate planning, local integration, live API calls, webhook handling, and MCP setup.
2. **Check public docs first.** Use `https://docs.xquik.com` for current endpoint, parameter, auth, webhook, and MCP setup details.
3. **Keep credentials external.** Read API keys from the user's environment or secret store. Never paste keys into code, prompts, logs, docs, or examples.
4. **Choose the smallest workflow.**
   - REST API: show request shape, pagination, retry handling, and typed response parsing.
   - Webhooks: verify signatures, handle retries idempotently, and store event IDs.
   - MCP: install and configure through the public MCP docs, then call tools only after the user opts in.
   - Monitoring or extraction: define target accounts, keywords, or tweet IDs before writing code.
5. **Validate without leaking data.** Use mock responses or redacted samples for tests unless the user explicitly asks for a live call and has provided credentials through a safe channel.

## Useful references

- Xquik docs: https://docs.xquik.com
- MCP setup: https://docs.xquik.com/mcp/overview
- Package source: https://github.com/Xquik-dev/x-twitter-scraper
