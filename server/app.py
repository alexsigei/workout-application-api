from flask import Flask

from server.extensions import db, migrate
from server import models
from server.workout_routes import workout_api
from server.exercise_routes import exercise_api
from server.association_routes import association_api


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Allow tests to override the default configuration.
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(workout_api)
    app.register_blueprint(exercise_api)
    app.register_blueprint(association_api)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5555, debug=True)
