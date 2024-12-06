from core.database import db
from core.models.Cobro.Cobro import Cobros
from core.models.Equipo.Equipo import Equipos
from sqlalchemy import asc, desc


def list_Cobros(page=1, per_page=2):
    """
    Devuelve todos los cobros no borrados de manera paginada

    Args:
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Cantidad de Cobros por página. Por defecto es 10.

    Returns:
        Pagination: Un objeto de paginación con la lista de cobros que no están borrados.
    """
    query = Cobros.query.filter_by(borrado=False)
    cobros = query.paginate(page=page, per_page=per_page, error_out=False)
    return cobros
def list_Cobros_all():
    """
    Devuelve todos los cobros no borrados de manera paginada.
    Returns:
        Lista de cobros que no están borrados.
    """
    cobros = Cobros.query.filter_by(borrado=False)
    return cobros
def filtro_api(fecha_inicio=None,fecha_fin=None, JA_Ref=None):
    """
        Devuelve todos los cobros no borrados de manera paginada.
        Args:
            fecha_inicio (datetime, optional): Fecha de inicio para filtrar los cobros por fecha de pago.
            fecha_fin (datetime, optional): Fecha de fin para filtrar los cobros por fecha de pago.
            JA_Ref (str, optional): Referencia de JyA para filtrar los cobros.
        Return:
        list: Una lista de objetos Cobros que no están borrados y cumplen con los filtros especificados.
    """
    query = Cobros.query.filter_by(borrado=False)
    if fecha_inicio:
        query = query.filter(Cobros.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Cobros.fecha_pago <= fecha_fin)
    if JA_Ref:
        query = query.filter_by(JyA_ref=JA_Ref)
    cobros = query
    return cobros

def find_cobros_by_fields(
    nombre=None,
    apellido=None,
    filtro_mp=None,
    fecha_inicio=None,
    fecha_fin=None,
    orden=True,
    orden_by="fecha_pago",
    page=1,
    per_page=10,
):
    """
    Busca cobros en función de varios filtros y los devuelve de manera paginada.

    Args:
        nombre (str, optional): Nombre parcial del receptor del cobro.
        apellido (str, optional): Apellido parcial del receptor del cobro.
        filtro_mp (str, optional): Tipo de medio de pago para filtrar cobros.
        fecha_inicio (str, optional): Fecha de inicio para filtrar cobros (formato 'YYYY-MM-DD').
        fecha_fin (str, optional): Fecha de fin para filtrar cobros (formato 'YYYY-MM-DD').
        orden (bool, optional): Determina si el orden es ascendente (True) o descendente (False).
        orden_by (str, optional): Campo por el cual ordenar (por defecto 'fecha_pago').
        page (int, optional): Número de página para la paginación (por defecto es 1).
        per_page (int, optional): Cantidad de cobros por página (por defecto es 10).

    Returns:
        Pagination: Un objeto de paginación con la lista de cobros filtrados y ordenados.
    """
    query = Cobros.query.filter_by(borrado=False)

    # Filtro por medio de pago
    if filtro_mp:
        query = query.filter_by(medio_pago=filtro_mp)

    # Filtro por rango de fechas
    if fecha_inicio:
        query = query.filter(Cobros.fecha_pago >= fecha_inicio)

    if fecha_fin:
        query = query.filter(Cobros.fecha_pago <= fecha_fin)

    # Ordenar los resultados
    if orden:
        if orden_by == "fecha_pago":
            query = query.order_by(asc(Cobros.fecha_pago))
    else:
        if orden_by == "fecha_pago":
            query = query.order_by(desc(Cobros.fecha_pago))

    if nombre:
        query = query.join(Cobros.receptor_dinero).filter(
            Equipos.nombre.ilike(f"{nombre}%")
        )

    if apellido:
        query = query.join(Cobros.receptor_dinero).filter(
            Equipos.apellido.ilike(f"{apellido}%")
        )
    # Paginación
    cobros = query.paginate(page=page, per_page=per_page, error_out=False)
    return cobros


def create_Cobro(**kwargs):
    """
    Crea un nuevo cobro en base a los argumentos proporcionados.

    Args:
        **kwargs: Los argumentos necesarios para crear el cobro, como campos clave-valor.

    Returns:
        Cobros: El objeto Cobros recién creado y guardado en la base de datos.
    """
    cobro = Cobros(**kwargs)
    db.session.add(cobro)
    db.session.commit()
    return cobro


def get_cobro_by_id(id):
    """
    Encuentra un cobro por su ID.

    Args:
        id (int): El ID del cobro que se desea buscar.

    Returns:
        Cobros: El objeto Cobros si se encuentra, de lo contrario, None.
    """
    cobro = Cobros.query.filter_by(id=id).first()
    return cobro


def delete_cobro(id):
    """
    Realiza un borrado lógico de un cobro por su ID, marcándolo como borrado.

    Args:
        id (int): El ID del cobro que se desea borrar.

    Returns:
        Cobros: El objeto Cobros con la marca de borrado lógico aplicada si se encuentra,
        de lo contrario, None.
    """
    cobro = get_cobro_by_id(id)
    if cobro is None:
        return None
    cobro.borrado = True
    db.session.commit()
    return cobro


def modificar_cobro(id, **kwargs):
    """
    Modifica un cobro existente en la base de datos.

    Busca el cobro por su ID y, si existe, actualiza sus campos con los valores proporcionados.

    Args:
        id (int): El ID del cobro a modificar.
        **kwargs: Los nuevos valores de los campos a actualizar, como clave-valor.

    Returns:
        Cobros: El objeto Cobros actualizado si se encuentra, de lo contrario, None.
    """
    cobro = get_cobro_by_id(id)
    if cobro:
        for key, value in kwargs.items():
            setattr(cobro, key, value)  # Actualiza los atributos del cobro
        db.session.commit()
        return cobro
    return None  # O lanzar un error si el cobro no existe
