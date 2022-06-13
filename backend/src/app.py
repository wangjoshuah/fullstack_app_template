import os

from flask import Flask, Response
from flask_compress import Compress
from flask_cors import CORS
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from settings import settings

app = Flask(__name__)
app.config["API_TITLE"] = "Full Stack Template"
app.config["API_VERSION"] = "v0.1.0"
app.config["OPENAPI_VERSION"] = "3.0.2"

Compress(app)
CORS(app)

api = Api(app)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
engine: Engine = db.engine
# https://github.com/sqlalchemy/sqlalchemy/issues/5645
engine.dialect.description_encoding = None
session = db.session
Base = declarative_base(metadata=metadata)


@app.route("/api/ping")
def ping():
    return Response(
        "pong",
        mimetype="text/plain",
    )


if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.run(debug=True, host="0.0.0.0", port=settings.port)
