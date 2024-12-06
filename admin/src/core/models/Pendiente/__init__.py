from core.models.Pendiente.Pendiente import Pendientes
from core.database import db


def cargar_pendiente(email, alias):
    """Carga en la DB un usuario pendiente.

    Args:
        email (str): email que se desea registrar
        alias (str): nombre y apellido en un campo
    """
    pendiente = Pendientes(email=email,alias=alias)
    db.session.add(pendiente)
    db.session.commit()

def listar_pendientes(page=1, max=5):
    """
    Obtiene una lista de usuarios pendientes, paginada y con el total de usuarios en la base de datos.

    Esta función se encarga de recuperar los usuarios que están marcados como pendientes en la base de datos.
    La consulta es paginada, lo que permite cargar un número limitado de usuarios por cada solicitud. 
    Además, se calcula el número total de usuarios pendientes para facilitar la paginación en el frontend.

    :param page: Número de la página actual que se desea mostrar. El valor por defecto es 1.
    :param max: Número máximo de usuarios a mostrar por página. El valor por defecto es 5.

    :return: Un diccionario con dos claves:
        - "users": Un objeto de tipo `Pagination` con los usuarios pendientes correspondientes a la página solicitada.
        - "total": El número total de usuarios pendientes en la base de datos.
    """
    try:  
        pendientes = Pendientes.query.paginate(page=page,per_page=max)
        cant = Pendientes.query.count()
        return {"users": pendientes,
                "total" : cant}
    except Exception as e:
        return e
    
def buscar_pendiente_email(email):
    """
    Busca un usuario pendiente en la base de datos a partir de su dirección de correo electrónico.

    Esta función consulta la base de datos para verificar si existe un registro de un usuario pendiente
    utilizando el correo electrónico proporcionado. Si se encuentra un usuario pendiente con ese correo electrónico,
    la función retorna `True`; de lo contrario, retorna `False`.

    :param email: El correo electrónico del usuario pendiente que se desea buscar.

    :return: 
        - `True` si el usuario pendiente existe en la base de datos.
        - `False` si no se encuentra un usuario pendiente con el correo electrónico proporcionado.
        - En caso de error, se retorna el error capturado.
    """
    try:
        pendiente = Pendientes.query.get(email)
        if pendiente:
            return True
        else:
            return False
    except Exception as e:
        return e
    
def eliminar_pend(email):
    """Elimina un usuario pendiente

    Args:
        email (str): email del usuario pendiente

    Returns:
        Boolean/Exception: Resultado de la operacion
    """
    try:
        pendiente = Pendientes.query.get(email)
        db.session.delete(pendiente)
        db.session.commit()
        return True
    except Exception as e:
        return e