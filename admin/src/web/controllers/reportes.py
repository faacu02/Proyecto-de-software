from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Response,
)
from .validaciones import (
    validar_campos_obligatorios,
    validar_numeros,
    validar_anio_anterior,
    validar_JA,
    validar_fechas, 
    validar_fecha_anterior,
)
from web.handlers.auth import check, login_required, blocked_user
import matplotlib

matplotlib.use("Agg")  # Selecciona el backend 'Agg' para evitar problemas con tkinter
import matplotlib.pyplot as plt
from core.models import Legajo as legajoDB
import io
from core.models import Cobro as CobroDB

MEDIOS_DE_PAGO = {
    "tarjeta_credito": "Tarjeta de Crédito",
    "tarjeta_debito": "Tarjeta de Débito",
    "efectivo": "Efectivo",
    "transferencia": "Transferencia",
    "otro": "Otro"
}
app = Flask(__name__)

bp = Blueprint("reportes", __name__, url_prefix="/reportes")


@bp.get("/")
@login_required
@blocked_user
@check("reportes_index")
def reportes_home():
    """
    Muestra la página principal de reportes.
    """
    return render_template("reportes/reportes.html", JAs=legajoDB.list_legajos())


@bp.get("/becados")
@login_required
@blocked_user
@check("reportes_show")
def JA_becados():
    """
    Muestra la pagina donde esta el grafico de J&A becados.
    """
    return render_template("reportes/grafico_beca.html",JAs=legajoDB.list_legajos())


@bp.get("/tipoDiscapacidad")
@login_required
@blocked_user
@check("reportes_show")
def JA_tipo_discapacidad():
    """
    Muestra la pagina donde esta el grafico de la cantidad de los JA con los tipo de discapacidad distintos
    """
    return render_template("reportes/grafico_tipo_discapacidad.html",JAs=legajoDB.list_legajos())


@bp.get("/gananciasAnuales/:anio")
@login_required
@blocked_user
@check("reportes_show")
def ganancias():
    """
    Muestra la pagina con el gráfico de ganancias anuales para un año específico.
    El año se obtiene como parámetro de la URL.

    Parámetros:
        anio: Año para el cual se generará el reporte.
    """
    datos = request.args.to_dict()
    if not validar_campos_obligatorios(datos, ["anio"]):
        return redirect(url_for("reportes.reportes_home"))
    if not validar_numeros(datos, ["anio"]):
        return redirect(url_for("reportes.reportes_home"))
    if not validar_anio_anterior(int(datos["anio"])):
        return redirect(url_for("reportes.reportes_home"))
    return render_template("reportes/grafico_ganancias.html", anio=datos["anio"],JAs=legajoDB.list_legajos())


@bp.get("/reporteCobros")
@login_required
@blocked_user
@check("reportes_show")
def reporte_cobros():
    """
    Muestra la pagina con reporte histórico de cobros en un rango de fechas asociado a una persona.
    Parámetros:
        anio: Año para el cual se generará el reporte.
    """
    datos = request.args.to_dict()
    fecha_inicio = datos.get("fecha_inicio","")
    fecha_fin = datos.get("fecha_fin","")
    JA_Ref = datos.get("ja_id","")  
    if not validar_campos_obligatorios(datos, ["ja_id"]):
        return redirect(url_for("reportes.reportes_home"))
    if not validar_JA(JA_Ref):
        return redirect(url_for("reportes.reportes_home"))
    if fecha_inicio :
        if not validar_fecha_anterior(datos, ["fecha_inicio"]):
            return redirect(url_for("reportes.reportes_home"))
        fecha_inicio = datetime.strptime(datos["fecha_inicio"], "%Y-%m-%d")
    if fecha_inicio and fecha_fin:
        if not validar_fechas(datos["fecha_inicio"], datos["fecha_fin"]):
            return redirect(url_for("reportes.reportes_home"))
    if fecha_fin:
        fecha_fin = datetime.strptime(datos["fecha_fin"], "%Y-%m-%d")
    cobros = CobroDB.filtro_api(fecha_inicio,fecha_fin,JA_Ref)
    for cobro in cobros:
        cobro.fecha_pago = cobro.fecha_pago.strftime("%Y-%m-%d")
        cobro.medio_pago = MEDIOS_DE_PAGO.get(cobro.medio_pago, cobro.medio_pago)
    return render_template("reportes/reporte_cobro.html", cobros=cobros,JAs=legajoDB.list_legajos())


