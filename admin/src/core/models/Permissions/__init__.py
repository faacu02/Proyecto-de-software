from core.database import db
from core.models.Permissions.Permissions import Permission


def create_permisos(**kwargs):
    permiso = Permission(**kwargs)
    db.session.add(permiso)
    db.session.commit()

    return permiso
