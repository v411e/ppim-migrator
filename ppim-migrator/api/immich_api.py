import requests
import json
import datetime


class ImmichApi:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

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

    # POST /albums
    def create_album(
        self,
        albumName: str,
        assetIds = [],
        description = f'Imported from photoprism ({datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})',
    ) -> str:
        url = f"{self.base_url}/api/albums"
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

    # PUT /api/assets/:id
    def set_as_favorite(self, uid: str):
        url = f"{self.base_url}/api/assets/{uid}"
        payload = json.dumps({"isFavorite": True})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.api_key,
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        return response.text
