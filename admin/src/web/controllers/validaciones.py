import re
from datetime import datetime
from flask import flash
from core.models import Equipo as equipoDB
from core.models import Legajo as legajoDB
from core.models import Cobro as cobroDB
from core.models import Encuestre as ecuDB
import os


def validar_campos_obligatorios(params, required_fields):
    """Valida que los campos especificados no estén vacíos."""
    for field in required_fields:
        if not params.get(field):
            flash(f"El campo {field.replace('_', ' ')} es obligatorio", "error")
            return False
    return True


def validar_opcion_seleccionada(field, opciones_permitidas):
    """
    Valida que la opción seleccionada esté dentro de las opciones permitidas.

    :param field: Campo del cual se validará la opción seleccionada.
    :param opciones_permitidas: Lista de opciones permitidas.
    :return: bool True si la opción es válida, False en caso contrario.
    """
    if field not in opciones_permitidas:
        flash(
            f"La opción seleccionada para {field.replace('_', ' ')} no es válida. Opciones permitidas: {', '.join(opciones_permitidas)}.",
            "error",
        )
        return False
    return True


def validar_numeros(params, fields):
    """Valida que los campos especificados contengan solo números."""
    for field in fields:
        if not params[field].isdigit():
            flash(f"El {field.replace('_', ' ')} solo puede contener números", "error")
            return False
    return True


def validar_numero(param):
    """
    Valida que el campo mandado por parametro sea un numero
    """
    if not param.isdigit():
        flash(f"El {param.replace('_', ' ')} solo puede contener números", "error")
        return False
    return True


