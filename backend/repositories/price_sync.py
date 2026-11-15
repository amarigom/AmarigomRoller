from models import PriceSyncState
from repositories.base import BaseRepository


class PriceSyncRepository(BaseRepository):
    model = PriceSyncState

    def state(self, lock=False):
        query = PriceSyncState.query.filter_by(id=1)
        if lock:
            query = query.with_for_update()
        return query.first()
