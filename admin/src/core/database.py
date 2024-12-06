from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """
    Inicializa la aplicación Flask con la base de datos SQLAlchemy.

    Esta función inicializa la aplicación Flask dada con la instancia de la
    base de datos SQLAlchemy y configura la aplicación.

    Parámetros:
    app (Flask): La instancia de la aplicación Flask a inicializar.

    Retorna:
    Flask: La instancia de la aplicación Flask inicializada.
    """
    db.init_app(app)
    config(app)

    return app


def config(app):
    """
    Configura la aplicación Flask.

    Esta función configura la aplicación Flask dada estableciendo un contexto
    de finalización para cerrar la sesión de la base de datos después de cada
    solicitud.

    Parámetros:
    app (Flask): La instancia de la aplicación Flask a configurar.

    Retorna:
    Flask: La instancia de la aplicación Flask configurada.
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        """
        Cierra la sesión de la base de datos.

        Esta función cierra la sesión de la base de datos SQLAlchemy. Es llamada
        automáticamente por Flask cuando el contexto de la aplicación se cierra.

        Parámetros:
        exception (Exception, opcional): Una excepción opcional que puede haber
                                         ocurrido durante la solicitud.
        """
        db.session.close()

    return app


def reset():
    """
    Reinicia la base de datos.

    Esta función elimina todas las tablas en la base de datos y luego las crea
    nuevamente. Usa esta función con precaución ya que eliminará todos los datos
    en la base de datos.
    """
    db.drop_all()
    db.create_all()
