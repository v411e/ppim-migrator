import click
from api.photoprism_api import PhotoprismApi
from api.immich_api import ImmichApi
from config import Config
from migrator import Migrator

@click.group()
def cli():
    pass


@cli.command()
@click.argument("uid")
def migrate_album(uid):
    click.echo(f"Migrating album with id {uid}")
    migrator = Migrator()
    migrator.migrate_album(uid=uid)


@cli.command()
def migrate_favorites():
    click.echo("Migrating favorites")
    migrator = Migrator()
    migrator.migrate_favorites()

if __name__ == "__main__":
    cli()
