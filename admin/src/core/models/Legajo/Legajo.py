from core.database import db
from datetime import datetime


class Legajos(db.Model):

    __tablename__ = "legajo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento = db.Column(db.String(100), nullable=False)
    domicilio_actual = db.Column(db.String(100), nullable=False)
    telefono_actual = db.Column(db.String(100), nullable=False)
    contacto_emergencia = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(100), nullable=False)
    becado = db.Column(db.Boolean(), nullable=False)
    porcentaje_beca = db.Column(db.String(100), nullable=False)
    profesionales_atienden = db.Column(db.String(100), nullable=False)
    documentos_externos = db.relationship("DocumentoExterno", back_populates="legajo")
    cobros = db.relationship("Cobros", back_populates="JyA")
    deuda = db.Column(db.Boolean(), default=False)
    eliminado = db.Column(db.Boolean(), default=False, nullable=False)
    certificado_discapacidad = db.Column(db.Boolean(), nullable=False)
    diagnostico = db.Column(db.String(100), nullable=False)
    tipo_diagnostico = db.Column(db.String(100), nullable=True)
    tipo_discapacidad = db.Column(db.String(100), nullable=False)
    asignacion_familiar = db.Column(db.Boolean(), default=False, nullable=False)
    tipo_asignacion_familiar = db.Column(db.String(100), nullable=True)
    es_veneficiaro_pension = db.Column(db.Boolean(), default=False, nullable=False)
    pension = db.Column(db.String(100), nullable=True)
    obra_social = db.Column(db.String(100), nullable=False)
    num_afiliado = db.Column(db.String(100), nullable=False)
    posee_curatela = db.Column(db.Boolean(), default=False, nullable=False)
    observaciones_curatela = db.Column(db.String(100), nullable=True)
    nombre_escuela = db.Column(db.String(100), nullable=True)
    direccion_escuela = db.Column(db.String(100), nullable=True)
    telefono_escuela = db.Column(db.String(100), nullable=True)
    anio_actual_escuela = db.Column(db.String(100), nullable=True)
    observaciones_escuela = db.Column(db.String(100), nullable=True)
    parentesco_tutor_1 = db.Column(db.String(100), nullable=False)
    nombre_tutor_1 = db.Column(db.String(100), nullable=False)
    apellido_tutor_1 = db.Column(db.String(100), nullable=False)
    dni_tutor_1 = db.Column(db.String(100), nullable=False)
    domicilio_tutor_1 = db.Column(db.String(100), nullable=False)
    celular_tutor_1 = db.Column(db.String(100), nullable=False)
    email_tutor_1 = db.Column(db.String(100), nullable=False)
    nivel_escolaridad_tutor_1 = db.Column(db.String(100), nullable=False)
    ocupacion_tutor_1 = db.Column(db.String(100), nullable=False)
    parentesco_tutor_2 = db.Column(db.String(100), nullable=True)
    nombre_tutor_2 = db.Column(db.String(100), nullable=True)
    apellido_tutor_2 = db.Column(db.String(100), nullable=True)
    dni_tutor_2 = db.Column(db.String(100), nullable=True)
    domicilio_tutor_2 = db.Column(db.String(100), nullable=True)
    celular_tutor_2 = db.Column(db.String(100), nullable=True)
    email_tutor_2 = db.Column(db.String(100), nullable=True)
    nivel_escolaridad_tutor_2 = db.Column(db.String(100), nullable=True)
    ocupacion_tutor_2 = db.Column(db.String(100), nullable=True)
    propuesta_trabajo = db.Column(db.String(100), nullable=False)
    condicion = db.Column(db.String(100), nullable=False)
    sede = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.String(100), nullable=False)
    profesora_terapeuta = db.Column(
        db.Integer, db.ForeignKey("equipo.id"), nullable=False
    )
    conductor_caballo = db.Column(
        db.Integer, db.ForeignKey("equipo.id"), nullable=False
    )
    caballo = db.Column(db.Integer, db.ForeignKey("encuestre.id"), nullable=False)
    caballo_actual = db.relationship(
        "Encuestres", backref="caballo", foreign_keys=caballo
    )
    auxiliar_pista = db.Column(db.Integer, db.ForeignKey("equipo.id"), nullable=False)
    profesor = db.relationship(
        "Equipos", backref="profesores", foreign_keys=profesora_terapeuta
    )
    conductor = db.relationship(
        "Equipos", backref="conductores", foreign_keys=conductor_caballo
    )
    auxiliar = db.relationship(
        "Equipos", backref="auxiliares", foreign_keys=auxiliar_pista
    )


