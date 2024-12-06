from core.database import db
from datetime import datetime


class Equipos(db.Model):

    __tablename__ = "equipo"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(50), nullable=False)
    domicilio = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    profesion = db.Column(db.String(100), nullable=False)
    puesto_laboral = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=False)
    contacto_emergencia_nombre = db.Column(db.String(100), nullable=False)
    contacto_emergencia_telefono = db.Column(db.String(100), nullable=False)
    obra_social = db.Column(db.String(100), nullable=False)
    num_afiliado = db.Column(db.Integer, nullable=False)
    condicion = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    titulo = db.Column(db.String(100), nullable=True)
    copia_dni = db.Column(db.String(100), nullable=True)
    cv_actualizado = db.Column(db.String(100), nullable=True)
    receptor_dinero = db.relationship("Cobros", back_populates="receptor_dinero")
    encuestres = db.relationship(
        "Encuestres", back_populates="entrenadores_conductores"
    )
    borrado = db.Column(db.Boolean, nullable=False, default=False)
    usuario = db.relationship("Users", back_populates="miembro", uselist=False)

    encuestres_asociados = db.relationship("EncuestreEquipo", back_populates="equipo")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "domicilio": self.domicilio,
            "email": self.email,
            "localidad": self.localidad,
            "telefono": self.telefono,
            "profesion": self.profesion,
            "puesto_laboral": self.puesto_laboral,
            "fecha_inicio": (
                self.fecha_inicio.strftime("%Y-%m-%d") if self.fecha_inicio else None
            ),  # Formato YYYY-MM-DD
            "fecha_cese": (
                self.fecha_cese.strftime("%Y-%m-%d") if self.fecha_cese else None
            ),
            "contacto_emergencia_nombre": self.contacto_emergencia_nombre,
            "contacto_emergencia_telefono": self.contacto_emergencia_telefono,
            "obra_social": self.obra_social,
            "num_afiliado": self.num_afiliado,
            "condicion": self.condicion,
            "activo": self.activo,
            "titulo": self.titulo,
            "copia_dni": self.copia_dni,
            "cv_actualizado": self.cv_actualizado,
            "borrado": self.borrado,
        }
