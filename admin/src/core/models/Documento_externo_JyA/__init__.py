from core.database import db
from core.models.Documento_externo_JyA.Documento_externo_JyA import DocumentoExterno


def list_documentos(id):
    """
    Lista documentos externos asociados a un legajo específico.

    Esta función consulta la base de datos para obtener todos los documentos
    externos que no han sido eliminados y que están asociados al legajo
    con el identificador dado.

    Args:
        id (int): El identificador del legajo para filtrar los documentos.

    Returns:
        list: Lista de documentos externos asociados al legajo especificado.
    """
    docs = (
        DocumentoExterno.query.filter_by(legajo_id=id).filter_by(eliminado=False).all()
    )
    return docs


def list_documentos_filt(id_leg, titulo=None, tipo=None):
    """
    Filtra y lista documentos externos según el título y tipo.

    Esta función consulta la base de datos para obtener documentos
    externos que no han sido eliminados. Se pueden filtrar por
    título y tipo.

    Args:
        titulo (str, optional): Título del documento para filtrar.
                                Defaults to None.
        tipo (str, optional): Tipo del documento para filtrar.
                              Defaults to None.

    Returns:
        list: Lista de documentos externos filtrados.
    """
    try:
        query = DocumentoExterno.query.filter_by(eliminado=False).filter_by(
            legajo_id=id_leg
        )

        if titulo:
            query = query.filter(DocumentoExterno.titulo.like(f"%{titulo}%"))
        if tipo:
            query = query.filter(DocumentoExterno.tipo.like(f"%{tipo}%"))
        return query.all()
    except Exception as e:
        return {e: "Contacte al administrador"}


def ordenar_archivos_b(arch, ordn, sort):
    """
    Ordena una lista de archivos según una columna y un orden especificados.

    Esta función toma una lista de archivos y los ordena según la columna
    especificada (por ejemplo, título o fecha de subida) y el orden (ascendente
    o descendente).

    Args:
        arch (list): Lista de archivos a ordenar.
        ordn (str): Dirección del orden. Puede ser 'asc' para ascendente
                     o 'desc' para descendente.
        sort (str): Nombre de la columna por la que se desea ordenar.

    Returns:
        list: Lista de archivos ordenados.
    """
    try:
        columnas_validas = ["titulo", "fecha_subida"]
        if sort not in columnas_validas:
            sort = "titulo"

        if ordn == "desc":
            orden = True
        else:
            orden = False

        if orden:
            sorted_docs = sorted(arch, key=lambda x: getattr(x, sort), reverse=True)
        else:
            sorted_docs = sorted(arch, key=lambda x: getattr(x, sort))

        return sorted_docs
    except Exception as e:
        return {e: "Contacte al administrador"}


def create_doc(**kwargs):
    """
    Crea un nuevo documento externo en la base de datos.

    Esta función recibe un conjunto de parámetros a través de `kwargs`,
    crea una instancia de `DocumentoExterno`, la añade a la sesión de la base
    de datos y realiza un commit.

    Args:
        **kwargs: Argumentos clave-valor que se utilizarán para inicializar
                  el objeto `DocumentoExterno`.

    Returns:
        DocumentoExterno: El documento creado y guardado en la base de datos.
    """
    try:
        doc = DocumentoExterno(**kwargs)
        db.session.add(doc)
        db.session.commit()

        return doc
    except Exception as e:
        return {e: "CONTACTE AL ADMINISTRADOR"}


def update_documento_externo(id, titulo=None, tipo=None):
    try:
        doc = get_doc_by_id(id)
        if titulo:
            doc.titulo = titulo
        if tipo:
            doc.tipo = tipo
        db.session.commit()
    except Exception as e:
        return {e: "Contacte al administrador"}


def get_doc_by_id(id):
    """
    Obtiene un documento externo por su ID.

    Esta función busca un documento en la base de datos utilizando su ID
    y devuelve el título del documento.

    Args:
        id (int): El ID del documento a buscar.

    Returns:
        str: El título del documento si se encuentra, o un mensaje de error
             si no se encuentra.
    """
    try:
        doc = DocumentoExterno.query.filter_by(id=id).first()
        return doc
    except Exception as e:
        return {e: "Contacte al administrador"}


def eliminar_doc(id):
    """
    Marca un documento externo como eliminado.

    Esta función busca un documento en la base de datos utilizando su ID
    y lo marca como eliminado.

    Args:
        id (int): El ID del documento a eliminar.

    Returns:
        None: La función no devuelve ningún valor. Si ocurre un error,
              se devuelve un mensaje de error.
    """
    try:
        doc = DocumentoExterno.query.filter_by(id=id).first()
        doc.eliminado = True
        db.session.commit()
    except Exception as e:
        return {e: "Contacte al administrador"}
