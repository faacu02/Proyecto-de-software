from core.models.Documento_externo_Ecuestre.DocumentoExternoEncuestre import (
    DocumentoExternoEncuestre,
)
from core.database import db
from sqlalchemy import asc, desc


def list_documentos():
    """
    Devuelve todos los documentos externos de los ecuestres almacenados en la base de datos.

    Returns:
        list: Lista de todos los objetos DocumentoExternoEncuestre en la base de datos.
    """
    docs = DocumentoExternoEncuestre.query.all()
    return docs


def list_documentos_ecuestre(id):
    """
    Devuelve todos los documentos externos asociados a un ecuestre específico.

    Args:
        id (int): El ID del ecuestre para el cual se desean obtener los documentos.

    Returns:
        list: Lista de documentos externos asociados al ecuestre.
    """
    docs = DocumentoExternoEncuestre.query.filter(
        DocumentoExternoEncuestre.encuestre_id == id
    ).all()
    return docs


def get_documento_by_id(id):
    """
    Obtiene un documento externo ecuestre por su ID.

    Args:
        id (int): El ID del documento a buscar.

    Returns:
        DocumentoExternoEncuestre: El objeto DocumentoExternoEncuestre encontrado, o None si no existe.
    """
    doc = DocumentoExternoEncuestre.query.filter_by(id=id).first()
    return doc


def eliminar_documento(id):
    """
    Elimina un documento externo ecuestre por su ID.

    Args:
        id (int): El ID del documento a eliminar.

    Returns:
        bool: True si el documento fue eliminado exitosamente, False si no se encontró el documento.
    """
    # Buscar el documento por su id
    documento = DocumentoExternoEncuestre.query.get(id)

    # Si existe, eliminarlo
    if documento:
        db.session.delete(documento)
        db.session.commit()
        return True
    return False


def create_doc(**kwargs):
    """
    Crea y guarda un nuevo documento externo ecuestre en la base de datos.

    Args:
        **kwargs: Argumentos necesarios para crear el documento, como título, tipo, y ecuestre_id.

    Returns:
        DocumentoExternoEncuestre: El objeto DocumentoExternoEncuestre recién creado.
    """
    doc = DocumentoExternoEncuestre(**kwargs)
    db.session.add(doc)
    db.session.commit()
    return doc


def buscar_documentos(
    ecuestre_id, titulo="", tipo="", order_by="titulo", order_direction="asc"
):
    """
    Busca documentos externos asociados a un ecuestre según filtros opcionales.

    Args:
        ecuestre_id (int): El ID del ecuestre asociado.
        titulo (str, opcional): El título o parte del título del documento a buscar. Por defecto es ''.
        tipo (str, opcional): El tipo de documento a buscar. Por defecto es ''.
        order_by (str, opcional): La columna por la cual se debe ordenar la búsqueda. Por defecto es 'titulo'.
        order_direction (str, opcional): La dirección de la ordenación, 'asc' para ascendente o 'desc' para descendente. Por defecto es 'asc'.

    Returns:
        list: Lista de objetos DocumentoExternoEncuestre que coinciden con los filtros.
    """
    query = DocumentoExternoEncuestre.query.filter_by(encuestre_id=ecuestre_id)

    if titulo:
        query = query.filter(DocumentoExternoEncuestre.titulo.ilike(f"%{titulo}%"))

    if tipo:
        query = query.filter_by(tipo=tipo)

    if order_by:
        order_column = getattr(DocumentoExternoEncuestre, order_by)
        if order_direction == "asc":
            query = query.order_by(asc(order_column))
        else:
            query = query.order_by(desc(order_column))

    return query.all()


def modificar_documento(titulo, tipo, id):
    """
    Modifica el Documento externo, en concreto su titulo y su tipo
    Args:
        id:id del documento a modificar
        titulo:nuevo titulo del docuemnto
        tipo:nuevo tipo del documento
    """
    doc = get_documento_by_id(id)
    if doc:
        setattr(doc, "nombre", titulo)
        setattr(doc, "tipo", tipo)
        db.session.commit()
    return None
