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
Publicar una versión cierra la vigente; `fecha=YYYY-MM-DD` o `version=N` seleccionan la receta histórica.
El cálculo usa precios y reglas actuales, por lo que no reproduce necesariamente el presupuesto original.

- `GET /api/recipes/calculation-types`, `GET /api/recipes/<pid>/versions`, `POST /api/recipes/<pid>/versions` (admin).
- Cada ítem admite `formula_ancho`, `formula_alto`, `formula_cantidad` y `condicion`, por ejemplo `ancho > 200`
  o `ceil(ancho/100)`. Variables: `ancho`, `alto` y las opciones del pedido (query params extra en GET, `opciones` en POST).
- Evaluador propio por lista blanca de nodos (`strategies/formulas.py`); nunca usa `eval`.
  Permitido: `+ - * / // %`, comparaciones, `and/or/not`, `a if c else b`, `ceil floor round min max abs`.
- Cada ítem tiene `merma_pct` y `minutos_mano_obra`; el tipo `perfil` calcula piezas de 2/4/6 m con reutilización de sobrantes.
- Para telas configuradas, roller y tradicional usan `lineal_alto`: el alto de corte en metros por el precio
  por metro lineal. La merma aumenta el costo de referencia, pero no el largo físico descontado del rollo.
  El ancho de corte no puede superar el ancho de la tela. Cada corte de tela requiere un ítem con cantidad 1.
  La estrategia `superficie` y el precio por m² se conservan únicamente para recalcular versiones históricas;
  no se pueden publicar recetas nuevas con esa estrategia.
- Si se utiliza un retazo de tela lineal, su costo adicional y el consumo del rollo son cero. Para venderlo como
  tela nueva se informa aparte `cantidad_reposicion` (largo más merma) y `costo_reposicion` (esa cantidad por el
  precio por metro). El retazo se marca usado en su totalidad, incluso si es mayor que el corte.
- Un corte de perfil sale siempre de una sola pieza (nunca se empalma). Si el perfil de la receta es más corto que el
  ancho, se usa la alternativa más corta que alcance (`insumos_alternativos`; en CSV: ids separados por `|`).
  Si ninguna alcanza, el cálculo responde 422 indicando el largo máximo disponible.

### Cotización comercial

- `POST /api/quotes/calculate` requiere permiso `quotes:read` y recibe por ejemplo
  `{"receta_id": 5, "ancho": 150, "alto": 200, "km_obra": 15}`. El ID identifica una versión concreta de receta;
  admite además `referencia` y un objeto `opciones`. Calcula sin descontar stock ni guardar un presupuesto.
- `GET /api/recipes/<pid>/quote?w=150&h=200&km_obra=15` usa el ID de producto, para la calculadora.
  Acepta también `fecha`, `version`, `referencia` y opciones de variantes.
- El markup es fijo: `(costo adicional de fabricación + costo de reposición de retazos lineales) × 2`,
  redondeado a centavos. Es un recargo del 100% sobre la base de referencia, no un margen del 100% sobre ventas.
  Sin retazos equivale a un margen del 50% sobre ventas cuando el costo es positivo; con retazos el margen real
  aumenta, porque se cobran como tela nueva pero tienen costo adicional cero. Se informa también la ganancia bruta
  y el margen sobre ventas (cero cuando el precio es cero). Colocación y traslado van aparte y no reciben markup.
  El traslado considera ida y vuelta; `km_obra` es la distancia de ida no negativa (máximo dos decimales).
  `TARIFA_BASE_COLOCACION` (8000 por defecto) y `COSTO_POR_KM` (450 por defecto) se configuran en el backend.
  La tarifa base se incluye también cuando la distancia es cero.
- Cada cálculo agrega automáticamente una unidad del insumo `Etiqueta` (SKU `ROLLER-ETIQUETA`) a todas las recetas,
  incluidas versiones existentes y vistas previas. No se debe agregar manualmente al editar recetas. Su precio inicial
  es $200 y puede modificarse por inventario. La producción descuenta una unidad; si no hay stock, no se confirma.
