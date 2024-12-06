from core.database import db
from core.models.User.User import Users as User
from core.bcrypt import bcrypt
from sqlalchemy import asc, desc
from core.models.Equipo import find_member_by_email
from core.models.Roles.Roles import Rol


def list_users(orden, page=1, per_page=10):
    """
    Lista usuarios activos en el sistema con paginación y ordenación.

    Args:
        orden (bool): Si es True, ordena por `email` en orden descendente;
                      de lo contrario, en orden ascendente.
        page (int, opcional): Número de la página a mostrar. Por defecto es 1.
        per_page (int, opcional): Cantidad de usuarios por página. Por defecto es 10.

    Returns:
        Pagination: Objeto de paginación con la lista de usuarios.
    """
    query = User.query.filter_by(borrado=False)
    if orden:
        query = query.order_by(desc(User.email))
    else:
        query = query.order_by(asc(User.email))
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    return users



def list_users_nopage():
    """
    Lista todos los usuaruarios no eliminados logicamente en la DB

    Returns:
        users : lista de usuarios.
    """

    users = User.query.filter_by(borrado=False).all()
    return users



def create_user(**kwargs):
    """
    Crea un nuevo usuario en la base de datos si el email no está en uso.

    Args:
        **kwargs: Diccionario con los datos del usuario.

    Returns:
        User: El usuario creado si la operación es exitosa.
        None: Si el email ya está asociado a otro usuario o el miembro no existe.
    """
    miembro = find_member_by_email(kwargs["email"])
    another_user = find_user_by_email(kwargs["email"])
    if miembro is None or another_user is not None:
        return None
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs["password"] = hash.decode("utf-8")
    user = User(**kwargs)
    user.miembro = miembro
    db.session.add(user)
    db.session.commit()
    return user


def edit_user(**kwargs):
    """
    Edita los datos de un usuario existente.

    Args:
        **kwargs: Diccionario con los datos del usuario.
                  Debe incluir `old_email`, `email`, `alias`, `activo`, `role_id` y opcionalmente `password`.

    Returns:
        bool: True si la edición fue exitosa, False en caso contrario.
    """
    old_email = kwargs.pop("old_email", None)
    old_user = find_user_by_email(old_email)
    new_user = find_user_by_email(kwargs["email"])
    if not old_user or not new_user:
        return False
    if kwargs["password"] != "":
        hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
        kwargs["password"] = hash.decode("utf-8")
    if old_email != kwargs["email"]:
        old_user.email = kwargs["email"]
        old_user.miembro.email = kwargs["email"]
    old_user.alias = kwargs["alias"]
    old_user.activo = kwargs["activo"]
    old_user.role_id = kwargs["role_id"]
    old_user.password = kwargs["password"]
    db.session.commit()
    return True


def find_user_by_email(email):
    """
    Busca un usuario no borrado por su email.

    Args:
        email (str): Email del usuario a buscar.

    Returns:
        User: Usuario encontrado.
        None: Si no se encuentra un usuario con ese email.
    """
    user = User.query.filter_by(email=email, borrado=False).first()
    return user


def find_user_by_fields(email, orden, orden_by, is_activo, rol, page=1, per_page=10):
    """
    Filtra y ordena usuarios según campos específicos.

    Args:
        email (str): Email parcial para buscar usuarios.
        orden (bool): True para orden descendente, False para ascendente.
        orden_by (str): Campo de ordenación (`mail` o `fecha_creacion`).
        is_activo (bool): Filtrar usuarios activos o bloqueados.
        rol (str): Nombre parcial del rol a buscar.
        page (int, opcional): Número de página. Por defecto es 1.
        per_page (int, opcional): Usuarios por página. Por defecto es 10.

    Returns:
        Pagination: Objeto de paginación con los usuarios encontrados.
    """
    query = User.query.filter_by(borrado=False)
    if email:
        query = query.filter(User.email.like(f"%{email}%"))
    if is_activo:
        query = query.filter_by(activo=is_activo)
    if rol:
        query = query.join(User.role).filter(Rol.name.like(f"%{rol}%"))
    if orden == True:
        if orden_by == "mail":
            query = query.order_by(desc(User.email))
        else:
            query = query.order_by(desc(User.fecha_creacion))
    else:
        if orden_by == "mail":
            query = query.order_by(asc(User.email))
        else:
            query = query.order_by(asc(User.fecha_creacion))
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    return users


def check_user(email, password):
    """
    Verifica las credenciales de un usuario.

    Args:
        email (str): Email del usuario.
        password (str): Contraseña ingresada.

    Returns:
        User: Usuario si las credenciales son correctas.
        None: Si las credenciales son incorrectas o el usuario no existe.
    """
    user = find_user_by_email(email)

    if user and bcrypt.check_password_hash(user.password, password):
        return user

    return None


def get_permisos(mail):
    """
    Obtiene los permisos asociados al rol de un usuario.

    Args:
        mail (str): Email del usuario.

    Returns:
        list: Lista de permisos asociados al rol del usuario.
    """
    user = find_user_by_email(mail)
    permisos = user.role.permissions
    return permisos


def delete_user(email):
    """
    Marca un usuario como borrado.

    Args:
        email (str): Email del usuario a borrar.

    Returns:
        bool: True si la operación fue exitosa, False si el usuario no existe.
    """
    user = find_user_by_email(email)
    if user is None:
        return False
    user.borrado = True
    db.session.commit()
    return True


def es_admin(email):
    """
    Verifica si un usuario tiene el rol SystemAdmin.

    Args:
        email (str): Email del usuario.

    Returns:
        bool: True si el usuario es administrador, False en caso contrario.
    """
    user = find_user_by_email(email)
    if user.role.name == "SystemAdmin":
        return True
    return False