@bp.get("/gananciasGraph/:anio")
@login_required
@blocked_user
@check("reportes_show")
def ganancias_graph():
    """
    Genera un gráfico de barras de ganancias mensuales para un año específico.
    El año se obtiene como parámetro de la URL y los datos se extraen de los registros de cobros.

    Parámetros:
        anio: Año para el cual se generará el gráfico.

    Retorna:
        Response: Imagen del gráfico en formato PNG.
    """
    data = request.args.to_dict()
    anio = request.args.get("anio")
    if not validar_campos_obligatorios(data, ["anio"]):
        return redirect(url_for("reportes.reportes_home"))
    if not validar_numeros(data, ["anio"]):
        return redirect(url_for("reportes.reportes_home"))
    Cobros = CobroDB.list_Cobros_all()
    count = [0] * 12  # Lista para acumular montos (12 meses)

    for cobro in Cobros:

        if cobro.fecha_pago.year == int(anio):

            mes = cobro.fecha_pago.month  # Obtiene el mes del pago
            count[mes - 1] += float(
                cobro.monto
            )  # Restamos 1 para ajustar al índice de la lista

    # print(count)
    fig, ax = plt.subplots(figsize=(16, 9))

    barras = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    counts = count
    bar_colors = ["tab:red"]

    ax.bar(barras, counts, color=bar_colors)
    st = "Ganancias Anuales por Mes, del año " + anio
    ax.set_ylabel("Ganancias por Mes")
    ax.set_title(st)

    # plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return Response(buf, mimetype="image/png")


@bp.get("/becadosGraph")
@login_required
@blocked_user
@check("reportes_show")
def JA_becados_graph():
    """
    Genera un gráfico de barras que muestra la cantidad de J&A becados y no becados.

    Retorna:
        Response: Imagen del gráfico en formato PNG.
    """
    legajos = legajoDB.list_legajos()
    count_becas = len([legajo for legajo in legajos if legajo.becado])
    count_no_becas = len([legajo for legajo in legajos if not legajo.becado])

    fig, ax = plt.subplots(figsize=(16, 9))

    barras = ["J&A Becados", "J&A no Becados"]
    counts = [count_becas, count_no_becas]
    bar_colors = ["tab:red", "tab:blue"]

    ax.bar(barras, counts, color=bar_colors)

    ax.set_ylabel("Cantidad de J&As")
    ax.set_title("Cantidad de J&As becados y no becados")

    # plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return Response(buf, mimetype="image/png")


@bp.get("/tipoDiscapacidadGraph")
@login_required
@blocked_user
@check("reportes_show")
def JA_tipo_discapacidad_graph():
    """
    Genera un gráfico de barras que muestra la distribución de tipos de discapacidad en J&A.

    Retorna:
        Response: Imagen del gráfico en formato PNG.
    """
    legajos = legajoDB.list_legajos()
    count_mental = len(
        [legajo for legajo in legajos if legajo.tipo_discapacidad == "Mental"]
    )
    count_motora = len(
        [legajo for legajo in legajos if legajo.tipo_discapacidad == "Motora"]
    )
    count_sensorial = len(
        [legajo for legajo in legajos if legajo.tipo_discapacidad == "Sensorial"]
    )
    count_viseral = len(
        [legajo for legajo in legajos if legajo.tipo_discapacidad == "Visceral"]
    )
    fig, ax = plt.subplots(figsize=(16, 9))
    barras = ["Mental", "Motroa", "Sensorial", "Viseral"]
    counts = [count_mental, count_motora, count_sensorial, count_viseral]
    bar_colors = ["tab:red", "tab:blue", "tab:green", "tab:orange"]

    ax.bar(barras, counts, color=bar_colors)

    ax.set_ylabel("Cantidad de J&As")
    ax.set_title("Cantidad de J&As con su tipo de discapacidad")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return Response(buf, mimetype="image/png")

    # Reportes


@bp.get("/deudores")
@login_required
@blocked_user
@check("reportes_show")
def get_deudores():
    """
    Muestra un reporte de J&A con deudas.

    Retorna:
        Template: Página HTML con la lista de deudores.
    """
    legajos = legajoDB.list_legajos()
    deudores = []
    for legajo in legajos:
        if legajo.deuda:
            deudores.append(legajo)
    return render_template("reportes/deudores.html", deudores=deudores,JAs=legajoDB.list_legajos())


@bp.get("/propuestas_trabajo")
@login_required
@blocked_user
@check("reportes_show")
def get_best_propuesta_trabajo():
    """
    Muestra un reporte de las propuestas de trabajo con su respectiva cantidad, ordenadas de mayor a menor.

    Retorna:
        Template: Página HTML con las propuestas ordenadas.
    """
    legajos = legajoDB.list_legajos()
    count = {}
    for legajo in legajos:
        if legajo.propuesta_trabajo in count:
            count[legajo.propuesta_trabajo] += 1
        else:
            count[legajo.propuesta_trabajo] = 1
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return render_template("reportes/propuestas_trabajo.html", count=sorted_count,JAs=legajoDB.list_legajos())
