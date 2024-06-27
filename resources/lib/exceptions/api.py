""" Apiv3 exception module """
from xbmcgui import Dialog


class ApiException(Exception):
    """
    Throw exception when HTTP code is diferent from 2XX
    """

    # def __init__(self, errors: str):
    #     super().__init__()
    #     Dialog().ok("eFilm API Error", errors)

    def __init__(self, error: dict):
        super().__init__()
        Dialog().ok("eFilm API Error", error["title"])