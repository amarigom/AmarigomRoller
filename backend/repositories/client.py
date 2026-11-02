from models import Cliente
from repositories.base import BaseRepository


class ClientRepository(BaseRepository):
    model = Cliente

    def list(self, limit=None, offset=0):
        return self.paginate(Cliente.query.order_by(Cliente.id), limit, offset).all()

    def get_by_email(self, email):
        return Cliente.query.filter(Cliente.email == email).first()
