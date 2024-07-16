""" WatchLater module """
from .base import Base
from ..common import api
from ..models.video import Video 

class WatchLater(Base):
    """WatchLater view"""

    has_dirs = True
    has_videos = True

    def set_items(self):
        products = filter(lambda x: x["product_info"]["active"], api.users_save_product())
        for item in products:
            info = api.videos_audiovisuals(item["product"])
            video = Video(info)
            self.items.append(video)
        collections = filter(lambda x: x["collection_info"]["active"], api.users_save_collections())
        for item in collections:
            info = api.videos_series(item["collection"]) 
            video = Video(info) # TODO folder
            self.items.append(video)  

