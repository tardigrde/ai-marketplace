# Contributing to AI Plugin Marketplace

Thank you for contributing! This guide walks you through adding a new plugin to the marketplace.

## Prerequisites

- Python 3.11+
- Git

## Adding a New Plugin

### 1. Fork and clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-plugin-marketplace.git
cd ai-plugin-marketplace
```

### 2. Scaffold your plugin

Use the CLI tool to generate the plugin skeleton:

```bash
cd tools/cli
pip install -r requirements.txt
python -m cli add --name my-plugin --description "What your plugin does" --author your-name --category general --init
```

This creates:
- `plugins/my-plugin/plugin.json` — Plugin manifest
- `plugins/my-plugin/skills/SKILL.md` — Skill instructions with frontmatter

### 3. Edit SKILL.md

Write clear, actionable instructions in the skill file. The YAML frontmatter must include:

```yaml
---
name: my-plugin
description: A clear one-line description
---
```

The body should contain detailed instructions for the AI agent.

### 4. Optional features

**Commands** — Add slash commands in `commands/`:
```
plugins/my-plugin/commands/my-command.md
```
Include YAML frontmatter with `name`, `description`, and optional `argument-hint`.

**Agents** — Add autonomous agents in `agents/`:
```
plugins/my-plugin/agents/my-agent.json
```
Include `name`, `description`, `capabilities`, and `triggers`.

**MCP Servers** — Add MCP server config to `plugin.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"]
    }
  }
}
```

### 5. Validate your plugin

```bash
cd tools/cli
python -m cli validate --path ../../.github/plugin/marketplace.json
```

### 6. Submit a Pull Request

1. Create a feature branch: `git checkout -b add-my-plugin`
2. Commit your changes: `git commit -m "feat: add my-plugin"`
3. Push and open a PR

## Plugin Guidelines

- **Single responsibility** — Each plugin should do one thing well
- **Clear instructions** — SKILL.md should be self-contained and actionable
- **Keywords** — Use relevant keywords for discoverability
- **Compatibility** — Declare which platforms your plugin supports
- **Version** — Start at `0.1.0`, use semver for updates

## Code Style

- Python 3.11+ for CLI and adapters
- Use `click` for CLI commands, `rich` for output, `pydantic` for validation
- 4-space indentation (PEP 8)
- Type hints encouraged

## Questions?

Open an issue on GitHub for questions or discussion.
