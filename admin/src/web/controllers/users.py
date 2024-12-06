from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from core.models.User import (
    create_user,
    list_users,
    find_user_by_fields,
    delete_user,
    find_user_by_email,
    edit_user,
)
from core.models.Roles import list_roles
from core.database import db
from .validaciones import (
    validar_email,
    validar_opcion_seleccionada,
    validar_campos_obligatorios,
    validar_is_admin,
)
from web.handlers.auth import check, login_required, blocked_user, check_permissions

app = Flask(__name__)

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/")
@login_required
@blocked_user
@check("user_index")
def render():
    """
    Renderiza la página principal de usuarios con la lista de todos los usuarios.

    Esta vista requiere que el usuario esté autenticado, no esté bloqueado y
    tenga el permiso 'user_index' para acceder a la página.

    Obtiene la lista de roles y la lista de usuarios en función de los parámetros de paginación y ordenamiento.

    Parámetros en la URL:
        - page (int): El número de página para la paginación. Por defecto es 1.
        - orden (str): Determina si el orden es ascendente o descendente. Debe ser "True" para ascendente.

    Returns:
        str: Renderiza la plantilla 'usuarios/usuarios.html' con la lista de usuarios y roles.
    """
    roles = list_roles()
    page = request.args.get("page", 1, type=int)
    if not isinstance(page, int):
        flash("Error al procesar la petición. Por favor, intente nuevamente.", "error")
        return redirect(url_for("home_page"))
    orden = request.args.get("orden", "") == "True"
    all_users = list_users(orden, page=page, per_page=2)
    return render_template("usuarios/usuarios.html", users=all_users, rol=roles)


@bp.route("/user_form", methods=["GET", "POST"])
@login_required
@blocked_user
@check_permissions("user_new", "user_update")
def render_form():
    """
    Renderiza el formulario de usuario para crear o actualizar usuarios.

    Esta vista requiere que el usuario esté autenticado y tenga los permisos
    'user_new' o 'user_update' para acceder. Puede manejar solicitudes GET y POST.

    - Si la solicitud es GET, renderiza un formulario vacío para crear un nuevo usuario.
    - Si la solicitud es POST, busca el usuario en la base de datos por email y
      renderiza el formulario con los datos del usuario encontrado para su actualización.

    Returns:
        str: Renderiza la plantilla 'usuarios/usuarios_form.html' con la lista de roles
        y, en el caso de una solicitud POST, con los datos del usuario encontrado.
    """
    roles = list_roles()

    if request.method == "GET":
        return render_template("usuarios/usuarios_form.html", rol=roles, user=None)
    else:
        email = request.form.get("email")
        if not validar_email(email):
            flash("El email no es válido", "error")
            return render_template("usuarios/usuarios_form.html", rol=roles, user=None)
        user = find_user_by_email(email)
        if validar_is_admin(user):
            flash("No se puede editar un usuario con el rol SystemAdmin", "error")
            return redirect(url_for("user.render"))
        if user is None:
            flash("El usuario a editar no existe", "error")
            return redirect(url_for("user.render"))
        return render_template("usuarios/usuarios_form.html", rol=roles, user=user)


@bp.get("/buscar")
@login_required
@blocked_user
@check("user_index")
def render_search():
    """
    Renderiza la página de búsqueda de usuarios en función de varios filtros y parámetros de ordenamiento.

    Esta vista requiere que el usuario esté autenticado y tenga el permiso 'user_index' para acceder.

    Parámetros en la URL:
        - email (str): El email del usuario para buscar.
        - orden (str): Determina si el orden es ascendente o descendente. Debe ser "True" para ascendente.
        - orden_by (str): El campo por el cual se ordenarán los usuarios (por defecto 'mail').
        - activo (str): Filtra usuarios activos o inactivos.
        - rol (str): Filtra usuarios por rol específico.
        - page (int): El número de página para la paginación. Por defecto es 1.

    Returns:
        str: Renderiza la plantilla 'usuarios/usuarios.html' con la lista de usuarios filtrados y roles.
    """
    roles = list_roles()

    email = request.args.get("email", "")
    orden = request.args.get("orden", "False") == "True"
    orden_by = request.args.get("orden_by", "mail")
    activo = request.args.get("activo")
    rol = request.args.get("rol", "")
    all_roles = [role.name for role in list_roles()]
    if rol and not validar_opcion_seleccionada(rol, all_roles):
        return redirect(url_for("user.render"))
    page = request.args.get("page", 1, type=int)
    if not isinstance(page, int):
        flash("Error al procesar la petición. Por favor, intente nuevamente.", "error")
        return redirect(url_for("home_page"))
    usuarios = find_user_by_fields(
        email=email,
        orden=orden,
        orden_by=orden_by,
        is_activo=activo,
        rol=rol,
        page=page,
        per_page=2,
    )
    return render_template("usuarios/usuarios.html", users=usuarios, rol=roles)


