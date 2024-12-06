from core.database import db
from datetime import datetime


class Cobros(db.Model):

    __tablename__ = "cobros"

    id = db.Column(db.Integer, primary_key=True)
    JyA = db.relationship("Legajos", back_populates="cobros")
    JyA_ref = db.Column(db.Integer, db.ForeignKey("legajo.id"), nullable=True)
    fecha_pago = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    medio_pago = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.String(100), nullable=False)
    receptor_dinero = db.relationship("Equipos", back_populates="receptor_dinero")
    receptor = db.Column(db.Integer, db.ForeignKey("equipo.id"), nullable=True)
    observaciones = db.Column(db.String(100), nullable=False)
    borrado = db.Column(db.Boolean, nullable=False, default=False)
