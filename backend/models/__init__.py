from flask_sqlalchemy import SQLAlchemy

# Agregamos engine_options para que SQLAlchemy verifique la conexión antes de usarla
db = SQLAlchemy(engine_options={
    "pool_pre_ping": True,
    "pool_recycle": 300,
})
from .supply import Supply
from .supply_category import SupplyCategory
from .recipe_bom import RecipeBOM