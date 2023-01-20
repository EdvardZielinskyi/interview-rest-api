import datetime

from marshmallow import Schema, fields, validate, validates, ValidationError


class InterviewSchema(Schema):
    interviewer_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
    )
    interviewee_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    date_time_of_interview = fields.DateTime(required=True, format="%Y-%m-%d %H:%M")
    note = fields.Str(
        required=False,
        validate=validate.Length(min=5, max=300)
    )

    @validates("date_time_of_interview")
    def validate_date_of_interview(self, date_time):
        if date_time.strftime("%Y-%m-%d %H:%M") < datetime.datetime.now().strftime("%Y-%m-%d %H:%M"):
            raise ValidationError("Input upcoming date and time only")


class InterviewUpdateSchema(Schema):
    note = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=300)
    )

