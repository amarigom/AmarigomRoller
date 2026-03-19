from flask_sqlalchemy import SQLAlchemy

# Agregamos engine_options para que SQLAlchemy verifique la conexión antes de usarla
db = SQLAlchemy(engine_options={
    "pool_pre_ping": True,
    "pool_recycle": 300,
})


# Importamos los modelos para que estén disponibles en toda la app
from .insumo import Insumo, CategoriaInsumo