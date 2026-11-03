from datetime import date

from server.extensions import db
from server.models import Exercise, Workout, WorkoutExercise


def create_workout_and_exercise():
    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=45,
        notes="Strength training"
    )

    exercise = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    db.session.add_all([workout, exercise])
    db.session.commit()

    return workout, exercise


def test_add_exercise_to_workout(client):
    workout, exercise = create_workout_and_exercise()

    payload = {
        "reps": 15,
        "sets": 3
    }

    response = client.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json=payload
    )

    assert response.status_code == 201
    assert response.json["workout_id"] == workout.id
    assert response.json["exercise_id"] == exercise.id
    assert response.json["reps"] == 15
    assert response.json["sets"] == 3


def test_add_time_based_exercise_to_workout(client):
    workout, exercise = create_workout_and_exercise()

    response = client.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json={"duration_seconds": 120}
    )

    assert response.status_code == 201
    assert response.json["duration_seconds"] == 120


def test_add_exercise_without_metrics(client):
    workout, exercise = create_workout_and_exercise()

    response = client.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json={}
    )

    assert response.status_code == 400


def test_add_exercise_with_invalid_metrics(client):
    workout, exercise = create_workout_and_exercise()

    response = client.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json={"reps": -5}
    )

    assert response.status_code == 400


def test_add_duplicate_exercise_to_workout(client):
    workout, exercise = create_workout_and_exercise()

    payload = {"reps": 10, "sets": 3}

    first_response = client.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json=payload
    )

    second_response = client.post(
        f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
        json=payload
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_add_exercise_to_nonexistent_workout(client):
    exercise = Exercise(
        name="Squats",
        category="Strength"
    )

    db.session.add(exercise)
    db.session.commit()

    response = client.post(
        f"/workouts/999/exercises/{exercise.id}/workout_exercises",
        json={"reps": 10}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Workout not found."


def test_add_nonexistent_exercise_to_workout(client):
    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=30
    )

    db.session.add(workout)
    db.session.commit()

    response = client.post(
        f"/workouts/{workout.id}/exercises/999/workout_exercises",
        json={"reps": 10}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Exercise not found."
