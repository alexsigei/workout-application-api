
from flask import Flask

from server.extensions import db, migrate
from server import models
from server.workout_routes import workout_api


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(workout_api)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5555, debug=True)
