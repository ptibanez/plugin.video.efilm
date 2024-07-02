""" HTTPS Api for eFilm """

import requests
from .exceptions.api import ApiException
from .exceptions.dialog import DialogException
from .helpers.misc import is_drm
from .helpers.headers import Headers
import logging


class Api:
    """
    Class for handling API calls to eFilm
    """

    s = requests.Session()

    TOKENS = {
        "ANDALUCÍA.EFILM Red de Bibliotecas Públicas de Andalucía": {
            "CLIENT_ID": 134  # ,
            # "CLIENT_SECRET": "yICstBCQ8CKB8RF6KuDmr9R20xtfyYbm",
        }
    }

    LIMIT = 20

    client_id = 134
    # client_secret = ""

    domain = "ANDALUCÍA.EFILM Red de Bibliotecas Públicas de Andalucía"

    def __init__(self, domain: str):
        # Set headers
        Headers.set_common(self.s)
        Headers.set_old(self.s)
        Headers.set_new(self.s)

        self.set_domain(domain)

        self.s.headers["X-Client-Id"] = str(self.client_id)

    def _get_base_url(self) -> str:
        """
        Get the base URL used depending on your domain
        """

        # subdomain = "uapi" if uapi else "api"
        # host = "filminlatino" if self.domain == "mx" else "filmin"
        # return f"https://{subdomain}.{host}.{self.domain}"
        return f"https://backend-prod.efilm.online/api/v1"

    def _req(
        self,
        endpoint: str,
        body: dict=None,
        query: dict=None 
    ):
        """
        Sends the request
        """

        method = "GET"

        if body is not None:
            method = "POST"

        base_url = self._get_base_url()
        res = self.s.request(
            method,
            base_url + endpoint,
            json=body,
            params=query
        )
        
        self.logger.info(res)
        
        # Avoid non JSON response
        if res.headers.get("Content-Type") != "application/json":
            raise DialogException("Non JSON response")

        res_json = res.json()
        if res.ok:
            return res_json

        raise ApiException(res_json["detail"])

    def login(self, username: str, password: str) -> dict:
        """
        Login into eFilm using a username and a password
        """

        res = self._req(
            "/auth/",
            body={
                "id_client": self.client_id,
                "password": password,
                "username": username
            },
        )
        return res

    def profiles(self) -> list:
        """
        Get all profiles available
        """
    
        res = self._req("/auth/profiles/")  # , uapi=True)
        return res

    def logout(self):
        """
        Logout of eFilm
        Returns void
        """

        self._req("/logout/", body={})

    # def user(self):
    #     """
    #     Get user data
    #     """
    #
    #     res = self._req(endpoint="/user/")
    #     return res["data"]

    def genres(self):
        """
        Get all media genres available (Action, Adventure...)
        """

        res = self._req(endpoint="/genres")
        return res["data"]

    def catalog(
        self,
        page: int,
        item_type: str="",
        genre: int=-1,
        subgenre: int=-1
    ):
        """
        Filter media available by genre and subgenre
        """

        query = {}
        if item_type:
            query["type"] = item_type

        # Picked both genre and subgenre
        if genre != -1 and subgenre != -1:
            query["filter_entity"] = "tag"
            query["filter_id"] = subgenre

        # Picked genre only
        if genre != -1 and subgenre == -1:
            query["filter_entity"] = "genre"
            query["filter_id"] = genre

        res = self._req(
            endpoint="/media/catalog",
            query=self._paginated_query(query, page)
        )
        return res["data"]

    def search(self, term: str) -> list:
        """
        Search by title using a term
        """

        res = self._req(endpoint="/search", query={
            "query": term
        }, uapi=True)

        # Return only media
        return [o for o in res["data"]["items"] if o.get('_type') == 'Media']

    def purchased(self) -> list:
        """
        Get all media purchased
        """

        res = self._req(endpoint="/loans/loans/actives/?order_by=-recent&page_size=5&page=1")
        return res 

    def highlighteds(self) -> list:
        """
        Get trending, this is usually the first thing to show up in Android
        """

        items = []
        res = self._req(endpoint="/highlighteds/home")

        for item in res["data"]:
            items.append(item["item"]["data"])

        return items

    def collections(self) -> list:
        """
        Get all collections available
        """

        res = self._req(endpoint="/collections")
        return res["data"]

    def collection(self, collection_id: int, page: int) -> list:
        """
        Get all media from a specific collection
        """

        res = self._req(
            endpoint=f"/collections/{collection_id}/medias",
            query=self._paginated_query({}, page)
        )
        return res["data"]

    def watching(self) -> list:
        """
        Get all unfinished media
        """

        items = []
        res = self._req(endpoint="/auth/keep-watching", uapi=True)

        items = [x["media"] for x in res["data"]]

        return items

    def playlists(self) -> list:
        """
        Get user's playlists
        """
        res = self._req("/user/playlists")
        return res["data"]

    def playlist(self, playlist_id: int):
        """
        Get all media for a playlist
        """

        res = self._req(f"/user/playlists/{playlist_id}/medias")
        return res["data"]

    def media_simple(self, item_id: int):
        """
        Get details of media
        """
        res = self._req(endpoint=f"/media/{item_id}/simple")
        return res["data"]

    def seasons(self, item_id: int):
        """
        Get all seasons of a show
        """

        res = self.media_simple(item_id)
        return res["seasons"]["data"]

    def episodes(self, item_id: int, season_id: int):
        """
        Get all episodes of a season
        """

        items = []
        seasons = self.seasons(item_id)
        for season in seasons:
            if int(season_id) == season["id"]:
                items = season["episodes"]["data"]

        return items

    def watch_later(self) -> list:
        """
        Get all media added to watch later
        """

        res = self._req(endpoint="/auth/watch-later", uapi=True)
        return res["data"]

    def use_tickets(self, item_id: int):
        """
        Rent media using a ticket
        """

        self._req(endpoint="/user/tickets/activate", body={"id": item_id})

    def streams(self, item_id: int) -> dict:
        """
        Get all media versions available (dubbed, subtitled...)
        """

        res = self._req(endpoint=f"/version/{item_id}")
        streams = {}
        # -- Single feed -- #
        if "feeds" not in res:
            if not is_drm(res.get("type", "FLVURL")):
                # Add support for v1 (DRM-Free) video
                res["src"] = res.get("FLVURL") or res.get("src")
                res["type"] = "FLVURL"

            # We have to convert it to the multi-feed response
            streams = {
                "feeds": [res],
                "media_viewing_id": res["media_viewing_id"],
                "xml": res["xml"],
            }
        # -- More than one feed -- #
        else:
            # Leave it as it is
            streams = res

        return streams

    # -- HELPERS -- #
    def set_token(self, token: str):
        """
        Add auth token to HTTP session header
        """

        self.s.headers["Authorization"] = f"JWT {token}"

    def set_profile_id(self, profile_id: str):
        """
        Add profile id to HTTP session header
        """

        self.s.headers["x-user-profile-id"] = profile_id

    def set_domain(self, domain: str):
        """
        Set domain and change client_id and client_secret
        """

        self.domain = domain
        tokens = self.TOKENS[domain]
        self.client_id = tokens["CLIENT_ID"]
        # self.client_secret = tokens["CLIENT_SECRET"]

    def _paginated_query(self, query: dict, page: int) -> dict:
        new_query = {
            **query,
            'page': page,
            'limit': self.LIMIT
        }

        return new_query
