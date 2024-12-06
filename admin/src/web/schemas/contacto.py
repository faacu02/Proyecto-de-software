from marshmallow import Schema, fields, validate

class ContactoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    email = fields.Email(required=True, validate=validate.Email(error="Invalid email address"))
    comentario = fields.Str()
    estado = fields.Str()
    mensaje = fields.Str(required=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    
contacto_schema = ContactoSchema()
contactos_schemas = ContactoSchema(many=True)
create_contacto_Schema = ContactoSchema(only=("nombre", "apellido", "email", "mensaje"))