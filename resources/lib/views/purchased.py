""" Purchased module """

from .base import Base
from ..common import api
from ..common import settings


class Purchased(Base):
    """Purchased view"""

    has_dirs = False
    has_videos = True

    def set_items(self):
        # remaining_loans = settings.get_remaining_loans()
        # self.items = [{"id": 1, "name_product": f"Te quedan {remaining_loans} préstamos", "product_type": ""}]
        self.items = api.loans_actives()
        # convert to video info
        
                    # video = Video(name = item["name_product"], 
            #               cover = item["cover"],
            #               expire = item["expire"],
            #               subinfo = item["subinfo"],
            #               director = item["subinfo"]["director"],
            #               year = None)
        
        video = Video()
        
        for item in api.loans_actives():
            video.title = item["name_product"]
            video.plot = item["description"]
            self.items.append(video)
    
        # title = video.name
        # if video.subinfo:
        #    title += ListItemExtra.subinfoToStr(video.subinfo)
        #
        # if video.expire:
        #    title += ListItemExtra.expireToStr(video.expire)  
        
    def expireToStr(expire: str) -> str:
        return " - vence: " + datetime.fromisoformat(expire).strftime("%d/%m/%Y a las %H:%M")
    
    def subinfoToStr(subinfo: dict) -> str:
        subinfoToStr = ""
        for key, value in subinfo.items():
            keyTranslated = settings.get_localized_string(sum(map(ord, hashlib.md5(key.encode('utf-8')).hexdigest())) + 40053)
            subinfoToStr += f' - {keyTranslated}: {value}'
        return subinfoToStr
