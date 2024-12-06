from datetime import datetime
from core.database import db

class Articulos(db.Model):
    __tablename__ = "Articulo"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)  
    copete = db.Column(db.Text, nullable=True)
    contenido = db.Column(db.Text, nullable=True)  
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    estado = db.Column(db.Enum('Borrador', 'Publicado', 'Archivado', name='estado_articulo'), default='Borrador', nullable=False)
    fecha_publicacion = db.Column(db.DateTime, nullable=True)  
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    publico = db.Column(db.Boolean(), default=False)
    creador_pub = db.relationship("Users", back_populates="creador_pub")  
 
    def __repr__(self):
        return f"<Articulo {self.titulo}>"

