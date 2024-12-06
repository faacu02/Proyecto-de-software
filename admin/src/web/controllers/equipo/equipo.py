from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    current_app as app,
)
from core.models.Equipo.__init__ import (
    create_member,
    find_member_by_email,
    delete_member,
    get_memberby_id,
    find_member_by_dni,
    actualizar_miembro,
    find_member_by_fields,
)
from core.models.User.__init__ import es_admin
from core.database import db
from os import fstat
from web.handlers.auth import login_required, check, blocked_user
import urllib.parse

EXTENSIONES_PERMITIDAS = ["pdf", "doc", "xls", "jpeg"]
PROFESIONES = [
    "Psicólogo/a",
    "Psicomotricista",
    "Médico/a",
    "Kinesiólogo/a",
    "Terapista Ocupacional",
    "Psicopedagogo/a",
    "Docente",
    "Profesor",
    "Fonoaudiólogo/a",
    "Veterinario/a",
    "Otro",
]
PUESTOS_LABORALES = [
    "Administrativo/a",
    "Terapeuta",
    "Conductor",
    "Auxiliar de pista",
    "Herrero",
    "Veterinario",
    "Entrenador de Caballos",
    "Domador",
    "Profesor de Equitación",
    "Docente de Capacitación",
    "Auxiliar de mantenimiento",
    "Otro",
]
ORDENES = ["nombre", "apellido", "fecha_creacion"]
DIRECCIONES = ["asc", "desc"]
CONDICIONES = ["voluntario", "personal_rentado"]
ACTIVOS = ["si", "no"]

from ..validaciones import (
    validar_campos_obligatorios,
    validar_numeros,
    validar_email,
    validar_fechas,
    convertir_activo,
    validar_miembro_existente,
    validar_miembro_existente_actualizacion,
    validar_solo_letras,
    validar_extension,
    validar_tamano,
    validar_opcion_seleccionada,
    validar_miembro_existente_actualizacion_admin,
)


bp = Blueprint("equipo", __name__, url_prefix="/equipo")


