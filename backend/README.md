# Backend AmarigomRoller (Flask)

## Estructura

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| Endpoints | `routes/` | Traducen HTTP ⇄ servicios. Sin lógica de negocio. |
| Servicios | `services/` | Reglas de negocio (inventario, clientes, recetas, auth, usuarios, cotización). |
| Repositorios | `repositories/` | Única capa que consulta/persiste con SQLAlchemy. |
| Modelos | `models/` | Tablas (SQLAlchemy). |
| Esquemas | `schemas/` | Validación de entrada y serialización de salida (pydantic). |
| Strategy | `strategies/` | Cálculo por `tipo_calculo` de receta, conversión de unidades, canal de notificación. |
| Factory | `factory.py`, `strategies/notifications.py` | `create_app()` y `create_notifier()`. |
| Seguridad | `security/` | JWT, permisos por rol, decoradores. |
| Composición | `container.py` | Arma los servicios con su configuración. |

Para sumar un tipo de cálculo de receta: subclase de `CalculationStrategy` y `register_strategy(...)`.

## Roles y permisos

Definidos en `security/permissions.py`. Los endpoints piden un permiso, no un rol.

| Permiso | admin | ventas | taller |
|---|:-:|:-:|:-:|
| inventory:read / recipes:read | ✔ | ✔ | ✔ |
| inventory:write | ✔ | | ✔ |
| recipes:produce (confirmar producción: descuenta stock y usa retazos) | ✔ | | ✔ |
| inventory:delete | ✔ | | |
| clients:read / clients:write | ✔ | ✔ | |
| users:manage | ✔ | | |

Login: `POST /api/auth/login` → token Bearer (JWT). `GET /api/auth/me`, `POST /api/auth/change-password`.
Administración de usuarios (solo admin): `GET/POST /api/users`, `PATCH /api/users/<id>`.
Tras `LOGIN_MAX_ATTEMPTS` fallos la cuenta se bloquea `LOGIN_LOCK_MINUTES` (429).

## Puesta en marcha

```powershell
pip install -r requirements-dev.txt
copy .env.example .env        # completar SECRET_KEY y DATABASE_URL
flask --app app db upgrade    # migraciones (0001 índices, 0002 usuarios)
flask --app app create-admin  # primer administrador
python app.py
```

Base nueva sin esquema: `AUTO_CREATE_TABLES=1` una vez, y luego `flask db upgrade`.

## Tests

```powershell
python -m pytest
```
