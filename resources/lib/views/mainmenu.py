""" MainMenu module """
from .base import Base
from ..common import settings
from ..constants import Routes


class MainMenu(Base):
    """
    Main menu, default route. Does not have a path string
    """

    static = True
    items = [
        {
            "id": Routes.PURCHASED.value,
            "title": settings.get_localized_string(40023)
        }
    ]
