""" Video model module """
from dataclasses import dataclass


@dataclass
class Video:
    """Wrapper for all data needed for Video"""

    name: str
    year: int
    director: str
    cover: str
    subinfo: dict
    expire: str
