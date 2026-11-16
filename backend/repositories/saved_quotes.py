from models import SavedQuote
from repositories.base import BaseRepository


class SavedQuoteRepository(BaseRepository):
    model = SavedQuote

    def recent(self, limit=100):
        return SavedQuote.query.order_by(SavedQuote.creado_en.desc(), SavedQuote.id.desc()).limit(limit).all()