def validar_email(param):
    """
    Valida que la variable mandada por parametro sea un email valido
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, param):
        flash("El correo electrónico no tiene un formato válido", "error")
        return False
    return True


def validar_fechas(ini, fin):
    """Valida que la fecha de inicio no sea mayor a la fecha de fin."""
    try:

        if ini:
            fecha_inicio_dt = datetime.strptime(ini, "%Y-%m-%d")
            if fin:
                fecha_cese_dt = datetime.strptime(fin, "%Y-%m-%d")
                if fecha_cese_dt < fecha_inicio_dt:
                    flash(
                        "La fecha de fin no puede ser anterior a la fecha de inicio",
                        "error",
                    )
                    return False
    except ValueError:
        flash("El formato de fecha es incorrecto. Usa el formato YYYY-MM-DD.", "error")
        return False
    return True


def convertir_activo(params):
    """
    Convierte el parámetro "activo" a un valor booleano.

    Esta función convierte el valor del parámetro "activo" a True si es "si",
    y a False en caso contrario.

    Parámetros:
    params (dict): Un diccionario con los parámetros de la solicitud.

    Retorna:
    bool: True si el parámetro "activo" es "si", False en caso contrario.
    """
    params["activo"] = params.get("activo")
    if params["activo"] == "si":
        return True
    else:
        return False


def validar_miembro_existente(params, find_member_by_email, find_member_by_dni):
    """
    Valida si un miembro ya existe en la base de datos con el mismo email o DNI.

    Esta función verifica si ya existe un miembro en la base de datos con el
    mismo email o DNI proporcionados en los parámetros.

    Parámetros:
    params (dict): Un diccionario con los parámetros de la solicitud, incluyendo el email y el DNI.
    find_member_by_email (function): Una función que busca un miembro por su email.
    find_member_by_dni (function): Una función que busca un miembro por su DNI.

    Retorna:
    bool: True si no existe un miembro con el mismo email o DNI, False en caso contrario.
    """
    member = find_member_by_email(params["email"]) or find_member_by_dni(params["dni"])
    if member:
        flash("El miembro ya existe con el mismo email o DNI", "error")
        return False
    return True


def validar_miembro_existente_actualizacion(
    params, id, find_member_by_email, find_member_by_dni
):
    """
    Valida si un miembro existente puede ser actualizado sin conflictos de email o DNI.

    Esta función verifica si el email o DNI proporcionados ya están registrados en otro
    miembro que no sea el miembro con el ID dado.

    Parámetros:
    params (dict): Un diccionario con los parámetros de la solicitud, incluyendo el email y el DNI.
    id (int): El ID del miembro que se está actualizando.
    find_member_by_email (function): Una función que busca un miembro por su email.
    find_member_by_dni (function): Una función que busca un miembro por su DNI.

    Retorna:
    bool: True si el miembro puede ser actualizado sin conflictos, False si el email o DNI ya están registrados en otro miembro.
    """
    existing_member_by_email = find_member_by_email(params["email"])
    existing_member_by_dni = find_member_by_dni(params["dni"])
    if (existing_member_by_email and existing_member_by_email.id != id) or (
        existing_member_by_dni and existing_member_by_dni.id != id
    ):
        flash("El DNI o el email ya están registrados en otro miembro", "error")
        return False
    return True


def validar_solo_letras(params, fields):
    """Valida que los campos especificados contengan solo letras"""
    for field in fields:
        if not params.get(field, "").isalpha():
            flash(f"El campo {field} solo puede contener letras", "error")
            return False
    return True


def validar_opcion_seleccionada(field, opciones_permitidas):
    """
    Valida que la opción seleccionada esté dentro de las opciones permitidas.

    :param field: Campo del cual se validará la opción seleccionada.
    :param opciones_permitidas: Lista de opciones permitidas.
    :return: bool True si la opción es válida, False en caso contrario.
    """
    if field not in opciones_permitidas:
        flash(
            f"La opción seleccionada para {field.replace('_', ' ')} no es válida. Opciones permitidas: {', '.join(opciones_permitidas)}.",
            "error",
        )
        return False
    return True


def validar_fecha_anterior(params, fields):
    """
    Valida que la fecha especificada en 'field' no sea una fecha futura.

    :param params: Diccionario con los datos (por ejemplo, request.form).
    :param field: Campo que contiene la fecha que se va a validar.
    :return: True si la fecha no es futura, False en caso contrario.
    """
    fecha_actual = datetime.now()

    for field in fields:

        try:
            fecha_str = params.get(field)
            # if not fecha_str:
            # flash(f"El campo {field.replace('_', ' ')} es obligatorio", "error")
            # return False

            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")

            if fecha > fecha_actual:
                flash(
                    f"La fecha en el campo {field.replace('_', ' ')} no puede ser una fecha futura",
                    "error",
                )
                return False
        except ValueError:
            flash(
                f"El formato de la fecha en el campo {field.replace('_', ' ')} es incorrecto. Usa el formato YYYY-MM-DD.",
                "error",
            )
            return False

    return True


def validar_miembro(id):
    """Valida si existe en la base de datos un miembro con el id pasado por parametro
    :param id: el id del meimbro a buscar
    """
    if equipoDB.get_memberby_id(id) == None:
        flash(f"El miembro con ese id no existe", "error")

        return False
    return True


def validar_JA(id):
    """Valida si existe en la base de datos un JA con el id pasado por parametro
    :param id: el id del Jinete a buscar
    """
    if legajoDB.get_legajo_by_id(id) == None:
        flash(f"El JA con ese id no existe", "error")
        return False
    return True


def validar_Cobro(id):
    """Valida si existe en la base de datos un cobro con el id pasado por parametro
    :param id: el id del cobro a buscar
    """
    if cobroDB.get_cobro_by_id(id) == None:
        flash(f"El Cobro con ese id no existe", "error")
        return False
    return True


def validar_profesor_o_Terapeuta(ids):
    """Valida si existe un miembro
    del equipo con el rol de
    conductor o entrenador en
    todas las ids"""
    for id in ids:
        miembro = equipoDB.get_memberby_id(id)
        if miembro is None:
            return False
        if not (
            miembro.puesto_laboral == "Profesor de Equitacion"
            or miembro.puesto_laboral == "Terapeuta"
        ):
            flash(f"Algun miembro elegido no es conductor o entrenadro", "error")
            return False
    return True


def validar_conductor_o_entrenador(ids):
    """Valida si existe un miembro
    del equipo con el rol de
    conductor o entrenador en
    todas las ids"""
    for id in ids:
        miembro = equipoDB.get_memberby_id(id)
        if miembro is None:
            return False  # No se encontró un miembro con el ID
        # Verificar si el puesto laboral es "Conductor"
        if not (
            miembro.puesto_laboral == "Conductor"
            or miembro.puesto_laboral == "Entrenador de Caballos"
        ):
            flash(f"Algun miembro elegido no es conductor o entrenadro", "error")
            return False
    return True


def validar_extension(filename, extensiones_permitidas):
    """
    Valida si la extensión del archivo está en la lista de extensiones permitidas.

    :param filename: Nombre del archivo a validar.
    :param extensiones_permitidas: Lista de extensiones permitidas (ej. ['pdf', 'doc', 'xls', 'jpeg']).
    :return: bool True si la extensión es válida, False en caso contrario.
    """
    extension = os.path.splitext(filename)[1][1:].lower()
    if extension in extensiones_permitidas:
        return True
    else:
        flash(
            f"Extensión '{extension}' no permitida. Extensiones permitidas: {', '.join(extensiones_permitidas)}.",
            "error",
        )
        return False


def validar_tamano(tamano_archivo, tamano_maximo=3 * 1024 * 1024):
    """
    Valida si el tamaño del archivo es menor o igual al tamaño máximo permitido.

    :param tamano_archivo: Tamaño del archivo en bytes.
    :param tamano_maximo: Tamaño máximo permitido en bytes (por defecto 3 MB).
    :return: bool True si el tamaño es válido, False en caso contrario.
    """
    if tamano_archivo <= tamano_maximo:
        return True
    else:
        flash(
            f"Tamaño del archivo excede el máximo permitido de {tamano_maximo / (1024 * 1024)} MB.",
            "error",
        )
        return False


def validar_Ecuestre(id):
    """Valida si existe en la base de datos un ecuestre con el id pasado por parametro
    :param id: el id del cobro a buscar
    """
    if ecuDB.get_Ecuestre_by_id(id) == None:
        flash(f"El Ecuestre con ese id no existe", "error")
        return False
    return True



def validar_is_admin(user):
    """
    Valida si el usuario es un administrador del sistema.

    Esta función verifica si el rol del usuario es "SystemAdmin".

    Parámetros:
    user (User): El objeto usuario a validar.

    Retorna:
    bool: True si el usuario es un administrador del sistema, False en caso contrario.
    """
    if user.role.name == "SystemAdmin":
        return True
    else:
        return False


def validar_miembro_existente_actualizacion_admin(params, id, find_member_by_dni):
    """
    Valida si un miembro existente puede ser actualizado por un administrador.

    Esta función verifica si el DNI proporcionado ya está registrado en otro miembro
    que no sea el miembro con el ID dado.

    Parámetros:
    params (dict): Un diccionario con los parámetros de la solicitud, incluyendo el DNI.
    id (int): El ID del miembro que se está actualizando.
    find_member_by_dni (function): Una función que busca un miembro por su DNI.

    Retorna:
    bool: True si el miembro puede ser actualizado, False si el DNI ya está registrado en otro miembro.
    """
    existing_member_by_dni = find_member_by_dni(params["dni"])
    if existing_member_by_dni and existing_member_by_dni.id != id:
        flash("El DNI ya está registrado en otro miembro", "error")
        return False
    return True


def validar_anio_anterior(anio):
    """
    Valida que el año ingresado no sea un año futuro.
    Parámetros:
        anio (int): Año que se desea validar.
    Retorna:
        bool: Retorna `False` si el año ingresado es mayor al año actual, mostrando un mensaje de error.
              Retorna `True` si el año es válido.
    """
    anioAct = datetime.now().year
    print(anioAct, type(anioAct))
    print(anio, type(anio))
    if anio > anioAct:
        flash("El año ingreaso no puede ser un año a futuro", "error")
        return False
    return True
