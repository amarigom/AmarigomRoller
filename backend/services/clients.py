from exceptions import ConflictError
from models import Cliente
from repositories.client import ClientRepository
from schemas.clients import ClienteOut


class ClientService:
    def __init__(self, clients=None):
        self.clients = clients or ClientRepository()

    def list_clients(self, limit=None, offset=0):
        return [ClienteOut.from_model(c) for c in self.clients.list(limit, offset)]

    def create_client(self, datos):
        if self.clients.get_by_email(datos.email):
            raise ConflictError("Este email ya está registrado")
        cliente = self.clients.add(Cliente(**datos.model_dump()))
        try:
            self.clients.commit()
        except ConflictError as e:
            raise ConflictError("Este email ya está registrado") from e
        return ClienteOut.from_model(cliente)
