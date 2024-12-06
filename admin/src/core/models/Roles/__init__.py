from core.database import db
from core.models.Roles.Roles import Rol


def create_rol(**kwargs):
    rol = Rol(**kwargs)
    db.session.add(rol)
    db.session.commit()

    return rol


def list_roles():
    all_roles = Rol.query.filter(Rol.name != "SystemAdmin").all()
    return all_roles


def get_rol_by_id(id):
    rol = Rol.query.get(id)
    return rol
