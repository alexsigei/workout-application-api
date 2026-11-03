from datetime import date

from server.extensions import db
from server.models import Workout, Exercise, WorkoutExercise


def test_get_workouts(client):
    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=45,
        notes="Strength training"
    )

    db.session.add(workout)
    db.session.commit()

    response = client.get("/workouts")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["duration_minutes"] == 45


def test_get_workout_by_id(client):
    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=60,
        notes="Full body workout"
    )

    db.session.add(workout)
    db.session.commit()

    response = client.get(f"/workouts/{workout.id}")

    assert response.status_code == 200
    assert response.json["id"] == workout.id
    assert response.json["duration_minutes"] == 60


def test_get_nonexistent_workout(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404
    assert response.json["error"] == "Workout not found."


def test_create_workout(client):
    payload = {
        "date": "2026-11-03",
        "duration_minutes": 40,
        "notes": "Evening workout"
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 201
    assert response.json["duration_minutes"] == 40
    assert response.json["notes"] == "Evening workout"


def test_create_workout_with_invalid_duration(client):
    payload = {
        "date": "2026-11-03",
        "duration_minutes": -10,
        "notes": "Invalid workout"
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 400
    assert "duration_minutes" in response.json["errors"]


def test_create_workout_without_required_fields(client):
    response = client.post(
        "/workouts",
        json={"notes": "Missing date and duration"}
    )

    assert response.status_code == 400


def test_delete_workout(client):
    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=30,
        notes="Workout to delete"
    )

    db.session.add(workout)
    db.session.commit()

    response = client.delete(f"/workouts/{workout.id}")

    assert response.status_code == 204
    assert db.session.get(Workout, workout.id) is None


def test_delete_workout_cascades_associations(client):
    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=45
    )

    exercise = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    db.session.add_all([workout, exercise])
    db.session.flush()

    association = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=15,
        sets=3
    )

    db.session.add(association)
    db.session.commit()

    association_id = association.id

    response = client.delete(f"/workouts/{workout.id}")

    assert response.status_code == 204
    assert db.session.get(WorkoutExercise, association_id) is None
