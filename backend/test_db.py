import os
from dotenv import load_dotenv
from neon_api import NeonAPI # O como sea que conectes

load_dotenv()
url = os.getenv("DATABASE_URL")

print(f"🚀 Conectando a: {url.split('@')[1]}") # Solo mostramos el host por seguridad

# Intenta un select simple
# Si no tira error, estás adentro de la base de desarrollo
# Intenta un select simple
# Si no tira error, estás adentro de la base de desarrollo
# Intenta un select simple
# Si no tira error, estás adentro de la base de desarrollo