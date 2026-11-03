
from datetime import date, timedelta

from server.app import app
from server.extensions import db
from server.models import Exercise, Workout, WorkoutExercise


def seed_data():
    # Clear existing data in dependency order.
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create reusable exercises.
    exercises = [
        Exercise(
            name="Push-ups",
            category="Strength",
            equipment_needed=False
        ),
        Exercise(
            name="Squats",
            category="Strength",
            equipment_needed=False
        ),
        Exercise(
            name="Bench Press",
            category="Strength",
            equipment_needed=True
        ),
        Exercise(
            name="Running",
            category="Cardio",
            equipment_needed=False
        ),
        Exercise(
            name="Plank",
            category="Core",
            equipment_needed=False
        ),
        Exercise(
            name="Cycling",
            category="Cardio",
            equipment_needed=True
        )
    ]

    db.session.add_all(exercises)
    db.session.flush()

    # Create workout sessions.
    workouts = [
        Workout(
            date=date.today() - timedelta(days=2),
            duration_minutes=45,
            notes="Upper body strength training."
        ),
        Workout(
            date=date.today() - timedelta(days=1),
            duration_minutes=60,
            notes="Cardio and core training."
        ),
        Workout(
            date=date.today(),
            duration_minutes=50,
            notes="Full body workout."
        )
    ]

    db.session.add_all(workouts)
    db.session.flush()

    # Associate exercises with workouts.
    workout_exercises = [
        WorkoutExercise(
            workout_id=workouts[0].id,
            exercise_id=exercises[0].id,
            sets=3,
            reps=15
        ),
        WorkoutExercise(
            workout_id=workouts[0].id,
            exercise_id=exercises[2].id,
            sets=4,
            reps=10
        ),
        WorkoutExercise(
            workout_id=workouts[1].id,
            exercise_id=exercises[3].id,
            duration_seconds=1800
        ),
        WorkoutExercise(
            workout_id=workouts[1].id,
            exercise_id=exercises[4].id,
            sets=3,
            duration_seconds=60
        ),
        WorkoutExercise(
            workout_id=workouts[2].id,
            exercise_id=exercises[1].id,
            sets=4,
            reps=12
        ),
        WorkoutExercise(
            workout_id=workouts[2].id,
            exercise_id=exercises[0].id,
            sets=3,
            reps=12
        ),
        WorkoutExercise(
            workout_id=workouts[2].id,
            exercise_id=exercises[5].id,
            duration_seconds=1200
        )
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Exercises: {Exercise.query.count()}")
    print(f"Workouts: {Workout.query.count()}")
    print(f"Workout exercises: {WorkoutExercise.query.count()}")


if __name__ == "__main__":
    with app.app_context():
        seed_data()
