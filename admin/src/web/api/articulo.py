from flask import Blueprint, request, jsonify
import math
from core.models import Articulo
from web.schemas.articulo import articulo_schema, articulos_schema
from web.controllers.validaciones import validar_fechas, validar_fecha_anterior

bp = Blueprint("articulo_api", __name__, url_prefix="/api/articulo")


@bp.get("/filtrar")
def filtrar_articulos():
    """
    Filtra artículos según parámetros opcionales y realiza la paginación.

    Este endpoint permite filtrar artículos basados en el autor, un rango de
    fechas de publicación y realizar la paginación de los resultados.

    Query Parameters:
        author (str, opcional): Nombre y apellido del autor relacionado al artículo.
        published_from (str, opcional): Fecha de inicio para filtrar artículos publicados (formato: YYYY-MM-DD).
        published_to (str, opcional): Fecha de fin para filtrar artículos publicados (formato: YYYY-MM-DD).
        page (int, opcional): Número de página para la paginación (por defecto: 1).
        per_page (int, opcional): Cantidad de artículos por página (por defecto: 10).
    Returns:
        dict: Un diccionario con los resultados paginados en caso de éxito:
            {
                "data": [<artículos_serializados>],
                "page": <número de página>,
                "per_page": <artículos por página>,
                "total": <cantidad total de artículos>,
                "cantidad_paginas": <total de páginas>
            }
        En caso de error, retorna un diccionario con el mensaje de error y un código de estado 500:
    """
    try:
        data = request.args
        autor = data.get("author", "")
        published_from = data.get("published_from", "")
        published_to = data.get("published_to", "")
        page = int(data.get("page", 1))
        per_page = int(data.get("per_page", 10))
        x = {}
        if published_from:
            fecha_str = data.get("published_from").split("T")[0]
            x["published_from"] = fecha_str
        if published_to:
            fecha_str = data.get("published_to").split("T")[0]
            x["published_to"] = fecha_str
        if published_from:
            if not validar_fecha_anterior(x, ["published_from"]):
                return {
                    "error": "La fecha de publicación desde no puede ser mayor a la fecha actual"
                }, 400
        if published_to:
            if not validar_fecha_anterior(x, ["published_to"]):
                return {
                    "error": "La fecha de publicación hasta no puede ser mayor a la fecha actual"
                }, 400
        if published_to and published_from:
            if not validar_fechas(x["published_from"], x["published_to"]):
                return {
                    "error": "La fecha de publicación desde no puede ser mayor a la fecha de publicación hasta"
                }, 400
        articulos = Articulo.listar_articulos_api(
            autor, published_from, published_to, page, per_page
        )
        response = {
            "data": articulos_schema.dump(articulos),
            "page": page,
            "per_page": per_page,
            "total": articulos.total,
            "cantidad_paginas": math.ceil(articulos.total / per_page),
        }
        return jsonify(response), 200
    except Exception as e:
        return {"error": f"Ocurrió un error al filtrar los articulos: {str(e)}"}, 500

@bp.get("/<int:id>")
def obtener_articulo(id):
    """
    Obtiene un artículo por su ID.

    :param id: ID del artículo.
    :return: El artículo si existe, de lo contrario un mensaje de error.
    """
    try:
        articulo = Articulo.obtener_articulo(id)
        if articulo["success"]:
            art = articulo["articulo"]
            if art.estado == "Publicado":
                return articulo_schema.dump(art), 200
            else:
                return jsonify({"error": "Artículo no encontrado"}), 404
        else:
            return jsonify({"error": "Artículo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500