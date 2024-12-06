from core.database import db
from datetime import datetime


class Pagos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beneficiario = db.Column(db.String(100), nullable=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    tipo_pago = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    eliminado = db.Column(db.Boolean(), default=False, nullable=False)

    def imprimir_detalles(self):
        detalles = (
            f"ID: {self.id}\n"
            f"Beneficiario: {self.beneficiario}\n"
            f"Monto: {self.monto}\n"
            f"Fecha de Pago: {self.fecha_pago}\n"
            f"Tipo de Pago: {self.tipo_pago}\n"
            f"Descripción: {self.descripcion}"
        )
        return detalles
