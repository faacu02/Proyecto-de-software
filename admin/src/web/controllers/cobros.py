"""Este modulo se encarga de controlar todo lo relacionado con los cobros"""

from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from core.models import Equipo as equipoDB
from core.models import Cobro as CobroDB
from core.models import Legajo as legajoDB
from web.handlers.auth import check, login_required
from .validaciones import (
    validar_numeros,
    validar_fechas,
    validar_solo_letras,
    validar_fecha_anterior,
    validar_miembro,
    validar_JA,
    validar_opcion_seleccionada,
    validar_Cobro,
)

MEDIOS_DE_PAGO = {
    "tarjeta_credito": "Tarjeta de Crédito",
    "tarjeta_debito": "Tarjeta de Débito",
    "efectivo": "Efectivo",
    "transferencia": "Transferencia",
    "otro": "Otro",
}
app = Flask(__name__)

bp = Blueprint("cobro", __name__, url_prefix="/cobro")


@bp.get("/")
@login_required
@check("cobro_index")
def cobro_page():
    """
    Renderiza la página que muestra todos los cobros registrados en la base de datos.

    Returns:
        El contenido HTML de la página de cobros.
    """
    cobros = CobroDB.list_Cobros()
    for cobro in cobros:
        cobro.fecha_pago = cobro.fecha_pago.strftime("%Y-%m-%d")
        cobro.medio_pago = MEDIOS_DE_PAGO.get(cobro.medio_pago, cobro.medio_pago)
    return render_template("cobro/cobros.html", cobros=cobros)


@bp.get("/registrarCobro")
@login_required
@check("cobro_create")
def registrar_cobro_page():
    """
    Renderiza el formulario para registrar un nuevo cobro con los datos necesarios.

    Returns:
        str: El contenido HTML de la página para registrar un cobro.
    """
    miembros = equipoDB.list_equipo()
    JAs = legajoDB.list_legajos()
    return render_template("cobro/registrarCobro.html", miembros=miembros, JAs=JAs)


@bp.post("/registrarCobro")
@login_required
@check("cobro_create")
def registrar_cobro():
    """
    Registra un nuevo cobro en la base de datos.

    Returns:
        Redirige a la página de cobros después de registrar el cobro.
    """
    datos = request.form.to_dict()
    # Validaciones
    if not validar_numeros(datos, ["monto"]):
        return redirect(url_for("cobro.registrar_cobro_page"))
    if not validar_fecha_anterior(datos, ["fecha_pago"]):
        return redirect(url_for("cobro.registrar_cobro_page"))
    if not validar_miembro(datos["receptor"]):
        return redirect(url_for("cobro.registrar_cobro_page"))
    if not validar_JA(datos["JyA_ref"]):
        return redirect(url_for("cobro.registrar_cobro_page"))
    if not validar_opcion_seleccionada(
        datos["medio_pago"],
        ["efectivo", "tarjeta_credito", "tarjeta_debito", "transferencia", "otro"],
    ):
        return redirect(url_for("cobro.registrar_cobro_page"))
    if CobroDB.create_Cobro(**datos):  # Crea en la bsae dedatos el nuevo cobro
        flash("Cobro registrado exitosamente", "success")
    else:
        flash("Hubo un error al intentar registrar el cobro", "error")
    return redirect(url_for("cobro.filtrar_cobros"))


@bp.get("/filtrar")
@login_required
@check("cobro_index")
def filtrar_cobros():
    """
    Filtra y ordena los cobros mostrados en la página de cobros.

    Realiza filtros y ordenamientos basados en los parámetros recibidos
    en la solicitud GET, incluyendo filtros por medio de pago, nombre,
    apellido y fechas. También valida los parámetros antes de aplicar
    los filtros para asegurar la consistencia de los datos.

    Returns:
        Renderiza la vista con los cobros filtrados y ordenados.
    """
    filtro_mp = request.args.get("medio_pago", "")  # Filtro por tipo J&A
    columna_orden = request.args.get("Orden", "fecha_pago")  # Ordenar por columna
    direccion_orden = request.args.get(
        "direccion", "Ascendente"
    )  # Ascendente o descendente
    # busqueda = request.args.get("busqueda")
    # valor_busqueda = request.args.get("valor_busqueda")
    apellido = request.args.get("apellido")
    nombre = request.args.get("nombre")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    page = request.args.get("page", 1, type=int)
    datos = request.args.to_dict()
    # Validaciones
    if apellido:
        if not validar_solo_letras(datos, ["apellido"]):
            return redirect(url_for("cobro.filtrar_cobros"))
    if nombre:
        if not validar_solo_letras(datos, ["nombre"]):
            return redirect(url_for("cobro.filtrar_cobros"))
    if fecha_fin:
        if not validar_fecha_anterior(datos, ["fecha_fin"]):
            return redirect(url_for("cobro.filtrar_cobros"))
    if fecha_inicio:
        if not validar_fecha_anterior(datos, ["fecha_inicio"]):
            return redirect(url_for("cobro.filtrar_cobros"))
    if fecha_fin and fecha_inicio:
        if not validar_fechas(fecha_inicio, fecha_fin):
            return redirect(url_for("cobro.filtrar_cobros"))
    if filtro_mp:
        if not validar_opcion_seleccionada(
            filtro_mp,
            ["efectivo", "tarjeta_credito", "tarjeta_debito", "transferencia", "otro"],
        ):
            return redirect(url_for("cobro.filtrar_cobros"))

    cobros = CobroDB.find_cobros_by_fields(
        nombre=nombre,
        apellido=apellido,
        filtro_mp=filtro_mp,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        orden=direccion_orden == "Ascendente",
        orden_by=columna_orden,
        page=page,
        per_page=2,
    )
    for cobro in cobros:
        cobro.fecha_pago = cobro.fecha_pago.strftime("%Y-%m-%d")
        cobro.medio_pago = MEDIOS_DE_PAGO.get(cobro.medio_pago, cobro.medio_pago)
    # flash("Filtros y ordenaciones aplicados correctamente", "success")
    # Renderizar la vista con los resultados filtrados y ordenados
    return render_template("cobro/cobros.html", cobros=cobros)


