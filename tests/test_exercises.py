from datetime import date

from server.extensions import db
from server.models import Exercise, Workout, WorkoutExercise


def test_get_exercises(client):
    exercises = [
        Exercise(name="Push-ups", category="Strength"),
        Exercise(name="Running", category="Cardio")
    ]

    db.session.add_all(exercises)
    db.session.commit()

    response = client.get("/exercises")

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Push-ups"
    assert response.json[1]["name"] == "Running"


def test_get_exercise_by_id(client):
    exercise = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    db.session.add(exercise)
    db.session.commit()

    response = client.get(f"/exercises/{exercise.id}")

    assert response.status_code == 200
    assert response.json["name"] == "Squats"
    assert response.json["category"] == "Strength"


def test_get_exercise_includes_associated_workouts(client):
    exercise = Exercise(
        name="Bench Press",
        category="Strength",
        equipment_needed=True
    )

    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=45,
        notes="Upper body training"
    )

    db.session.add_all([exercise, workout])
    db.session.flush()

    association = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=10,
        sets=3
    )

    db.session.add(association)
    db.session.commit()

    response = client.get(f"/exercises/{exercise.id}")

    assert response.status_code == 200
    assert len(response.json["workouts"]) == 1
    assert response.json["workouts"][0]["id"] == workout.id


def test_get_nonexistent_exercise(client):
    response = client.get("/exercises/999")

    assert response.status_code == 404
    assert response.json["error"] == "Exercise not found."


def test_create_exercise(client):
    payload = {
        "name": "Deadlift",
        "category": "Strength",
        "equipment_needed": True
    }

    response = client.post("/exercises", json=payload)

    assert response.status_code == 201
    assert response.json["name"] == "Deadlift"
    assert response.json["equipment_needed"] is True


def test_create_exercise_with_default_equipment(client):
    payload = {
        "name": "Plank",
        "category": "Core"
    }

    response = client.post("/exercises", json=payload)

    assert response.status_code == 201
    assert response.json["equipment_needed"] is False


def test_create_exercise_with_empty_name(client):
    payload = {
        "name": "   ",
        "category": "Strength"
    }

    response = client.post("/exercises", json=payload)

    assert response.status_code == 400
    assert "name" in response.json["errors"]


def test_create_exercise_with_missing_fields(client):
    response = client.post(
        "/exercises",
        json={"name": "Deadlift"}
    )

    assert response.status_code == 400


def test_delete_exercise(client):
    exercise = Exercise(
        name="Cycling",
        category="Cardio"
    )

    db.session.add(exercise)
    db.session.commit()

    response = client.delete(f"/exercises/{exercise.id}")

    assert response.status_code == 204
    assert db.session.get(Exercise, exercise.id) is None


def test_delete_exercise_cascades_associations(client):
    exercise = Exercise(
        name="Push-ups",
        category="Strength"
    )

    workout = Workout(
        date=date(2026, 11, 3),
        duration_minutes=30
    )

    db.session.add_all([exercise, workout])
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

    response = client.delete(f"/exercises/{exercise.id}")

    assert response.status_code == 204
    assert db.session.get(WorkoutExercise, association_id) is None
