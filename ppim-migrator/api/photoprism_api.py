import requests


class PhotoprismApi:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password

    # GET /api/v1/session
    def _get_session_id(self) -> str:
        # if we already have a session ID, return it
        if hasattr(self, "session_id") and self.session_id:
            return self.session_id

        auth_url = f"{self.base_url}/api/v1/session"
        response = requests.post(
            auth_url, json={"username": self.username, "password": self.password}
        )
        json_response = response.json()
        self.session_id = json_response.get("id")
        return self.session_id

    # GET /api/v1/photos/:uid
    def _get_photo_data(self, uid: str) -> dict:
        photo_url = f"{self.base_url}/api/v1/photos/{uid}"
        headers = {"X-Session-ID": self._get_session_id()}
        response = requests.get(photo_url, headers=headers)
        json_response = response.json()
        return json_response

    # GET /api/v1/albums?count=100&type=album
    def _get_all_albums_data(self, count: int = 1000) -> dict:
        album_url = f"{self.base_url}/api/v1/albums?count={count}&type=album"
        headers = {"X-Session-ID": self._get_session_id()}
        response = requests.get(album_url, headers=headers)
        json_response = response.json()
        return json_response

    # GET /api/v1/albums/:uid
    def _get_album_data(self, uid: str) -> dict:
        album_url = f"{self.base_url}/api/v1/albums/{uid}"
        headers = {"X-Session-ID": self._get_session_id()}
        response = requests.get(album_url, headers=headers)
        json_response = response.json()
        return json_response

    # GET /api/v1/photos?count=100000&s=:uid
    def _get_photos_in_album(self, uid: str, count: int = 100000) -> dict:
        album_url = f"{self.base_url}/api/v1/photos?count={count}&s={uid}"
        headers = {"X-Session-ID": self._get_session_id()}
        response = requests.get(album_url, headers=headers)
        json_response = response.json()
        return json_response

    # GET /api/v1/photos?count=100000&favorite=true
    def _get_photos_in_favorites(self, count: int = 100000) -> list:
        album_url = f"{self.base_url}/api/v1/photos?count={count}&favorite=true"
        headers = {"X-Session-ID": self._get_session_id()}
        response = requests.get(album_url, headers=headers)
        json_response = response.json()
        return json_response

    @staticmethod
    def _map_file_name(photos: list) -> list:
        photo_files = []
        for photo in photos:
            photo_files.append(photo["FileName"])
        return photo_files

    def _filter_sidecar_files(self, photo_files: list) -> list:
        return [file for file in photo_files if not file["FileRoot"] == "sidecar"]

    def get_all_albums_data(self, count: int = 1000) -> list:
        albums_data = self._get_all_albums_data(count)
        return albums_data

    def get_photo_files_in_album(self, uid: str, count: int = 100000) -> list:
        photos: list = self._get_photos_in_album(uid, count)
        photos = self._filter_sidecar_files(photos)
        return self._map_file_name(photos)

    def get_photo_files_in_favorites(self, count: int = 100000) -> list:
        photos: list = self._get_photos_in_favorites(count)
        photos = self._filter_sidecar_files(photos)
        return self._map_file_name(photos)

    def get_album_title(self, uid: str) -> str:
        album_data = self._get_album_data(uid)
        title_from_server = album_data.get("Title", "")
        return title_from_server

    def get_taken_at(self, uid: str) -> str:
        photo_data = self._get_photo_data(uid)
        taken_at_from_server = photo_data.get("TakenAt", "")
        return taken_at_from_server
