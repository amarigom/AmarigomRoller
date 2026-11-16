from html import escape

from schemas.quote import PresupuestoIn


class QuoteService:
    def __init__(self, notifier, recipient):
        self.notifier = notifier
        self.recipient = recipient

    def request_quote(self, datos: PresupuestoIn):
        e = lambda v: escape(str(v))  # los datos vienen de un formulario público
        html = f"""
            <h3>Nueva solicitud de presupuesto</h3>
            <p><strong>Email del Cliente:</strong> {e(datos.email)}</p>
            <hr>
            <p><strong>Detalles del Producto:</strong></p>
            <ul>
                <li><strong>Tela:</strong> {e(datos.fabric_type.capitalize())}</li>
                <li><strong>Calidad:</strong> {e(datos.quality.capitalize())}</li>
                <li><strong>Color:</strong> {e(datos.color)}</li>
                <li><strong>Medidas:</strong> {e(datos.width)}cm x {e(datos.height)}cm</li>
            </ul>
            <p><strong>Observaciones:</strong> {e(datos.observations)}</p>
            <br>
            <p>---<br>Sistema Amarigo Deco</p>
        """
        asunto = f"NUEVA COTIZACIÓN: {datos.fabric_type[:50]} - Amarigo Deco"
        self.notifier.send(asunto, html, self.recipient)
