from .api.photoprism_api import PhotoprismApi
from .api.immich_api import ImmichApi
from .config import Config
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

    def migrate_stacked_raws(self, count: int = 100000):
        click.echo(f"Migrating all stacks (limit: {count})...")
        jpg_raw_pairs = self.pp_api.get_raws_with_jpg_original(count)

        for filelist in jpg_raw_pairs:
            matching_uids = self._get_matching_uids(filelist)
            matches_uids = matching_uids.get("uids")
            files_not_found = matching_uids.get("files_not_found")
            self._summary(matches_uids=matches_uids, files_not_found=files_not_found)

            if(len(matches_uids) >= 2):
                click.echo("Creating stack ...")
                stack = self.im_api.create_stack(matches_uids)
                click.echo(stack)


    def migrate_all_albums(self, count: int = 1000):
        click.echo(f"Migrating all albums (limit: {count})...")
        data = self.pp_api.get_all_albums_data(count)

        # Migrate one by one...
        album_num = len(data)
        for index, album in enumerate(data):
            click.echo(f"-------------- ({index + 1}/{album_num})")
            self._migrate_album(uid=album["UID"], album_title=album["Title"])

        click.echo("--------------")
        click.echo("Done.")

    def migrate_album(self, uid):
        click.echo(f"Migrating album with id {uid}")

        album_title = self.pp_api.get_album_title(uid)
        click.echo(f"Album title: {album_title}")

        self._migrate_album(uid=uid, album_title=album_title)
        click.echo("Done.")

    def _migrate_album(self, uid: str, album_title: str):
        click.echo(f"Migrating album with id {uid}")
        click.echo(f"Album title: {album_title}")

        photo_file_list = self.pp_api.get_photo_files_in_album(uid=uid)
        click.echo(f"Photo file list: {photo_file_list}")

        matching_uids = self._get_matching_uids(photo_file_list)
        matches_uids = matching_uids.get("uids")
        files_not_found = matching_uids.get("files_not_found")
        self._summary(matches_uids=matches_uids, files_not_found=files_not_found)

        click.echo("Creating album...")

        self.im_api.create_album(albumName=album_title, assetIds=matches_uids)

    def migrate_favorites(self):
        click.echo("Migrating favorites")
        photo_file_list = self.pp_api.get_photo_files_in_favorites()

        matching_uids = self._get_matching_uids(photo_file_list)
        matches_uids = matching_uids.get("uids")
        files_not_found = matching_uids.get("files_not_found")
        self._summary(matches_uids=matches_uids, files_not_found=files_not_found)

        click.echo("Setting images as favorites...")

        for uid in matches_uids:
            self.im_api.set_as_favorite(uid)

        click.echo("Done.")

    @staticmethod
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

    def _get_matching_uids(self, photo_file_list: list) -> dict:
        def _no_match():
            files_not_found.append(photo_file)
            click.echo(f"No match: {photo_file} in Immich")

        matches_uids = []
        files_not_found = []
        for photo_file in photo_file_list:
            uri_components = photo_file.split("/")
            filename = uri_components[-1]
            search_result = self.im_api.search_metadata(originalFileName=filename)
            items: list = search_result.get("assets").get("items")

            matches_paths = []
            # no items in search result → no match
            if len(items) == 0:
                _no_match()

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
                    click.echo("Possible matches in Immich:")
                    for match in matches_paths:
                        click.echo(f" - {match.get('originalPath')}")
                else:
                    _no_match()
        return {
            "uids": matches_uids,
            "files_not_found": files_not_found,
        }

    @staticmethod
    def _summary(matches_uids: list, files_not_found: list):
        if files_not_found:
            click.echo(f"Images found in immich: {len(matches_uids)}")
            click.echo("Images not found in immich:")
            for file in files_not_found:
                click.echo(f" - {file}")
        else:
            click.echo("Migration successful!")
            click.echo(f"All images found in immich: {len(matches_uids)}")
