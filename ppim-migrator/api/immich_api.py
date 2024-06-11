import requests
import json


class ImmichApi:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    # GET /api/album/:id
    def _get_album_info(self, album_id: str) -> dict:
        url = f"{self.base_url}/api/album/{album_id}"
        headers = {"Accept": "application/json", "x-api-key": self.api_key}
        response = requests.request("GET", url, headers=headers)
        json_response = response.json()
        return json_response

    def get_album_asset_uids(self, album_id: str) -> dict:
        album_info = self._get_album_info(album_id)
        assets = album_info.get("assets")
        asset_uids = [asset.get("id") for asset in assets]
        return set(asset_uids)

    # POST /api/search/metadata
    def search_metadata(self, originalFileName: str) -> dict:
        url = f"{self.base_url}/api/search/metadata"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.api_key
        }
        payload = json.dumps(
            {
                "originalFileName": originalFileName,
            }
        )
        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = response.json()
        return json_response

    # POST /album
    def create_album(
        self,
        albumName: str,
        assetIds: list = [],
        description: str = "Imported from photoprism",
    ) -> str:
        url = f"{self.base_url}/api/album"
        payload = json.dumps(
            {
                "albumName": albumName,
                "assetIds": assetIds,
                "description": description,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.api_key,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    # PUT /api/asset/:id
    def set_as_favorite(self, uid: str):
        url = f"{self.base_url}/api/asset/{uid}"
        payload = json.dumps({"isFavorite": True})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.api_key,
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        return response.text
