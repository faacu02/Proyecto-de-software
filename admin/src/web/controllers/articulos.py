from datetime import datetime
from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from core.models.Articulo import listar_articulos, crear_articulo, eliminar_articulo, obtener_articulo, actualizar_articulo, obtener_estado
from core.models.User import list_users_nopage
from web.controllers.validaciones import validar_campos_obligatorios
from web.handlers.auth import login_required, check, blocked_user

bp = Blueprint("articulo", __name__, url_prefix="/articulo")


@bp.get("/")
@login_required
@blocked_user
@check("art_index")
def home_articulos():
    """
    Controlador para la página de inicio, muestra un listado paginado de artículos.

    Esta función se encarga de recuperar y mostrar los artículos en la página principal del sitio.
    La visualización de los artículos está paginada para facilitar la navegación y evitar cargar
    demasiados datos en una sola página. 

    :return: Renderiza el template de la página principal con los artículos paginados.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 10 

    resultado = listar_articulos(page=page, per_page=per_page)

    if not resultado['success']:
        return render_template("error.html", message=resultado["message"])

    return render_template(
        "archivos/home.html",
        articulos=resultado['articulos'],
        page=page
    )


@bp.get("/postear")
@login_required
@blocked_user
@check("art_create")
def agregar_art():
    """
    Renderiza la página para crear un nuevo artículo.

    La función obtiene una lista de usuarios para que el artículo pueda ser asociado a un autor
    y luego renderiza la página de creación de artículos (usualmente un formulario donde se ingresan
    los detalles del artículo).

    Returns:
        render_template: Redirige al usuario a la página de creación de artículos,
                         pasándole la lista de usuarios para asociar el artículo a un autor.
    """
    users = list_users_nopage()
    return render_template(
        "archivos/crear.html",
        usuarios=users
    )



@bp.post("/load")
@login_required
@blocked_user
@check("art_create")
def load ():
    """
    Carga un artículo en la base de datos con los datos proporcionados en el formulario.

    La función obtiene los datos del formulario de la solicitud, valida los campos obligatorios (título, contenido y autor),
    y si todos los campos son válidos, crea un nuevo artículo con estado "Borrador" y las fechas de creación y actualización
    configuradas con la fecha y hora actuales. Si los campos obligatorios no están completos, redirige al formulario de
    creación del artículo. Después de la creación del artículo, redirige al usuario a la página principal de artículos.

    Returns:
        redirect: Redirige a la página principal de artículos después de agregar el artículo o si no se validan los campos.
    """
    articulo = dict(request.form)
    articulo["estado"] = "Borrador"
    articulo["fecha_creacion"] = datetime.now()
    articulo["fecha_actualizacion"] = datetime.now()
    if not validar_campos_obligatorios(articulo,["titulo", "contenido", "autor_id"]):
        return agregar_art()
    crear_articulo(**articulo)
    return redirect(url_for("articulo.home_articulos"))



@bp.post("/delete")
@login_required
@blocked_user
@check("art_destroy")
def delete():
    """
    Elimina un artículo de la base de datos.

    La función obtiene el ID del artículo desde los parámetros de la URL. Si el ID es válido, elimina el artículo
    correspondiente de la base de datos y muestra un mensaje de éxito. Si no se proporciona un ID válido o si ocurre
    un error durante la eliminación, muestra un mensaje de advertencia o error adecuado.

    Returns:
        redirect: Redirige a la página principal de artículos después de la operación, con un mensaje de éxito, advertencia o error.
    """
    try:
        id_a = request.args.get("art_id", None)
        if id_a:
            eliminar_articulo(id_a)
            flash("Artículo eliminado exitosamente.", "success") 
        else:
            flash("No se proporcionó un ID válido.", "warning")
    except Exception as e:
        flash(f"Ocurrió un error al eliminar el artículo: {str(e)}", "danger")  
    return redirect(url_for("articulo.home_articulos"))  
    

@bp.get("/edit")
@login_required
@blocked_user
@check("art_update")
def edit():
    """
    Muestra el formulario de edición de un artículo existente.

    La función obtiene el ID del artículo desde los parámetros de la URL. Si el ID es válido, obtiene la información
    del artículo desde la base de datos y obtiene la lista de usuarios sin paginación. Luego, muestra un formulario
    de edición con los detalles del artículo y la lista de usuarios. Si no se proporciona un ID válido o ocurre un error,
    redirige al usuario a la página principal de artículos con un mensaje adecuado.

    Returns:
        redirect: Redirige a la página principal de artículos si no se proporciona un ID válido o si ocurre un error.
        render_template: Si el ID es válido, muestra el formulario de edición del artículo con los detalles y los usuarios.
    """
    try:
        id_a = request.args.get("art_id", None)
        if id_a:
            resp = obtener_articulo(id_a)
            users = list_users_nopage()
            return render_template(
                "archivos/editar.html",
                articulo=resp["articulo"],
                usuarios=users,
                id=id_a
            )
        else:
            flash("No se proporcionó un ID válido.", "warning")
    except Exception as e:
        flash(f"Ocurrió un error al encontrar el artículo: {str(e)}", "danger") 
    return redirect(url_for("articulo.home_articulos")) 

@bp.post("/update")
@login_required
@blocked_user
@check("art_update")
def update():
    """
    Actualiza los detalles de un artículo existente.

    La función obtiene los datos del formulario de actualización y el ID del artículo a través de los parámetros de la URL.
    Luego, valida que todos los campos obligatorios estén presentes. Si los campos son válidos y el artículo existe,
    la función actualiza el artículo en la base de datos. Si el artículo se marca como "Publicado", se establece la fecha
    de publicación. Al finalizar, se muestra un mensaje de éxito. Si ocurre un error, se muestra un mensaje de error.

    Returns:
        redirect: Redirige a la página principal de artículos después de la actualización.
    """
    try:
        resp = dict(request.form)
        id_a = request.args.get("id_a",None)
        if not validar_campos_obligatorios(resp,["titulo", "copete", "autor_id", "contenido", "estado"]):
            return redirect(url_for("articulo.home_articulos"))
        if id_a:
            if resp["estado"] == "Publicado":
                if not obtener_estado(id_a):
                    resp["fecha_publicacion"] = datetime.now()
                    resp["publico"] = True
            resp["fecha_actualizacion"] = datetime.now()
            actualizar_articulo(id_a,**resp) 
            flash("Artículo actualizado exitosamente.", "success")
    except Exception as e:
        flash(f"Ocurrió un error al encontrar el artículo: {str(e)}", "danger") 
    return redirect(url_for("articulo.home_articulos"))

@bp.get("/show")
@login_required
@blocked_user
@check("art_show")
def show():
    """
    Muestra los detalles de un artículo específico.

    La función obtiene el ID de un artículo desde los parámetros de la URL. Si se proporciona un ID válido,
    consulta la base de datos o alguna fuente de datos para obtener los detalles del artículo y luego renderiza
    el template correspondiente, mostrando la información del artículo. Si no se proporciona un ID válido o
    ocurre algún error durante el proceso, se muestra un mensaje de advertencia o error.

    Returns:
        - render_template: renderiza el template `archivos/view.html` mostrando los detalles del artículo.
        - redirect: Si no se proporciona un ID válido o ocurre un error, redirige a la página principal de artículos.
    """
    try:
        id_a = request.args.get("art_id", None)
        if id_a:
            resp = obtener_articulo(id_a)
            return render_template(
                "archivos/view.html",
                articulo=resp["articulo"]
            )
        else:
            flash("No se proporcionó un ID válido.", "warning")
    except Exception as e:
        flash(f"Ocurrió un error al encontrar el artículo: {str(e)}", "danger")  
    return redirect(url_for('articulo.home_articulos'))