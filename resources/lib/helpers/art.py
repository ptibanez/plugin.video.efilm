""" Art module """
from ..models.video import Video

class Art:
    """
    Convert eFilm art structure to Kodi
    """

    @staticmethod
    def api(video: Video) -> dict:
        
        thumb = video.cover
        poster = video.cover
        fanart = video.cover
        banner = video.cover
        landscape = video.cover
        icon = video.cover
        highlighted = video.cover

        if highlighted is not None:
            if banner is None:
                banner = highlighted
            if landscape is None:
                landscape = highlighted
            if icon is None:
                icon = highlighted

        return {
            "thumb": thumb,
            "poster": poster,
            "banner": banner,
            "fanart": fanart,
            "landscape": landscape,
            "icon": icon,
        }