- El costo incluye los insumos, la etiqueta, la mano de obra calculada con `COSTO_MINUTO_MANO_OBRA` y
  `COSTO_DESGASTE_MAQUINARIA` ($2000 por cortina por defecto), antes del markup.
  Si el costo por minuto está en cero, la mano de obra no suma costo. No hay rubros separados de servicios,
  impuestos ni otros costos indirectos; la ganancia mostrada no es ganancia neta. Las recetas deben contener solo
  fabricación: el modelo no permite identificar servicios ya cargados como insumos. El cálculo sin guardar puede
  variar si cambian los precios, el stock o las tarifas.
- En la calculadora, «Guardar presupuesto» conserva una instantánea del resultado mostrado, sus precios, medidas,
  receta, referencia y usuario; no descuenta ni reserva stock. El historial muestra los últimos 100 presupuestos.
  El token cifrado vence a la hora: al vencer hay que volver a calcularlo. Los tokens firmados anteriores
  a este cambio dejan de ser válidos y requieren recalcular. La instantánea no cambia si después
  cambian precios o recetas; las recetas históricas consultadas sin guardar sí usan costos actuales.
  Las producciones previamente registradas conservan sus totales y muestran desgaste cero.

### Acceso a costos por rol

- Administración consulta costos, márgenes y precios de venta; crea insumos y gestiona sus precios.
- Ventas consulta precios de venta y presupuestos, pero la API omite costos y márgenes en inventario,
  cálculos e historiales. Puede ver los materiales y cortes.
- Taller consulta materiales y cortes, registra movimientos y confirma producciones sin recibir importes.
  No accede a cotizaciones, presupuestos guardados ni historial de precios. El cálculo interno conserva
  los costos para la trazabilidad administrativa.

La restricción se aplica en el servidor, también a presupuestos y producciones históricos.
El precio de venta puede permitir inferir costos de referencia si se conoce el markup fijo; ocultar
los campos no garantiza confidencialidad matemática. Recargá el panel para revalidar el rol y los permisos
de una sesión abierta antes de estos cambios.

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

### Google Sheets: precios de compra

La integración es opcional; usa la pestaña `PRODUCTOS_INVENTARIO` y busca el encabezado
`Articulo`, `Descripción`, `Unidad Medida`, `Precio Final` en las columnas A a D. La fila anterior
puede contener título y fecha. Los precios deben ser celdas numéricas, no texto con símbolos de moneda.
`Articulo` debe coincidir exactamente con el SKU activo de Roller. Los artículos sin coincidencia se
omiten y se cuenta su cantidad; ningún insumo se crea automáticamente. Es importante revisar esa cantidad
y mantener correctos los SKU. Si no coincide ningún artículo, la sincronización falla.

- `Mt.Lineal` es precio por metro: si el insumo se guarda en centímetros se divide por 100.
- `Unidad` es precio por unidad; para un insumo lineal se interpreta como precio por pieza y se divide por
  su `largo_pieza_cm` configurado. Por ejemplo, $26.289,59 por una barra de 400 cm son $65,7240 por cm
  (redondeo a cuatro decimales). Verificá que el largo registrado coincida con el de la barra del proveedor.
- `Rollo` se acepta directamente cuando el stock también se controla en rollos.
- Para presentaciones como `Juego` o `Paquete`, `unidad_compra` debe coincidir con la unidad de la hoja y
  `factor_conversion` indicar cuántas unidades de stock contiene la presentación; el precio se divide por
  ese factor. Por ejemplo, usar factor 1 si cada unidad de stock representa un paquete completo.
- Las demás unidades, los precios no positivos, SKU repetidos con datos diferentes y los datos incompletos de
  artículos coincidentes bloquean toda la operación. Las filas idénticas se procesan una sola vez. Las telas
  en metros usan directamente el precio por metro. El precio histórico por m² no cambia.
- Los cambios se guardan en una sola transacción con su historial; valores iguales no generan entradas nuevas.
  La hoja prevalece sobre una edición manual en la próxima sincronización. Una falla conserva los precios anteriores.

