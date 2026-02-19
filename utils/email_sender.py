from flask import current_app
from flask_mail import Message
from threading import Thread

##def send_async_email(app, msg):
##  """Enviar email de forma asíncrona"""
##  with app.app_context():
##     try:
##        from app import mail
##        mail.send(msg)
##    except Exception as e:
##        current_app.logger.error(f'Error enviando email: {str(e)}')

def send_async_email(app, msg):
    with app.app_context():
        try:
            # En lugar de "from app import mail", usa esto:
            if hasattr(app, 'mail') and app.mail:
                app.mail.send(msg)
            else:
                print("Error: app.mail no está inicializado")
        except Exception as e:
            app.logger.error(f'Error enviando email: {str(e)}')

def send_quote_email(quote_data):
    """
    Envía email con la cotización solicitada.
    
    Args:
        quote_data: dict con email, width, height, fabric_type, color, quality, observations
    
    Returns:
        bool: True si se envió exitosamente, False en caso contrario
    """
    try:
        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER')
        if not sender_email:
            sender_email = 'tu-correo-real@gmail.com' # Remitente de respaldo
        # Email al cliente
        customer_msg = Message(
           subject='Cotización AMARIGOM DECO - Cortinas y Persianas',
           sender=sender_email,
           recipients=[quote_data['email']],
           html=render_customer_email(quote_data)
        )
        
        
        
        # Email a la empresa (copia)
        admin_msg = Message(
            subject=f'Nueva Cotización de {quote_data["email"]}',
            sender=sender_email,
            
            recipients=[current_app.config['CONTACT_EMAIL']],
            html=render_admin_email(quote_data)
        )
        
        # Enviar emails de forma asíncrona
        from app import app, mail
        Thread(target=send_async_email, args=(app, customer_msg)).start()
        Thread(target=send_async_email, args=(app, admin_msg)).start()
        
        return True
        
    except Exception as e:
        current_app.logger.error(f'Error preparando email: {str(e)}')
        return False

def render_customer_email(data):
    """Renderiza el HTML del email para el cliente"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #C9A961 0%, #8B6F47 100%); 
                      color: white; padding: 30px; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .detail {{ margin: 10px 0; padding: 10px; background: white; border-left: 3px solid #C9A961; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>AMARIGOM DECO</h1>
                <p>Cortinas Roller - Blackout - Sunscreen</p>
            </div>
            <div class="content">
                <h2>Gracias por tu consulta</h2>
                <p>Hemos recibido tu solicitud de cotización con los siguientes detalles:</p>
                
                <div class="detail">
                    <strong>Medidas:</strong> {data['width']} cm (ancho) x {data['height']} cm (alto)
                </div>
                <div class="detail">
                    <strong>Tipo de tela:</strong> {data['fabric_type']}
                </div>
                <div class="detail">
                    <strong>Color:</strong> {data['color']}
                </div>
                <div class="detail">
                    <strong>Calidad:</strong> {data['quality']}
                </div>
                <div class="detail">
                    <strong>Observaciones:</strong> {data['observations']}
                </div>
                
                <p style="margin-top: 30px;">
                    Te contactaremos pronto con tu cotización personalizada.
                </p>
                
                <p>
                    <strong>Contacto:</strong><br>
                    WhatsApp: +54 9 2494630750<br>
                    Instagram: @amarigom.deco
                </p>
            </div>
            <div class="footer">
                <p>AMARIGOM DECO - Andrea Marigomez</p>
            </div>
        </div>
    </body>
    </html>
    """

def render_admin_email(data):
    """Renderiza el HTML del email para el administrador"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #0A0A0A; color: #C9A961; padding: 20px; }}
            .content {{ padding: 20px; }}
            .detail {{ margin: 10px 0; padding: 10px; background: #f5f5f5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Nueva Solicitud de Cotización</h2>
            </div>
            <div class="content">
                <div class="detail">
                    <strong>Email del cliente:</strong> {data['email']}
                </div>
                <div class="detail">
                    <strong>Medidas:</strong> {data['width']} x {data['height']} cm
                </div>
                <div class="detail">
                    <strong>Tipo:</strong> {data['fabric_type']}
                </div>
                <div class="detail">
                    <strong>Color:</strong> {data['color']}
                </div>
                <div class="detail">
                    <strong>Calidad:</strong> {data['quality']}
                </div>
                <div class="detail">
                    <strong>Observaciones:</strong> {data['observations']}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
