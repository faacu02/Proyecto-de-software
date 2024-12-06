from flask import Blueprint, render_template, request, flash, session
from core.models.Pago import (
    create_Pago,
    find_pago,
    list_Pagos,
    list_pagos_pag,
    eliminar_pagos,
    update,
    buscarEntre,
)
from core.models.Equipo import list_equipo_dict, get_memberby_id
from web.handlers.auth import login_required, check
from datetime import datetime
from .validaciones import validar_numero, validar_opcion_seleccionada, validar_miembro

bp = Blueprint("pago", __name__, url_prefix="/pago")


@bp.get("/")
@login_required
@check("pagos_index")
def home_pago(fecha_ini=None, fecha_fin=None, tipo_pago=None, orden=None):
    """
    Renderiza la página principal de pagos.

    Esta función se encarga de mostrar la plantilla de inicio
    de pagos, incluyendo la lista de pagos existentes.

    Returns:
        str: Renderiza la plantilla de la página principal de pagos
              con la lista de pagos.
    """
    fecha_ini = request.args.get("fecha_inicio", None)
    fecha_fin = request.args.get("fecha_fin", None)
    tipo_pago = request.args.get("tipo_pago", None)
    orden = request.args.get("orden", None)
    current = request.args.get("page", 1, type=int)
    pagos = session.get("pagos_filt", list(list_Pagos()))
    todo = list_pagos_pag(pagos, 5, current)
    return render_template(
        "pagos/home.html",
        pagos=todo["pagos"],
        current_page=todo["current_page"],
        total_pages=todo["total_pages"],
        fecha_ini=fecha_ini,
        fecha_fin=fecha_fin,
        tipo_pago=tipo_pago,
        orden=orden,
    )


@bp.get("/crear_pago")
@login_required
@check("pagos_create")
def crear_pago():
    """
    Renderiza la plantilla para la creación de un nuevo pago.

    Esta función se encarga de mostrar el formulario para registrar
    un nuevo pago.

    Returns:
        str: Renderiza la plantilla para crear un pago.
    """
    return render_template("pagos/pagos.html")


@bp.get("/detalles_pago<int:id>")
@login_required
@check("pagos_show")
def detalles_pago(id):
    """
    Muestra los detalles de un pago específico.

    Esta función busca un pago por su ID y renderiza la plantilla
    correspondiente para mostrar sus detalles.

    Args:
        id (int): El identificador del pago.

    Returns:
        str: Renderiza la plantilla de detalles del pago.
    """
    return render_template("pagos/details.html", pago=find_pago(id))


@bp.post("/registrar_pago")
@login_required
@check("pagos_create")
def realizar_pago():
    """
    Registra un nuevo pago basado en los datos proporcionados en el formulario.

    Esta función obtiene los parámetros del formulario, busca el beneficiario
    si se proporciona un ID y crea un nuevo registro de pago. Luego,
    muestra un mensaje de éxito.

    Returns:
        str: Renderiza la plantilla de pagos con el estado actualizado.
    """
    try:
        params = request.form.to_dict()
        if not validar_numero(params["monto"]):
            return render_template("pagos/pagos.html")
        if not validar_opcion_seleccionada(
            params["tipo_pago"], ["honorario", "proveedor", "gastosVarios"]
        ):
            return render_template("pagos/pagos.html")
        if "beneficiario" in params.keys():
            if not validar_miembro(params["beneficiario"]):
                return render_template("pagos/pagos.html")
            member = get_memberby_id(params["beneficiario"])
            create_Pago(
                f"{member.nombre} {member.apellido}",
                params["monto"],
                params["tipo_pago"],
                params["descripcion"],
            )
        else:
            create_Pago(
                None, params["monto"], params["tipo_pago"], params["descripcion"]
            )
        flash(f"Pago registrado correctamente", "success")
        session.pop("pagos_filt", None)
        return render_template("pagos/pagos.html")
    except:
        flash("ocurrio un error", "error")
        home_pago()


