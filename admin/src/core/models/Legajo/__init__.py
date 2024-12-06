from core.database import db
from core.models.Legajo.Legajo import Legajos
from sqlalchemy import asc, desc


def list_legajos(page=None):
    """
    Lista los legajos no eliminados con opción de paginación.

    Parámetros:
    -----------
    page : int, opcional
        El número de página para la paginación. Si es None, se retornan todos los legajos.

    Retorna:
    --------
    list o Pagination:
        Si `page` es proporcionado, retorna un objeto `Pagination` con los legajos paginados.
        Si `page` es None, retorna una lista de todos los legajos no eliminados.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con el código de error y el mensaje de excepción.
    """
    try:
        if page != None:
            legajos = Legajos.query.filter_by(eliminado=False).paginate(
                page=page, per_page=10, error_out=False
            )
        else:
            legajos = Legajos.query.filter_by(eliminado=False).all()
        return legajos
    except Exception as e:
        return {400: f"error {e}"}


def buscar_por_titulo(nombre=None, apellido=None, dni=None, prof=None, page=1):
    """
    Busca legajos que coincidan con los filtros proporcionados y aplica paginación.

    Parámetros:
    -----------
    nombre : str, opcional
        El nombre para filtrar los legajos. Si es None, no se aplica este filtro.
    apellido : str, opcional
        El apellido para filtrar los legajos. Si es None, no se aplica este filtro.
    dni : str, opcional
        El DNI para filtrar los legajos. Si es None, no se aplica este filtro.
    prof : str, opcional
        El nombre del profesional que atiende para filtrar los legajos. Si es None, no se aplica este filtro.
    page : int, opcional
        Número de página para la paginación. El valor por defecto es 1.

    Retorna:
    --------
    Pagination:
        Un objeto de paginación que contiene los legajos filtrados en la página solicitada.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con la excepción y un mensaje indicando contactar al administrador.
    """
    try:
        query = Legajos.query.filter_by(eliminado=False)

        if nombre:
            query = query.filter(Legajos.nombre.like(f"%{nombre}%"))
        if dni:
            query = query.filter(Legajos.dni.like(f"%{dni}%"))
        if apellido:
            query = query.filter(Legajos.apellido.like(f"%{apellido}%"))
        if prof:
            query = query.filter(Legajos.profesionales_atienden.like(f"%{prof}%"))
        legajos = query.paginate(page=page, per_page=10, error_out=False)
        return legajos
    except Exception as e:
        return {e: "Contacte al administrador"}


def buscar_por_titulo_nopage(nombre=None, apellido=None, dni=None, prof=None):
    """
    Busca legajos que coincidan con los filtros proporcionados, sin paginación.

    Parámetros:
    -----------
    nombre : str, opcional
        El nombre para filtrar los legajos. Si es None, no se aplica este filtro.
    apellido : str, opcional
        El apellido para filtrar los legajos. Si es None, no se aplica este filtro.
    dni : str, opcional
        El DNI para filtrar los legajos. Si es None, no se aplica este filtro.
    prof : str, opcional
        El nombre del profesional que atiende para filtrar los legajos. Si es None, no se aplica este filtro.

    Retorna:
    --------
    list:
        Una lista de objetos `Legajos` que coinciden con los filtros aplicados.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con la excepción y un mensaje indicando contactar al administrador.
    """
    try:
        query = Legajos.query.filter_by(eliminado=False)

        if nombre:
            query = query.filter(Legajos.nombre.like(f"%{nombre}%"))
        if dni:
            query = query.filter(Legajos.dni.like(f"%{dni}%"))
        if apellido:
            query = query.filter(Legajos.apellido.like(f"%{apellido}%"))
        if prof:
            query = query.filter(Legajos.profesionales_atienden.like(f"%{prof}%"))

        legajos = query.all()

        return legajos
    except Exception as e:
        return {e: "Contacte al administrador"}


def obtenerTotalTitulos(nombre=None, apellido=None, dni=None, prof=None):
    """
    Obtiene el número total de registros (legajos) filtrados por los parámetros dados.

    Parámetros:
    -----------
    nombre : str, opcional
        El nombre para filtrar los legajos. Si es None, no se aplica este filtro.
    apellido : str, opcional
        El apellido para filtrar los legajos. Si es None, no se aplica este filtro.
    dni : str, opcional
        El DNI para filtrar los legajos. Si es None, no se aplica este filtro.
    prof : str, opcional
        El nombre del profesional que atiende para filtrar los legajos. Si es None, no se aplica este filtro.

    Retorna:
    --------
    int:
        El número total de registros que coinciden con los filtros aplicados.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con la excepción y un mensaje indicando contactar al administrador.
    """
    try:
        query = Legajos.query.filter_by(eliminado=False)

        if nombre:
            query = query.filter(Legajos.nombre.like(f"%{nombre}%"))
        if dni:
            query = query.filter(Legajos.dni.like(f"%{dni}%"))
        if apellido:
            query = query.filter(Legajos.apellido.like(f"%{apellido}%"))
        if prof:
            query = query.filter(Legajos.profesionales_atienden.like(f"%{prof}%"))

        legajos = query.count()
        return legajos
    except Exception as e:
        return {e: "Contacte al administrador"}


