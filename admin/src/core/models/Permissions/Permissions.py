from core.database import db


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roles = db.relationship(
        "Rol", secondary="role_permissions", back_populates="permissions"
    )