@bp.post("/eliminarPago/<int:id>")
@login_required
@check("pagos_destroy")
def eliminar_pago(id):
    """
    Elimina un pago y actualiza la vista de pagos.

    Esta función elimina el pago especificado por su ID y
    renderiza la plantilla de la página de pagos actualizada.

    Args:
        id (int): El ID del pago a eliminar.

    Returns:
        str: Renderiza la plantilla de pagos con la lista actualizada.
    """
    eliminar_pagos(id)
    return render_template("pagos/home.html", pagos=list_Pagos())


@bp.get("/buscarEmpleados")
@login_required
@check("pagos_create")
def buscar_empleados():
    """
    Busca y devuelve una lista de empleados.

    Esta función obtiene el equipo de empleados en formato de diccionario.

    Returns:
        list: Una lista de empleados en formato de diccionario.
    """
    pagos_filtrados = list_equipo_dict()
    return pagos_filtrados


@bp.post("/update_pago/<int:id>")
@login_required
@check("pagos_update")
def update_pago(id):
    """
    Actualiza un pago existente en la base de datos.

    Esta función recibe los datos de un pago en formato JSON a través de una solicitud
    y actualiza el pago correspondiente en la base de datos.

    Args:
        id (int): El identificador del pago a actualizar.

    Returns:
        Response: Una respuesta de éxito o error dependiendo del resultado de la actualización.
    """

    data = request.get_json()

    tipo_pago = data.get("tipo_pago", None)
    beneficiario = data.get("beneficiario", None)
    monto = data.get("monto", None)
    descripcion = data.get("descripcion", None)
    monto = monto.split(".")[0]
    if tipo_pago != "honorario":
        beneficiario = None
    if not validar_numero(monto):
        return home_pago()
    if not validar_opcion_seleccionada(
        tipo_pago, ["honorario", "proveedor", "gastosVarios"]
    ):
        return home_pago()
    if beneficiario:
        if not validar_miembro(int(beneficiario)):
            return home_pago()
        benef = get_memberby_id(int(beneficiario))
        beneficiario = benef.nombre + " " + benef.apellido
    else:
        beneficiario = " "

    update(id, tipo_pago, monto, descripcion, beneficiario)
    return detalles_pago(data.get("id"))


@bp.get("/ordenarFecha")
@login_required
@check("pagos_index")
def filtrar_por_fechas():
    """
    Filtra los pagos según las fechas de inicio y fin, el tipo de pago y el orden.

    La función convierte las fechas proporcionadas de cadenas a objetos de fecha y
    llama a la función `buscarEntre` para obtener los pagos filtrados.

    Args:
        fecha_inicio (str): La fecha de inicio en formato 'YYYY-MM-DD'.
        fecha_fin (str): La fecha de fin en formato 'YYYY-MM-DD'.
        tipo_pago (str): El tipo de pago para filtrar.
        orden (str): El orden en que se deben devolver los resultados.

    Returns:
        Response: Renderiza la plantilla con los pagos filtrados si se ejecuta correctamente.

    Raises:
        Exception: Si ocurre un error durante el proceso de filtrado.
    """
    try:
        session.pop("pagos_filt", None)
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)
        tipo_pago = request.args.get("tipo_pago", None)
        orden = request.args.get("orden", None)
        print(fecha_inicio, fecha_fin, tipo_pago, orden)
        if fecha_inicio and fecha_fin:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            pagos = buscarEntre(fecha_inicio_dt, fecha_fin_dt, tipo_pago, orden)
        else:
            pagos = buscarEntre(0, 0, tipo_pago, orden)
        session["pagos_filt"] = pagos
        return home_pago(
            fecha_ini=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_pago=tipo_pago,
            orden=orden,
        )
    except Exception as e:
        return {"error": f"Se produjo un error al filtrar los pagos: {str(e)}"}
