from __future__ import annotations

import json
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

    console.print("[blue]Validating Claude Code marketplace manifest...[/blue]")
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
    console.print(f"  [dim]Marketplace: {manifest.name} (by {manifest.owner.name})[/dim]")

    # Validate each plugin
    all_passed = True
    project_root = base_dir.parent

    for entry in manifest.plugins:
        plugin_dir = (project_root / entry.source).resolve()
        console.print(f"\n[blue]Validating plugin: {entry.name}[/blue]")
        console.print(f"  [dim]Source: {entry.source}[/dim]")

        # Check .claude-plugin/plugin.json
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json_path.exists():
            console.print(f"  [red]ERROR: .claude-plugin/plugin.json not found[/red]")
            all_passed = False
            continue

        try:
            plugin_raw = read_json(plugin_json_path)
            plugin = PluginManifest.model_validate(plugin_raw)
        except Exception as e:
            console.print(f"  [red]ERROR: Invalid plugin.json: {e}[/red]")
            all_passed = False
            continue

        console.print("  [green]OK: .claude-plugin/plugin.json is valid[/green]")

        # Check for skill directories
        skills_dir = plugin_dir / "skills"
        if skills_dir.exists():
            for skill_dir in sorted(skills_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_file = skill_dir / "SKILL.md"
                if not skill_file.exists():
                    console.print(f"  [red]ERROR: Missing SKILL.md in skills/{skill_dir.name}/[/red]")
                    all_passed = False
                    continue

                content = skill_file.read_text()
                fm = parse_frontmatter(content)
                if not fm:
                    console.print(f"  [red]ERROR: Missing or invalid frontmatter in skills/{skill_dir.name}/SKILL.md[/red]")
                    all_passed = False
                    continue

                try:
                    SkillFrontmatter.model_validate(fm)
                except Exception:
                    console.print(f"  [red]ERROR: Invalid frontmatter in skills/{skill_dir.name}/SKILL.md[/red]")
                    all_passed = False
                    continue

                console.print(f"  [green]OK: skills/{skill_dir.name}/SKILL.md frontmatter is valid[/green]")

        # Check agents directory
        agents_dir = plugin_dir / "agents"
        if agents_dir.exists():
            for agent_file in sorted(agents_dir.iterdir()):
                if agent_file.suffix not in (".json", ".md"):
                    continue
                if agent_file.suffix == ".json":
                    try:
                        read_json(agent_file)
                        console.print(f"  [green]OK: agents/{agent_file.name} is valid JSON[/green]")
                    except Exception:
                        console.print(f"  [red]ERROR: Invalid JSON in agents/{agent_file.name}[/red]")
                        all_passed = False
                else:
                    console.print(f"  [green]OK: agents/{agent_file.name} exists[/green]")

        # Check MCP config
        mcp_file = plugin_dir / ".mcp.json"
        if mcp_file.exists():
            try:
                read_json(mcp_file)
                console.print("  [green]OK: .mcp.json is valid[/green]")
            except Exception:
                console.print("  [red]ERROR: Invalid JSON in .mcp.json[/red]")
                all_passed = False

    console.print()
    if all_passed:
        console.print("[green bold]All validations passed![/green bold]")
    else:
        console.print("[red bold]Some validations failed.[/red bold]")
        raise SystemExit(1)
