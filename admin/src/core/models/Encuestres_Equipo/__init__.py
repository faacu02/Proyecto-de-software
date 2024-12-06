from core.models.Encuestres_Equipo.Encuestres_Equipo import EncuestreEquipo
from core.database import db


def list_relaciones():
    """
    Devuelve todas las relaciones entre encuestres y equipos.

    Returns:
        list: Lista de todos los objetos EncuestreEquipo en la base de datos.
    """
    relaciones = EncuestreEquipo.query.all()
    return relaciones


def create_relacion(encuestre_id, equipo_id):
    """
    Crea una nueva relación entre un encuestre y un equipo.

    Args:
        encuestre_id (int): El ID del encuestre a asociar.
        equipo_id (int): El ID del equipo a asociar.

    Returns:
        EncuestreEquipo: El objeto EncuestreEquipo recién creado y guardado en la base de datos.
    """
    relacion = EncuestreEquipo(encuestre_id=encuestre_id, equipo_id=equipo_id)
    db.session.add(relacion)
    db.session.commit()
    return relacion


def actualizar_relaciones(encuestre_id, nuevos_ids):
    """
    Actualiza las relaciones de un encuestre con equipos.

    Elimina todas las relaciones existentes para un encuestre específico y crea nuevas
    relaciones basadas en los IDs de equipos proporcionados.

    Args:
        encuestre_id (int): El ID del encuestre cuyas relaciones se van a actualizar.
        nuevos_ids (list): Una lista de IDs de equipos que se deben asociar con el encuestre.
    """
    # Eliminar las relaciones existentes
    db.session.query(EncuestreEquipo).filter_by(encuestre_id=encuestre_id).delete()

    # Crear nuevas relaciones
    for equipo_id in nuevos_ids:
        create_relacion(encuestre_id, equipo_id)

    db.session.commit()


def get_equipos_asociados(encuestre_id):
    """
    Devuelve todas las relaciones de equipos asociados a un encuestre específico.

    Args:
        encuestre_id (int): El ID del encuestre.

    Returns:
        list: Lista de objetos EncuestreEquipo asociados al encuestre.
    """
    return db.session.query(EncuestreEquipo).filter_by(encuestre_id=encuestre_id).all()


def get_ids_equipos_asociados(encuestre_id):
    """
    Devuelve una lista de IDs de equipos asociados a un encuestre específico.

    Args:
        encuestre_id (int): El ID del encuestre.

    Returns:
        list: Lista de IDs de equipos asociados al encuestre.
    """
    return [equipo.equipo_id for equipo in get_equipos_asociados(encuestre_id)]