@bp.route("/altaMiembro", methods=["POST", "GET"])
@login_required
@blocked_user
@check("equipo_new")
def altaMiembro():
    """
    Alta de un miembro del equipo.

    Permite la creación de un nuevo miembro del equipo a través de un formulario.
    Valida los datos de entrada y procesa archivos adjuntos si son proporcionados.
    Si se completa con éxito, redirige a la vista de miembros.

    Returns:
        Renderiza la plantilla para el formulario de alta o redirige a
        la vista de miembros después de la creación exitosa.
    """
    if request.method == "GET":
        return render_template("equipo/altaMiembro.html")
    else:
        params = request.form.to_dict()
        client = app.storage.client

        required_fields = [
            "nombre",
            "apellido",
            "dni",
            "domicilio",
            "email",
            "localidad",
            "telefono",
            "contacto_emergencia_telefono",
            "contacto_emergencia_nombre",
            "profesion",
            "puesto_laboral",
            "fecha_inicio",
            "condicion",
            "activo",
            "fecha_cese",
            "obra_social",
            "num_afiliado",
        ]

        if not validar_campos_obligatorios(params, required_fields):
            return redirect(url_for("equipo.altaMiembro"))

        if not validar_numeros(
            params, ["dni", "telefono", "contacto_emergencia_telefono"]
        ):
            return redirect(url_for("equipo.altaMiembro"))

        # Validación de que el email tenga un formato válido
        if not validar_email(params["email"]):
            return redirect(url_for("equipo.altaMiembro"))

        if not validar_opcion_seleccionada(params["profesion"], PROFESIONES):
            return redirect(url_for("equipo.altaMiembro"))

        if not validar_opcion_seleccionada(params["puesto_laboral"], PUESTOS_LABORALES):
            return redirect(url_for("equipo.altaMiembro"))

        if not validar_fechas(params["fecha_inicio"], params["fecha_cese"]):
            return redirect(url_for("equipo.altaMiembro"))

        if not validar_opcion_seleccionada(params["condicion"], CONDICIONES):
            return redirect(url_for("equipo.altaMiembro"))

        if not validar_opcion_seleccionada(params["activo"], ACTIVOS):
            return redirect(url_for("equipo.altaMiembro"))

        activo = convertir_activo(params)

        if not validar_solo_letras(
            params, ["nombre", "apellido", "contacto_emergencia_nombre"]
        ):
            return redirect(url_for("equipo.altaMiembro", id=id))

        if not validar_miembro_existente(
            params, find_member_by_email, find_member_by_dni
        ):
            return redirect(url_for("equipo.altaMiembro"))

        if "titulo" in request.files and request.files["titulo"].filename:
            fileTitulo = request.files["titulo"]
            if validar_extension(
                fileTitulo.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileTitulo.fileno()).st_size):
                size = fstat(fileTitulo.fileno()).st_size
                client.put_object(
                    "grupo20",
                    f"{params['dni']}_titulo_{fileTitulo.filename}",
                    fileTitulo,
                    size,
                    content_type=fileTitulo.content_type,
                )
                params["titulo"] = f"{params['dni']}_titulo_{fileTitulo.filename}"
            else:
                return redirect(url_for("equipo.altaMiembro"))

        if "copia_dni" in request.files and request.files["copia_dni"].filename:
            fileCopiaDni = request.files["copia_dni"]
            if validar_extension(
                fileCopiaDni.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileCopiaDni.fileno()).st_size):
                size = fstat(fileCopiaDni.fileno()).st_size
                client.put_object(
                    "grupo20",
                    f"{params['dni']}_copiaDNI_{fileCopiaDni.filename}",
                    fileCopiaDni,
                    size,
                    content_type=fileCopiaDni.content_type,
                )
                params["copia_dni"] = (
                    f"{params['dni']}_copiaDNI_{fileCopiaDni.filename}"
                )
            else:
                return redirect(url_for("equipo.altaMiembro"))

        if (
            "cv_actualizado" in request.files
            and request.files["cv_actualizado"].filename
        ):
            fileCvActualizado = request.files["cv_actualizado"]
            if validar_extension(
                fileCvActualizado.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileCvActualizado.fileno()).st_size):
                size = fstat(fileCvActualizado.fileno()).st_size
                client.put_object(
                    "grupo20",
                    f"{params['dni']}_cv_{fileCvActualizado.filename}",
                    fileCvActualizado,
                    size,
                    content_type=fileCvActualizado.content_type,
                )
                params["cv_actualizado"] = (
                    f"{params['dni']}_cv_{fileCvActualizado.filename}"
                )
            else:
                return redirect(url_for("equipo.altaMiembro"))

        new_member = create_member(
            nombre=params["nombre"],
            apellido=params["apellido"],
            dni=params["dni"],
            domicilio=params["domicilio"],
            email=params["email"],
            localidad=params["localidad"],
            telefono=params["telefono"],
            contacto_emergencia_nombre=params["contacto_emergencia_nombre"],
            contacto_emergencia_telefono=params["contacto_emergencia_telefono"],
            profesion=params["profesion"],
            puesto_laboral=params["puesto_laboral"],
            fecha_inicio=params["fecha_inicio"],
            condicion=params["condicion"],
            activo=activo,
            fecha_cese=params["fecha_cese"],
            obra_social=params["obra_social"],
            num_afiliado=params["num_afiliado"],
            titulo=params.get("titulo"),
            copia_dni=params.get("copia_dni"),
            cv_actualizado=params.get("cv_actualizado"),
        )

        flash("Miembro creado exitosamente", "success")
        return redirect(url_for("equipo.verMiembros"))


@bp.route("/eliminarMiembro/<int:id>", methods=["POST"])
@login_required
@blocked_user
@check("equipo_destroy")
def borrarMiembro(id):
    """
    Elimina un miembro por su ID.

    Args:
        id (int): ID del miembro a eliminar.

    Returns:
        Redirección a la vista de miembros
        después de la eliminación exitosa.
    """
    if (miembro := get_memberby_id(id)) is None:
        flash("No se encontró el miembro a eliminar", "error")
        return redirect(url_for("equipo.verMiembros"))
    if not(miembro.usuario.borrado) and es_admin(miembro.email):
        flash("No se puede eliminar a un system admin", "error")
        return redirect(url_for("equipo.verMiembros"))
    miembro = delete_member(id)
    flash(f"Miembro {miembro.nombre} {miembro.apellido} eliminado correctamente.")
    return redirect(url_for("equipo.verMiembros"))


