
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from server.extensions import db
from server.models import Exercise
from server.schemas import ExerciseSchema, ExerciseDetailSchema


exercise_api = Blueprint("exercise_api", __name__)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()


@exercise_api.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name.asc()).all()

    return jsonify(exercises_schema.dump(exercises)), 200


@exercise_api.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    return jsonify(exercise_detail_schema.dump(exercise)), 200


@exercise_api.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    exercise = Exercise(**validated_data)

    try:
        db.session.add(exercise)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create exercise."}), 500

    return jsonify(exercise_schema.dump(exercise)), 201


@exercise_api.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    try:
        db.session.delete(exercise)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not delete exercise."}), 500

    return "", 204
