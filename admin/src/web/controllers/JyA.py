from core.models.Legajo import (
    list_legajos,
    obtenerTotal,
    get_legajo_by_id,
    updateLegajo,
    create_legajo,
    eliminar_legajo,
    obtenerTotalTitulos,
    buscar_por_titulo,
    ordenar_legajos,
    buscar_por_titulo_nopage,
)
from web.handlers import error
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    url_for,
    redirect,
    current_app as app,
)
import uuid
from os import fstat
from core.models.Documento_externo_JyA import (
    create_doc,
    list_documentos,
    get_doc_by_id,
    eliminar_doc,
    list_documentos_filt,
    ordenar_archivos_b,
    update_documento_externo,
)
from core.models.Equipo import list_equipo_spf
from web.handlers.auth import login_required, check, blocked_user
from core.models.Encuestre import list_documentos_dict
from minio.error import S3Error
from .validaciones import (
    validar_numeros,
    validar_email,
    validar_fecha_anterior,
    validar_Ecuestre,
    validar_miembro,
    validar_opcion_seleccionada,
    validar_campos_obligatorios,
)

bp = Blueprint("jya", __name__, url_prefix="/jya")

FORMATOS_PERMITIDOS = ["pdf", "doc", "xls", "jpeg"]


@bp.get("/")
@login_required
@blocked_user
@check("jya_index")
def home_jya():
    """
    Renderiza la página principal del sistema JYA.

    Esta función recupera los legajos filtrados, los pagina y los muestra
    en la plantilla principal. También maneja errores en caso de que
    no se puedan recuperar los legajos.

    Retorna:
    --------
    Response:
        La plantilla principal de JYA o una página de error si ocurre un problema.
    """
    try:
        session.pop("filtered_legajos", None)
        page = request.args.get("page", 1, type=int)
        items = list_legajos(page=page)
        total = int(obtenerTotal() / 10)
        return render_template(
            "J&A/J&A.html", page=page, items=items, total_pages=total
        )
    except:
        erro = error(
            code=404,
            message="No se puedieron encontrar legajos",
            description="consultar al administrador",
        )
        return render_template("error.html", error=erro)


