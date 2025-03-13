"""Command line interface for iCloud Versioning."""

import click
from . import __version__
from .core import VersionManager


@click.group()
@click.version_option(version=__version__)
def cli():
    """iCloud Versioning - Track and manage versions of your iCloud files."""
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def init(directory):
    """Initialize version tracking for a directory."""
    manager = VersionManager(directory)
    manager.initialize()
    click.echo(f"Initialized version tracking in {directory}")


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def status(directory):
    """Show status of tracked files."""
    manager = VersionManager(directory)
    status_info = manager.get_status()
    
    if not status_info:
        click.echo("No files being tracked.")
        return
        
    click.echo("Tracked files:")
    for file, info in status_info.items():
        click.echo(f"  {file} - {info['status']}")


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.argument("file", type=click.Path(exists=True))
def track(directory, file):
    """Start tracking a file."""
    manager = VersionManager(directory)
    manager.track_file(file)
    click.echo(f"Now tracking {file}")


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.argument("file", type=click.Path(exists=True))
@click.option("--version", "-v", type=int, help="Version to restore")
def restore(directory, file, version):
    """Restore a file to a previous version."""
    manager = VersionManager(directory)
    manager.restore_file(file, version)
    click.echo(f"Restored {file} to version {version}")


def main():
    """Main entry point for the application."""
    cli()


if __name__ == "__main__":
    main()