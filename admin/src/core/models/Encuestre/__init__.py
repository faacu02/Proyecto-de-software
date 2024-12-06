from core.models.Encuestre.Encuestre import Encuestres
from core.database import db
from sqlalchemy import asc, desc


def list_documentos():
    """
    Devuelve todos los registros de ecuestres en la base de datos.

    Returns:
        list: Lista de todos los objetos Encuestres en la base de datos.
    """
    docs = Encuestres.query.all()
    return docs


def list_documentos_dict():
    docs = Encuestres.query.filter_by(borrado=False).all()
    res = [cab.to_dict() for cab in docs]
    return res


def list_encuestres(page=1, per_page=10):
    """
    Devuelve todos los ecuestres que no estén marcados como borrados de manera paginada.

    Args:
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Cantidad de ecuestres por página. Por defecto es 10.

    Returns:
        Pagination: Un objeto de paginación con la lista de ecuestres que no están borrados.
    """
    query = Encuestres.query.filter_by(borrado=False)
    ecuestres = query.paginate(page=page, per_page=per_page, error_out=False)
    return ecuestres


def find_ecuestres_by_fields(nombre, filtro_ja, orden, orden_by, page=1, per_page=10):
    """
    Busca ecuestres en función de varios filtros y los devuelve de manera paginada.

    Args:
        nombre (str): El nombre parcial para filtrar ecuestres.
        filtro_ja (str): El tipo de JA para filtrar ecuestres.
        orden (bool): Determina si el orden es ascendente (True) o descendente (False).
        orden_by (str): El campo por el cual ordenar (FechaNacimiento, FechaIngreso, o nombre).
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Cantidad de ecuestres por página. Por defecto es 10.

    Returns:
        Pagination: Un objeto de paginación con la lista de ecuestres filtrados y ordenados.
    """
    query = Encuestres.query.filter_by(borrado=False)
    if nombre:
        query = query.filter(Encuestres.nombre.ilike(f"{nombre}%"))
    if filtro_ja:
        query = query.filter_by(tipo_JA=filtro_ja)
    if not orden:
        if orden_by == "FechaNacimiento":
            query = query.order_by(desc(Encuestres.fecha_nacimiento))
        elif orden_by == "FechaIngreso":
            query = query.order_by(desc(Encuestres.fecha_ingreso))
        else:
            query = query.order_by(desc(Encuestres.nombre))
    else:
        if orden_by == "FechaNacimiento":
            query = query.order_by(asc(Encuestres.fecha_nacimiento))
        elif orden_by == "FechaIngreso":
            query = query.order_by(asc(Encuestres.fecha_ingreso))
        else:
            query = query.order_by(asc(Encuestres.nombre))
    ecuestres = query.paginate(page=page, per_page=per_page, error_out=False)
    return ecuestres


def create_doc(**kwargs):
    """
    Crea un nuevo documento ecuestre en la base de datos.

    Args:
        **kwargs: Los argumentos necesarios para crear el ecuestre, como campos clave-valor.

    Returns:
        Encuestres: El objeto Encuestres recién creado y guardado en la base de datos.
    """
    doc = Encuestres(**kwargs)
    db.session.add(doc)
    db.session.commit()
    return doc


def modificar_ecuestre(id, **kwargs):
    """
    Modifica un ecuestre existente en la base de datos.

    Busca el ecuestre por su ID y, si existe, actualiza sus campos con los valores proporcionados.

    Args:
        id (int): El ID del ecuestre a modificar.
        **kwargs: Los nuevos valores de los campos a actualizar, como clave-valor.

    Returns:
        Encuestres: El objeto Encuestres actualizado si se encuentra, de lo contrario, None.
    """
    ecuestre = get_Ecuestre_by_id(id)
    if ecuestre:
        for key, value in kwargs.items():
            setattr(ecuestre, key, value)  # Actualiza los atributos dinámicamente
        db.session.commit()
        return ecuestre
    return None  # O lanzar un error si el ecuestre no existe


def get_Ecuestre_by_id(id):
    """
    Busca un ecuestre por su ID.

    Args:
        id (int): El ID del ecuestre a buscar.

    Returns:
        Encuestres: El objeto Encuestres si se encuentra, de lo contrario, None.
    """
    ecuestre = Encuestres.query.filter_by(id=id).first()
    return ecuestre


def delete_Ecuestre(id):
    """
    Realiza un borrado lógico de un ecuestre por su ID, marcándolo como borrado.

    Args:
        id (int): El ID del ecuestre que se desea borrar.

    Returns:
        Encuestres: El objeto Encuestres con la marca de borrado aplicada si se encuentra,
        de lo contrario, None.
    """
    member = get_Ecuestre_by_id(id)
    if member:
        member.borrado = True
        db.session.commit()
        return member
    return None
