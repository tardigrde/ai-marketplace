import click

from cli.commands.validate import validate
from cli.commands.list_cmd import list_cmd
from cli.commands.add import add
from cli.commands.build_web import build_web


@click.group()
@click.version_option("1.0.0", prog_name="marketplace")
def cli():
    """CLI tool for the Universal AI Plugin Marketplace."""
    pass


cli.add_command(validate)
cli.add_command(list_cmd)
cli.add_command(add)
cli.add_command(build_web)
