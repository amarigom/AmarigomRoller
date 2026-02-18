from flask import Blueprint, request, jsonify, current_app
from utils.email_sender import send_quote_email

quote_bp = Blueprint('quote', __name__)

@quote_bp.route('/request', methods=['POST'])
def request_quote():
    """
    Procesa solicitud de cotización.
    Si el email está configurado, envía email. Si no, solo guarda los datos.
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['email', 'width', 'height', 'fabric_type']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Preparar datos de cotización
        quote_data = {
            'email': data['email'],
            'width': data['width'],
            'height': data['height'],
            'fabric_type': data['fabric_type'],
            'color': data.get('color', 'No especificado'),
            'quality': data.get('quality', 'Estándar'),
            'observations': data.get('observations', 'Ninguna')
        }
        
        if current_app.config['MAIL_ENABLED']:
            success = send_quote_email(quote_data)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Cotización enviada exitosamente por email'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error al enviar el email'
                }), 500
        else:
            current_app.logger.info(f'Cotización recibida (sin email): {quote_data}')
            return jsonify({
                'success': True,
                'message': f'Cotización recibida. Te contactaremos a {quote_data["email"]} pronto.',
                'data': quote_data
            })
            
    except Exception as e:
        current_app.logger.error(f'Error en cotización: {str(e)}')
        return jsonify({'error': 'Error interno del servidor'}), 500

