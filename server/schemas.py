from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    validates_schema,
    pre_load,
    ValidationError
)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(max=50)
    )

    equipment_needed = fields.Bool(load_default=False)

    @pre_load
    def strip_strings(self, data, **kwargs):
        for field in ("name", "category"):
            if isinstance(data.get(field), str):
                data[field] = data[field].strip()

        return data

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value:
            raise ValidationError("Exercise name cannot be empty.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if not value:
            raise ValidationError("Exercise category cannot be empty.")
        

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    exercise = fields.Nested(
        ExerciseSchema,
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.Str(allow_none=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )

    exercises = fields.Nested(
        ExerciseSchema,
        many=True,
        dump_only=True
    )

    @validates_schema
    def validate_workout(self, data, **kwargs):
        if data.get("notes") is not None:
            if len(data["notes"]) > 1000:
                raise ValidationError({
                    "notes": ["Notes cannot exceed 1000 characters."]
                })


class WorkoutExerciseCreateSchema(Schema):
    reps = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_exercise_metrics(self, data, **kwargs):
        if not any(
            data.get(field) is not None
            for field in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError(
                "At least one of reps, sets or duration_seconds must be provided."
            )