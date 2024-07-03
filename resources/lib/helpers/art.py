""" Art module """


class Art:
    """
    Convert eFilm art structure to Kodi
    """

    @staticmethod
    def api(item: dict) -> dict:
        
        thumb = item.get("cover")
        poster = item.get("cover")
        fanart = item.get("cover")
        banner = item.get("cover")
        landscape = item.get("cover")
        icon = item.get("cover")
        highlighted = item.get("cover")

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
