from core.database import db
from datetime import datetime


class DocumentoExterno(db.Model):

    __tablename__ = "documentos_externos"

    id = db.Column(db.Integer, primary_key=True)
    legajo_id = db.Column(db.Integer, db.ForeignKey("legajo.id"), nullable=False)
    titulo = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.now, nullable=False)
    legajo = db.relationship("Legajos", back_populates="documentos_externos")
    eliminado = db.Column(db.Boolean(), default=False, nullable=False)
    es_enlace = db.Column(db.Boolean(), default=False, nullable=False)
