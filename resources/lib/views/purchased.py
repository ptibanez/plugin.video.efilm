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