def __init__(
    self,
    nombre,
    apellido,
    dni,
    edad,
    fecha_nacimiento,
    lugar_nacimiento,
    domicilio_actual,
    telefono_actual,
    contacto_emergencia,
    tel,
    becado,
    porcentaje_beca,
    profesionales_atienden,
    propuesta_trabajo,
    condicion,
    sede,
    dia,
    profesora_terapeuta,
    conductor_caballo,
    caballo,
    auxiliar_pista,
    parentesco_tutor_1,
    nombre_tutor_1,
    apellido_tutor_1,
    dni_tutor_1,
    domicilio_tutor_1,
    celular_tutor_1,
    email_tutor_1,
    nivel_escolaridad_tutor_1,
    ocupacion_tutor_1,
    deuda=False,
    eliminado=False,
    certificado_discapacidad=False,
    diagnostico=None,
    tipo_discapacidad=None,
    asignacion_familiar=False,
    tipo_asignacion_familiar=None,
    es_beneficiario_pension=False,
    pension=None,
    obra_social=None,
    num_afiliado=None,
    posee_curatela=False,
    observaciones_curatela=None,
    nombre_escuela=None,
    direccion_escuela=None,
    telefono_escuela=None,
    anio_actual_escuela=None,
    observaciones_escuela=None,
    parentesco_tutor_2=None,
    nombre_tutor_2=None,
    apellido_tutor_2=None,
    dni_tutor_2=None,
    domicilio_tutor_2=None,
    celular_tutor_2=None,
    email_tutor_2=None,
    nivel_escolaridad_tutor_2=None,
    ocupacion_tutor_2=None,
):

    self.nombre = nombre
    self.apellido = apellido
    self.dni = dni
    self.edad = edad
    self.fecha_nacimiento = fecha_nacimiento
    self.lugar_nacimiento = lugar_nacimiento
    self.domicilio_actual = domicilio_actual
    self.telefono_actual = telefono_actual
    self.contacto_emergencia = contacto_emergencia
    self.tel = tel
    self.becado = becado
    self.porcentaje_beca = porcentaje_beca
    self.profesionales_atienden = profesionales_atienden
    self.deuda = deuda
    self.eliminado = eliminado
    self.certificado_discapacidad = certificado_discapacidad
    self.diagnostico = diagnostico
    self.tipo_discapacidad = tipo_discapacidad
    self.asignacion_familiar = asignacion_familiar
    self.tipo_asignacion_familiar = tipo_asignacion_familiar
    self.es_beneficiario_pension = es_beneficiario_pension
    self.pension = pension
    self.obra_social = obra_social
    self.num_afiliado = num_afiliado
    self.posee_curatela = posee_curatela
    self.observaciones_curatela = observaciones_curatela
    self.nombre_escuela = nombre_escuela
    self.direccion_escuela = direccion_escuela
    self.telefono_escuela = telefono_escuela
    self.anio_actual_escuela = anio_actual_escuela
    self.observaciones_escuela = observaciones_escuela
    self.parentesco_tutor_1 = parentesco_tutor_1
    self.nombre_tutor_1 = nombre_tutor_1
    self.apellido_tutor_1 = apellido_tutor_1
    self.dni_tutor_1 = dni_tutor_1
    self.domicilio_tutor_1 = domicilio_tutor_1
    self.celular_tutor_1 = celular_tutor_1
    self.email_tutor_1 = email_tutor_1
    self.nivel_escolaridad_tutor_1 = nivel_escolaridad_tutor_1
    self.ocupacion_tutor_1 = ocupacion_tutor_1
    self.parentesco_tutor_2 = parentesco_tutor_2
    self.nombre_tutor_2 = nombre_tutor_2
    self.apellido_tutor_2 = apellido_tutor_2
    self.dni_tutor_2 = dni_tutor_2
    self.domicilio_tutor_2 = domicilio_tutor_2
    self.celular_tutor_2 = celular_tutor_2
    self.email_tutor_2 = email_tutor_2
    self.nivel_escolaridad_tutor_2 = nivel_escolaridad_tutor_2
    self.ocupacion_tutor_2 = ocupacion_tutor_2
    self.propuesta_trabajo = propuesta_trabajo
    self.condicion = condicion
    self.sede = sede
    self.dia = dia
    self.professora_terapeuta = profesora_terapeuta
    self.conductor_caballo = conductor_caballo
    self.caballo = caballo
    self.auxiliar_pista = auxiliar_pista
