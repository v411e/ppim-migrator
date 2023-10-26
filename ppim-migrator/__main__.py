import click
from .migrator import Migrator


@click.group()
def cli():
    pass


@cli.command()
@click.argument("uid")
def migrate_album(uid):
    migrator = Migrator()
    migrator.migrate_album(uid=uid)


@cli.command()
def migrate_favorites():
    migrator = Migrator()
    migrator.migrate_favorites()


if __name__ == "__main__":
    cli()
