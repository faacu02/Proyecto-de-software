from datetime import datetime
from core.models.Roles.Roles import Rol
from core.models.Permissions.Permissions import Permission
from core.models.User import create_user
from core.models.Equipo import create_member
from core.models import Encuestre as ec
from core.models import Equipo as EquipoDB
from core.models import Legajo as JABD
from core.models.Pago.Pago import Pagos
from core.models.Contacto.__init__ import create_contacto
from core.models.Articulo.__init__ import crear_articulo
from core.database import db


def run():
    """
    Carga la base dedatos de los roles y permisos, y ejemplos.
    """
    print("sedding database")
    # Creando los permisos

    # Modulo de usuarios
    user_index = Permission(name="user_index")
    user_update = Permission(name="user_update")
    user_new = Permission(name="user_new")
    user_destroy = Permission(name="user_destroy")
    user_show = Permission(name="user_show")
    user_activate = Permission(name="user_activate")
    user_deactivate = Permission(name="user_deactivate")

    # Modulo pagos
    pagos_show = Permission(name="pagos_show")
    pagos_index = Permission(name="pagos_index")
    pagos_destroy = Permission(name="pagos_destroy")
    pagos_create = Permission(name="pagos_create")
    pagos_update = Permission(name="pagos_update")

    # Modulo de equipo
    equipo_index = Permission(name="equipo_index")
    equipo_update = Permission(name="equipo_update")
    equipo_new = Permission(name="equipo_new")
    equipo_destroy = Permission(name="equipo_destroy")
    equipo_show = Permission(name="equipo_show")

    # Modulo de ecuestres
    ecuestre_show = Permission(name="ecuestre_show")
    ecuestre_index = Permission(name="ecuestre_index")
    ecuestre_create = Permission(name="ecuestre_create")
    ecuestre_update = Permission(name="ecuestre_update")
    ecuestre_destroy = Permission(name="ecuestre_destroy")
    
    # Modulo contacto
    
    contacto_index = Permission(name="contacto_index")
    contacto_show = Permission(name="contacto_show")
    contacto_update = Permission(name="contacto_update")
    contacto_destroy = Permission(name="contacto_destroy")

    # Modulo Tecnica
    tecnica_show = Permission(name="tecnica_show")

    # Moudulo Voluntariado
    voluntariado_show = Permission(name="voluntariado_show")
    # Modulo pagos
    pagos_show = Permission(name="pagos_show")
    pagos_index = Permission(name="pagos_index")
    pagos_destroy = Permission(name="pagos_destroy")
    pagos_create = Permission(name="pagos_create")
    pagos_update = Permission(name="pagos_update")

    # Modulo Cobros
    cobro_index = Permission(name="cobro_index")
    cobro_show = Permission(name="cobro_show")
    cobro_update = Permission(name="cobro_update")
    cobro_create = Permission(name="cobro_create")
    cobro_destroy = Permission(name="cobro_destroy")

    # Modulo JyA
    jya_index = Permission(name="jya_index")
    jya_show = Permission(name="jya_show")
    jya_update = Permission(name="jya_update")
    jya_create = Permission(name="jya_create")
    jya_destroy = Permission(name="jya_destroy")

    # Modulo Articulo
    art_index = Permission(name="art_index")
    art_show = Permission(name="art_show")
    art_update = Permission(name="art_update")
    art_create = Permission(name="art_create")
    art_destroy = Permission(name="art_destroy")

    # Modulo Pendiente
    pen_create = Permission(name="pen_create")


    # Modulo de administracion
    admin_show = Permission(name="admin_show")
    # Modulo de Reportes
    reportes_index = Permission(name="reportes_index")
    reportes_show = Permission(name="reportes_show")
    # Añadiendo los permisos
    db.session.add_all(
        [
            user_index,
            user_update,
            user_new,
            user_destroy,
            user_show,
            user_activate,
            user_deactivate,
            ecuestre_show,
            tecnica_show,
            voluntariado_show,
            admin_show,
            cobro_index,
            cobro_show,
            cobro_update,
            cobro_destroy,
            cobro_create,
            equipo_index,
            equipo_update,
            equipo_new,
            equipo_destroy,
            equipo_show,
            ecuestre_show,
            ecuestre_index,
            ecuestre_create,
            ecuestre_update,
            ecuestre_destroy,
            pagos_show,
            pagos_create,
            pagos_destroy,
            pagos_index,
            pagos_update,
            jya_create,
            jya_destroy,
            jya_index,
            jya_show,
            jya_update,
            contacto_index,
            contacto_show,
            contacto_update,
            contacto_destroy,
            reportes_index,
            reportes_show,
            art_index,
            art_show,
            art_create,
            art_update,
            art_destroy,
            pen_create
        ]
    )
    db.session.commit()

    # Creando los roles
    system_admin_role = Rol(name="SystemAdmin")
    ecuestre_role = Rol(name="Ecuestre")
    tecnica_role = Rol(name="Tecnica")
    voluntariado_role = Rol(name="Voluntariado")
    administracion_role = Rol(name="Administracion")

    # Añadiendo los roles
    db.session.add_all(
        [
            system_admin_role,
            ecuestre_role,
            tecnica_role,
            voluntariado_role,
            administracion_role,
        ]
    )
    db.session.commit()

    # Añadiendo los permisos a los roles
    all_permissions = db.session.query(Permission).all()
    system_admin_role.permissions.extend(all_permissions)

    ecuestre_permissions = (
        db.session.query(Permission).filter(Permission.name.like("ecuestre_%")).all()
    )
    ecuestre_role.permissions.extend(ecuestre_permissions)
    ecuestre_role.permissions.append(jya_index)
    ecuestre_role.permissions.append(jya_show)

    tecnica_permissions = (
        db.session.query(Permission).filter(Permission.name.like("tecnica_%")).all()
    )
    tecnica_role.permissions.extend(tecnica_permissions)
    tecnica_role.permissions.append(cobro_show)
    tecnica_role.permissions.append(cobro_index)
    tecnica_role.permissions.append(ecuestre_show)
    tecnica_role.permissions.append(ecuestre_index)
    tecnica_role.permissions.append(jya_index)
    tecnica_role.permissions.append(jya_create)
    tecnica_role.permissions.append(jya_destroy)
    tecnica_role.permissions.append(jya_show)
    tecnica_role.permissions.append(jya_update)
    tecnica_role.permissions.append(reportes_show)
    tecnica_role.permissions.append(reportes_index)

    voluntariado_permissions = (
        db.session.query(Permission)
        .filter(Permission.name.like("voluntariado_%"))
        .all()
    )
    voluntariado_role.permissions.extend(voluntariado_permissions)

    admin_permissions = (
        db.session.query(Permission).filter(Permission.name.like("admin_%")).all()
    )

    administracion_role.permissions.extend(admin_permissions)
    administracion_role.permissions.append(user_index)
    administracion_role.permissions.append(cobro_show)
    administracion_role.permissions.append(cobro_index)
    administracion_role.permissions.append(cobro_create)
    administracion_role.permissions.append(cobro_destroy)
    administracion_role.permissions.append(cobro_update)

    administracion_role.permissions.append(equipo_update)
    administracion_role.permissions.append(equipo_new)
    administracion_role.permissions.append(equipo_destroy)
    administracion_role.permissions.append(equipo_show)
    administracion_role.permissions.append(equipo_index)

    administracion_role.permissions.append(pagos_update)
    administracion_role.permissions.append(pagos_create)
    administracion_role.permissions.append(pagos_destroy)
    administracion_role.permissions.append(pagos_show)
    administracion_role.permissions.append(pagos_index)

    administracion_role.permissions.append(ecuestre_index)
    administracion_role.permissions.append(ecuestre_show)

    administracion_role.permissions.append(pagos_index)
    administracion_role.permissions.append(pagos_create)
    administracion_role.permissions.append(pagos_destroy)
    administracion_role.permissions.append(pagos_show)
    administracion_role.permissions.append(pagos_update)

    administracion_role.permissions.append(jya_index)
    administracion_role.permissions.append(jya_create)
    administracion_role.permissions.append(jya_destroy)
    administracion_role.permissions.append(jya_show)
    administracion_role.permissions.append(jya_update)
    administracion_role.permissions.append(contacto_index)
    administracion_role.permissions.append(contacto_show)
    administracion_role.permissions.append(contacto_update)
    administracion_role.permissions.append(contacto_destroy)
    
    administracion_role.permissions.append(art_create)
    administracion_role.permissions.append(art_destroy)
    administracion_role.permissions.append(art_update)
    administracion_role.permissions.append(art_index)
    administracion_role.permissions.append(art_show)

    administracion_role.permissions.append(pen_create)

    administracion_role.permissions.append(reportes_index)
    administracion_role.permissions.append(reportes_show)
    db.session.add_all(
        [
            system_admin_role,
            ecuestre_role,
            tecnica_role,
            voluntariado_role,
            administracion_role,
        ]
    )
    db.session.commit()

    # Creando miembros
    equipo_1 = {
        "nombre": "Melman",
        "apellido": "Pacheco",
        "dni": "123451231223678",
        "domicilio": "Calle Falsa 123",
        "email": "admin@cedica.com",
        "localidad": "Buenos Aires",
        "telefono": "1112345678",
        "profesion": "Terapista Ocupacional",
        "puesto_laboral": "Terapeuta",
        "fecha_inicio": "2020-01-15",
        "fecha_cese": "2023-05-01",
        "contacto_emergencia_nombre": "MaríaLópez",
        "contacto_emergencia_telefono": "1123456789",
        "obra_social": "OSDE",
        "num_afiliado": "654321",
        "condicion": "Contratado",
        "activo": True,
    }
    EquipoDB.create_member(**equipo_1)

    equipo_2 = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "30567890",
        "domicilio": "Av. Corrientes 1234",
        "email": "user_1@cedica.com",
        "localidad": "Buenos Aires",
        "telefono": "1112345678",
        "profesion": "Docente",
        "puesto_laboral": "Conductor",
        "fecha_inicio": "2020-01-15",
        "fecha_cese": "2023-05-01",
        "contacto_emergencia_nombre": "MaríaLópez",
        "contacto_emergencia_telefono": "1123456789",
        "obra_social": "OSDE",
        "num_afiliado": "654321",
        "condicion": "Contratado",
        "activo": True,
    }
    EquipoDB.create_member(**equipo_2)

    equipo_3 = {
        "nombre": "felipe",
        "apellido": "Pérez",
        "dni": "305642347890",
        "domicilio": "Av. Corrientes 1234",
        "email": "user_3@cedica.com",
        "localidad": "Buenos Aires",
        "telefono": "1112345678",
        "profesion": "Psicopedagogo/a",
        "puesto_laboral": "Terapeuta",
        "fecha_inicio": "2020-01-15",
        "fecha_cese": "2023-05-01",
        "contacto_emergencia_nombre": "MaríaLópez",
        "contacto_emergencia_telefono": "1123456789",
        "obra_social": "OSDE",
        "num_afiliado": "654321",
        "condicion": "Contratado",
        "activo": True,
    }
    EquipoDB.create_member(**equipo_3)

    create_member(
        nombre="tadeo",
        apellido="coronel",
        dni="123456732138",
        domicilio="Calle Falsa 123",
        email="user_2@cedica.com",
        localidad="Ciudad",
        telefono="123456789",
        contacto_emergencia_nombre="MariaPerez",
        contacto_emergencia_telefono="987654321",
        profesion="Psicologo/a",
        puesto_laboral="Auxiliar de pista",
        fecha_inicio="2023-01-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-01-01",
        obra_social="OSDE",
        num_afiliado="87654321",
    )

    create_member(
        nombre="Ana",
        apellido="Gomez",
        dni="87654321",
        domicilio="Avenida Siempre Viva 742",
        email="user_4@cedica.com",
        localidad="Ciudad",
        telefono="987654321",
        contacto_emergencia_nombre="CarlosGomez",
        contacto_emergencia_telefono="123456789",
        profesion="Profesor",
        puesto_laboral="Conductor",
        fecha_inicio="2023-02-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-02-01",
        obra_social="Swiss Medical",
        num_afiliado="12345678",
    )

    # Creando usuarios
    admin_user = {
        "email": "admin@cedica.com",
        "password": "admin",
        "role_id": system_admin_role.id,
        "alias": "Admin",
        "activo": True,
    }
    create_user(**admin_user)

    user_1 = {
        "email": "user_1@cedica.com",
        "password": "user_1",
        "role_id": ecuestre_role.id,
        "alias": "Usuario 1",
        "activo": True,
    }
    create_user(**user_1)

    user_2 = {
        "email": "user_2@cedica.com",
        "password": "user_2",
        "role_id": tecnica_role.id,
        "alias": "Usuario 2",
        "activo": True,
    }
    create_user(**user_2)

    user_3 = {
        "email": "user_3@cedica.com",
        "password": "user_3",
        "role_id": voluntariado_role.id,
        "alias": "Usuario 3",
        "activo": True,
    }
    create_user(**user_3)

    user_4 = {
        "email": "user_4@cedica.com",
        "password": "user_4",
        "role_id": administracion_role.id,
        "alias": "Usuario 4",
        "activo": True,
    }
    create_user(**user_4)
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

    create_member(
        nombre="Luis",
        apellido="Martinez",
        dni="23456789",
        domicilio="Calle Luna 456",
        email="luis.martinez@example.com",
        localidad="Ciudad",
        telefono="234567890",
        contacto_emergencia_nombre="LauraMartinez",
        contacto_emergencia_telefono="345678901",
        profesion="Veterinario/a",
        puesto_laboral="Entrenador de Caballos",
        fecha_inicio="2023-03-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-03-01",
        obra_social="Galeno",
        num_afiliado="23456789",
    )

    create_member(
        nombre="Maria",
        apellido="Lopez",
        dni="34567890",
        domicilio="Calle Sol 789",
        email="maria.lopez@example.com",
        localidad="Ciudad",
        telefono="345678901",
        contacto_emergencia_nombre="JoseLopez",
        contacto_emergencia_telefono="456789012",
        profesion="Terapeuta Ocupacional",
        puesto_laboral="Terapeuta",
        fecha_inicio="2023-04-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-04-01",
        obra_social="Medicus",
        num_afiliado="34567890",
    )

    create_member(
        nombre="Carlos",
        apellido="Ramirez",
        dni="45678901",
        domicilio="Calle Estrella 101",
        email="carlos.ramirez@example.com",
        localidad="Ciudad",
        telefono="456789012",
        contacto_emergencia_nombre="AnaRamirez",
        contacto_emergencia_telefono="567890123",
        profesion="Psicólogo/a",
        puesto_laboral="Administrativo/a",
        fecha_inicio="2023-05-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-05-01",
        obra_social="OSDE",
        num_afiliado="45678901",
    )

    create_member(
        nombre="Elena",
        apellido="Fernandez",
        dni="56789012",
        domicilio="Calle Cometa 202",
        email="elena.fernandez@example.com",
        localidad="Ciudad",
        telefono="567890123",
        contacto_emergencia_nombre="LuisFernandez",
        contacto_emergencia_telefono="678901234",
        profesion="Psicomotricista",
        puesto_laboral="Entrenador de Caballos",
        fecha_inicio="2023-06-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-06-01",
        obra_social="Swiss Medical",
        num_afiliado="56789012",
    )

    create_member(
        nombre="Miguel",
        apellido="Sanchez",
        dni="67890123",
        domicilio="Calle Galaxia 303",
        email="miguel.sanchez@example.com",
        localidad="Ciudad",
        telefono="678901234",
        contacto_emergencia_nombre="MariaSanchez",
        contacto_emergencia_telefono="789012345",
        profesion="Médico/a",
        puesto_laboral="Conductor",
        fecha_inicio="2023-07-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-07-01",
        obra_social="Galeno",
        num_afiliado="67890123",
    )

    create_member(
        nombre="Laura",
        apellido="Diaz",
        dni="78901234",
        domicilio="Calle Nebulosa 404",
        email="laura.diaz@example.com",
        localidad="Ciudad",
        telefono="789012345",
        contacto_emergencia_nombre="CarlosDiaz",
        contacto_emergencia_telefono="890123456",
        profesion="Kinesiólogo/a",
        puesto_laboral="Auxiliar de pista",
        fecha_inicio="2023-08-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-08-01",
        obra_social="Medicus",
        num_afiliado="78901234",
    )

    create_member(
        nombre="Pedro",
        apellido="Gonzalez",
        dni="89012345",
        domicilio="Calle Universo 505",
        email="pedro.gonzalez@example.com",
        localidad="Ciudad",
        telefono="890123456",
        contacto_emergencia_nombre="AnaGonzalez",
        contacto_emergencia_telefono="901234567",
        profesion="Terapista Ocupacional",
        puesto_laboral="Herrero",
        fecha_inicio="2023-09-01",
        condicion="Activo",
        activo=True,
        fecha_cese="2024-09-01",
        obra_social="OSDE",
        num_afiliado="89012345",
    )

    caballo1 = {
        "nombre": "Turco",
        "fecha_nacimiento": datetime.now(),
        "sexo": "M",
        "raza": "shesh",
        "pelaje": "negro",
        "comprado": False,
        "fecha_ingreso": datetime.now(),
        "sede_asignada": "CFD",
        "tipo_JA": "hipoterapia",
    }

    ec.create_doc(**caballo1)

    legajo = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "edad": 25,
        "fecha_nacimiento": "1999-05-14",
        "lugar_nacimiento": "Buenos Aires",
        "domicilio_actual": "Calle Falsa 123",
        "telefono_actual": "01112345678",
        "contacto_emergencia": "María López",
        "tel": "01187654321",
        "becado": True,
        "porcentaje_beca": 50,
        "profesionales_atienden": "Dr. Gómez, Lic. Rodríguez",
        "deuda": False,
        "certificado_discapacidad": True,
        "diagnostico": "Trastorno del espectro autista",
        "tipo_diagnostico": "Neurológico",
        "tipo_discapacidad": "Mental",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación universal por hijo",
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "OSDE",
        "num_afiliado": "98765432",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela Nº 5",
        "direccion_escuela": "Av. Siempreviva 742",
        "telefono_escuela": "01111223344",
        "anio_actual_escuela": 5,
        "observaciones_escuela": "Buen rendimiento académico",
        "parentesco_tutor_1": "Madre",
        "nombre_tutor_1": "María",
        "apellido_tutor_1": "López",
        "dni_tutor_1": "22334455",
        "domicilio_tutor_1": "Calle Falsa 123",
        "celular_tutor_1": "01187654321",
        "email_tutor_1": "maria.lopez@example.com",
        "nivel_escolaridad_tutor_1": "Secundario completo",
        "ocupacion_tutor_1": "Docente",
        "parentesco_tutor_2": "Padre",
        "nombre_tutor_2": "Carlos",
        "apellido_tutor_2": "Pérez",
        "dni_tutor_2": "33445566",
        "domicilio_tutor_2": "Calle Falsa 123",
        "celular_tutor_2": "01199887766",
        "email_tutor_2": "carlos.perez@example.com",
        "nivel_escolaridad_tutor_2": "Universitario completo",
        "ocupacion_tutor_2": "Ingeniero",
        "propuesta_trabajo": "Hipoterapia",
        "condicion": "Activa",
        "sede": "Centro Norte",
        "dia": ["Lunes", "Miércoles"],
        "profesora_terapeuta": 1,  # ID del profesor en la tabla relacionada
        "conductor_caballo": 2,  # ID del conductor de caballo
        "caballo": 1,  # ID del caballo
        "auxiliar_pista": 4,  # ID del auxiliar de pista
    }

    JABD.create_legajo(**legajo)
    contacto1 = {
    'nombre': 'Juan',
    'apellido': 'Perez',
    'email': 'juan.perez@example.com',
    'cuerpo_mensaje': 'Este es un mensaje de prueba',
    'fecha_creacion': '2018-05-01',  # Convertir la cadena a datetime
    'estado': 'Pendiente',
    'comentario': 'Sin comentario',
    'borrado': False
}

    create_contacto(**contacto1)
    
    contacto2 = {
    'nombre': 'Maria',
    'apellido': 'Lopez',
    'email': "dadsg@gmail.com",
    'cuerpo_mensaje': 'Este es un mensaje de prueba',
    'fecha_creacion': '2022-05-01', 
    'estado': 'Pendiente',
    'comentario': 'Sin comentario',
    'borrado': False
}
    create_contacto(**contacto2)
    
    contacto3 = {
    'nombre': 'Carlos',
    'apellido': 'Ramirez',
    'email': "carlitotevez@gmail.com"   ,
    'cuerpo_mensaje': 'Este es un mensaje de prueba de contacto', 
    'fecha_creacion': '2023-05-01',
    'estado': 'Pendiente',
    'comentario': 'Sin comentario'
}
    create_contacto(**contacto3)
    
    contacto4 = {
    'nombre': 'Elena',
    'apellido': 'Fernandez',
    'email': "elena@gmail.com",
    'cuerpo_mensaje': 'Este es un mensaje de prueba',
    'fecha_creacion': '2023-05-05',
    'estado': 'Pendiente',
    'comentario': 'Sin comentario'
    }
    create_contacto(**contacto4)
    
    legajo2 = {
        "nombre": "Lucas",
        "apellido": "Ramírez",
        "dni": "99887766",
        "edad": 12,
        "fecha_nacimiento": "2012-08-17",
        "lugar_nacimiento": "Mar del Plata",
        "domicilio_actual": "Calle Colón 987",
        "telefono_actual": "02231234567",
        "contacto_emergencia": "Ana Ramírez",
        "tel": "02238765432",
        "becado": True,
        "porcentaje_beca": 100,
        "profesionales_atienden": "Dr. Pereira, Lic. Nuñez",
        "deuda": False,
        "certificado_discapacidad": True,
        "diagnostico": "Dislexia",
        "tipo_diagnostico": "Cognitivo",
        "tipo_discapacidad": "Intelectual",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación por hijo discapacitado",
        "es_veneficiaro_pension": True,
        "pension": "Pensión no contributiva",
        "obra_social": "IOMA",
        "num_afiliado": "22334455",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela N° 25",
        "direccion_escuela": "Av. Libertador 500",
        "telefono_escuela": "02235678901",
        "anio_actual_escuela": 3,
        "observaciones_escuela": "Requiere apoyo escolar",
        "parentesco_tutor_1": "Madre",
        "nombre_tutor_1": "Ana",
        "apellido_tutor_1": "Ramírez",
        "dni_tutor_1": "55443322",
        "domicilio_tutor_1": "Calle Colón 987",
        "celular_tutor_1": "02238765432",
        "email_tutor_1": "ana.ramirez@example.com",
        "nivel_escolaridad_tutor_1": "Secundario incompleto",
        "ocupacion_tutor_1": "Ama de casa",
        "parentesco_tutor_2": "Padre",
        "nombre_tutor_2": "Pablo",
        "apellido_tutor_2": "Ramírez",
        "dni_tutor_2": "33445566",
        "domicilio_tutor_2": "Calle Colón 987",
        "celular_tutor_2": "02239887766",
        "email_tutor_2": "pablo.ramirez@example.com",
        "nivel_escolaridad_tutor_2": "Secundario completo",
        "ocupacion_tutor_2": "Pescador",
        "propuesta_trabajo": "Terapia ocupacional",
        "condicion": "Inactiva",
        "sede": "Centro Este",
        "dia": ["Viernes"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }

    JABD.create_legajo(**legajo2)

    legajo3 = {
        "nombre": "Mariana",
        "apellido": "González",
        "dni": "87654321",
        "edad": 30,
        "fecha_nacimiento": "1993-03-25",
        "lugar_nacimiento": "Rosario",
        "domicilio_actual": "Calle Libertad 456",
        "telefono_actual": "03412345678",
        "contacto_emergencia": "Luis Fernández",
        "tel": "03418765432",
        "becado": True,
        "porcentaje_beca": 75,
        "profesionales_atienden": "Dr. Martinez, Lic. Sosa",
        "deuda": True,
        "certificado_discapacidad": True,
        "diagnostico": "Síndrome de Asperger",
        "tipo_diagnostico": "Neurológico",
        "tipo_discapacidad": "Intelectual",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación universal por hijo",
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "Swiss Medical",
        "num_afiliado": "12344321",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela N° 12",
        "direccion_escuela": "Av. Las Heras 1024",
        "telefono_escuela": "03415678901",
        "anio_actual_escuela": 6,
        "observaciones_escuela": "Excelente progreso",
        "parentesco_tutor_1": "Hermano",
        "nombre_tutor_1": "Luis",
        "apellido_tutor_1": "Fernández",
        "dni_tutor_1": "11223344",
        "domicilio_tutor_1": "Calle Libertad 456",
        "celular_tutor_1": "03418765432",
        "email_tutor_1": "luis.fernandez@example.com",
        "nivel_escolaridad_tutor_1": "Universitario incompleto",
        "ocupacion_tutor_1": "Comerciante",
        "parentesco_tutor_2": "Abuela",
        "nombre_tutor_2": "Rosa",
        "apellido_tutor_2": "González",
        "dni_tutor_2": "44556677",
        "domicilio_tutor_2": "Calle Libertad 456",
        "celular_tutor_2": "03419887766",
        "email_tutor_2": "rosa.gonzalez@example.com",
        "nivel_escolaridad_tutor_2": "Primario completo",
        "ocupacion_tutor_2": "Jubilada",
        "propuesta_trabajo": "Asistencia semanal",
        "condicion": "Activa",
        "sede": "Centro Sur",
        "dia": ["Martes", "Jueves"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }
    JABD.create_legajo(**legajo3)

    legajo4 = {
        "nombre": "Sofía",
        "apellido": "Méndez",
        "dni": "33442211",
        "edad": 28,
        "fecha_nacimiento": "1995-01-30",
        "lugar_nacimiento": "Córdoba",
        "domicilio_actual": "Av. Libertad 200",
        "telefono_actual": "03514561234",
        "contacto_emergencia": "Pedro Méndez",
        "tel": "03519876543",
        "becado": False,
        "porcentaje_beca": 0,
        "profesionales_atienden": "Dr. Silva, Lic. Romero",
        "deuda": True,
        "certificado_discapacidad": True,
        "diagnostico": "Trastorno de ansiedad",
        "tipo_diagnostico": "Psicológico",
        "tipo_discapacidad": "Psíquica",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación universal por hijo",
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "PAMI",
        "num_afiliado": "12398765",
        "posee_curatela": True,
        "observaciones_curatela": "Bajo supervisión de curador asignado",
        "nombre_escuela": "Colegio San José",
        "direccion_escuela": "Calle Mayor 333",
        "telefono_escuela": "03519871234",
        "anio_actual_escuela": 4,
        "observaciones_escuela": "Buena conducta y progreso",
        "parentesco_tutor_1": "Hermano",
        "nombre_tutor_1": "Pedro",
        "apellido_tutor_1": "Méndez",
        "dni_tutor_1": "44556677",
        "domicilio_tutor_1": "Av. Libertad 200",
        "celular_tutor_1": "03519876543",
        "email_tutor_1": "pedro.mendez@example.com",
        "nivel_escolaridad_tutor_1": "Secundario completo",
        "ocupacion_tutor_1": "Comerciante",
        "parentesco_tutor_2": "Tía",
        "nombre_tutor_2": "Ana",
        "apellido_tutor_2": "Méndez",
        "dni_tutor_2": "33445566",
        "domicilio_tutor_2": "Av. Libertad 200",
        "celular_tutor_2": "03519876542",
        "email_tutor_2": "ana.mendez@example.com",
        "nivel_escolaridad_tutor_2": "Universitario completo",
        "ocupacion_tutor_2": "Administrativa",
        "propuesta_trabajo": "Sesión grupal semanal",
        "condicion": "Activa",
        "sede": "Centro Oeste",
        "dia": ["Martes"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }
    JABD.create_legajo(**legajo4)

    legajo5 = {
        "nombre": "Tomás",
        "apellido": "García",
        "dni": "22334455",
        "edad": 22,
        "fecha_nacimiento": "2002-02-18",
        "lugar_nacimiento": "San Juan",
        "domicilio_actual": "Calle Nueva 245",
        "telefono_actual": "02644561234",
        "contacto_emergencia": "Miguel García",
        "tel": "02649876543",
        "becado": True,
        "porcentaje_beca": 50,
        "profesionales_atienden": "Dr. Suárez, Lic. Benítez",
        "deuda": False,
        "certificado_discapacidad": True,
        "diagnostico": "Trastorno bipolar",
        "tipo_diagnostico": "Psiquiátrico",
        "tipo_discapacidad": "Psíquica",
        "asignacion_familiar": False,
        "tipo_asignacion_familiar": None,
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "OSP",
        "num_afiliado": "11223344",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Instituto La Paz",
        "direccion_escuela": "Calle Vieja 120",
        "telefono_escuela": "02648761234",
        "anio_actual_escuela": 5,
        "observaciones_escuela": "Avances constantes",
        "parentesco_tutor_1": "Padre",
        "nombre_tutor_1": "Miguel",
        "apellido_tutor_1": "García",
        "dni_tutor_1": "33445566",
        "domicilio_tutor_1": "Calle Nueva 245",
        "celular_tutor_1": "02649876543",
        "email_tutor_1": "miguel.garcia@example.com",
        "nivel_escolaridad_tutor_1": "Universitario incompleto",
        "ocupacion_tutor_1": "Mecánico",
        "parentesco_tutor_2": "Madre",
        "nombre_tutor_2": "Mariana",
        "apellido_tutor_2": "López",
        "dni_tutor_2": "55667788",
        "domicilio_tutor_2": "Calle Nueva 245",
        "celular_tutor_2": "02649876542",
        "email_tutor_2": "mariana.lopez@example.com",
        "nivel_escolaridad_tutor_2": "Primario completo",
        "ocupacion_tutor_2": "Ama de casa",
        "propuesta_trabajo": "Terapia ocupacional",
        "condicion": "Inactiva",
        "sede": "Centro Este",
        "dia": ["Miércoles"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }

    JABD.create_legajo(**legajo5)

    legajo6 = {
        "nombre": "Cecilia",
        "apellido": "López",
        "dni": "55667788",
        "edad": 45,
        "fecha_nacimiento": "1979-12-05",
        "lugar_nacimiento": "Salta",
        "domicilio_actual": "Calle Colón 302",
        "telefono_actual": "03874561234",
        "contacto_emergencia": "Laura Rodríguez",
        "tel": "03879876543",
        "becado": True,
        "porcentaje_beca": 75,
        "profesionales_atienden": "Dr. Cabral, Lic. Rossi",
        "deuda": True,
        "certificado_discapacidad": True,
        "diagnostico": "Depresión",
        "tipo_diagnostico": "Psiquiátrico",
        "tipo_discapacidad": "Psíquica",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación por hijo discapacitado",
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "PAMI",
        "num_afiliado": "77889944",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela Municipal",
        "direccion_escuela": "Av. Independencia 234",
        "telefono_escuela": "03879871234",
        "anio_actual_escuela": 6,
        "observaciones_escuela": "Participación activa en clases",
        "parentesco_tutor_1": "Hermana",
        "nombre_tutor_1": "Laura",
        "apellido_tutor_1": "Rodríguez",
        "dni_tutor_1": "44557788",
        "domicilio_tutor_1": "Calle Colón 302",
        "celular_tutor_1": "03879876543",
        "email_tutor_1": "laura.rodriguez@example.com",
        "nivel_escolaridad_tutor_1": "Universitario completo",
        "ocupacion_tutor_1": "Contadora",
        "parentesco_tutor_2": "Hermano",
        "nombre_tutor_2": "Carlos",
        "apellido_tutor_2": "López",
        "dni_tutor_2": "66778899",
        "domicilio_tutor_2": "Calle Colón 302",
        "celular_tutor_2": "03879876542",
        "email_tutor_2": "carlos.lopez@example.com",
        "nivel_escolaridad_tutor_2": "Secundario completo",
        "ocupacion_tutor_2": "Operario",
        "propuesta_trabajo": "Seguimiento mensual",
        "condicion": "Activa",
        "sede": "Centro Norte",
        "dia": ["Jueves"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }

    JABD.create_legajo(**legajo6)

    legajo7 = {
        "nombre": "Lucas",
        "apellido": "Sánchez",
        "dni": "11223344",
        "edad": 30,
        "fecha_nacimiento": "1993-06-15",
        "lugar_nacimiento": "Rosario",
        "domicilio_actual": "Calle Mitre 500",
        "telefono_actual": "03411234567",
        "contacto_emergencia": "Luciana Sánchez",
        "tel": "03411239876",
        "becado": True,
        "porcentaje_beca": 100,
        "profesionales_atienden": "Dr. Vargas, Lic. Ayala",
        "deuda": False,
        "certificado_discapacidad": True,
        "diagnostico": "Esquizofrenia",
        "tipo_diagnostico": "Psiquiátrico",
        "tipo_discapacidad": "Psíquica",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación universal por hijo",
        "es_veneficiaro_pension": True,
        "pension": "Pensión no contributiva",
        "obra_social": "IOMA",
        "num_afiliado": "33445566",
        "posee_curatela": True,
        "observaciones_curatela": "Tutela bajo orden judicial",
        "nombre_escuela": "Escuela Primaria Nº12",
        "direccion_escuela": "Av. Argentina 1200",
        "telefono_escuela": "03411876543",
        "anio_actual_escuela": 7,
        "observaciones_escuela": "Requiere acompañamiento especial",
        "parentesco_tutor_1": "Hermana",
        "nombre_tutor_1": "Luciana",
        "apellido_tutor_1": "Sánchez",
        "dni_tutor_1": "44556677",
        "domicilio_tutor_1": "Calle Mitre 500",
        "celular_tutor_1": "03411239876",
        "email_tutor_1": "luciana.sanchez@example.com",
        "nivel_escolaridad_tutor_1": "Universitario completo",
        "ocupacion_tutor_1": "Psicóloga",
        "parentesco_tutor_2": "Tío",
        "nombre_tutor_2": "Alberto",
        "apellido_tutor_2": "Sánchez",
        "dni_tutor_2": "55667788",
        "domicilio_tutor_2": "Calle Mitre 600",
        "celular_tutor_2": "03411876544",
        "email_tutor_2": "alberto.sanchez@example.com",
        "nivel_escolaridad_tutor_2": "Secundario completo",
        "ocupacion_tutor_2": "Carpintero",
        "propuesta_trabajo": "Sesión semanal grupal",
        "condicion": "Activa",
        "sede": "Centro Oeste",
        "dia": ["Lunes", "Viernes"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }

    JABD.create_legajo(**legajo7)

    legajo8 = {
        "nombre": "María",
        "apellido": "Gutiérrez",
        "dni": "22334455",
        "edad": 35,
        "fecha_nacimiento": "1988-10-21",
        "lugar_nacimiento": "La Plata",
        "domicilio_actual": "Av. Central 987",
        "telefono_actual": "02214561234",
        "contacto_emergencia": "Fernando Gutiérrez",
        "tel": "02219876543",
        "becado": False,
        "porcentaje_beca": 0,
        "profesionales_atienden": "Dra. Moreno, Lic. Rojas",
        "deuda": True,
        "certificado_discapacidad": True,
        "diagnostico": "Discapacidad motora",
        "tipo_diagnostico": "Física",
        "tipo_discapacidad": "Motora",
        "asignacion_familiar": False,
        "tipo_asignacion_familiar": None,
        "es_veneficiaro_pension": True,
        "pension": "Pensión por discapacidad",
        "obra_social": "OSDE",
        "num_afiliado": "88776655",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela Nº21",
        "direccion_escuela": "Calle Principal 321",
        "telefono_escuela": "02219876543",
        "anio_actual_escuela": 4,
        "observaciones_escuela": "Asistencia diaria",
        "parentesco_tutor_1": "Padre",
        "nombre_tutor_1": "Fernando",
        "apellido_tutor_1": "Gutiérrez",
        "dni_tutor_1": "33445566",
        "domicilio_tutor_1": "Av. Central 987",
        "celular_tutor_1": "02219876543",
        "email_tutor_1": "fernando.gutierrez@example.com",
        "nivel_escolaridad_tutor_1": "Secundario completo",
        "ocupacion_tutor_1": "Comerciante",
        "parentesco_tutor_2": "Madre",
        "nombre_tutor_2": "Lucía",
        "apellido_tutor_2": "Pérez",
        "dni_tutor_2": "55667788",
        "domicilio_tutor_2": "Av. Central 987",
        "celular_tutor_2": "02219876544",
        "email_tutor_2": "lucia.perez@example.com",
        "nivel_escolaridad_tutor_2": "Primario completo",
        "ocupacion_tutor_2": "Ama de casa",
        "propuesta_trabajo": "Terapia física diaria",
        "condicion": "Activa",
        "sede": "Centro Este",
        "dia": ["Martes", "Jueves"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }
    JABD.create_legajo(**legajo8)

    legajo9 = {
        "nombre": "Ana",
        "apellido": "Rodríguez",
        "dni": "55667788",
        "edad": 40,
        "fecha_nacimiento": "1983-04-11",
        "lugar_nacimiento": "Mendoza",
        "domicilio_actual": "Av. Libertad 567",
        "telefono_actual": "02614561234",
        "contacto_emergencia": "Pedro Rodríguez",
        "tel": "02619876543",
        "becado": True,
        "porcentaje_beca": 75,
        "profesionales_atienden": "Dr. Romero, Lic. Martínez",
        "deuda": False,
        "certificado_discapacidad": True,
        "diagnostico": "Discapacidad auditiva",
        "tipo_diagnostico": "Sensorial",
        "tipo_discapacidad": "Auditiva",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación universal por hijo",
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "IOMA",
        "num_afiliado": "66778899",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela Nº32",
        "direccion_escuela": "Calle Mayor 453",
        "telefono_escuela": "02619876543",
        "anio_actual_escuela": 6,
        "observaciones_escuela": "Participación activa en talleres",
        "parentesco_tutor_1": "Hermano",
        "nombre_tutor_1": "Pedro",
        "apellido_tutor_1": "Rodríguez",
        "dni_tutor_1": "44557788",
        "domicilio_tutor_1": "Av. Libertad 567",
        "celular_tutor_1": "02619876543",
        "email_tutor_1": "pedro.rodriguez@example.com",
        "nivel_escolaridad_tutor_1": "Secundario completo",
        "ocupacion_tutor_1": "Obrero",
        "parentesco_tutor_2": "Hermana",
        "nombre_tutor_2": "Clara",
        "apellido_tutor_2": "Rodríguez",
        "dni_tutor_2": "33445566",
        "domicilio_tutor_2": "Av. Libertad 567",
        "celular_tutor_2": "02619876542",
        "email_tutor_2": "clara.rodriguez@example.com",
        "nivel_escolaridad_tutor_2": "Universitario completo",
        "ocupacion_tutor_2": "Profesora",
        "propuesta_trabajo": "Sesiones grupales",
        "condicion": "Inactiva",
        "sede": "Centro Sur",
        "dia": ["Lunes", "Miércoles"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }
    JABD.create_legajo(**legajo9)

    legajo10 = {
        "nombre": "Jorge",
        "apellido": "Martínez",
        "dni": "66778899",
        "edad": 29,
        "fecha_nacimiento": "1994-08-19",
        "lugar_nacimiento": "San Juan",
        "domicilio_actual": "Calle Comercio 200",
        "telefono_actual": "02644561234",
        "contacto_emergencia": "Alejandra Martínez",
        "tel": "02649876543",
        "becado": False,
        "porcentaje_beca": 0,
        "profesionales_atienden": "Dr. López, Lic. Torres",
        "deuda": True,
        "certificado_discapacidad": True,
        "diagnostico": "Parálisis cerebral",
        "tipo_diagnostico": "Neurológico",
        "tipo_discapacidad": "Motora",
        "asignacion_familiar": False,
        "tipo_asignacion_familiar": None,
        "es_veneficiaro_pension": True,
        "pension": "Pensión no contributiva",
        "obra_social": "OSDE",
        "num_afiliado": "99887766",
        "posee_curatela": True,
        "observaciones_curatela": "Curatela completa asignada",
        "nombre_escuela": "Escuela Especial Nº3",
        "direccion_escuela": "Av. San Juan 123",
        "telefono_escuela": "02649876543",
        "anio_actual_escuela": 8,
        "observaciones_escuela": "Apoyo escolar diario",
        "parentesco_tutor_1": "Tía",
        "nombre_tutor_1": "Alejandra",
        "apellido_tutor_1": "Martínez",
        "dni_tutor_1": "77889900",
        "domicilio_tutor_1": "Calle Comercio 200",
        "celular_tutor_1": "02649876543",
        "email_tutor_1": "alejandra.martinez@example.com",
        "nivel_escolaridad_tutor_1": "Universitario completo",
        "ocupacion_tutor_1": "Abogada",
        "parentesco_tutor_2": "Primo",
        "nombre_tutor_2": "Martín",
        "apellido_tutor_2": "Martínez",
        "dni_tutor_2": "66778811",
        "domicilio_tutor_2": "Calle Comercio 250",
        "celular_tutor_2": "02649876542",
        "email_tutor_2": "martin.martinez@example.com",
        "nivel_escolaridad_tutor_2": "Primario completo",
        "ocupacion_tutor_2": "Mecánico",
        "propuesta_trabajo": "Terapia ocupacional semanal",
        "condicion": "Activa",
        "sede": "Centro Norte",
        "dia": ["Martes", "Jueves"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }
    JABD.create_legajo(**legajo10)

    legajo11 = {
        "nombre": "Sofía",
        "apellido": "Mendoza",
        "dni": "88990011",
        "edad": 23,
        "fecha_nacimiento": "2001-12-05",
        "lugar_nacimiento": "Córdoba",
        "domicilio_actual": "Av. Olmos 432",
        "telefono_actual": "03514561234",
        "contacto_emergencia": "Nicolás Mendoza",
        "tel": "03519876543",
        "becado": True,
        "porcentaje_beca": 100,
        "profesionales_atienden": "Dr. Ibáñez, Lic. Romero",
        "deuda": False,
        "certificado_discapacidad": True,
        "diagnostico": "Discapacidad visual",
        "tipo_diagnostico": "Sensorial",
        "tipo_discapacidad": "Visual",
        "asignacion_familiar": True,
        "tipo_asignacion_familiar": "Asignación por hijo con discapacidad",
        "es_veneficiaro_pension": False,
        "pension": None,
        "obra_social": "PAMI",
        "num_afiliado": "77889900",
        "posee_curatela": False,
        "observaciones_curatela": None,
        "nombre_escuela": "Escuela para Ciegos Nº4",
        "direccion_escuela": "Calle del Sol 567",
        "telefono_escuela": "03519876543",
        "anio_actual_escuela": 3,
        "observaciones_escuela": "Programa especial de lectura",
        "parentesco_tutor_1": "Hermano",
        "nombre_tutor_1": "Nicolás",
        "apellido_tutor_1": "Mendoza",
        "dni_tutor_1": "99001122",
        "domicilio_tutor_1": "Av. Olmos 432",
        "celular_tutor_1": "03519876543",
        "email_tutor_1": "nicolas.mendoza@example.com",
        "nivel_escolaridad_tutor_1": "Secundario completo",
        "ocupacion_tutor_1": "Empleado de comercio",
        "parentesco_tutor_2": "Abuela",
        "nombre_tutor_2": "Josefina",
        "apellido_tutor_2": "Martínez",
        "dni_tutor_2": "12344321",
        "domicilio_tutor_2": "Av. Olmos 433",
        "celular_tutor_2": "03519876544",
        "email_tutor_2": "josefina.martinez@example.com",
        "nivel_escolaridad_tutor_2": "Primario completo",
        "ocupacion_tutor_2": "Jubilada",
        "propuesta_trabajo": "Sesiones de rehabilitación visual",
        "condicion": "Activa",
        "sede": "Centro Sur",
        "dia": ["Viernes"],
        "profesora_terapeuta": 1,
        "conductor_caballo": 2,
        "caballo": 1,
        "auxiliar_pista": 4,
    }
    
    # Creando artículos
    articulo1 = {
        "titulo": "Primer Artículo",
        "copete": "Este es el copete del primer artículo",
        "contenido": "Contenido del primer artículo",
        "autor_id": 1,  # ID del autor en la tabla relacionada
        "estado": "Publicado",
        "fecha_publicacion": datetime(2023, 10, 1),
    }

    articulo2 = {
        "titulo": "Segundo Artículo",
        "copete": "Este es el copete del segundo artículo",
        "contenido": "Contenido del segundo artículo",
        "autor_id": 2,
        "estado": "Borrador",
        "fecha_publicacion": datetime(2023,1,29),
    }

    articulo3 = {
        "titulo": "Tercer Artículo",
        "copete": "Este es el copete del tercer artículo",
        "contenido": "Contenido del tercer artículo",
        "autor_id": 3,
        "estado": "Archivado",
        "fecha_publicacion": datetime(2023, 9, 15),
    }

    articulo4 = {
        "titulo": "Cuarto Artículo",
        "copete": "Este es el copete del cuarto artículo",
        "contenido": "Contenido del cuarto artículo",
        "autor_id": 4,
        "estado": "Publicado",
        "fecha_publicacion": datetime(2023, 8, 20),
    }

    articulo5 = {
        "titulo": "Quinto Artículo",
        "copete": "Este es el copete del quinto artículo",
        "contenido": "Contenido del quinto artículo",
        "autor_id": 5,
        "estado": "Borrador",
        "fecha_publicacion": datetime(2023,8,15),
    }
    crear_articulo(**articulo1)
    crear_articulo(**articulo2)
    crear_articulo(**articulo3)
    crear_articulo(**articulo4)
    crear_articulo(**articulo5)

    # Añadiendo los artículos
    

    db.session.commit()
