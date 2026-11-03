
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from server.extensions import db
from server.models import Workout, Exercise, WorkoutExercise
from server.schemas import WorkoutExerciseCreateSchema, WorkoutExerciseSchema


association_api = Blueprint("association_api", __name__)

create_schema = WorkoutExerciseCreateSchema()
response_schema = WorkoutExerciseSchema()


@association_api.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    try:
        validated_data = create_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    association = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        **validated_data
    )

    try:
        db.session.add(association)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "This exercise is already associated with this workout."
        }), 409

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "error": "Could not add exercise to workout."
        }), 500

    return jsonify(response_schema.dump(association)), 201
