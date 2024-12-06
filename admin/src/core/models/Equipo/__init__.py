from core.database import db
from sqlalchemy import asc, desc, or_
from core.models.Equipo.Equipo import Equipos
from datetime import datetime


def list_equipo():
    """
    Devuelve todos los equipos que no están marcados como borrados.

    Returns:
        list: Lista de diccionarios que representan los equipos no borrados.
    """
    team = Equipos.query.filter_by(borrado=False).all()
    return team


def list_equipo_dict():
    """
    Devuelve todos los equipos que no están marcados como borrados.
    """
    team = Equipos.query.filter_by(borrado=False).all()
    team_list = [tm.to_dict() for tm in team]
    return team_list


def list_equipo_spf(puesto):
    """
    Devuelve todos los equipos que no están marcados como borrados y que tienen el puesto laboral indicado.
    """
    try:
        if puesto == "Profesor de Equitacion":
            team = (
                Equipos.query.filter_by(borrado=False)
                .filter(
                    or_(
                        Equipos.puesto_laboral == puesto,
                        Equipos.puesto_laboral == "Terapeuta",
                    )
                )
                .all()
            )
            team_list = [equipo.to_dict() for equipo in team]
        else:
            team = (
                Equipos.query.filter_by(borrado=False)
                .filter_by(puesto_laboral=puesto)
                .all()
            )
            team_list = [equipo.to_dict() for equipo in team]
        return team_list
    except Exception as e:
        return {e: "Contacte con el administrador"}


def actualizar_miembro(miembro, params, activo):
    """
    Actualiza los campos del miembro con los valores proporcionados en params.

    Args:
        miembro (Equipos): El objeto miembro a actualizar.
        params (dict): Diccionario con los valores a actualizar.

    Returns:
        Equipos: El objeto miembro actualizado.
    """
    miembro.nombre = params.get("nombre", miembro.nombre)
    miembro.apellido = params.get("apellido", miembro.apellido)
    miembro.dni = params.get("dni", miembro.dni)
    miembro.domicilio = params.get("domicilio", miembro.domicilio)
    miembro.email = params.get("email", miembro.email)
    if miembro.usuario:
        miembro.usuario.email = params.get("email", miembro.email)
    miembro.localidad = params.get("localidad", miembro.localidad)
    miembro.telefono = params.get("telefono", miembro.telefono)
    miembro.profesion = params.get("profesion", miembro.profesion)
    miembro.puesto_laboral = params.get("puesto_laboral", miembro.puesto_laboral)
    miembro.fecha_inicio = datetime.strptime(params.get("fecha_inicio"), "%Y-%m-%d")
    miembro.fecha_cese = datetime.strptime(params.get("fecha_cese"), "%Y-%m-%d")
    miembro.contacto_emergencia_nombre = params.get(
        "contacto_emergencia_nombre", miembro.contacto_emergencia_nombre
    )
    miembro.contacto_emergencia_telefono = params.get(
        "contacto_emergencia_telefono", miembro.contacto_emergencia_telefono
    )
    miembro.obra_social = params.get("obra_social", miembro.obra_social)
    miembro.num_afiliado = params.get("num_afiliado", miembro.num_afiliado)
    miembro.condicion = params.get("condicion", miembro.condicion)
    miembro.activo = activo
    miembro.titulo = params.get("titulo", miembro.titulo)
    miembro.copia_dni = params.get("copia_dni", miembro.copia_dni)
    miembro.cv_actualizado = params.get("cv_actualizado", miembro.cv_actualizado)
    return miembro


def find_member_by_email(email):
    """
    Busca un miembro del equipo por su email.

    Args:
        email (str): El email del miembro del equipo.

    Returns:
        Equipos: El objeto miembro si se encuentra, de lo contrario, None.
    """
    member = Equipos.query.filter_by(email=email, borrado=False).first()
    return member


def find_member_by_dni(dni):
    """
    Busca un miembro del equipo por su DNI.

    Args:
        dni (str): El DNI del miembro del equipo.

    Returns:
        Equipos: El objeto miembro si se encuentra, de lo contrario, None.
    """
    member = Equipos.query.filter_by(dni=dni, borrado=False).first()
    return member


