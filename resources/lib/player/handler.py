""" Player handler """

from xbmc import Monitor
from xbmcgui import Dialog, ListItem
from xbmcplugin import setResolvedUrl
from ..common import api, settings, _HANDLE
from ..helpers.listitem_extra import ListItemExtra
from ..helpers.misc import is_drm
from .player import Player
from ..exceptions.drm import DRMException
from ..models.mediamark_data import MediamarkData
from ..models.video import Video


class PlayHandler:
    """
    Handles playing media
    Rents media if it needs to and chooses a valid stream
    """

    item = {}

    #can_watch = True
    #can_buy = True

    def __init__(self, el_id: int):
        #self.item = api.loan(el_id)
        # if "can_watch" in self.item["user_data"]:
        #     can_watch = self.item["user_data"]["can_watch"]
        #     self.can_watch = len(can_watch["data"]) > 0
        #can_watch = self.item["enabled"]
        #can_buy = self.item["remaining_loans"] > 0
        self.item = api.videos_audiovisuals(el_id)

    # def buy_media(self):
    #     """
    #     Asks user if they want to buy media, send request if true
    #     """
    #     print("TODO buy_media")
    #
    #     user = api.user()
    #     tickets = len(user["tickets"]["data"])
    #     self.can_watch = Dialog().yesno(
    #         settings.get_localized_string(40050),
    #         settings.get_localized_string(40051) % tickets,
    #     )
    #     if self.can_watch:
    #         api.use_tickets(self.item["id"])

    # def version_picker(self, item_displays: dict) -> dict:
    #     """
    #     Return version that user selects
    #     """
    #     versions_api = item_displays["languages"]
    #
    #     v_show = []
    #     for v_tmp in versions_api:
    #         label = f"{v_tmp['language']['name']} - {v_tmp['subtitle']['name']}"
    #         list_item = ListItem(label=label)
    #         v_show.append(list_item)
    #
    #     index = Dialog().select(settings.get_localized_string(40052), v_show)
    #     if index == -1:
    #         return None
    #     else:
    #         return versions_api[index]

    def start(self):
        """
        Entrypoint for starting media playback
        """

        #if not self.can_watch and settings.can_buy():
        # if not self.can_watch and self.can_buy():
        #     self.buy_media()
        #
        # if not self.can_watch:
        #     Dialog().ok("Error", settings.get_localized_string(40053))
        #     return
        
        #loan_displays = api.loan_displays(self.item["id"])
        #info = api.videos_audiovisuals(self.item["id"])

        # version = self.version_picker(self.item)
        #
        # if version is None:
        #     return

        # Handle subtitles todo
        # subtitles_api = version["subtitles"]["data"]
        # subtitles = []
        # for subtitle in subtitles_api:
        #     subtitles.append(subtitle["subtitleFiles"]["data"][0]["path"])

        # Handle stream todo
        #streams = api.streams(version["id"])
        #streams = api.streams(item_displays)
        #stream = streams["feeds"][0]
        #stream = loan_displays["player"]["source"]
        stream = self.item["url_embedded"]

        # Handle PlayItem
        
        video = Video(self.item)
        
        play_item = ListItemExtra.video(stream, video)
        
        # play_item.setSubtitles(subtitles)

        # Start playing
        monitor = Monitor()
        # todo mediamark para sync
        # player = Player(
        #     # settings.can_sync(),
        #     # Force false, mediamark is currently broken
        #     False,
        #     MediamarkData(
        #         settings.get_user_id(),
        #         settings.get_profile_id(),
        #         self.item["id"],
        #         version["id"],
        #         streams["media_viewing_id"],
        #         settings.get_auth()["access"],
        #     ),
        # )
        
        player = Player(False, None)

        player.play(listitem=play_item)
        setResolvedUrl(_HANDLE, True, play_item)
        while not monitor.abortRequested():
            monitor.waitForAbort(5)
