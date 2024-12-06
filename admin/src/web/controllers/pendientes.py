from core.models.Pendiente.Pendiente import Pendientes
from core.models.User import create_user
from core.models.Roles import list_roles
from core.models.Pendiente import listar_pendientes, eliminar_pend
from flask import Blueprint, flash, request, render_template, redirect, url_for, session
from web.controllers.validaciones import validar_campos_obligatorios
from web.handlers.auth import login_required, check, blocked_user

bp = Blueprint("pendiente", __name__, url_prefix="/pendiente")


@bp.get("/")
@login_required
@blocked_user
@check("pen_create")
def home_pend():
    """
    Retorna el template de la página principal de usuarios pendientes.

    La función obtiene los parámetros de la página y muestra la lista de usuarios pendientes, con paginación, 
    en el template `pendientes/home.html`. La paginación se maneja mediante los parámetros `page` y `per_page`, 
    que determinan la página actual y la cantidad de usuarios a mostrar por página.

    La función también calcula el número total de páginas basado en la cantidad total de usuarios pendientes
    y el valor fijo de `per_page`.

    Returns:
        - render_template: renderiza el template `pendientes/home.html` con la lista de usuarios pendientes, 
          el número total de páginas, y los parámetros de paginación.
    """
    page = request.args.get("page",1, int)
    resp = listar_pendientes(page)
    return render_template("pendientes/home.html", usuarios_pendientes=resp["users"], total_paginas=int(resp["total"]/5)+1 ,page=page, per_page=5)

@bp.get("/user_accept")
@login_required
@blocked_user
@check("pen_create")
def accept_user():
    """
    Maneja la lógica para mostrar un formulario de edición de usuario pendiente, donde se pueden actualizar el alias 
    y asignar un rol a un usuario pendiente.

    La función espera recibir dos parámetros a través de la URL (`email` y `alias`), que son pasados al template 
    "pendientes/edit.html". También obtiene la lista de roles disponibles, que es pasada al template para que el 
    administrador pueda seleccionar un rol para el usuario.

    Si ocurre algún error durante el proceso, el mismo será capturado y devuelto como una excepción.

    Returns:
        - Si todo va bien, renderiza el template "pendientes/edit.html" con los valores de `email`, `alias` y los 
          roles disponibles.
        - En caso de error, devuelve el mensaje de excepción correspondiente.
    """
    try:
        session.pop("email_us",None)
        email = request.args.get("email")
        alias = request.args.get("alias")
        session["email_us"] = email
        rol = list_roles()
        return render_template("pendientes/edit.html", email=email, alias=alias, rol=rol)
    except Exception as e:
        return e


@bp.post("/enable")
@login_required
@blocked_user
@check("pen_create")
def enable_user():
    """
    Habilita un usuario pendiente, sacándolo de la lista de pendientes y creándolo como un usuario activo en el sistema.

    La función recibe los datos del formulario enviado, asigna una contraseña predeterminada al usuario, 
    marca al usuario como activo y luego lo crea en el sistema utilizando la función `create_user`. 
    Si el usuario con el email proporcionado no existe, se le solicita al administrador crear el miembro correspondiente.

    Si la creación del usuario es exitosa, el usuario se elimina de la lista de pendientes y se muestra un mensaje 
    de éxito. En caso contrario, se muestra un mensaje de advertencia.

    Returns:
        - Redirige al usuario a la lista de usuarios pendientes después de habilitar al usuario.
    """
    resp = dict(request.form)
    resp["password"] = "gs_.ddqwksd>"
    resp["activo"] = True
    email_check = session.get("email_us")
    print(email_check, " and ", resp["email"])
    if email_check != resp["email"]:
        flash("Datos no validos del email ingresado", "danger")
        return redirect(url_for("pendiente.home_pend"))
    if not validar_campos_obligatorios(resp,["email","alias","role_id"]):
        return redirect(url_for("pendiente.home_pend"))
    response = create_user(**resp)
    if not response:
        flash("No existe un miembro con ese email, cree un miembro que tenga ese email para continuar", "warning")
    else:
        eliminar_pend(resp["email"])
        flash("Se ha habilitado el usuario correctamente", "success")
    return redirect(url_for('pendiente.home_pend'))


@bp.post("/discart")
@login_required
@blocked_user
@check("pen_create")
def rechazar_user():
    """
    Elimina un usuario pendiente de la lista en caso de encontrarlo.

    La función recibe el correo electrónico del usuario pendiente desde los parámetros de la solicitud (`request.args`), 
    y si se encuentra un usuario con ese correo, se elimina de la lista de pendientes utilizando la función `eliminar_pend`.
    Si el proceso es exitoso, se muestra un mensaje de éxito; de lo contrario, se muestra un mensaje de error.

    Returns:
        - Redirige a la vista de la lista de usuarios pendientes (`pendiente.home_pend`).
    """

    email = request.args.get("email", None)
    if email:
        eliminar_pend(email)
        flash("Usuario pendiente eliminado correctamente", "success")
    else:
        flash("No se pudo eliminar al usuario pendiente", "danger")
    return redirect(url_for("pendiente.home_pend"))