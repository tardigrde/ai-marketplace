# Contributing to AI Plugin Marketplace

Thank you for contributing! This guide walks you through adding a new plugin to the marketplace.

## Prerequisites

- Python 3.11+
- Git

## Adding a New Plugin

### 1. Fork and clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-marketplace.git
cd ai-marketplace
```

### 2. Scaffold your plugin

```bash
cd tools/cli
pip install -r requirements.txt
python -m cli add --name my-plugin --description "What your plugin does" --category general --init
```

This creates:
- `plugins/my-plugin/.claude-plugin/plugin.json` — Plugin manifest
- `plugins/my-plugin/skills/my-plugin/SKILL.md` — Skill instructions with frontmatter

### 3. Edit SKILL.md

The YAML frontmatter must include:

```yaml
---
name: my-plugin
description: A clear one-line description
---
```

The body contains instructions for the AI agent.

### 4. Add more skills (optional)

Create additional skill directories under `skills/`:

```
plugins/my-plugin/skills/
├── my-plugin/SKILL.md      # default skill
└── extra-skill/SKILL.md    # additional skill
```

### 5. Add an agent (optional)

Create `agents/my-agent.json`:

```json
{
  "name": "my-agent",
  "description": "What the agent does",
  "capabilities": ["do-thing-a", "do-thing-b"]
}
```

### 6. Add MCP servers (optional)

Create `.mcp.json` at plugin root:

```json
{
  "my-server": {
    "command": "npx",
    "args": ["-y", "my-mcp-server"]
  }
}
```

### 7. Validate your plugin

```bash
cd tools/cli
python -m cli validate
```

### 8. Submit a Pull Request

1. Create a feature branch: `git checkout -b add-my-plugin`
2. Commit your changes: `git commit -m "feat: add my-plugin"`
3. Push and open a PR

## Plugin Guidelines

- **Single responsibility** — Each plugin should do one thing well
- **Clear instructions** — SKILL.md should be self-contained and actionable
- **Keywords** — Use relevant keywords for discoverability
- **Version** — Start at `0.1.0`, use semver for updates

## Code Style

- Python 3.11+ for CLI and adapters
- `click` for CLI, `rich` for output, `pydantic` for validation
- 4-space indentation (PEP 8)
- Type hints encouraged

## Questions?

Open an issue on GitHub for questions or discussion.
