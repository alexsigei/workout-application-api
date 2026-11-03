
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from server.extensions import db
from server.models import Workout
from server.schemas import WorkoutSchema


workout_api = Blueprint("workout_api", __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


@workout_api.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc()).all()

    return jsonify(workouts_schema.dump(workouts)), 200


@workout_api.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    return jsonify(workout_schema.dump(workout)), 200


@workout_api.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    try:
        validated_data = workout_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    workout = Workout(**validated_data)

    try:
        db.session.add(workout)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create workout."}), 500

    return jsonify(workout_schema.dump(workout)), 201


@workout_api.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    try:
        db.session.delete(workout)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not delete workout."}), 500

    return "", 204

