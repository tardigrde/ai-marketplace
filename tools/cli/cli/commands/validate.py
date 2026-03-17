from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from cli.schema import MarketplaceManifest, PluginManifest, SkillFrontmatter
from cli.utils import parse_frontmatter, read_json, resolve_marketplace_path

console = Console()


@click.command()
@click.option("--path", "path_opt", default=None, help="Path to marketplace.json")
def validate(path_opt: str | None):
    """Validate marketplace manifest and all local plugins."""
    marketplace_path = resolve_marketplace_path(path_opt)
    base_dir = marketplace_path.parent

    console.print("[blue]Validating marketplace manifest...[/blue]")
    console.print(f"  [dim]Path: {marketplace_path}[/dim]")

    if not marketplace_path.exists():
        console.print(f"[red]ERROR: Marketplace file not found: {marketplace_path}[/red]")
        raise SystemExit(1)

    # Validate marketplace.json
    try:
        raw = read_json(marketplace_path)
        manifest = MarketplaceManifest.model_validate(raw)
    except Exception as e:
        console.print(f"[red]ERROR: Invalid marketplace.json: {e}[/red]")
        raise SystemExit(1)

    console.print("  [green]OK: marketplace.json is valid[/green]")

    # Validate each plugin
    all_passed = True
    project_root = base_dir.parent.parent

    for entry in manifest.plugins:
        plugin_dir = (project_root / entry.entry).parent
        console.print(f"\n[blue]Validating plugin: {entry.name}[/blue]")

        # Check plugin.json
        plugin_json_path = plugin_dir / "plugin.json"
        if not plugin_json_path.exists():
            console.print(f"  [red]ERROR: plugin.json not found at {plugin_json_path}[/red]")
            all_passed = False
            continue

        try:
            plugin_raw = read_json(plugin_json_path)
            plugin = PluginManifest.model_validate(plugin_raw)
        except Exception as e:
            console.print(f"  [red]ERROR: Invalid plugin.json: {e}[/red]")
            all_passed = False
            continue

        console.print("  [green]OK: plugin.json is valid[/green]")

        # Check SKILL.md files
        for skill_rel in plugin.skills:
            skill_file = plugin_dir / skill_rel
            if not skill_file.exists():
                console.print(f"  [red]ERROR: Skill file not found: {skill_rel}[/red]")
                all_passed = False
                continue

            content = skill_file.read_text()
            fm = parse_frontmatter(content)
            if not fm:
                console.print(f"  [red]ERROR: Missing or invalid frontmatter in {skill_rel}[/red]")
                all_passed = False
                continue

            try:
                SkillFrontmatter.model_validate(fm)
            except Exception:
                console.print(f"  [red]ERROR: Invalid frontmatter in {skill_rel}[/red]")
                all_passed = False
                continue

            console.print(f"  [green]OK: {skill_rel} frontmatter is valid[/green]")

        # Check commands
        for cmd_rel in plugin.commands or []:
            cmd_file = plugin_dir / cmd_rel
            if not cmd_file.exists():
                console.print(f"  [red]ERROR: Command file not found: {cmd_rel}[/red]")
                all_passed = False
            else:
                console.print(f"  [green]OK: {cmd_rel} exists[/green]")

        # Check agents
        for agent_rel in plugin.agents or []:
            agent_file = plugin_dir / agent_rel
            if not agent_file.exists():
                console.print(f"  [red]ERROR: Agent file not found: {agent_rel}[/red]")
                all_passed = False
            else:
                try:
                    read_json(agent_file)
                    console.print(f"  [green]OK: {agent_rel} is valid JSON[/green]")
                except Exception:
                    console.print(f"  [red]ERROR: Invalid JSON in {agent_rel}[/red]")
                    all_passed = False

    console.print()
    if all_passed:
        console.print("[green bold]All validations passed![/green bold]")
    else:
        console.print("[red bold]Some validations failed.[/red bold]")
        raise SystemExit(1)
