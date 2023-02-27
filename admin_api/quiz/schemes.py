from typing import Dict, List, Optional

from marshmallow import Schema, fields
from marshmallow.validate import Length
from marshmallow.exceptions import ValidationError

from app.web.schemes import OkResponseSchema


class ThemeSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)


class ResponseThemeSchema(OkResponseSchema):
    data = fields.Nested(ThemeSchema)


def validate_unity_the_correct_answer(value):
    correct_answers: List[Optional[Dict[str, str]]] = [answer for answer in value
                                                       if answer.get("is_correct")]
    if len(correct_answers) != 1:
        raise ValidationError(message="The question must has only one correct answer",
                              field_name="answers")
    return value


class QuestionSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested("AnswerSchema",
                            validate=[Length(min=2), validate_unity_the_correct_answer],
                            many=True)

    class Meta:
        ordered = True


class ResponseQuestionSchema(OkResponseSchema):
    data = fields.Nested(QuestionSchema)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)

    class Meta:
        ordered = True


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ThemeListResponseSchema(OkResponseSchema):
    data = fields.Nested(ThemeListSchema)


class ThemeIdSchema(Schema):
    theme_id = fields.Int(required=False)


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)


class ListQuestionResponseSchema(OkResponseSchema):
    data = fields.Nested(ListQuestionSchema)
