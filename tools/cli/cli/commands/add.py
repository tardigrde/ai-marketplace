from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console

from cli.schema import MarketplaceManifest, MarketplacePluginEntry
from cli.utils import read_json, resolve_marketplace_path

console = Console()


@click.command()
@click.option("--name", "-n", required=True, help="Plugin name")
@click.option("--description", "-d", default=None, help="Plugin description")
@click.option("--category", "-c", default=None, help="Plugin category")
@click.option("--init", "init_skeleton", is_flag=True, help="Scaffold a new plugin skeleton")
def add(name: str, description: str | None, category: str | None, init_skeleton: bool):
    """Add a plugin entry to marketplace.json."""
    marketplace_path = resolve_marketplace_path()
    project_root = marketplace_path.parent.parent

    # Read existing marketplace
    try:
        raw = read_json(marketplace_path)
        manifest = MarketplaceManifest.model_validate(raw)
    except Exception as e:
        console.print(f"[red]ERROR: Cannot read marketplace.json: {e}[/red]")
        raise SystemExit(1)

    # Check for duplicate
    if any(p.name == name for p in manifest.plugins):
        console.print(f'[red]ERROR: Plugin "{name}" already exists in marketplace[/red]')
        raise SystemExit(1)

    plugin_dir = project_root / "plugins" / name
    source = f"./plugins/{name}"
    description = description or f"Description for {name}"
    category = category or "general"

    # Optionally scaffold plugin skeleton
    if init_skeleton:
        if plugin_dir.exists():
            console.print(f"[red]ERROR: Directory already exists: {plugin_dir}[/red]")
            raise SystemExit(1)

        claude_plugin_dir = plugin_dir / ".claude-plugin"
        skills_dir = plugin_dir / "skills" / name
        claude_plugin_dir.mkdir(parents=True)
        skills_dir.mkdir(parents=True)

        plugin_json = {
            "name": name,
            "description": description,
            "version": "0.1.0",
        }

        skill_md = f"""---
name: {name}
description: {description}
---

# {name}

Write your skill instructions here.
"""

        (claude_plugin_dir / "plugin.json").write_text(json.dumps(plugin_json, indent=2) + "\n")
        (skills_dir / "SKILL.md").write_text(skill_md)
        console.print(f"  [green]Created plugin skeleton at plugins/{name}/[/green]")

    # Add entry to marketplace
    plugins = [p.model_dump() for p in manifest.plugins]
    plugins.append(
        {
            "name": name,
            "source": source,
            "description": description,
            "version": "0.1.0",
            "category": category,
            "keywords": [name],
        }
    )

    raw["plugins"] = plugins
    marketplace_path.write_text(json.dumps(raw, indent=2) + "\n")
    console.print(f'[green]Added "{name}" to marketplace.json[/green]')
