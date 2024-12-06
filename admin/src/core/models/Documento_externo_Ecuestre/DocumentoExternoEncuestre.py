from core.database import db
from datetime import datetime


class DocumentoExternoEncuestre(db.Model):

    __tablename__ = "documentos_externos_enc"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(400), nullable=False)
    nombre = db.Column(db.String(400), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.now, nullable=False)
    encuestre_id = db.Column(db.Integer, db.ForeignKey("encuestre.id"), nullable=False)
    encuestre = db.relationship("Encuestres")
    esURL = db.Column(db.Boolean(), default=False)
