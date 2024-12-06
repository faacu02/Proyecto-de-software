from flask import Blueprint, request, Flask, abort
from flask import render_template, redirect, url_for, flash, session
from core.models import User as auth
from web.handlers.auth import login_required
from core.models.User import find_user_by_email
from core.models.Pendiente import buscar_pendiente_email, cargar_pendiente

app = Flask(__name__)

bp = Blueprint("auth", __name__, url_prefix="/auth")






@bp.get("/")
def login():
    """
    Renderiza la página de inicio de sesión.

    Returns:
        str: Renderización de la plantilla `login.html` para mostrar el formulario de inicio de sesión.
    """
    return render_template("auth/login.html")


@bp.post("/authenticate")
def authenticate():
    """
    Autentica al usuario con las credenciales proporcionadas.

    Recibe los datos del formulario de inicio de sesión (email y contraseña)
    y verifica si el usuario existe en la base de datos. Si las credenciales
    son correctas y el usuario no está bloqueado, inicia la sesión.

    Returns:
        werkzeug.wrappers.Response: Redirige a la página principal si la autenticación
        es exitosa. En caso de error, redirige al formulario de inicio de sesión.
    """
    params = request.form

    user = auth.check_user(params["email"], params["password"])
    if not user:
        flash("Email y/o contraseña incorrecta", "error")
        return redirect(url_for("auth.login"))
    if not user.activo:
        abort(504)

    session["user"] = user.email
    flash("Sesion iniciada exitosamente", "success")
    return redirect(url_for("home_page"))


@bp.get("/logout")
@login_required
def logout():
    """
    Cierra la sesión actual del usuario.

    Si existe una sesión activa, se elimina y se limpia la sesión. Si no hay
    sesión activa, muestra un mensaje de error.

    Returns:
        werkzeug.wrappers.Response: Redirige al formulario de inicio de sesión
        después de cerrar la sesión o si no hay sesión activa.
    """
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesión cerrada", "info")
    else:
        flash("No hay sesión activa", "error")

    return redirect(url_for("auth.login"))