def create_member(
    nombre,
    apellido,
    dni,
    domicilio,
    email,
    localidad,
    telefono,
    contacto_emergencia_nombre,
    contacto_emergencia_telefono,
    profesion,
    puesto_laboral,
    fecha_inicio,
    condicion,
    activo,
    fecha_cese,
    obra_social,
    num_afiliado,
    titulo=None,
    copia_dni=None,
    cv_actualizado=None,
):
    """
    Crea un nuevo miembro del equipo y lo agrega a la base de datos.

    Args:
        nombre (str): El nombre del miembro del equipo.
        apellido (str): El apellido del miembro del equipo.
        dni (str): El DNI del miembro del equipo.
        domicilio (str): La dirección del miembro del equipo.
        email (str): El email del miembro del equipo.
        localidad (str): La localidad del miembro del equipo.
        telefono (str): El número de teléfono del miembro del equipo.
        contacto_emergencia_nombre (str): El nombre del contacto de emergencia.
        contacto_emergencia_telefono (str): El teléfono del contacto de emergencia.
        profesion (str): La profesión del miembro del equipo.
        puesto_laboral (str): El puesto laboral del miembro del equipo.
        fecha_inicio (str): La fecha de inicio del miembro del equipo.
        condicion (str): La condición del miembro del equipo.
        activo (bool): Indica si el miembro está activo.
        fecha_cese (str, optional): La fecha de cese del miembro del equipo.
        obra_social (str): La obra social del miembro del equipo.
        num_afiliado (int): El número de afiliado del miembro del equipo.
        titulo (str, optional): El título del miembro del equipo.
        copia_dni (str, optional): La copia del DNI del miembro del equipo.
        cv_actualizado (str, optional): El CV actualizado del miembro del equipo.

    Returns:
        Equipos: El objeto miembro recién creado y guardado en la base de datos.
    """
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_cese = datetime.strptime(fecha_cese, "%Y-%m-%d")

    team = Equipos(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        domicilio=domicilio,
        email=email,
        localidad=localidad,
        telefono=telefono,
        contacto_emergencia_nombre=contacto_emergencia_nombre,
        contacto_emergencia_telefono=contacto_emergencia_telefono,
        profesion=profesion,
        puesto_laboral=puesto_laboral,
        fecha_inicio=fecha_inicio,
        fecha_cese=fecha_cese,
        condicion=condicion,
        activo=activo,
        titulo=titulo,
        obra_social=obra_social,
        num_afiliado=num_afiliado,
        copia_dni=copia_dni,
        cv_actualizado=cv_actualizado,
    )
    db.session.add(team)
    db.session.commit()
    return team


def get_memberby_id(id):
    """
    Busca un miembro del equipo por su ID.

    Args:
        id (int): El ID del miembro del equipo.

    Returns:
        Equipos: El objeto miembro si se encuentra, de lo contrario, None.
    """
    member = Equipos.query.filter_by(id=id, borrado=False).first()
    return member


def delete_member(id):
    """
    Elimina lógicamente un miembro del equipo por su ID, marcándolo como borrado.

    Args:
        id (int): El ID del miembro del equipo.

    Returns:
        Equipos: El objeto miembro si se encuentra y se marca como borrado, de lo contrario, None.
    """
    member = get_memberby_id(id)
    if member is None:
        return None
    member.borrado = True
    if member.usuario:
        member.usuario.borrado = True
    db.session.commit()
    return member


def find_member_by_fields(
    email, orden, direccion, nombre, apellido, dni, puesto, page=1, per_page=10
):
    """
    Busca miembros del equipo por varios campos y devuelve los resultados paginados.

    Args:
        email (str): El email del miembro.
        orden (str): El campo por el cual ordenar.
        direccion (str): La dirección de ordenamiento ('asc' o 'desc').
        nombre (str): El nombre del miembro.
        apellido (str): El apellido del miembro.
        dni (str): El DNI del miembro.
        puesto (str): El puesto laboral del miembro.
        page (int, optional): Número de página para la paginación. Por defecto es 1.
        per_page (int, optional): Cantidad de miembros por página. Por defecto es 10.

    Returns:
        Pagination: Un objeto de paginación con la lista de miembros que coinciden con los filtros.
    """
    query = Equipos.query.filter_by(borrado=False)
    if email:
        query = query.filter(Equipos.email.ilike(f"%{email}%"))
    if nombre:
        query = query.filter(Equipos.nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Equipos.apellido.ilike(f"%{apellido}%"))
    if dni:
        query = query.filter(Equipos.dni.ilike(f"%{dni}%"))
    if puesto:
        query = query.filter(Equipos.puesto_laboral.ilike(f"%{puesto}%"))
    if direccion == "asc":
        if orden == "nombre":
            query = query.order_by(asc(Equipos.nombre))
        elif orden == "apellido":
            query = query.order_by(asc(Equipos.apellido))
        else:
            query = query.order_by(asc(Equipos.fecha_inicio))
    else:
        if orden == "nombre":
            query = query.order_by(desc(Equipos.nombre))
        elif orden == "apellido":
            query = query.order_by(desc(Equipos.apellido))
        else:
            query = query.order_by(desc(Equipos.fecha_inicio))

    members = query.paginate(page=page, per_page=per_page, error_out=False)
    return members
