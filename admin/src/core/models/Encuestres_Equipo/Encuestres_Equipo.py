from core.database import db


class EncuestreEquipo(db.Model):
    __tablename__ = "encuestre_equipo"

    encuestre_id = db.Column(
        db.Integer, db.ForeignKey("encuestre.id"), primary_key=True
    )
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipo.id"), primary_key=True)

    encuestre = db.relationship("Encuestres", back_populates="equipos_asociados")
    equipo = db.relationship("Equipos", back_populates="encuestres_asociados")
