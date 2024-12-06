from core.database import db


class Rol(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship("Users", back_populates="role")
    permissions = db.relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )
