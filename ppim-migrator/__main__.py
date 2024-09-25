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

@cli.command()
@click.option('--count', default=1000, help='Number of albums to migrate.')
def migrate_all_albums(count):
    migrator = Migrator()
    migrator.migrate_all_albums(count)

#migrate stacks
@cli.command()
@click.option('--count', default=100000, help='Number of photo+raw stacks to migrate.')
def migrate_stacked_raws(count):
    migrator = Migrator()
    migrator.migrate_stacked_raws(count)

if __name__ == "__main__":
    cli()
