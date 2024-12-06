from core.database import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Rol", back_populates="users")
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    miembro_id = db.Column(db.Integer, db.ForeignKey("equipo.id"))
    miembro = db.relationship("Equipos", back_populates="usuario")
    borrado = db.Column(db.Boolean(), default=False)
    creador_pub = db.relationship("Articulos", back_populates="creador_pub")
