from marshmallow import Schema, fields

class ArticuloSchema(Schema):
    id =  fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    copete = fields.Str(allow_none=True)
    contenido = fields.Str(allow_none=True)
    autor = fields.Str(required=True)
    estado = fields.Str(required=True)
    fecha_publicacion = fields.DateTime(allow_none=True)
    fecha_actualizacion = fields.DateTime(required=True)
    fecha_creacion = fields.DateTime(required=True)
    autor_nombre = fields.Method("get_autor_nombre")

    def get_autor_nombre(self, obj):
        """
        Obtiene el nombre completo del autor/a del artículo.
        :return: El nombre completo del autor/a del artículo.
        """
        return obj.creador_pub.miembro.nombre + " " + obj.creador_pub.miembro.apellido
articulo_schema = ArticuloSchema()
articulos_schema = ArticuloSchema(many=True)