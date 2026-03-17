from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console

from cli.schema import MarketplaceManifest
from cli.utils import parse_frontmatter, read_json, resolve_marketplace_path

console = Console()


@click.command("build-web")
def build_web():
    """Generate web/plugins.json from marketplace manifest."""
    marketplace_path = resolve_marketplace_path()
    project_root = marketplace_path.parent.parent.parent
    web_dir = project_root / "web"

    try:
        raw = read_json(marketplace_path)
        manifest = MarketplaceManifest.model_validate(raw)
    except Exception as e:
        console.print(f"[red]ERROR: Cannot read marketplace.json: {e}[/red]")
        raise SystemExit(1)

    web_plugins = []

    for entry in manifest.plugins:
        plugin = {
            "name": entry.name,
            "version": entry.version,
            "description": entry.description,
            "author": entry.author,
            "category": entry.category,
            "keywords": entry.keywords,
        }

        # Read SKILL.md frontmatter for enhanced descriptions
        plugin_dir = (project_root / entry.entry).parent
        skill_path = plugin_dir / "skills" / "SKILL.md"
        if skill_path.exists():
            fm = parse_frontmatter(skill_path.read_text())
            if fm:
                plugin["skillDescription"] = fm["description"]

        web_plugins.append(plugin)

    web_dir.mkdir(exist_ok=True)
    output_path = web_dir / "plugins.json"
    output_path.write_text(json.dumps(web_plugins, indent=2) + "\n")
    console.print(f"[green]Wrote {len(web_plugins)} plugin(s) to web/plugins.json[/green]")
