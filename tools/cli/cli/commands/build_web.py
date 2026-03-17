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
    project_root = marketplace_path.parent.parent
    web_dir = project_root / "web"

    try:
        raw = read_json(marketplace_path)
        manifest = MarketplaceManifest.model_validate(raw)
    except Exception as e:
        console.print(f"[red]ERROR: Cannot read marketplace.json: {e}[/red]")
        raise SystemExit(1)

    web_plugins = []

    for entry in manifest.plugins:
        plugin_dir = (project_root / entry.source).resolve()

        plugin = {
            "name": entry.name,
            "version": entry.version or "1.0.0",
            "description": entry.description or "",
            "category": entry.category or "general",
            "keywords": entry.keywords or [],
        }

        # Read skill descriptions from SKILL.md frontmatter
        skills_dir = plugin_dir / "skills"
        skill_descriptions = []
        if skills_dir.exists():
            for skill_dir in sorted(skills_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_path = skill_dir / "SKILL.md"
                if skill_path.exists():
                    fm = parse_frontmatter(skill_path.read_text())
                    if fm:
                        skill_descriptions.append(fm["description"])
        plugin["skills"] = skill_descriptions

        # Check for agent
        agents_dir = plugin_dir / "agents"
        if agents_dir.exists():
            plugin["hasAgent"] = any(agents_dir.iterdir())

        web_plugins.append(plugin)

    web_dir.mkdir(exist_ok=True)
    output_path = web_dir / "plugins.json"
    output_path.write_text(json.dumps(web_plugins, indent=2) + "\n")
    console.print(f"[green]Wrote {len(web_plugins)} plugin(s) to web/plugins.json[/green]")