def ordenar_legajos(arch, sort, ord, page):
    """
    Ordena una lista de legajos por una columna específica y paginada.

    Parámetros:
    -----------
    arch : list
        Lista de objetos que representan los legajos a ordenar.
    sort : str
        El nombre de la columna por la cual ordenar. Debe ser "nombre" o "apellido".
    ord : str
        El orden de clasificación, puede ser "asc" para ascendente o "desc" para descendente.
    page : int
        El número de página para la paginación. Cada página contiene 10 legajos.

    Retorna:
    --------
    tuple:
        - legajos_pag: La lista de legajos ordenados y paginados.
        - total: El número total de legajos en la lista original.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con la excepción y un mensaje indicando contactar al administrador.
    """
    try:
        columnas_validas = ["nombre", "apellido"]
        if sort not in columnas_validas:
            sort = "nombre"

        orden = True if ord == "asc" else False

        legajos = sorted(arch, key=lambda x: getattr(x, sort), reverse=not orden)

        total = len(legajos)
        legajos_pag = legajos[(page - 1) * 10 : page * 10]

        return legajos_pag, total
    except Exception as e:
        return {e: "Contacte al administrador"}


def obtenerTotalOrdenados(sort):
    """
    Obtiene el número total de registros ordenados por una columna específica.

    Parámetros:
    ----------
    sort : str
        El nombre de la columna por la cual ordenar. Debe ser "nombre" o "apellido".
    ord : str, opcional
        El orden de clasificación, puede ser "asc" para ascendente o "desc" para descendente (por defecto "asc").

    Retorna:
    --------
    int:
        El número total de registros que no han sido eliminados, ordenados por la columna especificada.

    Excepciones:
    ------------
    dict:
        En caso de error, retorna un diccionario con la excepción y un mensaje indicando contactar al administrador.
    """
    try:
        columnas_validas = ["nombre", "apellido"]
        if sort not in columnas_validas:
            sort = "nombre"
        if ord == "desc":
            orden = desc(sort)
        else:
            orden = asc(sort)

        query = Legajos.query.filter_by(eliminado=False).order_by(orden).count()

        return query
    except Exception as e:
        return {e: "Contacte al administrador"}


def obtenerTotal():
    """
    Devuelve el total de legajos que no están eliminados.

    Returns:
        int: El número total de legajos no eliminados.
        dict: Un diccionario con un código de error y un mensaje si ocurre una excepción.
    """
    try:
        return Legajos.query.filter_by(eliminado=False).count()
    except Exception as e:
        return {400: f"error {e}"}


