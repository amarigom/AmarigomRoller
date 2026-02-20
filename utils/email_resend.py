import resend
import os

resend.api_key = os.environ.get("RESEND_API_KEY")

def send_resend_email(asunto, quote_data):
    try:
        cuerpo_html = f"""
        <html>
            <body>
                <h2>Nueva Cotización Recibida</h2>
                <p><strong>Email:</strong> {quote_data.get('email')}</p>
                <p><strong>Medidas:</strong> {quote_data.get('width')} x {quote_data.get('height')}</p>
                <p><strong>Tela:</strong> {quote_data.get('fabric_type')}</p>
                <p><strong>Observaciones:</strong> {quote_data.get('observations', 'Sin observaciones')}</p>
            </body>
        </html>
        """
        params = {
            "from": "Amarigom <onboarding@resend.dev>", # Al principio usá este de prueba
            "to": ["amarigomdeco@gmail.com"], # Tu correo donde querés recibir las cotizaciones
            "subject": asunto,
            "html": mensaje_html,
        }
        resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Error con Resend: {e}")
        return False