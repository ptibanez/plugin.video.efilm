""" Purchased module """

from .base import Base
from ..common import api
from ..common import settings
from ..models.video import Video 


class Purchased(Base):
    """Purchased view"""

    has_dirs = False
    has_videos = True

    def set_items(self):
        # convert to video info
        items = filter(lambda x: (x["active"] and x["product_type"] == "audiovisual"), api.loans_actives())
        for item in items:
            info = api.videos_audiovisuals(item["product"])
            video = Video(info, item["expire"])
            self.items.append(video)
    

        

    

