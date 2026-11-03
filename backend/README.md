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

## Recetas versionadas

`productos` (lo que se vende) → `recetas` (versión con `vigente_desde`/`vigente_hasta`) → `receta_items`.
Publicar una versión cierra la vigente, así los cálculos con `fecha=YYYY-MM-DD` o `version=N` no cambian.

- `GET /api/recipes/calculation-types`, `GET /api/recipes/<pid>/versions`, `POST /api/recipes/<pid>/versions` (admin).
- Cada ítem admite `formula_ancho`, `formula_alto`, `formula_cantidad` y `condicion`, por ejemplo `ancho > 200`
  o `ceil(ancho/100)`. Variables: `ancho`, `alto` y las opciones del pedido (query params extra en GET, `opciones` en POST).
- Evaluador propio por lista blanca de nodos (`strategies/formulas.py`); nunca usa `eval`.
  Permitido: `+ - * / // %`, comparaciones, `and/or/not`, `a if c else b`, `ceil floor round min max abs`.
- Cada ítem tiene `merma_pct` y `minutos_mano_obra`; el tipo `perfil` calcula piezas de 2/4/6 m con reutilización de sobrantes.

## Roles y permisos

Definidos en `security/permissions.py`. Los endpoints piden un permiso, no un rol.

| Permiso | admin | ventas | taller |
|---|:-:|:-:|:-:|
| inventory:read / recipes:read | ✔ | ✔ | ✔ |
| inventory:write | ✔ | | ✔ |
| recipes:produce (confirmar producción: descuenta stock y usa retazos) | ✔ | | ✔ |
| recipes:write (publicar versiones de receta) | ✔ | | |
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
flask --app app db upgrade    # migraciones (0001 índices, 0002 usuarios, 0003 unidades/perfiles, 0004 recetas versionadas)
flask --app app create-admin  # primer administrador
python app.py
```

Base nueva sin esquema: `AUTO_CREATE_TABLES=1` una vez, y luego `flask db upgrade`.

## Tests

```powershell
python -m pytest
```