**Preparación:** habilitar Google Sheets API en Google Cloud, crear una cuenta de servicio y compartir la hoja
privada con el correo de esa cuenta (lector). Configurar `GOOGLE_SHEETS_ID` con el ID del enlace,
`GOOGLE_SHEETS_TAB` con el nombre de la pestaña y `GOOGLE_APPLICATION_CREDENTIALS` con la ruta al archivo JSON
privado de la cuenta de servicio. Alternativamente, usar `GOOGLE_SHEETS_CREDENTIALS_JSON` con el contenido JSON
en una variable segura; si se configuran ambos, se utiliza esa variable. Mantener la credencial fuera del
repositorio y no publicarla. Aplicar primero
`flask --app app db upgrade`; iniciar el backend con las variables configuradas.

Un administrador puede ejecutar «Sincronizar ahora» en Control de stock y costos o correr
`flask --app app sincronizar-precios-sheets`. La calculadora y el inventario muestran la última sincronización
exitosa; se advierte ante un error, falta de configuración o más de 18 horas sin una sincronización exitosa.
Las pantallas consultan el estado cada minuto y la calculadora vuelve a calcular cuando detecta una sincronización
exitosa. Sondeos y ejecuciones pueden demorarse: esto no garantiza actualización instantánea.

**Programación automática:** en el servidor donde se ejecuta el backend, configurar el programador del sistema
para ejecutar `flask --app app sincronizar-precios-sheets` desde el directorio `backend` a las 09:00 y 17:00
en la zona `America/Argentina/Buenos_Aires`, con el entorno virtual y las mismas variables del backend.
Por ejemplo, en un cron que admita `CRON_TZ`, configurar `CRON_TZ=America/Argentina/Buenos_Aires` y la
expresión `0 9,17 * * *`, usando rutas absolutas al directorio y al ejecutable `flask`. No poner credenciales
en el comando ni en archivos compartidos. Revisar los registros del programador: si el proceso no puede arrancar
o conectarse a la base, no puede registrar el error allí; la advertencia por antigüedad permite detectar
ejecuciones ausentes. La programación debe habilitarse en el servidor de despliegue; no se inicia por sí sola.

- `inventario_movimientos` traza aperturas migradas, entradas, ajustes y consumos de producción. `insumos.stock_actual`
  se conserva como saldo actual y se actualiza en la misma transacción que cada movimiento.
- `POST /api/inventory/<id>/movements`: registrar una `entrada` positiva o un `ajuste` con signo; no permite saldo negativo.
  La producción registra consumos con receta, medidas, referencia y usuario.
- Para perfiles de receta, el saldo debe coincidir con la suma de las longitudes de `stock_piezas_detalle` y la
  producción exige una pieza física para cada corte. La entrada de barras se hace con
  `POST /api/inventory/<id>/pieces` y `{"cantidad": 2}`; actualiza saldo, piezas y movimiento en una transacción.
  Los movimientos genéricos se bloquean para perfiles. En inventario, un administrador puede cargar el estado de
  piezas, registrar el conteo real y confirmar una conciliación con motivo obligatorio. Las piezas retiradas se
  conservan con largo cero; la operación guarda el detalle anterior y posterior, el ajuste y el usuario.
  Si el saldo anterior no coincide con la suma de movimientos de la misma unidad, primero registra una regularización
  del historial sin cambiar ese saldo. Si cambió el inventario desde la consulta, hay que volver a cargarlo.
- `GET /api/inventory/<id>/pieces/reconcile` devuelve el saldo y las piezas activas para preparar el conteo.
  `POST` a la misma ruta exige permiso `inventory:manage`, el estado consultado, las piezas contadas y el motivo.
  Para conciliar desde consola, guardar una lista JSON como la siguiente y ejecutar primero la simulación desde `backend`:

  ```json
  [{
    "id_insumo": 7,
    "stock_esperado": "400.0000",
    "piezas_esperadas": [],
    "piezas": [{"id": null, "longitud_original_cm": "400.00", "longitud_actual_cm": "400.00", "es_retazo": false}],
    "motivo": "Conteo físico realizado por operador"
  }]
  ```

  Los valores de `stock_esperado` y `piezas_esperadas` deben copiarse del `GET` actual (`stock` y `piezas`);
  `piezas` debe incluir todas las piezas existentes, usando longitud cero para las retiradas y `id: null` para nuevas.
  `flask --app app conciliar-piezas conteo.json` simula la operación con rollback;
  agregar `--apply` confirma todas las entradas en una única transacción. No adivina el conteo físico.