@bp.route("/modificarMiembro/<int:id>", methods=["POST", "GET"])
@login_required
@blocked_user
@check("equipo_update")
def editarMiembro(id):
    """
    Modifica los datos de un miembro.

    Args:
        id (int): ID del miembro a modificar.

    Returns:
        Renderiza la plantilla para el formulario de modificación o
        redirige a la vista de miembros después de la actualización exitosa.
    """
    if (miembro := get_memberby_id(id)) is None:
        flash("No se encontró el miembro a modificar", "error")
        return redirect(url_for("equipo.verMiembros"))

    miembro = get_memberby_id(id)
    required_fields = [
        "nombre",
        "apellido",
        "dni",
        "domicilio",
        "email",
        "localidad",
        "telefono",
        "contacto_emergencia_telefono",
        "contacto_emergencia_nombre",
        "profesion",
        "puesto_laboral",
        "fecha_inicio",
        "condicion",
        "activo",
        "fecha_cese",
        "obra_social",
        "num_afiliado",
    ]
    if request.method == "POST":

        params = request.form.to_dict()
        client = app.storage.client

        if miembro.usuario and es_admin(miembro.email):
            required_fields_without_email = [
                field for field in required_fields if field != "email"
            ]
            if not validar_campos_obligatorios(params, required_fields_without_email):
                return redirect(url_for("equipo.editarMiembro", id=id))
        else:
            if not validar_campos_obligatorios(params, required_fields):
                return redirect(url_for("equipo.editarMiembro", id=id))

        if not validar_numeros(
            params, ["dni", "telefono", "contacto_emergencia_telefono", "num_afiliado"]
        ):
            return redirect(url_for("equipo.editarMiembro", id=id))

        if miembro.usuario and es_admin(miembro.email):
            if "email" in params and params["email"] != miembro.email:
                flash("No se puede modificar el email de un system admin", "error")
                return redirect(url_for("equipo.editarMiembro", id=id))
        else:
            if not validar_email(params["email"]):
                return redirect(url_for("equipo.editarMiembro", id=id))

        if not validar_fechas(params["fecha_inicio"], params["fecha_cese"]):
            return redirect(url_for("equipo.editarMiembro", id=id))

        if not validar_opcion_seleccionada(params["profesion"], PROFESIONES):
            return redirect(url_for("equipo.editarMiembro", id=id))

        if not validar_opcion_seleccionada(params["puesto_laboral"], PUESTOS_LABORALES):
            return redirect(url_for("equipo.editarMiembro", id=id))

        if not validar_opcion_seleccionada(params["condicion"], CONDICIONES):
            return redirect(url_for("equipo.editarMiembro", id=id))

        if not validar_opcion_seleccionada(params["activo"], ACTIVOS):
            return redirect(url_for("equipo.editarMiembro", id=id))

        activo = convertir_activo(params)

        if not validar_solo_letras(
            params, ["nombre", "apellido", "contacto_emergencia_nombre"]
        ):
            return redirect(url_for("equipo.editarMiembro", id=id))

        if miembro.usuario and es_admin(miembro.email):
            if not validar_miembro_existente_actualizacion_admin(
                params, id, find_member_by_dni
            ):
                return redirect(url_for("equipo.editarMiembro", id=id))
        else:
            if not validar_miembro_existente_actualizacion(
                params, id, find_member_by_email, find_member_by_dni
            ):
                return redirect(url_for("equipo.editarMiembro", id=id))

        """ Actualizar los archivos adjuntos """

        if "titulo" in request.files and request.files["titulo"].filename:
            fileTitulo = request.files["titulo"]
            if validar_extension(
                fileTitulo.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileTitulo.fileno()).st_size):
                size = fstat(fileTitulo.fileno()).st_size
                client.put_object(
                    "grupo20",
                    f"{params['dni']}_titulo_{fileTitulo.filename}",
                    fileTitulo,
                    size,
                    content_type=fileTitulo.content_type,
                )
                params["titulo"] = f"{params['dni']}_titulo_{fileTitulo.filename}"
            else:
                return redirect(url_for("equipo.editarMiembro", id=id))

        if "copia_dni" in request.files and request.files["copia_dni"].filename:
            fileCopiaDni = request.files["copia_dni"]
            if validar_extension(
                fileCopiaDni.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileCopiaDni.fileno()).st_size):
                size = fstat(fileCopiaDni.fileno()).st_size
                client.put_object(
                    "grupo20",
                    f"{params['dni']}_copiaDNI_{fileCopiaDni.filename}",
                    fileCopiaDni,
                    size,
                    content_type=fileCopiaDni.content_type,
                )
                params["copia_dni"] = (
                    f"{params['dni']}_copiaDNI_{fileCopiaDni.filename}"
                )
            else:
                return redirect(url_for("equipo.editarMiembro", id=id))

        if (
            "cv_actualizado" in request.files
            and request.files["cv_actualizado"].filename
        ):
            fileCvActualizado = request.files["cv_actualizado"]
            if validar_extension(
                fileCvActualizado.filename, EXTENSIONES_PERMITIDAS
            ) and validar_tamano(fstat(fileCvActualizado.fileno()).st_size):
                size = fstat(fileCvActualizado.fileno()).st_size
                client.put_object(
                    "grupo20",
                    f"{params['dni']}_cv_{fileCvActualizado.filename}",
                    fileCvActualizado,
                    size,
                    content_type=fileCvActualizado.content_type,
                )
                params["cv_actualizado"] = (
                    f"{params['dni']}_cv_{fileCvActualizado.filename}"
                )
            else:
                return redirect(url_for("equipo.editarMiembro", id=id))

        if "borrar_titulo" in request.form:
            borrar_archivo(id, miembro.titulo)
            miembro.titulo = None

        if "borrar_copia_dni" in request.form:
            borrar_archivo(id, miembro.copia_dni)
            miembro.copia_dni = None

        if "borrar_cv_actualizado" in request.form:
            borrar_archivo(id, miembro.cv_actualizado)
            miembro.cv_actualizado = None

        miembro = actualizar_miembro(miembro, params, activo)

        db.session.commit()
        flash(f"Miembro {miembro.nombre} {miembro.apellido} modificado correctamente.")
        return redirect(url_for("equipo.verMiembros"))

    return render_template(
        "equipo/modificarMiembro.html", miembro=miembro, urllib=urllib
    )


