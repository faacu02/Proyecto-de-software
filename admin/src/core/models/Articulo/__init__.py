from core.database import db
from core.models.Equipo.Equipo import Equipos
from sqlalchemy.exc import SQLAlchemyError
from core.models.Articulo.Articulo import Articulos
from core.models.User.User import Users  
from sqlalchemy import desc, func



def crear_articulo(**kwargs):
    """
    Crea un nuevo artículo en la base de datos.

    :param kwargs: Diccionario con los datos del artículo. Campos esperados:
        - titulo (str): Título del artículo.
        - copete (str): Breve resumen del artículo.
        - contenido (str): Contenido del artículo.
        - autor_id (int): ID del autor/a.
        - estado (str): Estado del artículo ("Borrador", "Publicado" o "Archivado").
        - fecha_publicacion (datetime, opcional): Fecha de publicación.
    :return: Diccionario con el resultado de la operación.
    """
    try:
        articulo = Articulos(**kwargs)
        db.session.add(articulo)
        db.session.commit()
        return {"success": True, "message": "Artículo creado exitosamente", "id": articulo.id}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}


def obtener_articulo(articulo_id):
    """
    Obtiene un artículo por su ID.

    :param articulo_id: ID del artículo a buscar.
    :return: Diccionario con el artículo o un mensaje de error si no se encuentra.
    """
    try:
        articulo = Articulos.query.get(articulo_id)
        if articulo:
            return {"success": True, "articulo": articulo}
        else:
            return {"success": False, "message": "Artículo no encontrado"}
    except SQLAlchemyError as e:
        return {"success": False, "message": str(e)}


def actualizar_articulo(articulo_id, **kwargs):
    """
    Actualiza un artículo existente.

    :param articulo_id: ID del artículo a actualizar.
    :param kwargs: Campos a actualizar (ej. titulo, copete, contenido, etc.).
    :return: Diccionario con el resultado de la operación.
    """
    try:
        articulo = Articulos.query.get(articulo_id)
        if not articulo:
            return {"success": False, "message": "Artículo no encontrado"}

        for key, value in kwargs.items():
            if hasattr(articulo, key):
                setattr(articulo, key, value)
        db.session.commit()
        return {"success": True, "message": "Artículo actualizado exitosamente"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}


def eliminar_articulo(articulo_id):
    """
    Elimina un artículo por su ID.

    :param articulo_id: ID del artículo a eliminar.
    :return: Diccionario con el resultado de la operación.
    """
    try:
        articulo = Articulos.query.get(articulo_id)
        if not articulo:
            return {"success": False, "message": "Artículo no encontrado"}

        db.session.delete(articulo)
        db.session.commit()
        return {"success": True, "message": "Artículo eliminado exitosamente"}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}


def listar_articulos(filtros=None, page=1, per_page=10):
    """
    Lista los artículos con filtros opcionales y paginación.

    :param filtros: Diccionario con filtros opcionales. Campos soportados:
        - estado (str): Filtrar por estado ("Borrador", "Publicado", "Archivado").
        - autor_id (int): Filtrar por autor.
    :param page: Número de página (por defecto 1).
    :param per_page: Cantidad de artículos por página (por defecto 10).
    :return: Diccionario con los artículos paginados o un mensaje de error.
    """
    try:
        query = Articulos.query
        if filtros:
            for key, value in filtros.items():
                if hasattr(Articulos, key):
                    query = query.filter(getattr(Articulos, key) == value)

        paginated_articulos = query.order_by(Articulos.fecha_creacion.desc()).paginate(page=page, per_page=per_page)

        return {
            "success": True,
            "articulos": paginated_articulos 
        }
    except SQLAlchemyError as e:
        return {"success": False, "message": str(e)}


def listar_articulos_api(autor,published_from,published_to, page, per_page):
    """
    Lista los artículos con filtros opcionales y paginación.

    :param autor: Nombre y apellido del autor (equipo relacionado al usuario creador).
    :param published_from: Fecha de inicio para filtrar artículos publicados (formato: YYYY-MM-DD).
    :param published_to: Fecha de fin para filtrar artículos publicados (formato: YYYY-MM-DD).
    :param page: Número de página (por defecto 1).
    :param per_page: Cantidad de artículos por página (por defecto 10).
    :return: Paginación de artículos o un mensaje de error en caso de excepción.
    """
    try:
        query = Articulos.query.filter(Articulos.estado == "Publicado")
        if autor:
            query = query.join(Users).join(Equipos).filter(
                func.concat(Equipos.nombre, ' ', Equipos.apellido).ilike(f"{autor}%")
            )
            print(query)
            #query = query.join(Articulos.creador_pub).filter(Users.alias.ilike(f"{autor}%"))
        if published_from:
            query = query.filter(Articulos.fecha_publicacion >= published_from)
        if published_to:
            query = query.filter(Articulos.fecha_publicacion <= published_to)
        query = query.order_by(desc(Articulos.fecha_publicacion))

        return query.paginate(page=page, per_page=per_page, error_out=False)
    except SQLAlchemyError as e:
        return {"success": False, "message": str(e)}

def obtener_estado(articulo_id):
    """
    Obtiene el estado de publicación de un artículo dado su ID.

    Esta función consulta la base de datos para recuperar el artículo correspondiente al ID proporcionado y
    retorna el valor de su atributo `publico`, que indica si el artículo está publicado o no.

    :param articulo_id: El ID del artículo cuyo estado se desea obtener.

    :return: 
        - El valor del atributo `publico` del artículo (un valor booleano que indica si el artículo está publicado o no).
        - En caso de error, retorna el error capturado.
    """
    try:
        articulo = Articulos.query.get(articulo_id)
        return articulo.publico 
    except Exception as e:
        return e