from models import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def list(self):
        return User.query.order_by(User.id).all()

    def get_by_email(self, email):
        return User.query.filter(User.email == email).first()

    def count_active_admins(self):
        return User.query.filter_by(rol='admin', activo=True).count()