@bp.route("/", methods=["GET"])
@login_required
@blocked_user
@check("equipo_index")
def verMiembros():
    """
    Muestra los miembros del equipo, según los valores ingresados en los filtros.

    Se permite filtrar por nombre, apellido, DNI, email, puesto laboral,
    dirección y orden.

    Returns:
        Renderiza la plantilla para la vista de miembros con los filtros aplicados.
    """
    nombre = request.args.get("nombre", "")
    apellido = request.args.get("apellido", "")
    dni = request.args.get("dni", "")
    email = request.args.get("email", "")
    puesto = request.args.get("puesto", "")
    page = request.args.get("page", 1, type=int)
    direccion = request.args.get("direccion", "asc")
    orden = request.args.get("orden", "nombre")

    if nombre and not validar_solo_letras({"nombre": nombre}, ["nombre"]):
        return redirect(url_for("equipo.verMiembros"))

    if apellido and not validar_solo_letras({"apellido": apellido}, ["apellido"]):
        return redirect(url_for("equipo.verMiembros"))

    if dni and not validar_numeros({"dni": dni}, ["dni"]):
        return redirect(url_for("equipo.verMiembros"))

    if email and not validar_email(email):
        return redirect(url_for("equipo.verMiembros"))

    if puesto and not validar_opcion_seleccionada(puesto, PUESTOS_LABORALES):
        return redirect(url_for("equipo.verMiembros"))

    if direccion and not validar_opcion_seleccionada(direccion, DIRECCIONES):
        return redirect(url_for("equipo.verMiembros"))

    if orden and not validar_opcion_seleccionada(orden, ORDENES):
        return redirect(url_for("equipo.verMiembros"))

    miembros = find_member_by_fields(
        email, orden, direccion, nombre, apellido, dni, puesto, page=page, per_page=5
    )
    return render_template("equipo/verMiembros.html", miembros=miembros, urllib=urllib)


@bp.get("/download_file/<filename>")
@login_required
@blocked_user
@check("equipo_show")
def download_file(filename):
    """
    Genera una URL prefirmada para la descarga de un archivo desde el bucket de almacenamiento.

    Args:
        filename (str): El nombre del archivo a descargar.

    Returns:
        Redirección a la URL prefirmada para la descarga del archivo.
    """
    client = app.storage.client
    bucket_name = "grupo20"
    filename = urllib.parse.unquote(filename)
    url = client.presigned_get_object(bucket_name, filename)

    return redirect(url)


def borrar_archivo(id, filename):
    """
    Elimina un archivo del almacenamiento y realiza el commit del cambio en la base de datos.

    Args:
        id (int): El ID del miembro cuyo archivo se está eliminando.
        filename (str): El nombre del archivo que se va a eliminar.

    Returns:
        Redirección a la vista 'editarMiembro'.
    """
    client = app.storage.client
    client.remove_object("grupo20", filename)
    db.session.commit()
    flash("Archivo borrado exitosamente.")
    return redirect(url_for("equipo.editarMiembro", id=id))
