from core.models.Contacto.contacto import Contacto
from core.database import db
from sqlalchemy import asc, desc


def get_contacto(id):
    """
    Obtiene un contacto por su ID.

    :param id: ID del contacto.
    :return: El contacto si existe y no está borrado, de lo contrario None.
    """
    contacto = Contacto.query.filter_by(id=id, borrado=False).first()
    return contacto


def list_contactos(orden, estado_p, pagina, per_page):
    """
    Lista los contactos con paginación y filtrado por estado y orden.

    :param orden: Orden de los contactos ('asc' o 'desc').
    :param estado_p: Estado del contacto para filtrar.
    :param pagina: Número de la página.
    :param per_page: Cantidad de contactos por página.
    :return: Contactos paginados.
    """
    query = Contacto.query.filter_by(borrado=False)
    if estado_p:
        query = query.filter(Contacto.estado == estado_p)
    if orden == "asc":
        query = query.order_by(asc(Contacto.fecha_creacion))
    else:
        query = query.order_by(desc(Contacto.fecha_creacion))

    contactos = query.paginate(page=pagina, per_page=per_page, error_out=False)
    return contactos


def delete_contacto(id):
    """
    Marca un contacto como borrado.

    :param id: ID del contacto.
    :return: El contacto si se marcó como borrado, de lo contrario None.
    """
    contacto = get_contacto(id)
    if contacto:
        contacto.borrado = True
        db.session.commit()
        return contacto
    return None


def create_contacto(nombre, apellido, email, cuerpo_mensaje, fecha_creacion, estado='Pendiente', comentario='Sin comentario', borrado=False):
    """
    Crea un nuevo contacto.

    :param nombre: Nombre del contacto.
    :param apellido: Apellido del contacto.
    :param email: Email del contacto.
    :param cuerpo_mensaje: Cuerpo del mensaje del contacto.
    :param fecha_creacion: Fecha de creación del contacto.
    :param estado: Estado del contacto (por defecto 'Pendiente').
    :param comentario: Comentario del contacto (por defecto 'Sin comentario').
    :param borrado: Estado de borrado del contacto (por defecto False).
    :return: El nuevo contacto creado.
    """
    nuevo_contacto = Contacto(
        nombre=nombre,
        apellido=apellido,
        email=email,
        cuerpo_mensaje=cuerpo_mensaje,
        estado=estado,
        fecha_creacion=fecha_creacion,
        comentario=comentario,
        borrado=borrado
    )
    db.session.add(nuevo_contacto)
    db.session.commit()
    return nuevo_contacto


def update_contacto(contacto, estado, comentario):
    """
    Actualiza el estado y comentario de un contacto.

    :param contacto: El contacto a actualizar.
    :param estado: Nuevo estado del contacto.
    :param comentario: Nuevo comentario del contacto.
    """
    contacto.estado = estado
    contacto.comentario = comentario
    db.session.commit()