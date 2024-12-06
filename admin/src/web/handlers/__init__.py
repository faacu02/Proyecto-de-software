from flask import render_template, url_for
from dataclasses import dataclass


@dataclass
class Error:
    code: int
    img: str
    message: str
    description: str


def error_not_found(e):
    img_path = url_for("static", filename="404.jpg")
    error = Error(404, img_path, "No encontrado", "La url solicitada no existe")
    return render_template("error.html", error=error), 404


def error_unauthorized(e):
    img_path = url_for("static", filename="401.jpg")
    error = Error(
        401,
        img_path,
        "No autorizado",
        "Parece que no tienes una sesion iniciada todavia!",
    )
    return render_template("error.html", error=error), 401


def error_forbidden(e):
    img_path = url_for("static", filename="403.jpg")
    error = Error(
        403, img_path, "No autorizado", "No tienes permisos para acceder a esta url"
    )
    return render_template("error.html", error=error), 403


def error_blocked(e):
    img_path = url_for("static", filename="504.jpg")
    error = Error(
        504,
        img_path,
        "Usuario bloqueado",
        "Tu usuario ha sido bloqueado, para mas informacion consultar con el area administrativa",
    )
    return render_template("error.html", error=error), 504
