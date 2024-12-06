from minio import Minio


class Storage:
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Inicializa el cliente de Minio y le adjunta el contexto de la aplicación"""  # configuracion para local
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", False)

        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )

        # Adjunta el contexto de la aplicación
        app.storage = self

        return app

    @property
    def client(self):
        """Propiedad que devuelve el cliente de Minio"""
        return self._client

    @client.setter
    def client(self, value):
        """Setter de la propiedad client"""
        self._client = value


storage = Storage()

storage