- Los demás insumos se pueden auditar en Control de stock y costos: seleccionar el insumo, consultar saldo e
  historial, ingresar el conteo físico y un motivo, y confirmar. `GET /api/inventory/<id>/reconcile` devuelve
  `stock`, `historial`, `diferencia` y `unidad`; `POST` requiere permiso `inventory:manage` y recibe
  `stock_esperado`, `historial_esperado`, `stock_contado` y `motivo`. Si el saldo o historial cambió, volver a
  consultar. La regularización del historial y el ajuste por conteo son movimientos separados, con usuario y motivo.
  El historial en cm de telas normalizadas se convierte a metros; unidades incompatibles o mixtas con movimientos
  sin unidad requieren revisión manual. Esto no concilia físicamente retazos ni rollos individuales.
- Las tarjetas de inventario y los cálculos muestran cantidades en metros y precios por metro cuando el insumo se
  registra en cm: dividen la cantidad por 100 y multiplican el precio por 100. No cambian los datos almacenados.
  Los campos de movimientos, mínimos y lista general de precios siguen usando la unidad de registro del insumo;
  los cortes y las piezas de perfiles siguen en cm. El historial de producción conserva las unidades registradas.
- Las telas se configuran con `PATCH /api/inventory/<id>/fabric`, con `ancho_cm`, y opcionalmente
  `largo_pieza_cm`, `unidad_compra` y `factor_conversion`. El stock y `precio_costo_unitario` deben estar en metros
  lineales antes de configurarlas: la migración no convierte valores ni inventa precios. Para comprar un rollo de
  30 m, configurá `unidad_compra: "rollo"` y `factor_conversion: 30`, y registrá la compra con
  `POST /api/inventory/<id>/purchases` y `{"cantidad": 1}`.
- `POST /api/inventory/prices/fabrics/import` recibe `{"csv": "...", "aplicar": false}` para validar antes de aplicar;
  el CSV separado por punto y coma lleva encabezado `id_insumo;precio_metro`, por ejemplo `12;1500,50`.
  La aplicación es atómica. Se acepta la columna histórica opcional `precio_m2`; si se omite se conserva el valor
  previo. Un ajuste porcentual general también modifica los precios históricos por m² configurados.
- `PATCH /api/inventory/<id>/minimum`, `GET /api/inventory/purchase-suggestions`: stock mínimo y faltante sugerido.
- `historial_precios_insumos` conserva el precio inicial y cada cambio. `POST /api/inventory/prices` aplica un porcentaje
  o una lista `[{id_insumo, precio}]`; las calculadoras usan el precio actual.
- `POST /api/inventory/scraps/<id>/reserve` y `/release`: reserva atómica con referencia para evitar que dos pedidos
  asignen el mismo retazo. Usá la misma `referencia` al calcular y producir (`?referencia=...` o en el JSON de producción).
- Al confirmar un corte de rollo se registra el sobrante lateral como retazo si **ancho y largo son mayores a 80 cm**.
  `MIN_RETAZO_TELA_CM` configura ese umbral. El retazo y el consumo de stock se guardan en la misma transacción.
- `GET /api/recipes/productions` consulta el historial de producciones (requiere `recipes:read`); admite `producto_id`,
  `referencia`, `limit` y `offset`. Cada registro conserva una instantánea del producto, receta, medidas, opciones,
  costos, desglose, usuario y fecha. Los consumos de inventario se vinculan al registro de producción.
- El historial empieza con producciones realizadas después de aplicar la migración `0007_historial_producciones`;
  los movimientos anteriores no contienen datos suficientes para reconstruir registros históricos fiables.

