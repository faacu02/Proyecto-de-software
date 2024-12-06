from core.database import db


class Pendientes(db.Model):
    email = db.Column(db.String(100), nullable=False, primary_key=True, unique=True)
    alias = db.Column(db.String(100), nullable=False)
