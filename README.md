# AMARIGOM DECO - Flask Web Application

Aplicación web modular y escalable en Python Flask para venta de cortinas roller (sunscreen y blackout) y cortinas tradicionales.

## 📁 Estructura del Proyecto

\`\`\`
├── app.py                  # Aplicación principal Flask
├── config.py              # Configuración y variables de entorno
├── requirements.txt       # Dependencias Python
├── .env.example          # Ejemplo de variables de entorno
├── .gitignore            # Archivos ignorados por Git
│
├── routes/               # Blueprints (rutas modulares)
│   ├── __init__.py
│   ├── main.py          # Rutas principales (home, idioma)
│   ├── products.py      # API de productos
│   ├── quote.py         # Sistema de cotizaciones
│   └── cart.py          # Carrito de compras
│
├── templates/            # Templates HTML (Jinja2)
│   ├── base.html        # Template base con header/footer
│   └── index.html       # Página principal
│
├── static/              # Archivos estáticos
│   ├── css/
│   │   └── style.css    # Estilos principales
│   ├── js/
│   │   └── main.js      # JavaScript del cliente
│   └── images/          # Imágenes del sitio
│       ├── hero-bg.jpg
│       ├── products/    # Imágenes de productos
│       │   ├── sunscreen.jpg
│       │   ├── blackout.jpg
│       │   └── traditional.jpg
│       ├── gallery/     # Galería de instalaciones
│       │   ├── img1.jpg
│       │   ├── img2.jpg
│       │   └── ...
│       └── uploads/     # Imágenes subidas por usuarios
│
└── utils/               # Utilidades y helpers
    ├── __init__.py
    ├── translations.py  # Sistema de traducciones ES/EN
    └── email_sender.py  # Envío de emails para cotizaciones
\`\`\`

## 🎨 Paleta de Colores

Diseño elegante inspirado en Jean-François Bury:

- **Background Primary**: `#0A0A0A` - Negro profundo
- **Background Secondary**: `#1A1A1A` - Gris oscuro
- **Accent Gold**: `#C9A961` - Dorado elegante
- **Accent Bronze**: `#8B6F47` - Bronce cálido
- **Text Primary**: `#F5F1E8` - Blanco cálido
- **Text Secondary**: `#C9C5BC` - Gris claro

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

\`\`\`bash
git clone <tu-repositorio>
cd amarigom-deco
\`\`\`

### 2. Crear entorno virtual

\`\`\`bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
\`\`\`

### 3. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configurar variables de entorno MÍNIMAS

Copia `.env.example` a `.env`:

\`\`\`bash
cp .env.example .env
\`\`\`

Edita `.env` con estas 4 variables ESENCIALES:

\`\`\`env
SECRET_KEY=mi-clave-super-secreta-12345
CONTACT_EMAIL=tu-email@gmail.com
WHATSAPP_NUMBER=5492494630750
INSTAGRAM_URL=https://instagram.com/tu_perfil
\`\`\`

**¡Eso es todo!** Con estas 4 variables el sitio funcionará perfectamente.

### 5. Ejecutar la aplicación

\`\`\`bash
python app.py
\`\`\`

La aplicación estará disponible en `http://localhost:5000`

## 📧 Configuración de Email (OPCIONAL)

Si quieres que las cotizaciones se envíen automáticamente por email, agrega estas variables adicionales a tu `.env`:

\`\`\`env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-app
MAIL_DEFAULT_SENDER=noreply@amarigom.com
\`\`\`

**Para Gmail**: Necesitas crear una "Contraseña de aplicación":
1. Ve a tu cuenta de Google → Seguridad
2. Activa la verificación en dos pasos
3. Genera una contraseña de aplicación
4. Usa esa contraseña en `MAIL_PASSWORD`

**Sin email configurado**: Las cotizaciones se guardarán en los logs y el usuario verá un mensaje de confirmación. Podrás agregar el email más adelante cuando lo necesites.

## 🌐 Características

- ✅ **Modular**: Blueprints organizados por funcionalidad
- ✅ **Bilingüe**: Soporte completo para Español e Inglés
- ✅ **Carrito de Compras**: Sistema funcional con sesiones
- ✅ **Cotizaciones por Email**: Envío automático al cliente y negocio
- ✅ **Responsive**: Diseño adaptable a todos los dispositivos
- ✅ **Productos Promocionales**: Sistema de ofertas especiales
- ✅ **Galería con Carrusel**: Muestra instalaciones reales
- ✅ **Escalable**: Fácil de extender con base de datos

## 📝 Cómo Agregar Nuevas Imágenes

1. Coloca tus imágenes en `/static/images/`
   - Productos: `/static/images/products/`
   - Galería: `/static/images/gallery/`
   - Otros: `/static/images/`

2. Referencia las imágenes en templates usando:

\`\`\`html
<img src="{{ url_for('static', filename='images/products/mi-imagen.jpg') }}" alt="...">
\`\`\`

## 🛍️ Cómo Agregar Nuevos Productos

Edita `/routes/products.py` y agrega al array `PRODUCTS`:

\`\`\`python
PRODUCTS = [
    # ... productos existentes
    {
        'id': 4,
        'name_es': 'Nuevo Producto',
        'name_en': 'New Product',
        'description_es': 'Descripción en español',
        'description_en': 'Description in English',
        'image': '/static/images/products/nuevo.jpg',
        'category': 'sunscreen',  # o 'blackout', 'traditional', 'promo'
        'price': 20000
    }
]
\`\`\`

Para productos promocionales, agrega:

\`\`\`python
{
    'id': 103,
    'name_es': 'Oferta Especial',
    'name_en': 'Special Offer',
    'description_es': 'Descripción de la oferta',
    'description_en': 'Offer description',
    'image': '/static/images/products/oferta.jpg',
    'category': 'promo',
    'price': 15000,
    'original_price': 20000,
    'discount': 25  # porcentaje de descuento
}
\`\`\`

## 🌐 Cómo Agregar Traducciones

Edita `/utils/translations.py` y agrega nuevas claves:

\`\`\`python
TRANSLATIONS = {
    'es': {
        # ... traducciones existentes
        'nueva_clave': 'Texto en español',
    },
    'en': {
        # ... traducciones existentes
        'nueva_clave': 'Text in English',
    }
}
\`\`\`

Usa en templates:

\`\`\`html
{{ translations[lang]['nueva_clave'] }}
\`\`\`

## 📧 Sistema de Cotizaciones

El formulario de cotización funciona de dos maneras:

**Con email configurado**: Envía automáticamente dos emails:
1. **Al cliente**: Confirmación con detalles de su solicitud
2. **Al negocio**: Notificación de nueva cotización

**Sin email configurado**: Guarda la cotización en los logs y muestra un mensaje de confirmación al usuario. Los datos quedan registrados para que puedas contactar al cliente manualmente.

Los templates de email están en `/utils/email_sender.py` y pueden personalizarse.

## 🛒 Sistema de Carrito

El carrito usa sesiones de Flask para almacenar items. Endpoints disponibles:

- `POST /cart/add` - Agregar producto
- `GET /cart/get` - Obtener contenido del carrito
- `DELETE /cart/remove/<id>` - Eliminar producto
- `POST /cart/clear` - Vaciar carrito

## 🔧 Personalización

### Cambiar colores

Edita las variables CSS en `/static/css/style.css`:

\`\`\`css
:root {
  --color-bg-primary: #0a0a0a;
  --color-accent-gold: #c9a961;
  /* ... otras variables */
}
\`\`\`

### Cambiar tipografía

Edita los imports de Google Fonts en `/templates/base.html`:

\`\`\`html
<link href="https://fonts.googleapis.com/css2?family=Tu+Fuente&display=swap" rel="stylesheet">
\`\`\`

Y actualiza el CSS:

\`\`\`css
body {
  font-family: "Tu Fuente", sans-serif;
}
\`\`\`

## 📱 Contacto

- **WhatsApp**: +54 9 2494630750
- **Instagram**: @amarigom.deco
- **Email**: andrea.marigomez@amarigom.com

## 🚀 Próximas Mejoras

### Base de Datos
Actualmente los productos están en memoria. Para producción, considera:

\`\`\`python
# Instalar SQLAlchemy
pip install flask-sqlalchemy

# Crear modelo de producto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(100))
    price = db.Column(db.Float)
    # ... otros campos
\`\`\`

### Sistema de Pagos
Integrar Stripe o MercadoPago:

\`\`\`python
pip install stripe
# o
pip install mercadopago
\`\`\`

### Panel de Administración
Agregar Flask-Admin para gestionar productos:

\`\`\`python
pip install flask-admin
\`\`\`

### Autenticación de Usuarios
Implementar registro y login:

\`\`\`python
pip install flask-login flask-bcrypt
\`\`\`

## 📄 Licencia

© 2025 AMARIGOM DECO - Andrea Marigomez. Todos los derechos reservados.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:
1. Revisa la documentación
2. Verifica las variables de entorno
3. Contacta al desarrollador

