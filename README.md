# AI Plugin Marketplace

A universal plugin marketplace that works natively with **Claude Code**, with adapters for **GitHub Copilot CLI**, **Cursor**, and **Windsurf**.

## Compatibility

| Platform | Support | Method |
|---|---|---|
| Claude Code | Native | `.claude-plugin/marketplace.json` |
| GitHub Copilot CLI | Adapter | `python tools/adapters/copilot-cli.py` |
| Cursor | Adapter | `python tools/adapters/cursor.py` |
| Windsurf | Adapter | `python tools/adapters/windsurf.py` |

## Quick Start

### Install in Claude Code

```shell
/plugin marketplace add https://github.com/tardigrde/ai-marketplace
/plugin install swe@ai-plugin-marketplace
```

### Generate adapter files

```bash
# Copilot CLI
python tools/adapters/copilot-cli.py
# Output: dist/copilot-cli/marketplace.json

# Cursor
python tools/adapters/cursor.py
# Output: dist/cursor/*.cursorrules

# Windsurf
python tools/adapters/windsurf.py
# Output: dist/windsurf/*.windsurfrules
```

## Available Plugins

### swe — Software Engineering Toolkit

Skills:
- **code-review** — Review code for bugs, security, and best practices
- **test-generator** — Generate unit tests from source code
- **doc-writer** — Generate and update documentation

Agent: **swe-agent** — Orchestrates review, testing, and documentation

## CLI Tool

The CLI lives in `tools/cli/` (Python, click + pydantic + rich).

```bash
cd tools/cli
pip install -r requirements.txt
```

**Commands:**

```bash
# Validate marketplace and all plugins
python -m cli validate

# List plugins with search/filter
python -m cli list
python -m cli list --search review
python -m cli list --json

# Add a new plugin (optionally scaffold)
python -m cli add --name my-plugin --description "Does X" --init

# Generate web/plugins.json for the web UI
python -m cli build-web
```

## Web UI

Open `web/index.html` in a browser (or visit the GitHub Pages site) to browse plugins with search and category filtering.

```bash
python -m cli build-web  # generate data first
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
