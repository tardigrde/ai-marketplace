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
- **grill-me** — Relentlessly interview about a plan until shared understanding is reached
- **autoreview** — Structured closeout review using Codex/Claude with security and findings tracking

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

## Agent Plugins 1.0.0

`plugins/swe` is also a valid [Agent Plugins 1.0.0](https://agent-plugins.org)
package: `plugin.json` + `skills/<name>/SKILL.md` + `mcp.json` (Context7, no
auth). Clients that follow the spec (e.g. the Agentic Chat Obsidian plugin)
install it into their plugins folder and get the same skills plus the MCP
server.

```bash
# Install into an Agent Plugins client vault
mkdir -p <vault>/.agentic-plugins
cp -r plugins/swe <vault>/.agentic-plugins/
```

Keep the package spec-conformant when adding skills: the frontmatter `name`
must match the skill directory and stay lowercase-hyphen; the `description`
must not exceed 1024 characters.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgements

Some skills adapted from [mattpocock/skills](https://github.com/mattpocock/skills) and [steipete/agent-scripts](https://github.com/steipete/agent-scripts) (MIT License).

## License

MIT — see [LICENSE](LICENSE).
