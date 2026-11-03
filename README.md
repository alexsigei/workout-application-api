# Workout Application API

A RESTful API for managing workout sessions and exercises. Built with Flask, SQLAlchemy, and Marshmallow, the application supports creating and retrieving workouts, managing exercises, and tracking exercise performance.

## Technologies

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pytest

## Getting Started

Clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd workout-application-api
pipenv install --dev
```

Apply the database migrations:

```bash
pipenv run flask --app server.app db upgrade
```

Populate the database with sample data:

```bash
pipenv run python -m server.seed
```

Start the application:

```bash
pipenv run flask --app server.app run --port 5555 --debugger
```

The API will be available at `http://127.0.0.1:5555`.

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve a workout and its exercises |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve an exercise and its workouts |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Requests

Create a workout:

```json
{
  "date": "2026-11-03",
  "duration_minutes": 45,
  "notes": "Upper body training"
}
```

Create an exercise:

```json
{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}
```

Add an exercise to a workout:

```json
{
  "reps": 15,
  "sets": 3
}
```

For time-based exercises, use `duration_seconds` instead. At least one exercise metric must be provided.

## Data Relationships

A workout can contain multiple exercises, and an exercise can belong to multiple workouts. The `WorkoutExercise` model manages this relationship and stores performance details such as repetitions, sets, and duration.

## Validation and Testing

Request data is validated using Marshmallow. Database constraints and model validations enforce data integrity. Deleting a workout or exercise also removes its associated records.

Run the automated tests:

```bash
pipenv run pytest -v
```

## License

Developed as part of a software engineering coursework project.