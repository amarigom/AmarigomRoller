from werkzeug.security import generate_password_hash

from exceptions import ConflictError, NotFoundError
from models import Role, User
from repositories.user import UserRepository
from schemas.auth import UserOut


class UserService:
    def __init__(self, users=None):
        self.users = users or UserRepository()

    def list_users(self):
        return [UserOut.from_model(u) for u in self.users.list()]

    def create_user(self, datos):
        if self.users.get_by_email(datos.email):
            raise ConflictError("Ya existe un usuario con ese email")
        user = self.users.add(User(
            email=datos.email,
            nombre=datos.nombre,
            rol=datos.rol.value,
            password_hash=generate_password_hash(datos.password),
        ))
        try:
            self.users.commit()
        except ConflictError as e:
            raise ConflictError("Ya existe un usuario con ese email") from e
        return UserOut.from_model(user)

    def update_user(self, user_id, datos):
        user = self.users.get(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")

        cambios = datos.model_dump(exclude_unset=True)
        nuevo_rol = cambios['rol'].value if cambios.get('rol') else user.rol
        nuevo_activo = cambios.get('activo', user.activo)

        deja_de_ser_admin_activo = (
            user.rol == Role.ADMIN.value and user.activo
            and (nuevo_rol != Role.ADMIN.value or not nuevo_activo)
        )
        if deja_de_ser_admin_activo and self.users.count_active_admins() <= 1:
            raise ConflictError("Debe quedar al menos un administrador activo")

        if cambios.get('nombre'):
            user.nombre = cambios['nombre']
        user.rol = nuevo_rol
        user.activo = nuevo_activo
        if cambios.get('password'):
            user.password_hash = generate_password_hash(cambios['password'])
            user.intentos_fallidos = 0
            user.bloqueado_hasta = None
        self.users.commit()
        return UserOut.from_model(user)

    def create_admin(self, email, nombre, password):
        return self.create_user(_AdminData(email, nombre, password))


class _AdminData:
    """Datos mínimos para crear un admin desde la CLI, con la misma ruta que la API."""

    def __init__(self, email, nombre, password):
        self.email = email.strip().lower()
        self.nombre = nombre
        self.password = password
        self.rol = Role.ADMIN
