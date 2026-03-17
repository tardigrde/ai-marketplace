from __future__ import annotations

import json

import click
from rich.console import Console
from rich.table import Table

from cli.schema import MarketplaceManifest
from cli.utils import read_json, resolve_marketplace_path

console = Console()


@click.command("list")
@click.option("--search", "-s", default=None, help="Search by name, description, or keywords")
@click.option("--category", "-c", default=None, help="Filter by category")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def list_cmd(search: str | None, category: str | None, json_output: bool):
    """List all plugins in the marketplace."""
    marketplace_path = resolve_marketplace_path()

    try:
        raw = read_json(marketplace_path)
        manifest = MarketplaceManifest.model_validate(raw)
    except Exception as e:
        console.print(f"[red]ERROR: Cannot read marketplace.json: {e}[/red]")
        raise SystemExit(1)

    plugins = manifest.plugins

    # Filter by search
    if search:
        q = search.lower()
        plugins = [
            p
            for p in plugins
            if q in p.name.lower()
            or q in p.description.lower()
            or any(q in k.lower() for k in p.keywords)
        ]

    # Filter by category
    if category:
        plugins = [p for p in plugins if p.category == category]

    # JSON output
    if json_output:
        click.echo(json.dumps([p.model_dump() for p in plugins], indent=2))
        return

    # Table output
    if not plugins:
        console.print("[yellow]No plugins found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name", style="cyan")
    table.add_column("Version")
    table.add_column("Category", style="yellow")
    table.add_column("Description")

    for p in plugins:
        table.add_row(p.name, p.version, p.category, p.description)

    console.print()
    console.print(table)
    console.print(f"\n[dim]{len(plugins)} plugin(s)[/dim]")
