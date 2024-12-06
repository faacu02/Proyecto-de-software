from core.database import db


class Encuestres(db.Model):

    __tablename__ = "encuestre"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(100), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    pelaje = db.Column(db.String(100), nullable=False)
    comprado = db.Column(db.Boolean(), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    sede_asignada = db.Column(db.String(100), nullable=True)
    entrenadores_conductores = db.relationship("Equipos", back_populates="encuestres")
    entrenadores_conductores_id = db.Column(
        db.Integer, db.ForeignKey("equipo.id"), nullable=True
    )
    tipo_JA = db.Column(db.String(100), nullable=True)
    documentos_externos = db.relationship(
        "DocumentoExternoEncuestre", back_populates="encuestre"
    )
    borrado = db.Column(db.Boolean(), default=False)

    equipos_asociados = db.relationship("EncuestreEquipo", back_populates="encuestre")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nacimiento": (
                self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None
            ),
            "sexo": self.sexo,
            "raza": self.raza,
            "pelaje": self.pelaje,
            "comprado": self.comprado,
            "fecha_ingreso": (
                self.fecha_ingreso.isoformat() if self.fecha_ingreso else None
            ),
            "sede_asignada": self.sede_asignada,
            "tipo_JA": self.tipo_JA,
            "borrado": self.borrado,
        }
