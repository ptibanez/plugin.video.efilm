""" Video model module """
from datetime import datetime


class Video:
    """Wrapper for all data needed for Video"""

    id: int
    title: str
    year: int
    director: str
    poster: str
    fanart: str
    plot: str
    genre: []
    
    def __init__(self, info: dict, expire: str = None):
        self.id = info["id"]               
        self.title = info["name"] + self.expireToStr(expire) if expire else info["name"]
        self.year = info["year"]
        self.director = info["director"]["name"]
        self.poster = info["cover"]
        self.fanart = info["banner"]
        self.plot = info["description"]
        self.genre = [genre["name"] for genre in info["genres"]]    
    
    def __getitem__(self, item):
        return getattr(self, item)

    def expireToStr(self, expire: str) -> str:
        return " (vence el " + datetime.fromisoformat(expire).strftime("%d/%m/%Y a las %H:%M") + ")"