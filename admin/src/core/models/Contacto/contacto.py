from core.database import db
from datetime import datetime

class Contacto(db.Model):
    __tablename__ = "contacto"
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cuerpo_mensaje = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(100), default='Pendiente' ,nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    comentario = db.Column(db.String(100), default= 'Sin comentario', nullable=False)
    borrado = db.Column(db.Boolean, default=False, nullable=False)