import os
from pathlib import Path


class DBConfig:
    db_type = os.getenv("DB_TYPE", "postgresql")
    user = os.getenv("DB_USER", "postgres")
    passwd = os.getenv("DB_PASSWD", "root123")
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", 5432)
    db_name = os.getenv("DB_NAME", "fyyur_example")
    db_uri = f"postgresql://{user}:{passwd}@{host}:{port}/{db_name}"
    redis_uri = "redis://localhost:6379"
    esearch_uri = "localhost"


class Config:
    ENV = "dev"
    FLASK_DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "thisisashop")

    USE_REDIS = False
    REDIS_URL = os.getenv("REDIS_URI", DBConfig.redis_uri)

    USE_ES = False
    ES_HOSTS = [
        os.getenv("ESEARCH_URI", DBConfig.esearch_uri),
    ]

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", DBConfig.db_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_QUERY_TIMEOUT = 0.1  # log the slow database query, and unit is second
    SQLALCHEMY_RECORD_QUERIES = True


class ProdConfig(Config):
    ENV = "prod"
    FLASK_DEBUG = False
    DEBUG_TB_ENABLED = False
