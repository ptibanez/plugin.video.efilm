""" ListItem Helper """

from xbmcgui import ListItem
from .art import Art
from ..common import settings
from datetime import datetime
import hashlib


class ListItemExtra:
    """Helper for ListItem generation from eFilm data"""
    
    @staticmethod
    def subinfoToStr(subinfo: dict) -> str:
        subinfoToStr = ""
        for key, value in subinfo.items():
            print("subinfoToStr: " + key + " " + str(sum(map(ord, hashlib.md5(key.encode('utf-8')).hexdigest())) + 40053))
            keyTranslated = settings.get_localized_string(sum(map(ord, hashlib.md5(key.encode('utf-8')).hexdigest())) + 40053)
            subinfoToStr += f'{keyTranslated}: {value}, '
        return subinfoToStr
    
    @staticmethod
    def expireToStr(expire: str) -> str:
        return "vence: " + datetime.fromisoformat(expire).strftime("%d/%m/%Y a las %H:%M")

    @staticmethod
    def video(url: str, item: dict) -> ListItem:
        """ListItem for individual video"""

        list_item = ListItem(item["name_product"], path=url)
        info = {
            "title": item["name_product"] 
                             + " (" 
                             + ListItemExtra.subinfoToStr(item["subinfo"]) 
                             + ListItemExtra.expireToStr(item["expire"])
                             + ")",
            #"year": item["year"],
            #"plot": item["excerpt"],
            #"director": (item["subinfo"]["director"]) if item["subinfo"]["director"] else "" #,
            #"rating": item["avg_votes"],
            # Filmin returns duration in minutes, Kodi wants it in seconds
            #"duration": item["duration_in_minutes"] * 60,
        }
        list_item.setInfo("video", info)
        # ART
        list_item.setArt(Art.api(item))

        # Common
        list_item.setProperty("isPlayable", "true")
        list_item.setIsFolder(False)
        return list_item

    @staticmethod
    def folder(url: str, item: dict) -> ListItem:
        """ListItem for individual folder"""

        list_item = ListItem(item["name_product"], path=url)
        info = {
            "title": item["name_product"],
            #"year": item["year"],
            #"plot": item["excerpt"],
            "director": "DIRECTOR" #item["subinfo"]["director"] #,
            # "rating": item["avg_votes"],
            # Filmin returns duration in minutes, Kodi wants it in seconds
            #"duration": item["duration_in_minutes"] * 60,
        }

        list_item.setInfo("video", info)

        # ART
        #list_item.setArt(Art.uapi(item))
        list_item.setArt(Art.api(item))

        return list_item

    # @staticmethod
    # def folder_uapi(url: str, item: dict) -> ListItem:
    #     """Folder uapi flavour"""
    #
    #     list_item = ListItem(item["title"], path=url)
    #     info = {
    #         "title": item["title"],
    #         "year": item["year"],
    #         "plot": item["excerpt"],
    #         "director": item["director_names"],
    #         "rating": item["avg_votes"],
    #         # Filmin returns duration in minutes, Kodi wants it in seconds
    #         "duration": item["duration_in_minutes"] * 60,
    #     }
    #
    #     list_item.setInfo("video", info)
    #
    #     # ART
    #     list_item.setArt(Art.uapi(item))
    #     return list_item

    # @staticmethod
    # def folder_apiv3(url: str, item: dict) -> ListItem:
    #     """Folder apiv3 flavour"""
    #
    #     list_item = ListItem(item["title"], path=url)
    #     info = {"title": item["title"], "plot": item.get("excerpt")}
    #     list_item.setInfo("video", info)
    #     if "imageResources" in item:
    #         art = Art.apiv3(item["imageResources"]["data"])
    #         list_item.setArt(art)
    #
    #     return list_item
