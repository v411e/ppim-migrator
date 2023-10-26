from api.photoprism_api import PhotoprismApi
from api.immich_api import ImmichApi
from config import Config
import click

class Migrator:
    def __init__(self) -> None:
        config = Config()
        self.pp_api = PhotoprismApi(
            config.config["photoprism"]["base_url"],
            config.config["photoprism"]["username"],
            config.config["photoprism"]["password"],
        )
        self.im_api = ImmichApi(
            config.config["immich"]["base_url"], config.config["immich"]["api_key"]
        )

    def migrate_album(self, uid):
        click.echo(f"Migrating album with id {uid}")

        album_title = self.pp_api.get_album_title(uid)
        click.echo(f"Album title: {album_title}")

        photo_file_list = self.pp_api.get_photo_files_in_album(uid=uid)
        click.echo(f"Photo file list: {photo_file_list}")

        matches_uids = self._get_matching_uids(photo_file_list, self.im_api)
        click.echo(self.im_api.create_album(albumName=album_title, assetIds=matches_uids))

    def migrate_favorites(self):
        click.echo("Migrating favorites")
        config = Config()
        self.pp_api = PhotoprismApi(
            config.config["photoprism"]["base_url"],
            config.config["photoprism"]["username"],
            config.config["photoprism"]["password"],
        )
        photo_file_list = self.pp_api.get_photo_files_in_favorites()

        im_api = ImmichApi(
            config.config["immich"]["base_url"], config.config["immich"]["api_key"]
        )
        matches_uids = self._get_matching_uids(photo_file_list, im_api)
        click.echo(f"Total images found in immich: {len(matches_uids)}")
        for uid in matches_uids:
            im_api.set_as_favorite(uid)
        click.echo("Done.")

    def _is_same_path_ending(pp_path: list, im_path: list) -> bool:
        # compare file paths
        pp_path_depth = len(pp_path)
        im_path_depth = len(im_path)
        min_path_depth = min(pp_path_depth, im_path_depth)

        # take the last min_path_depth elements of each path and compare them
        pp_path_components = pp_path[-min_path_depth:]
        im_path_components = im_path[-min_path_depth:]

        # if the paths are the same, we have a match
        return pp_path_components == im_path_components

    def _get_matching_uids(self, photo_file_list: list, im_api: ImmichApi) -> list:
        matches_uids = []
        for photo_file in photo_file_list:
            uri_components = photo_file.split("/")
            filename = uri_components[-1]
            search_result = im_api.search(query=filename)
            items: list = search_result.get("assets").get("items")

            matches_paths = []
            # no items in search result → no match
            if len(items) == 0:
                click.echo(f"Could not find {filename} in Immich")

            # one or more items in search result → potential match
            elif len(items) >= 1:
                for item in items:
                    if self._is_same_path_ending(
                        pp_path=uri_components,
                        im_path=item.get("originalPath").split("/"),
                    ):
                        matches_uids.append(item.get("id"))
                        matches_paths.append(item.get("originalPath"))

                if len(matches_paths) == 1:
                    click.echo(
                        f"Added a match: {filename} (pp: {photo_file}, im: {matches_paths[0]})"
                    )
                elif len(matches_paths) > 1:
                    click.echo(
                        f"Added {len(matches_paths)} matches for {filename} in Immich"
                    )
                    click.echo(f"Original path in photoprism: {photo_file}")
                    click.echo(f"Possible matches in Immich:")
                    for match in matches_paths:
                        click.echo(f" - {match.get('originalPath')}")
                else:
                    click.echo(f"No match: {filename} in Immich")
        return matches_uids
