""" ListItem Helper """

from xbmcgui import ListItem
from .art import Art
from ..common import settings
from datetime import datetime
import hashlib
from ..models.video import Video


class ListItemExtra:
    """Helper for ListItem generation from eFilm data"""
    
    @staticmethod
    def video(url: str, video: Video) -> ListItem:
        """ListItem for individual video"""
        list_item = ListItem(video.title, path=url)
        
        info = {
             "title": video.title,
             "year": video.year,
             "plot": video.plot,
             "director": video.director,
             "genre": video.genre
        #     #"rating": item["avg_votes"],
        #     # Filmin returns duration in minutes, Kodi wants it in seconds
        #     #"duration": item["duration_in_minutes"] * 60,
        #
        }
        list_item.setInfo("video", info)
        # ART
        list_item.setArt(Art.api(video))

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

    
