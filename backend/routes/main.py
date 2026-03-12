from flask import Blueprint, session, request, jsonify, current_app
from utils.translations import get_translations
import resend  # Asegúrate de tener 'resend' en requirements.txt
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal con traducciones"""
    lang = session.get('language', 'es')
    translations = get_translations()
    return jsonify({
        "status": "ok",
        "message": "Cerebro de Python conectado",
        "translations": translations[lang]
    })

@main_bp.route('/set-language/<lang>')
def set_language(lang):
    """Cambiar idioma de la aplicación"""
    if lang in ['es', 'en']:
        session['language'] = lang
        session.modified = True
    return jsonify({'success': True, 'language': lang}), 200

@main_bp.route('/api/presupuesto', methods=['POST'])
def recibir_presupuesto():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # 1. Configurar Resend
        resend.api_key = os.environ.get("RESEND_API_KEY")
        
        # 2. Extraer datos
        email_cliente = data.get('email')
        ancho = data.get('width')
        alto = data.get('height')
        tipo_tela = data.get('fabric_type', 'No especificada')
        calidad = data.get('quality', 'Estándar')
        color = data.get('color', 'No especificado')
        observaciones = data.get('observations', 'Sin observaciones')

        print(f"SOLICITUD RECIBIDA: {email_cliente} - {tipo_tela}")

        # 3. Envío con Resend
        try:
            params = {
                "from": os.environ.get("MAIL_DEFAULT_SENDER", "onboarding@resend.dev"),
                "to": os.environ.get("MAIL_USERNAME"), 
                "subject": f"NUEVA COTIZACIÓN: {tipo_tela} - Amarigo Deco",
                "html": f"""
                    <h3>Nueva solicitud de presupuesto</h3>
                    <p><strong>Email del Cliente:</strong> {email_cliente}</p>
                    <hr>
                    <p><strong>Detalles del Producto:</strong></p>
                    <ul>
                        <li><strong>Tela:</strong> {tipo_tela.capitalize()}</li>
                        <li><strong>Calidad:</strong> {calidad.capitalize()}</li>
                        <li><strong>Color:</strong> {color}</li>
                        <li><strong>Medidas:</strong> {ancho}cm x {alto}cm</li>
                    </ul>
                    <p><strong>Observaciones:</strong> {observaciones}</p>
                    <br>
                    <p>---<br>Sistema Amarigo Deco</p>
                """
            }
            resend.Emails.send(params)
            print("Email enviado con éxito vía Resend")
        except Exception as e:
            print(f"Error al enviar con Resend: {e}")

        return jsonify({
            "status": "success",
            "message": "¡Solicitud enviada! Nos contactaremos pronto."
        }), 200

    except Exception as e:
        print(f"Error crítico: {e}")
        return jsonify({"status": "error", "message": "Error interno"}), 500