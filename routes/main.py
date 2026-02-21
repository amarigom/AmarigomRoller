from flask import Blueprint, render_template, session, request,jsonify
from utils.translations import get_translations
from flask import request, jsonify, current_app
from flask_mail import Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal con hero, productos y galería"""
    lang = session.get('language', 'es')
    translations = get_translations()
    return jsonify({
        "status": "ok",
        "message": "Cerebro de Python conectado",
        "translations": translations[lang]
    })
@main_bp.route('/set-language/<lang>')
def set_language(lang):
    """Cambiar idioma de la aplicacion"""
    if lang in ['es', 'en']:
        session['language'] = lang
        session.modified = True
    from flask import jsonify
    return jsonify({'success': True, 'language': lang}), 200



@main_bp.route('/api/presupuesto', methods=['POST'])
def recibir_presupuesto():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # 1. Extraemos los datos con los nombres exactos de tu formulario Next.js
        email_cliente = data.get('email')
        ancho = data.get('width')
        alto = data.get('height')
        tipo_tela = data.get('fabric_type', 'No especificada')
        calidad = data.get('quality', 'Estándar')
        color = data.get('color', 'No especificado')
        observaciones = data.get('observations', 'Sin observaciones')
        
        # El nombre no estaba en tu objeto simplificado, pero si lo agregas:
        nombre_cliente = data.get('nombre', 'Cliente Interesado')

        # 2. Log en consola para control
        print(f"✨ SOLICITUD RECIBIDA: {email_cliente} - {tipo_tela} ({calidad}) {ancho}x{alto}")

        # 3. Lógica de Envío de Email
        if current_app.mail:  # Verificamos si Mail está configurado
            try:
                msg = Message(
                    subject=f"NUEVA COTIZACIÓN: {tipo_tela} - Amarigo Deco",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[current_app.config['MAIL_USERNAME']] # Te lo mandas a ti mismo
                )
                
                msg.body = f"""
                Has recibido una nueva solicitud de presupuesto desde la web:
                
                DATOS DEL CLIENTE:
                ------------------
                Email: {email_cliente}
                
                DETALLES DEL PRODUCTO:
                ---------------------
                Tipo de Tela: {tipo_tela.capitalize()}
                Calidad: {calidad.capitalize()}
                Color: {color}
                Medidas: Ancho {ancho}cm x Alto {alto}cm
                
                OBSERVACIONES:
                --------------
                {observaciones}
                
                ---
                Sistema de Cotizaciones Amarigo Deco
                """
                
                current_app.mail.send(msg)
                print("Email enviado con éxito.")
                
            except Exception as e:
                print(f" Error al enviar email: {e}")
                # No detenemos el proceso si el mail falla, para no frustrar al cliente
        else:
            print("AVISO: Email no enviado (MAIL_ENABLED es False)")

        # 4. Respuesta de éxito para Next.js
        return jsonify({
            "status": "success",
            "message": "¡Solicitud enviada! Nos contactaremos pronto."
        }), 200

    except Exception as e:
        print(f"Error crítico en el servidor: {e}")
        return jsonify({
            "status": "error", 
            "message": "Error interno al procesar la solicitud"
        }), 500