def updateLegajo(id, arg):
    """
    Actualiza un legajo existente con los valores proporcionados.

    Args:
        id (int): El ID del legajo a actualizar.
        arg (dict): Un diccionario con los campos y valores para actualizar.

    Returns:
        dict: Un diccionario con un código de error y un mensaje si ocurre una excepción.
    """
    try:
        legajo = get_legajo_by_id(id)
        if arg["porcentaje"] == "":
            arg["porcentaje"] = 0
        if arg["becado"] == "true":
            arg["becado"] = True
        else:
            arg["becado"] = False
        legajo.nombre = arg["nombre"]
        legajo.apellido = arg["apellido"]
        legajo.dni = arg["dni"]
        legajo.edad = arg["edad"]
        legajo.fecha_nacimiento = arg["fecha_nacimiento"]
        legajo.lugar_nacimiento = arg["lugar_nacimiento"]
        legajo.domicilio_actual = arg["domicilio_actual"]
        legajo.telefono_actual = arg["telefono_actual"]
        legajo.becado = arg["becado"]
        legajo.porcentaje_beca = arg["porcentaje"]
        # legajo.contacto_emergencia = arg["contacto_emergencia"]
        # legajo.tel = arg["tel"]
        legajo.profesionales_atienden = arg["profesionales"]
        legajo.diagnostico = arg["diagnostico"]
        legajo.tipo_diagnostico = arg["tipo_diagnostico"]
        legajo.tipo_discapacidad = arg["tipo_discapacidad"]
        legajo.certificado_discapacidad = bool(arg["certificado_discapacidad"])
        legajo.asignacion_familiar = bool(arg["asignacion_familiar"])
        legajo.tipo_asignacion_familiar = arg["tipo_asignacion_familiar"]
        legajo.es_veneficiaro_pension = bool(arg["es_veneficiaro_pension"])
        legajo.pension = arg["pension"]
        legajo.obra_social = arg["obra_social"]
        legajo.num_afiliado = arg["num_afiliado"]
        legajo.posee_curatela = bool(arg["posee_curatela"])
        legajo.observaciones_curatela = arg["observaciones_curatela"]
        legajo.nombre_escuela = arg["nombre_escuela"]
        legajo.direccion_escuela = arg["direccion_escuela"]
        legajo.telefono_escuela = arg["telefono_escuela"]
        legajo.anio_actual_escuela = arg["anio_actual_escuela"]
        legajo.observaciones_escuela = arg["observaciones_escuela"]
        legajo.propuesta_trabajo = arg["propuesta_trabajo"]
        legajo.condicion = arg["condicion"]
        legajo.sede = arg["sede"]
        # legajo.dia = arg["dia"]
        legajo.profesora_terapeuta = int(arg["profesora_terapeuta"])
        legajo.conductor_caballo = int(arg["conductor_caballo"])
        legajo.caballo = int(arg["caballo"])
        legajo.auxiliar_pista = int(arg["auxiliar_pista"])
        # Datos del Tutor 1
        legajo.parentesco_tutor_1 = arg["parentesco_tutor_1"]
        legajo.nombre_tutor_1 = arg["nombre_tutor_1"]
        legajo.apellido_tutor_1 = arg["apellido_tutor_1"]
        legajo.dni_tutor_1 = arg["dni_tutor_1"]
        legajo.domicilio_tutor_1 = arg["domicilio_tutor_1"]
        legajo.celular_tutor_1 = arg["celular_tutor_1"]
        legajo.email_tutor_1 = arg["email_tutor_1"]
        legajo.nivel_escolaridad_tutor_1 = arg["nivel_escolaridad_tutor_1"]
        legajo.ocupacion_tutor_1 = arg["ocupacion_tutor_1"]

        # Datos del Tutor 2
        legajo.parentesco_tutor_2 = arg.get("parentesco_tutor_2", None)
        legajo.nombre_tutor_2 = arg.get("nombre_tutor_2", None)
        legajo.apellido_tutor_2 = arg.get("apellido_tutor_2", None)
        legajo.dni_tutor_2 = arg.get("dni_tutor_2", None)
        legajo.domicilio_tutor_2 = arg.get("domicilio_tutor_2", None)
        legajo.celular_tutor_2 = arg.get("celular_tutor_2", None)
        legajo.email_tutor_2 = arg.get("email_tutor_2", None)
        legajo.nivel_escolaridad_tutor_2 = arg.get("nivel_escolaridad_tutor_2", None)
        legajo.ocupacion_tutor_2 = arg.get("ocupacion_tutor_2", None)

        db.session.commit()
    except Exception as e:
        return {400: f"error {e} contacte al administrador"}


def create_legajo(**kwargs):
    """
    Crea un nuevo legajo y lo agrega a la base de datos.

    Args:
        **kwargs: Argumentos necesarios para crear el legajo, como campos clave-valor.

    Returns:
        Legajos: El objeto legajo recién creado y guardado en la base de datos.
    """
    legajo = Legajos(**kwargs)
    db.session.add(legajo)
    db.session.commit()
    return legajo


def actualizar_deuda(id, deuda_estado):
    """
    Actualiza el estado de la deuda de un legajo.

    Args:
        id (int): El ID del legajo a actualizar.
        deuda_estado (bool): El nuevo estado de la deuda (True o False).

    Returns:
        bool: True si se actualiza correctamente, False si no se encuentra el legajo.
    """
    ja = Legajos.query.get(id)
    if ja:
        ja.deuda = deuda_estado
        db.session.commit()
        return True
    return False


def get_legajo_by_id(id):
    """
    Busca un legajo por su ID.

    Args:
        id (int): El ID del legajo.

    Returns:
        Legajos: El objeto legajo si se encuentra, de lo contrario, None.
    """
    legajo = Legajos.query.filter_by(id=id).first()
    return legajo


def eliminar_legajo(id):
    """
    Marca un legajo como eliminado lógicamente por su ID.

    Args:
        id (int): El ID del legajo a eliminar.

    Returns:
        dict: Un diccionario con un código de error y un mensaje si ocurre una excepción.
    """
    try:
        legajo = get_legajo_by_id(id)
        legajo.eliminado = True
        db.session.commit()
    except Exception as e:
        return {400: f"{e} contactar al administrador"}
