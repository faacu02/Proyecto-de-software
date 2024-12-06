from core.database import db
from core.models.Pago.Pago import Pagos
from sqlalchemy import asc, desc
from datetime import datetime


def list_Pagos():
    """
    Lista todos los pagos no eliminados.

    Retorna:
    --------
    list:
        Una lista de objetos `Pagos` que no han sido eliminados.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con el código de error y el mensaje de excepción.
    """
    pay = Pagos.query.filter_by(eliminado=False).all()

    return pay


def list_pagos_pag(pagos, max: int = 5, page: int = 1):
    """
    Lista los pagos no eliminados con paginación usando una colección dada.

    Parámetros:
    -----------
    pagos : list
        Colección de objetos `Pagos` a paginar.
    max : int, opcional
        Número máximo de elementos por página (por defecto, 5).
    page : int, opcional
        Número de la página a obtener (por defecto, 1).

    Retorna:
    --------
    dict:
        Un diccionario que contiene los pagos paginados y los metadatos de la paginación.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con el código de error y el mensaje de excepción.
    """
    try:
        # Filtrar los pagos que no han sido eliminados
        filtered_pagos = [pago for pago in pagos if not pago.eliminado]

        # Total de pagos después del filtro
        total_pagos = len(filtered_pagos)

        # Calcular los índices para la paginación
        start_index = (page - 1) * max
        end_index = start_index + max

        # Obtener los pagos correspondientes a la página actual
        pagos_paginados = filtered_pagos[start_index:end_index]

        # Calcular el total de páginas
        total_pages = (total_pagos + max - 1) // max  # Redondeo hacia arriba

        return {
            "pagos": pagos_paginados,  # Lista de pagos en la página actual
            "current_page": page,  # Página actual
            "per_page": max,  # Número de elementos por página
            "total_pages": total_pages,  # Total de páginas
            "total_pagos": total_pagos,  # Total de registros después del filtro
            "has_next": page < total_pages,  # Indica si hay una página siguiente
            "has_prev": page > 1,  # Indica si hay una página anterior
        }
    except Exception as e:
        return {"error": "Error al procesar los pagos", "message": str(e)}


def create_Pago(beneficiario, monto, tipo_pago, descripcion):
    """
    Crea un nuevo registro de pago y lo guarda en la base de datos.

    Parámetros:
    -----------
    beneficiario : str
        El nombre del beneficiario del pago.
    monto : float
        El monto del pago.
    tipo_pago : str
        El tipo de pago realizado (e.g., "transferencia", "efectivo").
    descripcion : str
        Una descripción del pago.

    Retorna:
    --------
    Pagos:
        El objeto `Pagos` creado y almacenado en la base de datos.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con el código de error y el mensaje de excepción.
    """
    pay = Pagos(
        beneficiario=beneficiario,
        monto=monto,
        tipo_pago=tipo_pago,
        descripcion=descripcion,
        fecha_pago=datetime.now(),
    )
    db.session.add(pay)
    db.session.commit()

    return pay


def eliminar_pagos(id: int):
    """
    Marca un pago como eliminado en la base de datos.

    Parámetros:
    -----------
    id : int
        El ID del pago que se desea eliminar.

    Retorna:
    --------
    dict:
        Un diccionario con un mensaje de éxito o error.

    Excepciones:
    ------------
    dict:
        En caso de error o si no se encuentra el pago, retorna un diccionario con un mensaje de error.
    """
    pago = find_pago(id)
    if pago:
        pago.eliminado = True

        db.session.commit()
    else:
        print("error al eliminar pago")


def find_pago(id: int):
    """
    Busca un pago en la base de datos por su ID.

    Parámetros:
    -----------
    id : int
        El ID del pago que se desea buscar.

    Retorna:
    --------
    Pagos o None:
        Retorna el objeto `Pagos` si se encuentra, o `None` si no existe un pago con el ID dado.

    Excepciones:
    ------------
    dict:
        En caso de error en la búsqueda, retorna un diccionario con el código de error y el mensaje de excepción.
    """
    pago = Pagos.query.get(id)
    return pago


def update(id: int, tipo_pago: str, monto, descripcion, beneficiario):
    """
    Actualiza un registro de pago en la base de datos.

    Parámetros:
    -----------
    id : int
        El ID del pago que se desea actualizar.
    tipo_pago : str, opcional
        El nuevo tipo de pago. Si es None, no se actualiza.
    monto : float, opcional
        El nuevo monto del pago. Si es None, no se actualiza.
    descripcion : str, opcional
        La nueva descripción del pago. Si es None, no se actualiza.
    beneficiario : str, opcional
        El nuevo beneficiario del pago. Si es None, no se actualiza.

    Retorna:
    --------
    dict:
        Un diccionario que indica si la actualización fue exitosa o contiene un mensaje de error.

    Excepciones:
    ------------
    dict:
        En caso de error en la actualización, retorna un diccionario con el mensaje de error.
    """

    try:
        pago = Pagos.query.get(id)

        if tipo_pago:
            pago.tipo_pago = tipo_pago
        if monto:
            pago.monto = monto
        if descripcion:
            pago.descripcion = descripcion
        if beneficiario:
            pago.beneficiario = beneficiario

        db.session.commit()
        return {"success": "se actualizo el pago correctamente"}
    except:
        return {"error": "no se puedo actualizar el pago"}


def buscarEntre(fecha_ini, fecha_fin, tipo, orden):
    """
    Busca pagos entre dos fechas con opción de filtrar por tipo y orden.

    Parámetros:
    -----------
    fecha_ini : str
        La fecha de inicio para el rango de búsqueda en formato "YYYY-MM-DD".
    fecha_fin : str
        La fecha de fin para el rango de búsqueda en formato "YYYY-MM-DD".
    tipo : str
        El tipo de pago a filtrar. Puede ser "all" para todos los tipos o un tipo específico.
    orden : str
        El orden de los resultados. Puede ser "asc" para ascendente o cualquier otro valor para descendente.

    Retorna:
    --------
    list o dict:
        Una lista de objetos `Pagos` que cumplen con los criterios de búsqueda, o un diccionario con un mensaje de error.

    Excepciones:
    ------------
    dict:
        En caso de error en la búsqueda, retorna un diccionario con el mensaje de error.
    """
    try:
        order = asc(Pagos.fecha_pago) if orden == "asc" else desc(Pagos.fecha_pago)
        if fecha_ini != 0:
            if tipo == "all":
                pagos = (
                    Pagos.query.filter(Pagos.fecha_pago.between(fecha_ini, fecha_fin))
                    .filter_by(eliminado=False)
                    .order_by(order)
                    .all()
                )
            else:
                pagos = (
                    Pagos.query.filter(Pagos.fecha_pago.between(fecha_ini, fecha_fin))
                    .filter_by(eliminado=False)
                    .filter_by(tipo_pago=tipo)
                    .order_by(order)
                    .all()
                )
        else:
            if tipo == "all":
                pagos = Pagos.query.filter_by(eliminado=False).order_by(order).all()
            else:
                pagos = (
                    Pagos.query.filter_by(eliminado=False)
                    .order_by(order)
                    .filter_by(tipo_pago=tipo)
                    .all()
                )

        return pagos
    except Exception as e:
        return {"error": f"Se produjo un error al filtrar los pagos: {str(e)}"}
