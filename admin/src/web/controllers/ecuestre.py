from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    flash,
    current_app as appe,
)
from core.models import Equipo as equipoDB
from core.models import Encuestre as EncuestreDB
from web.handlers.auth import check, login_required, blocked_user
from core.models import Documento_externo_Ecuestre as DocDB
from datetime import datetime
from core.models import Encuestres_Equipo as ecuestre_equipoDB
from .validaciones import (
    validar_fechas,
    validar_fecha_anterior,
    validar_opcion_seleccionada,
    validar_conductor_o_entrenador,
    validar_extension,
    validar_tamano,
    validar_Ecuestre,
    validar_campos_obligatorios,
)
from os import fstat
import urllib.parse

EXTENSIONES_PERMITIDAS = ["pdf", "doc", "xls", "jpeg"]
TIPOS_JA = {
    "hipoterapia": "Hipoterapia",
    "monta_terapeutica": "Monta Terapéutica",
    "deporte_ecuestre_adaptado": "Deporte Ecuestre Adaptado",
    "actividades_recreativas": "Actividades Recreativas",
    "equitacion": "Equitación",
}

TIPOS_DOC = {
    "carga_imagenes": "Carga de Imagenes",
    "informe_evolucion": "Informe de Evolucion",
    "ficha_general": "Ficha General",
    "planificacion_entrenamiento": "Planificacion de Entrenamiento",
    "registro_veterinario": "Registro Veterinario",
}
app = Flask(__name__)

bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bp.get("/")
@login_required
@blocked_user
@check("ecuestre_index")
def ecuestre_page():
    """Renderiza la página principal de ecuestres."""
    page = request.args.get("page", 1, type=int)
    ecuestres = EncuestreDB.list_encuestres(page=page, per_page=2)
    for ecuestre in ecuestres:
        # Formateo de fechas
        ecuestre.fecha_ingreso = ecuestre.fecha_ingreso.strftime("%Y-%m-%d")
        ecuestre.fecha_nacimiento = ecuestre.fecha_nacimiento.strftime("%Y-%m-%d")

        # Formateo del tipo de J&A
        ecuestre.tipo_JA = TIPOS_JA.get(ecuestre.tipo_JA, ecuestre.tipo_JA)
    return render_template("ecuestre/ecuestre.html", ecuestres=ecuestres)


@bp.get("/registroEcuestre")
@login_required
@blocked_user
@check("ecuestre_create")
def ecuestre_register_page():
    """Renderiza la página de registro de un nuevo ecuestre."""
    equipos = equipoDB.list_equipo()
    equipos = [
        equipo
        for equipo in equipos
        if equipo.puesto_laboral in ["Conductor", "Entrenador de Caballos"]
    ]
    return render_template("ecuestre/registroEcuestre.html", equipos=equipos)


