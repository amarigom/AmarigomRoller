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
- Un corte de perfil sale siempre de una sola pieza (nunca se empalma). Si el perfil de la receta es más corto que el
  ancho, se usa la alternativa más corta que alcance (`insumos_alternativos`; en CSV: ids separados por `|`).
  Si ninguna alcanza, el cálculo responde 422 indicando el largo máximo disponible.

### Herramientas del equipo (admin, pantalla `/gestion/recetas`)

- `GET /api/recipes/products` (productos con versión vigente) y `POST /api/recipes/products`.
- `GET /api/recipes/<pid>/detail?version=N`: ítems completos para editar.
- `POST /api/recipes/preview`: calcula una receta sin guardarla, con medidas y opciones de prueba (valida igual que al publicar).
- `POST /api/recipes/<pid>/duplicate`: copia la receta a un producto nuevo.
- `POST /api/recipes/import` con `{csv, aplicar}`: carga en lote desde CSV (separador `;` o `,`, decimales con coma).
  Con `aplicar: false` solo valida. Es todo o nada. Columnas: `GET /api/recipes/import/template`.
- Regresión de cálculo: casos reales en `tests/regression_cases.json` (los corre `tests/test_regresion_calculo.py`).
  Para sumar un caso se agrega al JSON con el total revisado a mano.

## Inventario, precios y retazos

- `inventario_movimientos` traza aperturas migradas, entradas, ajustes y consumos de producción. `insumos.stock_actual`
  se conserva como saldo actual y se actualiza en la misma transacción que cada movimiento.
- `POST /api/inventory/<id>/movements`: registrar una `entrada` positiva o un `ajuste` con signo; no permite saldo negativo.
  La producción registra consumos con receta, medidas, referencia y usuario.
- `PATCH /api/inventory/<id>/minimum`, `GET /api/inventory/purchase-suggestions`: stock mínimo y faltante sugerido.
- `historial_precios_insumos` conserva el precio inicial y cada cambio. `POST /api/inventory/prices` aplica un porcentaje
  o una lista `[{id_insumo, precio}]`; las calculadoras usan el precio actual.
- `POST /api/inventory/scraps/<id>/reserve` y `/release`: reserva atómica con referencia para evitar que dos pedidos
  asignen el mismo retazo. Usá la misma `referencia` al calcular y producir (`?referencia=...` o en el JSON de producción).
- Al confirmar un corte de rollo se registra el sobrante lateral como retazo si **ancho y largo son mayores a 80 cm**.
  `MIN_RETAZO_TELA_CM` configura ese umbral. El retazo y el consumo de stock se guardan en la misma transacción.

El proyecto todavía no tiene una entidad persistente de pedidos confirmados. Por eso las sugerencias se basan en los mínimos
configurados, no en la demanda futura; la referencia de reserva puede enlazarse a un pedido externo.

## Roles y permisos

Definidos en `security/permissions.py`. Los endpoints piden un permiso, no un rol.

| Permiso | admin | ventas | taller |
|---|:-:|:-:|:-:|
| inventory:read / recipes:read | ✔ | ✔ | ✔ |
| inventory:write | ✔ | | ✔ |
| inventory:manage (mínimos y precios) | ✔ | | |
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
flask --app app db upgrade    # migraciones 0001-0006: índices, usuarios, unidades, recetas e inventario
flask --app app create-admin  # primer administrador
python app.py
```

Base nueva sin esquema: `AUTO_CREATE_TABLES=1` una vez, y luego `flask db upgrade`.

## Tests

```powershell
python -m pytest
```