@bp.post("/register")
@login_required
@blocked_user
@check("user_new")
def user_register():
    """
    Registra un nuevo usuario en el sistema.

    Esta vista requiere que el usuario esté autenticado y tenga el permiso 'user_new' para acceder.

    - Si el email proporcionado ya existe, muestra un mensaje de error y redirige al formulario de usuario.
    - Si el email no existe, crea el usuario con los datos proporcionados.

    Returns:
        Response: Redirige a la página principal de usuarios después de registrar el usuario o mostrar un error.
    """

    datos = request.form.to_dict()
    if not validar_email(datos["email"]):
        return redirect(url_for("user.render_form"))
    datos["role_id"] = int(datos["role_id"])
    datos["activo"] = datos.get("activo") == "True"
    if (
        not isinstance(datos["role_id"], int)
        or not isinstance(datos["alias"], str)
        or not isinstance(datos["password"], str)
        or not isinstance(datos["activo"], bool)
    ):
        flash("Los datos ingresados no son válidos", "error")
        return redirect(url_for("user.render_form"))

    user = find_user_by_email(datos["email"])
    if user:
        flash("Ya existe un usuario con ese email", "error")
        return redirect(url_for("user.render_form"))
    if not create_user(**datos):
        flash("No existe un miembro con ese email", "error")
        return redirect(url_for("user.render_form"))

    flash("Usuario registrado exitosamente", "success")
    return redirect(url_for("user.render"))


@bp.post("/delete")
@login_required
@blocked_user
@check("user_destroy")
def user_delete():
    """
    Elimina un usuario en función del email proporcionado.

    Esta vista requiere que el usuario esté autenticado y tenga el permiso 'user_destroy' para acceder.

    - Si el usuario es eliminado con éxito, muestra un mensaje de éxito.
    - Si no se puede eliminar, muestra un mensaje de error.

    Returns:
        Response: Redirige a la página principal de usuarios después de la operación.
    """
    datos = request.form.to_dict()
    if not validar_email(datos["email"]):
        return redirect(url_for("user.render"))
    user = find_user_by_email(datos["email"])
    if user is None:
        flash("El usuario no existe", "error")
        return redirect(url_for("user.render"))
    if validar_is_admin(user):
        flash("No se puede eliminar un usuario con el rol SystemAdmin", "error")
        return redirect(url_for("user.render"))
    if delete_user(datos["email"]):
        flash("Usuario eliminado exitosamente", "success")
    else:
        flash("No se pudo eliminar el usuario", "error")
    return redirect(url_for("user.render"))


@bp.post("/update")
@login_required
@blocked_user
@check("user_update")
def user_update():
    """
    Actualiza los datos de un usuario existente.

    Esta vista requiere que el usuario esté autenticado y tenga el permiso 'user_update' para acceder.

    - Si se proporcionan datos válidos y el usuario existe, actualiza la información.
    - Si los datos son inválidos o el usuario no existe, muestra un mensaje de error.

    Returns:
        Response: Redirige a la página principal de usuarios o al formulario en caso de error.
    """
    datos = request.form.to_dict()
    if not validar_campos_obligatorios(
        datos, ["email", "role_id", "alias", "activo", "old_email"]
    ):
        return redirect(url_for("user.render_form"))
    datos["role_id"] = int(datos["role_id"])
    if not validar_email(datos["old_email"]) and validar_email(datos["email"]):
        return redirect(url_for("user.render_form"))
    if (
        not isinstance(datos["role_id"], int)
        or not isinstance(datos["alias"], str)
        or not isinstance(datos["password"], str)
    ):
        flash("Los datos ingresados no son válidos", "error")
        return redirect(url_for("user.render_form"))

    user = find_user_by_email(datos["email"])
    if user is None:
        flash("El usuario no existe", "error")
        return redirect(url_for("user.render"))
    if validar_is_admin(user):
        flash("No se puede editar un usuario con el rol SystemAdmin", "error")
        return redirect(url_for("user.render"))
    datos["activo"] = datos.get("activo") == "True"
    if edit_user(**datos):
        flash("Usuario actualizado exitosamente.", "success")
    else:
        flash("El usuario no pudo ser actualizado.", "error")
    return redirect(url_for("user.render"))


@bp.post("/unblock")
@login_required
@blocked_user
@check("user_activate")
def user_unblock():
    """
    Desbloquea a un usuario en función del email proporcionado.

    Esta vista requiere que el usuario esté autenticado y tenga el permiso 'user_activate' para acceder.

    - Si el usuario es encontrado, cambia su estado a desbloqueado y guarda los cambios en la base de datos.
    - Si el usuario no es encontrado, muestra un mensaje de error.

    Returns:
        Response: Redirige a la página principal de usuarios.
    """

    email = request.form.get("email")
    user = find_user_by_email(email)
    if user is None:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("user.render"))
    if validar_is_admin(user):
        flash("No se puede desbloquear un usuario con el rol SystemAdmin", "error")
        return redirect(url_for("user.render"))
    user.activo = True
    db.session.commit()
    return redirect(url_for("user.render"))


@bp.post("/block")
@login_required
@blocked_user
@check("user_deactivate")
def user_block():
    """
    Bloquea a un usuario en función del email proporcionado.

    Esta vista requiere que el usuario esté autenticado y tenga el permiso 'user_deactivate' para acceder.

    - Si el usuario es encontrado, cambia su estado a bloqueado y guarda los cambios en la base de datos.
    - Si el usuario no es encontrado, muestra un mensaje de error.

    Returns:
        Response: Redirige a la página principal de usuarios.
    """

    email = request.form.get("email")
    if not validar_email(email):
        return redirect(url_for("user.render"))
    user = find_user_by_email(email)
    if user is None:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("user.render"))
    if validar_is_admin(user):
        flash("No se puede bloquear un usuario con el rol SystemAdmin", "error")
        return redirect(url_for("user.render"))
    user.activo = False
    db.session.commit()
    return redirect(url_for("user.render"))