@bp.post("/register")
@login_required
@blocked_user
@check("ecuestre_create")
def ecuestre_register():
    """
    Registra un nuevo ecuestre en la base de datos.

    Se valida el formulario y se guarda tanto la información del ecuestre como
    los archivos subidos o enlaces proporcionados.
    """
    datos = request.form.to_dict()
    client = appe.storage.client
    client = appe.storage.client
    entrenadores_conductores_ids = request.form.getlist("entrenadores_conductores_id")
    datosDoc = {}
    datosArchivos = {}
    required_fields = [
        "nombre",
        "fecha_nacimiento",
        "sexo",
        "raza",
        "pelaje",
        "comprado",
        "fecha_ingreso",
        "tipo_JA",
    ]
    if not validar_campos_obligatorios(datos, required_fields):
        return redirect(url_for("ecuestre.ecuestre_register_page"))
    # validaciones
    if not validar_fecha_anterior(datos, ["fecha_nacimiento", "fecha_ingreso"]):
        return redirect(url_for("ecuestre.ecuestre_register_page"))
    if not validar_fechas(datos["fecha_nacimiento"], datos["fecha_ingreso"]):
        return redirect(url_for("ecuestre.ecuestre_register_page"))
    if not validar_opcion_seleccionada(datos["comprado"], ["True", "False"]):
        return redirect(url_for("ecuestre.ecuestre_register_page"))
    if not validar_conductor_o_entrenador(entrenadores_conductores_ids):
        return redirect(url_for("ecuestre.ecuestre_register_page"))
    if datos["comprado"] == "True":
        datos["comprado"] = True
    else:
        datos["comprado"] = False
    if not validar_opcion_seleccionada(
        datos["tipo_JA"],
        [
            "hipoterapia",
            "monta_terapeutica",
            "deporte_ecuestre_adaptado",
            "actividades_recreativas",
            "equitacion",
        ],
    ):
        return redirect(url_for("ecuestre.ecuestre_register_page"))
    campos_a_ignorar = [
        "ficha_general",
        "planificacion_entrenamiento",
        "informe_evolucion",
        "carga_imagenes",
        "registro_veterinario",
    ]
    datosEnlace = {}
    datosTipo = {}
    for campo in campos_a_ignorar:
        datosArchivos[campo] = datos.pop(campo, None)
        datosTipo[campo] = datos.pop(f"tipo_subida_{campo}", None)
        datosEnlace[campo] = datos.pop(f"enlace_{campo}", None)

    ecuestre = EncuestreDB.create_doc(**datos)

    # Registrar files y o enlaces subidos
    for campo in campos_a_ignorar:
        if datosTipo[campo]:
            if not validar_opcion_seleccionada(datosTipo[campo], ["archivo", "link"]):
                return redirect(url_for("ecuestre.ecuestre_register_page"))
        if datosTipo[campo] == "archivo":
            if campo in request.files:
                fileTitulo = request.files[campo]
                if fileTitulo:
                    if validar_extension(
                        fileTitulo.filename, EXTENSIONES_PERMITIDAS
                    ) and validar_tamano(fstat(fileTitulo.fileno()).st_size):
                        size = fstat(fileTitulo.fileno()).st_size
                        client.put_object(
                            "grupo20",
                            f"{ecuestre.id}_titulo_{fileTitulo.filename}",
                            fileTitulo,
                            size,
                            content_type=fileTitulo.content_type,
                        )
                        datosDoc["titulo"] = (
                            f"{ecuestre.id}_titulo_{fileTitulo.filename}"
                        )
                        datosDoc["tipo"] = campo
                        datosDoc["encuestre_id"] = ecuestre.id
                        datosDoc["fecha_subida"] = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        datosDoc["esURL"] = False
                        DocDB.create_doc(**datosDoc)
                    else:
                        return redirect(url_for("ecuestre.FiltrarEcuestres"))
        else:  # Si se eligió ingresar un enlace
            enlace = datosEnlace[campo]
            if enlace:
                datosDoc["titulo"] = enlace
                datosDoc["tipo"] = campo
                datosDoc["encuestre_id"] = ecuestre.id
                datosDoc["fecha_subida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                datosDoc["esURL"] = True
                DocDB.create_doc(**datosDoc)
    # Registrar la relación de entrenadores o conductores
    for equipo_id in entrenadores_conductores_ids:
        ecuestre_equipoDB.create_relacion(encuestre_id=ecuestre.id, equipo_id=equipo_id)
    flash("Ecuestre registrado de manera correcta.")
    return redirect(url_for("ecuestre.FiltrarEcuestres"))


@bp.post("/subirArchivo/<int:id>")
@login_required
@blocked_user
@check("ecuestre_update")
def subir_archivo(id):
    """
    Sube un archivo o enlace asociado a un ecuestre específico.

    Args:
        id (int): El ID del ecuestre al que se sube el archivo.
    """
    campos = [
        "ficha_general",
        "planificacion_entrenamiento",
        "informe_evolucion",
        "carga_imagenes",
        "registro_veterinario",
    ]
    datos = request.form.to_dict()
    datosDoc = {}
    datosDoc["nombre"] = datos["nombre"]
    datosDoc["tipo"] = datos["tipo_archivo"]
    datosDoc["encuestre_id"] = id
    datosDoc["fecha_subida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Validaciones
    if not validar_Ecuestre(id):
        return redirect(url_for("ecuestre.FiltrarEcuestres"))
    if not validar_opcion_seleccionada(datosDoc["tipo"], campos):
        return redirect(url_for("ecuestre.archivos", id=id))
    if not validar_opcion_seleccionada(datos["tipo_subida"], ["archivo", "link"]):
        return redirect(url_for("ecuestre.archivos", id=id))
    if not validar_campos_obligatorios(datos, ["nombre"]):
        return redirect(url_for("ecuestre.archivos", id=id))
    # registrar file
    if datos["tipo_subida"] == "archivo":
        if not validar_opcion_seleccionada(datos["tipo_archivo"], campos):
            return redirect(url_for("ecuestre.archivos", id=id))
        fileTitulo = request.files["archivo"]
        if fileTitulo:
            if validar_extension(
                fileTitulo.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileTitulo.fileno()).st_size):
                size = fstat(fileTitulo.fileno()).st_size
                client = appe.storage.client
                client.put_object(
                    "grupo20",
                    f"{id}_titulo_{fileTitulo.filename}",
                    fileTitulo,
                    size,
                    content_type=fileTitulo.content_type,
                )
                datosDoc["titulo"] = f"{id}_titulo_{fileTitulo.filename}"
                datosDoc["esURL"] = False
                DocDB.create_doc(**datosDoc)
            else:
                return redirect(url_for("ecuestre.ecuestre_register"))
    # Registrar Enlace
    elif datos["tipo_subida"] == "link":
        datosDoc["titulo"] = datos["enlace"]
        datosDoc["esURL"] = True
        DocDB.create_doc(**datosDoc)
    flash("Archivo subido correctamente.")
    return redirect(url_for("ecuestre.archivos", id=id))


@bp.get("/archivos/<int:id>")
@login_required
@blocked_user
@check("ecuestre_show")
def archivos(id):
    """
    Muestra los archivos asociados a un ecuestre específico, con opción de filtrado.

    Args:
        id (int): El ID del ecuestre.
    """
    ecuestre = EncuestreDB.get_Ecuestre_by_id(id)
    campos = [
        "ficha_general",
        "planificacion_entrenamiento",
        "informe_evolucion",
        "carga_imagenes",
        "registro_veterinario",
    ]
    # Obtener los filtros y parámetros de ordenamiento desde la solicitud GET
    titulo = request.args.get("titulo", "")
    tipo = request.args.get("tipo", "")
    order_by = request.args.get("order_by", "titulo")
    order_direction = request.args.get("order_direction", "asc")
    if not validar_Ecuestre(id):
        return redirect(url_for("ecuestre.FiltrarEcuestres"))
    if tipo:
        if not validar_opcion_seleccionada(tipo, campos):
            return redirect(url_for("ecuestre.archivos", id=id))
    if not validar_opcion_seleccionada(order_by, ["titulo", "fecha_subida"]):
        return redirect(url_for("ecuestre.archivos", id=id))
    if not validar_opcion_seleccionada(order_direction, ["asc", "desc"]):
        return redirect(url_for("ecuestre.archivos", id=id))
    # Llamar al modelo para obtener los documentos filtrados
    documentos = DocDB.buscar_documentos(
        ecuestre_id=id,
        titulo=titulo,
        tipo=tipo,
        order_by=order_by,
        order_direction=order_direction,
    )
    for doc in documentos:
        doc.tipo = TIPOS_DOC[doc.tipo]
    # Renderizar la vista con los documentos filtrados
    return render_template(
        "ecuestre/verArchivos.html", ecuestre=ecuestre, documentos=documentos
    )


@bp.get("DescargarArchivo/<int:id>")
@login_required
@blocked_user
@check("ecuestre_show")
def download_file(id):
    """
    Si el archivo es un file en minio
    Genera una URL para descargar un archivo desde el bucket.

    Esta función obtiene el archivo correspondiente al ID proporcionado,
    genera una URL para la descarga desde el bucket de almacenamiento.
    Si el archivo es un enlace externo, redirige directamente a dicho enlace.

    Args:
        id (int): El ID del documento a descargar.

    Returns:
        Redirecciona a la URL de descarga del archivo.
    """
    doc = DocDB.get_documento_by_id(id)
    if doc:
        if doc.esURL:
            return redirect(doc.titulo)
        else:
            filename = doc.titulo
            client = appe.storage.client
            bucket_name = "grupo20"
            filename = urllib.parse.unquote(filename)
            url = client.presigned_get_object(bucket_name, filename)
            return redirect(url)
    else:
        return redirect(url_for(("ecuestre.ecuestre_register_page")))


@bp.post("/delete_archivo/<int:id>/<int:idE>")
@login_required
@blocked_user
@check("ecuestre_destroy")
def borrar_archivo(id, idE):
    """
    Elimina un archivo asociado a un ecuestre.

    Args:
        id (int): El ID del archivo a eliminar.
        idE (int): El ID del ecuestre asociado al archivo.

    Returns:
        Redirecciona a la página de archivos del ecuestre.
    """
    if eliminar_file(id):
        flash("Archivo borrado exitosamente.")
    return redirect(url_for("ecuestre.archivos", id=idE))


def eliminar_file(id):
    """
    Elimina un documento de la base de datos y, si es un archivo físico, lo elimina del almacenamiento externo.

    Args:
        id (int): El ID del documento a eliminar.

    Returns:
        bool: True si el documento fue eliminado exitosamente de la base de datos, False si no se encontró el documento.
    """
    doc = DocDB.get_documento_by_id(id)
    if doc:
        if not doc.esURL:
            client = appe.storage.client
            client.remove_object("grupo20", doc.titulo)
    return DocDB.eliminar_documento(id)


@bp.route("/eliminarEcuestre/<int:id>", methods=["POST"])
@login_required
@blocked_user
@check("ecuestre_destroy")
def borrarEcuestre(id):
    """
    Elimina un ecuestre de la base de datos.

    Args:
        id (int): El ID del ecuestre a eliminar.

    Returns:
        Redirecciona a la página principal de ecuestres.
    """
    archivos = DocDB.list_documentos_ecuestre(id)
    for archivo in archivos:
        eliminar_file(archivo.id)
    ecuestre = EncuestreDB.delete_Ecuestre(id)
    if ecuestre:
        flash("Ecuestre borrado exitosamente.")
    return redirect(url_for("ecuestre.FiltrarEcuestres"))


@bp.route("/ModificarEcuestre/<int:id>", methods=["Get"])
@login_required
@blocked_user
@check("ecuestre_update")
def GetModificarEcuestre(id):
    """
    Renderiza el formulario para modificar un ecuestre.

    Args:
        id (int): El ID del ecuestre a modificar.

    Returns:
        Renderizá la plantilla de modificación de ecuestre.
    """
    ecuestre = EncuestreDB.get_Ecuestre_by_id(id)
    equipos = equipoDB.list_equipo()
    equipos = [
        equipo
        for equipo in equipos
        if equipo.puesto_laboral in ["Conductor", "Entrenador de Caballos"]
    ]
    equipos_asociados_ids = ecuestre_equipoDB.get_ids_equipos_asociados(id)
    return render_template(
        "ecuestre/modificarEcuestre.html",
        ecuestre=ecuestre,
        equipos=equipos,
        equipos_asociados_ids=equipos_asociados_ids,
    )


@bp.route("/ModificarEcuestre/<int:id>", methods=["POST"])
@login_required
@blocked_user
@check("ecuestre_update")
def PostModificarEcuestre(id):
    """
    Modifica los detalles de un ecuestre en la base de datos.

    Se realizan validaciones en los campos de entrada y se actualizan tanto
    los datos del ecuestre como las relaciones con los entrenadores/conductores.

    Args:
        id (int): El ID del ecuestre a modificar.

    Returns:
        Redirecciona a la página principal de ecuestres.
    """
    datos = request.form.to_dict()
    entrenadores_conductores_ids = request.form.getlist("entrenadores_conductores_id")
    # validaciones
    required_fields = [
        "nombre",
        "fecha_nacimiento",
        "sexo",
        "raza",
        "pelaje",
        "comprado",
        "fecha_ingreso",
        "tipo_JA",
    ]
    if not validar_campos_obligatorios(datos, required_fields):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if not validar_fecha_anterior(datos, ["fecha_nacimiento", "fecha_ingreso"]):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if not validar_fechas(datos["fecha_nacimiento"], datos["fecha_ingreso"]):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if not validar_opcion_seleccionada(datos["comprado"], ["True", "False"]):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if not validar_opcion_seleccionada(datos["sexo"], ["M", "F"]):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if not validar_conductor_o_entrenador(entrenadores_conductores_ids):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if not validar_opcion_seleccionada(
        datos["tipo_JA"],
        [
            "hipoterapia",
            "monta_terapeutica",
            "deporte_ecuestre_adaptado",
            "actividades_recreativas",
            "equitacion",
        ],
    ):
        return redirect(url_for("ecuestre.GetModificarEcuestre", id=id))
    if datos["comprado"] == "True":
        datos["comprado"] = True
    else:
        datos["comprado"] = False
    if EncuestreDB.modificar_ecuestre(id, **datos):
        flash("Ecuestre modificado correctamente.")
    ecuestre_equipoDB.actualizar_relaciones(id, entrenadores_conductores_ids)
    return redirect(url_for("ecuestre.FiltrarEcuestres"))


@bp.route("/filtrar", methods=["GET"])
@login_required
@blocked_user
@check("ecuestre_index")
def FiltrarEcuestres():
    """
    Filtra y ordena la lista de ecuestres según los parámetros de búsqueda.

    Args:
        Ninguno, los parámetros se obtienen desde la URL.

    Returns:
        Renderizá de la plantilla con la lista de ecuestres filtrada y ordenada.
    """
    datos = request.args.to_dict()
    filtro_ja = request.args.get("filtroJA", "")
    columna_orden = request.args.get("orden_by", "FechaNacimiento")
    direccion_orden = request.args.get("orden", "Ascendente")
    filtro_nombre = request.args.get("nombre", "").strip()
    orden = direccion_orden == "Ascendente"
    page = request.args.get("page", 1, type=int)

    if not validar_opcion_seleccionada(
        columna_orden, ["FechaNacimiento", "FechaIngreso", "Nombre"]
    ):
        return redirect(url_for("ecuestre.FiltrarEcuestres"))
    if not validar_opcion_seleccionada(direccion_orden, ["Ascendente", "Descendente"]):
        return redirect(url_for("ecuestre.FiltrarEcuestres"))
    if filtro_ja:
        if not validar_opcion_seleccionada(
            datos["filtroJA"],
            [
                "hipoterapia",
                "monta_terapeutica",
                "deporte_ecuestre_adaptado",
                "actividades_recreativas",
                "equitacion",
            ],
        ):
            return redirect(url_for("ecuestre.FiltrarEcuestres"))
    ecuestres = EncuestreDB.find_ecuestres_by_fields(
        nombre=filtro_nombre,
        filtro_ja=filtro_ja,
        orden=orden,
        orden_by=columna_orden,
        page=page,
        per_page=2,
    )
    for ecuestre in ecuestres:
        # Formateo de fechas
        ecuestre.fecha_ingreso = ecuestre.fecha_ingreso.strftime("%Y-%m-%d")
        ecuestre.fecha_nacimiento = ecuestre.fecha_nacimiento.strftime("%Y-%m-%d")

        # Formateo del tipo de J&A
        ecuestre.tipo_JA = TIPOS_JA.get(ecuestre.tipo_JA, ecuestre.tipo_JA)
    return render_template("ecuestre/ecuestre.html", ecuestres=ecuestres)


@bp.get("ModificarArchivos/<int:id>")
@login_required
@blocked_user
@check("ecuestre_update")
def get_modificar_archivo(id):
    """
    Renderiza el template para modificar un archivo del ecuestre
    Args:
        Recive  el id del documento
    """
    archivo = DocDB.get_documento_by_id(id)
    if archivo == None:
        return redirect(url_for("ecuestre.FiltrarEcuestres"))
    return render_template("ecuestre/modificarArchivo.html", archivo=archivo)


@bp.post("ModificarArchivos/<int:id>")
@login_required
@blocked_user
@check("ecuestre_update")
def modificar_archivo(id):
    """
    Modifica el archivo del ecuestre
    Args:
        Recive  el id del documento por parametro
        Manda por form el nombre y el tipo nuevo del documento
    """
    campos = [
        "ficha_general",
        "planificacion_entrenamiento",
        "informe_evolucion",
        "carga_imagenes",
        "registro_veterinario",
    ]
    datos = request.form.to_dict()
    if not validar_opcion_seleccionada(datos["tipo"], campos):
        return redirect(url_for("ecuestre.get_modificar_archivo", id=id))
    DocDB.modificar_documento(datos["nombre"], datos["tipo"], id)
    doc = DocDB.get_documento_by_id(id)
    return redirect(url_for("ecuestre.archivos", id=doc.encuestre_id))
