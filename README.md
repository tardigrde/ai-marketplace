# AI Plugin Marketplace

A universal plugin marketplace that works natively with **GitHub Copilot CLI** and **Claude Code**, with adapter scripts for **Cursor** and **Windsurf**.

Copilot CLI and Claude Code share the same `marketplace.json` schema — one manifest, two harnesses.

## Compatibility

| Platform | Support | Method |
|---|---|---|
| GitHub Copilot CLI | Native | `.github/plugin/marketplace.json` |
| Claude Code | Native | `.claude-plugin/marketplace.json` (symlink) |
| Cursor | Adapter | `.cursorrules` files via `tools/adapters/cursor.py` |
| Windsurf | Adapter | `.windsurfrules` files via `tools/adapters/windsurf.py` |

## Quick Start

### For Consumers

Add this marketplace to your AI tool configuration:

**Copilot CLI / Claude Code** — reference this repo's `marketplace.json` in your tool's plugin config.

**Cursor** — generate `.cursorrules` files:
```bash
python tools/adapters/cursor.py
# Output: dist/cursor/*.cursorrules
```

**Windsurf** — generate `.windsurfrules` files:
```bash
python tools/adapters/windsurf.py
# Output: dist/windsurf/*.windsurfrules
```

### Available Plugins

| Plugin | Category | Description |
|---|---|---|
| code-reviewer | code-quality | AI-powered code review with best practices and security checks |
| test-generator | testing | Automatically generate unit tests from your source code |
| doc-writer | documentation | Generate and maintain project documentation automatically |
| git-helper | git | Smart git operations with conventional commit support |

## CLI Tool

The CLI tool lives in `tools/cli/` and provides commands for managing the marketplace.

### Setup

```bash
cd tools/cli
pip install -r requirements.txt
```

### Commands

**Validate** — Check marketplace manifest and all plugins:
```bash
python -m cli validate --path ../../.github/plugin/marketplace.json
```

**List** — View all plugins:
```bash
python -m cli list
python -m cli list --search test
python -m cli list --category git --json
```

**Add** — Add a new plugin entry:
```bash
python -m cli add --name my-plugin --description "Does X" --init
```

**Build Web** — Generate data for the web UI:
```bash
python -m cli build-web
```

## Web UI

Open `web/index.html` in a browser to browse plugins with search and category filtering. Run `cli build-web` first to generate `web/plugins.json`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the step-by-step plugin contribution guide.

## License

MIT — see [LICENSE](LICENSE).
