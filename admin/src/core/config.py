from os import environ


class Config(object):
    TESTING = False
    SECRET_KEY = "mysecretkey"
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True


class DevelopmentConfig(Config):
    DB_USER = "postgres"
    DB_PASSWORD = "Proyecto1"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "postgres"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "bDA8LNd0UkgeiDUaP5m0"
    MINIO_SECRET_KEY = "EZLn7FT7oGPb3NUi4WRBmQtPJzjzLmLijQ3fZaDF"
    MINIO_SECURE = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = None
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
