from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash
)

from  .validaciones import (
    validar_opcion_seleccionada,
)

from core.models.Contacto.__init__ import list_contactos,get_contacto,delete_contacto,update_contacto

import re

estados_validos = ['Pendiente', 'Aceptado', 'Rechazado', 'EnProceso']
ordenes = ['asc', 'desc']

from web.handlers.auth import login_required, check, blocked_user

bp = Blueprint('contacto', __name__, url_prefix='/contacto')

@bp.get('/')
@login_required
@blocked_user
@check('contacto_index')
def verContactos():
    """
    Vista para ver los contactos.

    Filtra los contactos por estado y orden, y los pagina.
    """
    estado = request.args.get('estado')
    orden = request.args.get('direccion', 'desc')
    page = request.args.get("page", 1, type=int)
    
    if estado and not validar_opcion_seleccionada(estado, estados_validos):
        return redirect(url_for('contacto.verContactos'))
    
    if orden and not validar_opcion_seleccionada(orden, ordenes):
        return redirect(url_for('contacto.verContactos'))
    
    contactos = list_contactos(orden,estado,page,per_page=3)
    return render_template('contacto/verContactos.html', contactos = contactos)

@bp.post('borrarContacto/<int:id>')
@login_required
@blocked_user
@check('contacto_destroy')
def borrarContacto(id):
    """
    Vista para borrar un contacto.

    Elimina el contacto con el ID proporcionado.
    """
    contacto = delete_contacto(id)
    if contacto:
        flash('Contacto eliminado correctamente', 'success')
    else:
        flash('No se pudo eliminar el contacto', 'danger')
    return redirect(url_for('contacto.verContactos'))


@bp.route('/editarContacto/<int:id>', methods=['GET', 'POST'])
@login_required
@blocked_user
@check('contacto_update')
def editarContacto(id):
    """
    Vista para editar un contacto.

    Permite editar el estado y el comentario del contacto.
    """
    
    contacto = get_contacto(id)
    if not contacto:
        flash('El contacto no existe', 'danger')
        return redirect(url_for('contacto.verContactos'))
    
    if request.method == 'POST':
        estado = request.form.get('estado')
        if estado and not validar_opcion_seleccionada(estado, estados_validos):
            flash('El estado no es válido', 'danger')
            return redirect(url_for('contacto.editarContacto', id=id))
        
        comentario = request.form.get('comentario')
        if comentario:
            if not re.match(r"^[A-Za-z\s]+$", comentario):
                flash('El comentario solo puede contener letras y espacios', 'danger')
                return redirect(url_for('contacto.editarContacto', id=id))
            
        update_contacto(contacto, estado, comentario)
        flash('Contacto actualizado correctamente', 'success')
        return redirect(url_for('contacto.verContactos'))
    
    return render_template('contacto/editarContacto.html', contacto=contacto)


@bp.route('/verMensaje/<int:id>', methods=['GET'])
@login_required
@blocked_user
@check('contacto_show')
def verMensaje(id):
    """
    Vista para ver un mensaje de contacto.

    Muestra los detalles del mensaje del contacto con el ID proporcionado.
    """
    contacto = get_contacto(id)
    if not contacto:
        flash('El contacto no existe', 'danger')
        return redirect(url_for('contacto.verContactos'))
    
    return render_template('contacto/verMensaje.html', contacto=contacto)  