El proyecto todavía no tiene una entidad persistente de pedidos confirmados. Por eso las sugerencias se basan en los mínimos
configurados, no en la demanda futura; la referencia de reserva puede enlazarse a un pedido externo.
El stock de tela es un saldo total lineal: no identifica cada rollo individual ni garantiza que un corte largo entre
en un único rollo parcialmente usado. La selección de perfiles en una cotización es orientativa; la disponibilidad
física se verifica al confirmar producción.

### Datos ficticios

Después de aplicar las migraciones, `flask --app app seed-demo-fabricacion` muestra una simulación sin cambios.
`flask --app app seed-demo-fabricacion --apply` agrega, sin borrar datos existentes, una tela con precio por metro,
tres barras físicas y recetas roller y tradicional. Si hace falta, agrega etiquetas ficticias mediante un movimiento.
El comando rechaza una segunda carga con los mismos códigos o productos. No corrige los datos preexistentes.

### Sincronización puntual de la rama de desarrollo

`flask --app app sincronizar-desarrollo` compara el origen configurado en `DEV_DATABASE_URL` con el destino
`DATABASE_URL`, ejecuta la reparación de esquema y la copia en una transacción que luego revierte. No imprime
los usuarios ni las contraseñas. `--apply` confirma la transacción y requiere una copia de seguridad previa.
El procedimiento está limitado al estado y cantidades auditadas: se detiene si cambian las revisiones, hay datos
nuevos en las tablas de destino a copiar, difieren categorías o piezas, o los insumos no corresponden por ID.
Conserva las recetas antiguas del destino y copia los usuarios, insumos, clientes, recetas versionadas,
movimientos, precios y retazos de desarrollo; no corrige discrepancias físicas preexistentes.
Es una operación puntual, no una sincronización continua ni una herramienta genérica para otras bases.
Retirá `DEV_DATABASE_URL` del entorno local cuando ya no la necesites; nunca la compartas ni la subas a Git.

### Normalización inicial de telas y etiqueta

En una copia de la base y después de aplicar las migraciones, ejecutar desde `backend`
`flask --app app preparar-telas-lineales` para simular. Solo con `--apply` confirma todo en una transacción.
Revisa todas las categorías llamadas `Telas`: extrae un único `ancho` del nombre (por ejemplo, `ancho 2.20`
son 220 cm; `ancho 220 cm` son 220 cm). Si es ambiguo o contradice un ancho existente, se detiene.
Para telas aún medidas en cm convierte stock y mínimo dividiendo por 100 y precio por cm multiplicando por 100.
Se marcan como telas con stock por metro; no se inventa el precio por m² ni la unidad de compra.
El historial anterior conserva sus valores y queda marcado en cm; la conversión y el nuevo precio por metro se registran
por separado. Los movimientos de unidades distintas deben convertirse antes de sumarse, no sumarse directamente.

El mismo comando registra la apertura faltante de 100 etiquetas **sin incrementar el saldo**, únicamente si el saldo
es 100 y todos los movimientos previos son cero. Si la situación cambió se detiene; al repetirlo no duplica la apertura. La
simulación no aplica migraciones ni deja datos escritos. El comando también crea versiones lineales nuevas de las
recetas vigentes con tela por superficie y conserva las versiones anteriores. Si una receta no supera las validaciones
o un ítem por superficie no apunta a una tela normalizada, revierte todo y muestra el motivo; corregirlo y repetir.
Requiere supervisión, una copia de seguridad y confirmar que los datos originales estén en cm y precio por cm; no
modifica Neon automáticamente ni reemplaza la conciliación física. `normalizar-inventario-inicial` sigue disponible
para normalizar inventario y etiqueta sin versionar recetas.

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
flask --app app db upgrade    # migraciones: recetas, inventario, producciones, etiqueta y telas
flask --app app create-admin  # primer administrador
python app.py
```

Base nueva sin esquema: `AUTO_CREATE_TABLES=1` una vez, y luego `flask db upgrade`.

## Tests

```powershell
python -m pytest
```
