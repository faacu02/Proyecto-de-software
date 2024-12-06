from flask import Blueprint, request, jsonify
import requests
from datetime import datetime
from core.models import Contacto as contactoDB
from web.schemas.contacto import (
    contacto_schema,
)

bp = Blueprint("contacto_api", __name__, url_prefix="/api/contacto")


@bp.post("/register")
def registrar_contacto():
    """
    Registra un nuevo contacto en la base de datos.

    Esta función recibe un conjunto de parámetros a través de `kwargs`,
    crea una instancia de `Contacto`, la añade a la sesión de la base
    de datos y luego guarda el registro en la base de datos.

    Args:
        **kwargs: Argumentos necesarios para crear el contacto, como campos clave-valor.

    Returns:
        Contacto: El contacto creado y guardado en la base de datos.
    """
    try:
        data = request.get_json()
        name = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        mensaje = data.get("mensaje")
        recaptcha_token = data.pop("recaptcha_token")
        errors = contacto_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        if  not recaptcha_token:
           return {"error": "Falta Captcha"}, 400
        recaptcha_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": "6Ld-3YIqAAAAANdDCulpFE2WfXM5SfrWfDTR4ouu",
                "response": recaptcha_token,
            },
        )
        recaptcha_result = recaptcha_response.json()

        if not recaptcha_result.get("success"):
            return jsonify({"error": "Falló la verificación de reCAPTCHA."}), 400

        contacto = contactoDB.create_contacto(
            name, apellido, email, mensaje, datetime.now().strftime("%Y-%m-%d")
        )
        contacto = contacto_schema.dump(contacto)
        contacto["fecha_creacion"] = datetime.now().strftime("%Y-%m-%d")
        return contacto, 200
    except Exception as e:
        return {"error": f"Ocurrió un error al registrar el contacto: {str(e)}"}, 500
