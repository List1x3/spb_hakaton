import os

from flask_sqlalchemy import SQLAlchemy

# Single SQLAlchemy instance shared across the app
db = SQLAlchemy()


def init_db(app):
    default_uri = "postgresql+psycopg2://postgres:postgres@localhost:5432/spb_hakaton"
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", os.getenv("DATABASE_URL", default_uri))
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.init_app(app)
