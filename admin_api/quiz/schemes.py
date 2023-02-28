from typing import Dict, List, Optional

from marshmallow import Schema, fields

from admin_api.web.schemes import OkResponseSchema


class ThemeSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)


class ResponseThemeSchema(OkResponseSchema):
    data = fields.Nested(ThemeSchema)


class QuestionSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answer = fields.Nested("AnswerSchema")

    class Meta:
        ordered = True


class ResponseQuestionSchema(OkResponseSchema):
    data = fields.Nested(QuestionSchema)


class AnswerSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)


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
