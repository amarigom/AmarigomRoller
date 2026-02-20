import resend
import os

resend.api_key = os.environ.get("RESEND_API_KEY")

def send_resend_email(asunto, mensaje_html):
    try:
        params = {
            "from": "Amarigom <onboarding@resend.dev>", # Al principio usá este de prueba
            "to": ["tu-correo@gmail.com"], # Tu correo donde querés recibir las cotizaciones
            "subject": asunto,
            "html": mensaje_html,
        }
        email = resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Error con Resend: {e}")
        return False