@bp.get("/deudas")
@login_required
@check("cobro_index")
def deudas_page():
    """
    Renderiza la página que muestra todos los registros y su estado de deuda.

    Muestra una lista de registros (J&A) y si están en deuda o no.

    Returns:
        Renderiza la plantilla de deudas.html con los registros cargados.
    """
    JAs = legajoDB.list_legajos()
    return render_template("cobro/deudas.html", JAs=JAs)


@bp.post("/deudas/<int:id>")
@login_required
@check("cobro_update")
def marcar_deuda(id):
    """
    Marca como verdadera o falsa la deuda de un registro específico.

    Modifica el estado de deuda de un registro (JA) en base al valor
    recibido en el formulario.

    Args:
        id (int): ID del registro al cual se le modificará su estado de deuda.

    Returns:
        Redirige a la página de deudas con un mensaje de éxito o error.
    """
    if not validar_opcion_seleccionada(request.form.get("deuda"), ["true", None]):
        return redirect(url_for("cobro.deudas_page"))
    deuda_estado = request.form.get("deuda") == "true"
    # Llamar al método de modelo para actualizar el estado de deuda
    if legajoDB.actualizar_deuda(id, deuda_estado):
        flash("Deuda actualizada exitosamente", "success")
    else:
        flash("Error al actualizar la deuda", "error")
    return redirect(url_for("cobro.deudas_page"))


@bp.post("/borrar_cobro/<int:id>")
@login_required
@check("cobro_destroy")
def borrar_cobro(id):
    """
    Realiza el borrado lógico de un cobro.

    Marca un cobro como eliminado en la base de datos sin eliminarlo
    físicamente.

    Args:
        id (int): ID del cobro a eliminar.

    Returns:
        Redirige a la página de cobros después de borrar el cobro.
    """
    if not validar_Cobro(id):
        return redirect(url_for("cobro.filtrar_cobros"))
    if CobroDB.delete_cobro(id):
        flash("Cobro borrado exitosamente")
    else:
        flash("Hubo un error al intentar borrar el cobro", "error")
    return redirect(url_for("cobro.filtrar_cobros"))


@bp.get("/editar_cobro/<int:id>")
@login_required
@check("cobro_update")
def editar_cobro(id):
    """
    Muestra la página para editar un cobro específico.

    Carga los datos necesarios para modificar el cobro, incluyendo los
    miembros y registros (J&A) disponibles.

    Args:
        id (int): ID del cobro a modificar.

    Returns:
        Renderiza la plantilla para modificar el cobro con los datos cargados.
    """
    cobro = CobroDB.get_cobro_by_id(id)
    miembros = equipoDB.list_equipo()
    JAs = legajoDB.list_legajos()
    return render_template(
        "cobro/modificarCobro.html", cobro=cobro, miembros=miembros, JAs=JAs
    )


@bp.post("/editar_cobro/<int:id>")
@login_required
@check("cobro_update")
def editar_cobro_POST(id):
    """
    Procesa la modificación de un cobro específico.

    Valida los datos recibidos del formulario y actualiza el cobro en la
    base de datos si los datos son válidos.

    Args:
        id (int): ID del cobro a modificar.

    Returns:
        Redirige a la página de cobros después de la modificación.
    """
    datos = request.form.to_dict()
    # Validaciones
    if not validar_numeros(datos, ["monto"]):
        return redirect(url_for("cobro.cobro_update"))
    if not validar_fecha_anterior(datos, ["fecha_pago"]):
        return redirect(url_for("cobro.cobro_update"))
    if not validar_miembro(datos["receptor"]):
        return redirect(url_for("cobro.cobro_update"))
    if not validar_JA(datos["JyA_ref"]):
        return redirect(url_for("cobro.cobro_update"))
    if not validar_opcion_seleccionada(
        datos["medio_pago"],
        ["efectivo", "tarjeta_credito", "tarjeta_debito", "transferencia", "otro"],
    ):
        return redirect(url_for("cobro.cobro_update"))
    if CobroDB.modificar_cobro(id, **datos):
        flash("Cobro modificado exitosamente", "success")
    else:
        flash("Hubo un error al intentar modificar el cobro", "error")
    return redirect(url_for("cobro.filtrar_cobros"))