@bp.get("/editar/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def editar_legajo(id):
    """
    Renderiza la plantilla para editar un legajo específico.

    Parámetros:
    ----------
    id : int
        El ID del legajo que se desea editar.

    Retorna:
    --------
    Response:
        La plantilla de edición del legajo o redirige a la página principal
        en caso de error.
    """
    try:
        caballos = obtener_caballo()
        profesores = obtener_puesto("Profesor de Equitacion")
        conductores = obtener_puesto("Conductor")
        auxiliares = obtener_puesto("Auxiliar de pista")
        legajo = get_legajo_by_id(id)
        return render_template(
            "J&A/editar.html",
            id=id,
            legajo=legajo,
            conductores=conductores,
            caballos=caballos,
            profesores=profesores,
            auxiliares=auxiliares,
        )
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/detalle/<int:id>")
@login_required
@blocked_user
@check("jya_show")
def detalle_legajo(id):
    """
    Renderiza la plantilla de detalle para un legajo específico.

    Parámetros:
    ----------
    id : int
        El ID del legajo que se desea mostrar.

    Retorna:
    --------
    Response:
        La plantilla de detalle del legajo o redirige a la página principal
        en caso de error.
    """
    try:
        legajo = get_legajo_by_id(id)
        return render_template("J&A/detalle.html", legajo=legajo)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.post("/update/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def actualizar_legajo(id):
    """
    Actualiza el legajo con el ID proporcionado con los datos del formulario.

    Parámetros:
    ----------
    id : int
        El ID del legajo a actualizar.

    Retorna:
    --------
    Response:
        La plantilla de detalle del legajo actualizado o redirige a la página principal
        en caso de error.
    """
    try:
        second_params = request.form
        params = dict(request.form)
        if not validar_email(params["email_tutor_1"]) or params["email_tutor_1"] == "":
            return home_jya()
        if params["email_tutor_2"]:
            if not validar_email(params["email_tutor_2"]):
                return home_jya()
        if not validar_miembro(params["profesora_terapeuta"]):
            return home_jya()
        if not validar_miembro(params["conductor_caballo"]):
            return home_jya()
        if not validar_miembro(params["auxiliar_pista"]):
            return home_jya()
        if not validar_Ecuestre(params["caballo"]):
            return home_jya()
        if not validar_campos_obligatorios(
            second_params,
            [
                "nombre",
                "apellido",
                "dni",
                "edad",
                "fecha_nacimiento",
                "lugar_nacimiento",
                "domicilio_actual",
                "telefono_actual",
                "profesionales",
                "becado",
                "certificado_discapacidad",
                "diagnostico",
                "tipo_discapacidad",
                "asignacion_familiar",
                "tipo_asignacion",
                "pension",
                "obra_social",
                "num_afiliado",
                "posee_curatela",
                "parentesco_tutor_1",
                "nombre_tutor_1",
                "apellido_tutor_1",
                "dni_tutor_1",
                "domicilio_tutor_1",
                "celular_tutor_1",
                "email_tutor_1",
                "nivel_escolaridad_tutor_1",
            ],
        ):
            return home_jya()
        updateLegajo(id, params)
        legajo = get_legajo_by_id(id)
        return render_template("J&A/detalle.html", legajo=legajo)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/addLegajo")
@login_required
@blocked_user
@check("jya_create")
def add_legajo():
    """
    Renderiza la plantilla para agregar un nuevo legajo.

    Retorna:
    --------
    Response:
        La plantilla de agregar legajo o un mensaje de error
        si ocurre algún problema.
    """
    try:
        return render_template("J&A/agregar.html")
    except Exception as e:
        return {400: f"{e} contacta al administrador"}


@bp.post("/delete_legajo/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def delete_legajo(id):
    """
    Elimina un legajo con el ID proporcionado.

    Parámetros:
    ----------
    id : int
        El ID del legajo que se desea eliminar.

    Retorna:
    --------
    Response:
        Redirige a la página principal después de la eliminación o
        muestra un mensaje de error si ocurre algún problema.
    """
    try:
        eliminar_legajo(id)
        return home_jya()
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.post("/crearLegajo")
@login_required
@blocked_user
@check("jya_create")
def crear_legajo():
    """
    Crea un nuevo legajo basado en los datos proporcionados en el formulario.

    Retorna:
    --------
    Response:
        Redirige a la página principal si el legajo se crea correctamente o
        redirige a la página de adición de legajo si hay errores en los datos.
    """
    try:
        second_params = request.form
        params = dict(request.form)
        dias = request.form.getlist("dia[]")
        if params["becado"] == "True":
            params["becado"] = True
        else:
            params["becado"] = False
        res = {
            "nombre": params["nombre"],
            "apellido": params["apellido"],
            "dni": params["dni"],
            "edad": params["edad"],
            "fecha_nacimiento": params["fecha_nacimiento"],
            "lugar_nacimiento": params["lugar_nacimiento"],
            "domicilio_actual": params["domicilio_actual"],
            "telefono_actual": params["telefono_actual"],
            "contacto_emergencia": params["contacto_emergencia"],
            "tel": params["tel"],
            "becado": params["becado"],
            "porcentaje_beca": params["porcentaje_beca"],
            "profesionales_atienden": params["profesionales_atienden"],
            "deuda": False,
            "certificado_discapacidad": bool(params["certificado_discapacidad"]),
            "diagnostico": params["diagnostico"],
            "tipo_diagnostico": params["tipo_diagnostico"],
            "tipo_discapacidad": params["tipo_discapacidad"],
            "asignacion_familiar": bool(params["asignacion_familiar"]),
            "tipo_asignacion_familiar": params["tipo_asignacion_familiar"],
            "es_veneficiaro_pension": bool(params["es_veneficiario_pension"]),
            "pension": params["pension"],
            "obra_social": params["obra_social"],
            "num_afiliado": params["num_afiliado"],
            "posee_curatela": bool(params["posee_curatela"]),
            "observaciones_curatela": params["observaciones_curatela"],
            "nombre_escuela": params["nombre_escuela"],
            "direccion_escuela": params["direccion_escuela"],
            "telefono_escuela": params["telefono_escuela"],
            "anio_actual_escuela": params["anio_actual_escuela"],
            "observaciones_escuela": params["observaciones_escuela"],
            "parentesco_tutor_1": params["parentesco_tutor_1"],
            "nombre_tutor_1": params["nombre_tutor_1"],
            "apellido_tutor_1": params["apellido_tutor_1"],
            "dni_tutor_1": params["dni_tutor_1"],
            "domicilio_tutor_1": params["domicilio_tutor_1"],
            "celular_tutor_1": params["celular_tutor_1"],
            "email_tutor_1": params["email_tutor_1"],
            "nivel_escolaridad_tutor_1": params["nivel_escolaridad_tutor_1"],
            "ocupacion_tutor_1": params["ocupacion_tutor_1"],
            "parentesco_tutor_2": params["parentesco_tutor_2"],
            "nombre_tutor_2": params["nombre_tutor_2"],
            "apellido_tutor_2": params["apellido_tutor_2"],
            "dni_tutor_2": params["dni_tutor_2"],
            "domicilio_tutor_2": params["domicilio_tutor_2"],
            "celular_tutor_2": params["celular_tutor_2"],
            "email_tutor_2": params["email_tutor_2"],
            "nivel_escolaridad_tutor_2": params["nivel_escolaridad_tutor_2"],
            "ocupacion_tutor_2": params["ocupacion_tutor_2"],
            "propuesta_trabajo": params["propuesta_trabajo"],
            "condicion": params["condicion"],
            "sede": params["sede"],
            "dia": dias,
            "profesora_terapeuta": int(params["profesor"]),
            "conductor_caballo": int(params["conductor"]),
            "caballo": int(params["caballo"]),
            "auxiliar_pista": int(params["auxiliar"]),
        }
        if not validar_numeros(res, ["dni", "edad", "dni_tutor_1"]):
            return redirect(url_for("jya.add_legajo"))
        if res["dni_tutor_2"]:
            if not validar_numeros(res, ["dni_tutor_2"]):
                return redirect(url_for("jya.add_legajo"))
        if not validar_email(res["email_tutor_1"]):
            return redirect(url_for("jya.add_legajo"))
        if res["email_tutor_2"]:
            if not validar_email(res["email_tutor_2"]):
                return redirect(url_for("jya.add_legajo"))
        if not validar_fecha_anterior(res, ["fecha_nacimiento"]):
            return redirect(url_for("jya.add_legajo"))
        if not validar_miembro(res["conductor_caballo"]):
            return redirect(url_for("jya.add_legajo"))
        if not validar_Ecuestre(res["caballo"]):
            return redirect(url_for("jya.add_legajo"))
        if not validar_miembro(res["auxiliar_pista"]):
            return redirect(url_for("jya.add_legajo"))
        if not validar_miembro(res["profesora_terapeuta"]):
            return redirect(url_for("jya.add_legajo"))
        if not validar_campos_obligatorios(
            second_params,
            [
                "nombre",
                "apellido",
                "dni",
                "edad",
                "fecha_nacimiento",
                "lugar_nacimiento",
                "domicilio_actual",
                "telefono_actual",
                "profesionales",
                "becado",
                "certificado_discapacidad",
                "diagnostico",
                "tipo_discapacidad",
                "asignacion_familiar",
                "tipo_asignacion",
                "pension",
                "obra_social",
                "num_afiliado",
                "posee_curatela",
                "parentesco_tutor_1",
                "nombre_tutor_1",
                "apellido_tutor_1",
                "dni_tutor_1",
                "domicilio_tutor_1",
                "celular_tutor_1",
                "email_tutor_1",
                "nivel_escolaridad_tutor_1",
            ],
        ):
            return redirect(url_for("jya.add_legajo"))
        create_legajo(**res)
        return home_jya()
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


def validar_ext(filename):
    """
    Valida si la extensión de un archivo está permitida.

    Parámetros:
    -----------
    filename : str
        El nombre del archivo cuyo formato se desea validar.

    Retorna:
    --------
    bool:
        True si la extensión está permitida, False en caso contrario.

    Excepciones:
    ------------
    ValueError:
        Se lanza si el nombre del archivo no contiene una extensión.
    """
    ext = filename.split(".")[1]
    return ext in FORMATOS_PERMITIDOS


@bp.post("/subirArchivo/<int:id>")
@login_required
@blocked_user
@check("jya_create")
def subir_archivo(id):
    """
    Sube un archivo o enlace asociado a un legajo específico.

    Parámetros:
    -----------
    id : int
        El ID del legajo al que se le subirá el archivo o enlace.

    Retorna:
    --------
    Response:
        Redirige a los detalles del legajo después de subir el archivo o enlace,
        o redirige a la página de inicio en caso de error.
    """
    try:
        params = dict(request.form)
        if params["tipo_subida"] == "archivo":
            client = app.storage.client
            if (
                "archivo" in request.files
                and request.files["archivo"].filename
                and params["categoria"]
            ):
                file = request.files["archivo"]
                if validar_ext(file.filename):
                    size = fstat(file.fileno()).st_size
                    tit = request.files["archivo"].filename
                    file_name = str(tit + str(uuid.uuid4()))
                    client.put_object(
                        "grupo20", file_name, file, size, content_type=file.content_type
                    )

                    res = {
                        "legajo_id": id,
                        "path": file_name,
                        "titulo": tit,
                        "tipo": params["categoria"],
                        "es_enlace": False,
                    }
                    create_doc(**res)
                    return detalle_legajo(id)
                else:
                    return exten_invalida(id)
        else:
            res = {
                "legajo_id": id,
                "path": params["enlace"],
                "titulo": params["enlace"],
                "tipo": params["categoria"],
                "es_enlace": True,
            }
            create_doc(**res)
            return detalle_legajo(id)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/extInvalida/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def exten_invalida(id):
    """
    Renderiza la plantilla de extensión inválida para un ID específico.

    Parámetros:
    -----------
    id : int
        El ID asociado a la extensión inválida.

    Retorna:
    --------
    Response:
        La respuesta de la plantilla renderizada con el ID proporcionado.
    """
    return render_template("J&A/extensionInvalida.html", id=id)


@bp.get("/visualizarArchivos/<int:id>")
@login_required
@blocked_user
@check("jya_index")
def visualizar_archivos(id):
    """
    Visualiza los archivos asociados a un ID específico.

    Parámetros:
    -----------
    id : int
        El ID para el cual se desea visualizar los archivos.

    Retorna:
    --------
    Response:
        Renderiza la plantilla de archivos o redirige a la página de inicio en caso de error.
    """
    try:
        session.pop("filtered_docs", None)
        docs = list_documentos(id)
        return render_template("J&A/archivosIndex.html", docs=docs, id=id)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/obtenerPuesto/<puesto>")
@login_required
@blocked_user
@check("jya_create")
def obtener_puesto(puesto):
    """
    Obtiene una lista de equipos según el puesto especificado.

    Parámetros:
    -----------
    puesto : str
        El puesto para el cual se desea obtener la lista de equipos.

    Retorna:
    --------
    list:
        Una lista de equipos correspondiente al puesto especificado obtenidos de la función `list_equipo_spf`.
    """
    return list_equipo_spf(puesto)


@bp.get("/obtenerCaballos")
@login_required
@blocked_user
@check("jya_create")
def obtener_caballo():
    """
    Obtiene una lista de documentos en formato de diccionario.

    Retorna:
    --------
    list:
        Una lista de documentos en formato de diccionario obtenidos de la función `list_documentos_dict`.
    """
    return list_documentos_dict()


@bp.get("/detallesdos/<int:id>")
@login_required
@blocked_user
@check("jya_show")
def mas_detalles(id):
    """
    Renderiza la plantilla de detalles para un legajo específico.

    Parámetros:
    -----------
    id : int
        El ID del legajo cuyo detalle se desea mostrar.

    Retorna:
    --------
    Response:
        La respuesta de la plantilla renderizada o un diccionario con un mensaje de error.

    Excepciones:
    ------------
    dict:
        En caso de error al renderizar la plantilla, retorna un diccionario con el mensaje de error.
    """
    try:
        return render_template("J&A/segundoDetalle.html", legajo=get_legajo_by_id(id))
    except Exception as e:
        return {e: "Contacte al administrador"}


@bp.get("/buscarTitulo")
@login_required
@blocked_user
@check("jya_index")
def buscar_jya():
    """
    Busca legajos basados en los filtros proporcionados, almacena los resultados
    en la sesión y los muestra paginados en el template correspondiente.

    La función busca por nombre, apellido, DNI y profesional que atiende, y realiza
    dos tipos de búsquedas: una paginada y otra sin paginación. Los resultados
    completos se guardan en la sesión para otros usos.

    Returns:
        str: Renderiza el template 'J&A/J&A.html' con los resultados filtrados y paginados.
        dict: En caso de error, devuelve un diccionario con el error y el mensaje.

    Raises:
        Exception: Si ocurre un error durante el proceso de búsqueda o renderización.

    """
    try:
        session.pop("filtered_legajos", None)
        nombre = request.args.get("nombre")
        apellido = request.args.get("apellido")
        dni = request.args.get("dni")
        prof = request.args.get("prof")
        page = request.args.get("page", 1, type=int)

        res = buscar_por_titulo(nombre, apellido, dni, prof, page=page)
        res2 = buscar_por_titulo_nopage(nombre, apellido, dni, prof)

        session["filtered_legajos"] = res2
        total = int(obtenerTotalTitulos(nombre, apellido, dni, prof) / 10)

        return render_template("J&A/J&A.html", page=page, items=res, total_pages=total)

    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/ordenar")
@login_required
@blocked_user
@check("jya_index")
def ordenar():
    """
    Ordena la lista de legajos basada en los criterios de orden y tipo de orden proporcionados.

    La función obtiene los parámetros de orden y sort desde la solicitud HTTP, y
    también recupera los legajos previamente filtrados de la sesión. Si no hay legajos
    filtrados en la sesión, los obtiene llamando a `list_legajos(page)`. Luego, aplica
    el orden especificado utilizando la función `ordenar_legajos`, y renderiza el
    template 'J&A/J&A.html' con los legajos ordenados.

    Returns:
        str: Renderiza el template 'J&A/J&A.html' con los legajos ordenados.

    Raises:
        Exception: Si ocurre algún error durante el proceso de ordenación o renderización.
    """
    try:
        ordw = request.args.get("order")
        sort = request.args.get("sort")
        page = request.args.get("page", 1, type=int)

        arch = session.get("filtered_legajos", list(list_legajos()))
        arch, total = ordenar_legajos(arch, sort, ordw, page)
        return render_template(
            "J&A/J&A.html", page=page, items=arch, total_pages=int(total / 10)
        )
    except:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/download/<int:id_file>")
@login_required
@blocked_user
@check("jya_index")
def download_file(id_file):
    """
    Genera una URL de descarga pre-firmada para un archivo almacenado en S3
    y redirige al usuario a dicha URL.

    La función obtiene el archivo correspondiente al `id_file` utilizando `get_doc_by_id`,
    y luego genera una URL de descarga pre-firmada desde el cliente de almacenamiento
    en S3. Si la operación es exitosa, redirige al usuario a la URL generada. En caso
    de error, devuelve un mensaje con el detalle del mismo.

    Args:
        id_file (int): El ID del archivo a descargar.

    Returns:
        werkzeug.wrappers.Response: Redirige al usuario a la URL de descarga o
        devuelve un mensaje de error en caso de fallo.

    Raises:
        S3Error: Si ocurre un error al intentar generar la URL de descarga.
    """
    try:
        client = app.storage.client
        doc = get_doc_by_id(id_file).path
        print(doc)

        presigned_url = client.presigned_get_object(
            bucket_name="grupo20", object_name=doc
        )

        return redirect(presigned_url)
    except S3Error as exc:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.post("/delete/<int:id>")
@login_required
@blocked_user
@check("jya_destroy")
def delete_file(id):
    """
    Elimina un archivo almacenado en S3 y lo elimina de la base de datos.

    La función obtiene el archivo correspondiente al `id_file` desde los argumentos
    de la solicitud, lo elimina del almacenamiento S3, y luego lo elimina de la
    base de datos. Finalmente, redirige al usuario a la vista de los archivos
    relacionados. En caso de error, devuelve un mensaje con el detalle del mismo.

    Args:
        id (int): El ID del legajo asociado a los archivos.

    Returns:
        werkzeug.wrappers.Response: Redirige a la vista de archivos después de la
        eliminación exitosa, o devuelve un mensaje de error y un código de estado
        500 en caso de fallo.

    Raises:
        S3Error: Si ocurre un error al intentar eliminar el archivo de S3.
    """
    try:
        client = app.storage.client
        id_file = request.args.get("id_file")
        doc = get_doc_by_id(id_file).path

        client.remove_object(bucket_name="grupo20", object_name=doc)
        eliminar_doc(id_file)
        return visualizar_archivos(id)
    except S3Error as exc:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.post("/buscarArchivo/<int:id>")
@login_required
@blocked_user
@check("jya_index")
def buscar_archivo(id):
    """
    Filtra y busca archivos relacionados con un legajo basado en el título y tipo.

    La función toma los parámetros de búsqueda del formulario enviado, realiza el
    filtrado de los archivos correspondientes y guarda los resultados en la sesión
    actual para su posterior uso. Finalmente, redirige a la plantilla para mostrar
    los archivos filtrados.

    Args:
        id (int): El ID del legajo relacionado con los archivos.

    Returns:
        werkzeug.wrappers.Response: Renderiza la plantilla "archivosIndex.html" con
        los documentos filtrados. En caso de error, devuelve un mensaje con el detalle
        del error.

    Raises:
        Exception: Si ocurre un error durante el proceso de filtrado o renderización.
    """
    try:
        session.pop("filtered_docs", None)
        titulo = request.form.get("titulo", None)
        tipo = request.form.get("tipo", None)
        docs = list_documentos_filt(id, titulo, tipo)
        session["filtered_docs"] = docs
        return render_template("J&A/archivosIndex.html", docs=docs, id=id)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/ordenarArchivos/<int:id>")
@login_required
@blocked_user
@check("jya_index")
def ordenar_archivos(id):
    """
    Ordena los archivos filtrados por el usuario en función de los parámetros de
    ordenación proporcionados.

    La función recupera los documentos filtrados previamente desde la sesión o lista
    todos los documentos si no hay filtrado. Luego aplica el criterio de ordenación
    sobre los documentos y renderiza la plantilla con los resultados ordenados.

    Args:
        id (int): El ID del legajo relacionado con los archivos.

    Returns:
        werkzeug.wrappers.Response: Renderiza la plantilla "archivosIndex.html" con
        los documentos ordenados.

    Raises:
        Exception: Si ocurre un error durante el proceso de ordenación o renderización.
    """
    try:
        orde = request.args.get("order")
        sort = request.args.get("sort")
        # docs = request.args.get("docs")
        filtrados = session.get("filtered_docs", list_documentos(id))
        archivos = ordenar_archivos_b(filtrados, orde, sort)
        return render_template("J&A/archivosIndex.html", docs=archivos, id=id)
    except:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.post("/deleteEnlace/<int:id>")
@login_required
@blocked_user
@check("jya_destroy")
def delete_enlace(id):
    """
    Elimina un enlace de archivo del sistema y actualiza la vista de los archivos.

    La función obtiene el identificador del archivo a eliminar a partir de los
    parámetros de la solicitud. Luego, intenta eliminar el archivo del sistema
    y finalmente actualiza la lista de archivos renderizando la vista de los archivos.

    Args:
        id (int): El ID relacionado con el grupo o legajo que contiene el archivo.

    Returns:
        werkzeug.wrappers.Response: Renderiza la plantilla con los archivos actualizados
        después de eliminar el archivo.

    Raises:
        S3Error: Si ocurre un error durante el proceso de eliminación del archivo.
    """
    try:
        id_file = request.args.get("id_file")
        eliminar_doc(id_file)
        return visualizar_archivos(id)
    except S3Error as exc:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/EditArchivo/<int:id_file>/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def update_file(id_file, id):
    """
    Actualiza el archivo mostrado en la interfaz de usuario.

    Esta función recupera un documento por su ID y renderiza
    la plantilla para mostrar los detalles del archivo.

    Parámetros:
    -----------
    id_file : int
        El ID del archivo que se desea actualizar.
    id : int
        El ID asociado que se puede utilizar en la plantilla.

    Retorna:
    --------
    Response:
        La plantilla con los detalles del archivo o la página principal si ocurre un error.
    """
    try:
        doc = get_doc_by_id(id_file)
        return render_template("J&A/detalleArchivo.html", document=doc, id=id)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.post("/updateArchivo/<int:id_file>/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def update_document(id_file, id):
    """
    Actualiza los detalles de un documento existente.

    Esta función recupera el título y el tipo de un documento
    desde el formulario, valida el tipo seleccionado y luego
    actualiza el documento en la base de datos.

    Parámetros:
    -----------
    id_file : int
        El ID del documento que se desea actualizar.
    id : int
        El ID asociado que se puede utilizar en la plantilla.

    Retorna:
    --------
    Response:
        La plantilla con los detalles del archivo actualizado o
        la página principal si ocurre un error.
    """
    try:
        titulo = request.form.get("titulo")
        tipo = request.form.get("categoria")
        if not validar_opcion_seleccionada(
            tipo,
            [
                "entrevista",
                "evaluacion",
                "planificaciones",
                "evolucion",
                "cronicas",
                "documental",
            ],
        ):
            return visualizar_archivos(id)
        update_documento_externo(id_file, titulo, tipo)
        return update_file(id_file, id)
    except Exception as e:
        flash("¡Ocurrió un error!", "error")
        return home_jya()


@bp.get("/redirect_visual/<int:id>")
@login_required
@blocked_user
@check("jya_update")
def redirect_visual(id):
    """
    Redirige a la visualización de archivos de un legajo específico.

    Parámetros:
    -----------
    id : int
        El ID del legajo cuyo archivo se desea visualizar.

    Retorna:
    --------
    Response:
        La respuesta de la función visualizar_archivos con el ID proporcionado.
    """
    return visualizar_archivos(id)
