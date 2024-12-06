from flask import Flask
from flask import session as session_user
from flask import render_template
from flask_cors import CORS
from core.config import config
from core.models.User.User import Users
from core.models.User.__init__ import find_user_by_email
from core.models.Roles.__init__ import get_rol_by_id
from core.models.Cobro.Cobro import Cobros
from core.models.Documento_externo_Ecuestre.DocumentoExternoEncuestre import (
    DocumentoExternoEncuestre,
)
from core.models.Documento_externo_JyA.Documento_externo_JyA import DocumentoExterno
from core.models.Encuestre.Encuestre import Encuestres
from core.models.Equipo.Equipo import Equipos
from core.models.Legajo.Legajo import Legajos
from core.models.Pendiente.Pendiente import Pendientes
from core.models.Pago.Pago import Pagos
from core.models.Articulo.Articulo import Articulos
from core.models.Roles.Roles import Rol
from core.models.Permissions.Permissions import Permission
from core.models.Role_permissions import Role_permissions
from web.storage import storage
from web.handlers import (
    error_not_found,
    error_unauthorized,
    error_forbidden,
    error_blocked,
)
from web.handlers.auth import check_permission, is_authenticated
from core import database
from core.database import db
from core.config import config
from web.controllers.auth import bp as auth_bp
from web.controllers.pago import bp as pago_bp
from web.controllers.JyA import bp as jya_bp
from web.controllers.pendientes import bp as pend_bp
from web.controllers.articulos import bp as art_bp
from flask_session import Session
from core.bcrypt import bcrypt
from core import seeds
from web.controllers.users import bp as user_bp
from web.controllers.ecuestre import bp as ecuestre_bp
from web.controllers.equipo.equipo import bp as equipo_bp
from core.models.User import create_user
from web.handlers.auth import login_required, check_permission
from web.controllers.cobros import bp as cobro_bp
from web.controllers.contacto import bp as contacto_bp
from web.api.contacto import bp as api_bp_c
from web.api.articulo import bp as api_bp_a
from web.controllers.reportes import bp as reporte_bp
from flask_cors import CORS

session = Session()


def create_app(env="development", static_folder="../../static"):

    app = Flask(__name__, static_folder=static_folder)

    # load config
    app.config.from_object(config[env])

    # init db
    database.init_app(app)

    # init session
    session.init_app(app)

    # init bcrypt
    bcrypt.init_app(app)

    # init storage
    storage.init_app(app)
    
    # CORS
    CORS(app)

    @app.route("/")
    def home_page():
        return render_template("home.html")

    @app.route("/J&A")
    @login_required
    def JyA_page():
        return render_template("J&A/J&A.html")

    @app.route("/logout")
    @login_required
    def logout():
        return render_template("home.html")

    @app.route("/profile")
    @login_required
    def profile_user():
        """
        Renderiza la página de perfil de usuario autenticado.

        Esta función es accesible solo para usuarios autenticados.
        Obtiene la información del usuario desde la sesión actual, busca los
        detalles del usuario y su rol asociado en la base de datos, y luego
        renderiza la plantilla de perfil con los datos correspondientes.

        Returns:
            str: El HTML renderizado de la página de perfil, con los datos del usuario y su rol.

        Raises:
            KeyError: Si no se encuentra la clave 'user' en la sesión.
        """
        user_email = session_user["user"]
        datos_usuario = find_user_by_email(user_email)
        rol = datos_usuario.role_id
        nombre_rol = get_rol_by_id(rol)
        return render_template(
            "auth/profile.html", usuario=datos_usuario, rol=nombre_rol
        )

    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(is_authenticated=is_authenticated)

    # Register error handlers
    app.register_error_handler(404, error_not_found)
    app.register_error_handler(401, error_unauthorized)
    app.register_error_handler(403, error_forbidden)
    app.register_error_handler(504, error_blocked)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(equipo_bp)
    app.register_blueprint(ecuestre_bp)
    app.register_blueprint(pago_bp)
    app.register_blueprint(jya_bp)
    app.register_blueprint(cobro_bp)
    app.register_blueprint(art_bp)
    app.register_blueprint(contacto_bp)
    app.register_blueprint(api_bp_c)
    app.register_blueprint(api_bp_a)
    app.register_blueprint(reporte_bp)
    app.register_blueprint(pend_bp)

    # CLI commands
    @app.cli.command(name="reset-db")
    def reset_db():
        print("Reiniciando la base de datos...")
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    # Register global functions for jinja

    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(is_authenticated=is_authenticated)

    return app
